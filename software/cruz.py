"""Monitor local de Cruz. La adquisición sigue aunque se cierre el navegador."""

import argparse
import csv
import fcntl
import io
import json
import math
import signal
import sqlite3
import threading
import time
from contextlib import closing, contextmanager
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from adquisicion import ambiental, simulada


BASE = Path(__file__).resolve().parent
DEFAULTS = {"intervalo_s": 900, "automatico": True}
OPTICAL_DEFAULTS = {
    "exposure_ms": 50, "analogue_gain": 11.0, "pixel_format": "raw10",
    "roi": {"x1": 100, "y1": 300, "x2": 1100, "y2": 420},
    "replicates": 10, "cooldown_enabled": True, "cooldown_after": 3, "cooldown_seconds": 60,
    "as7265x_gain": None, "as7265x_integration": None,
}
RESUMEN_SQL = """
    SELECT id, inicio_utc, fin_utc, duracion_ms, estado,
           json_extract(datos, '$.temperatura.valor') AS temperatura,
           json_extract(datos, '$.conductividad.valor') AS conductividad,
           json_extract(datos, '$.errores') AS errores
    FROM ciclos
"""


def utc():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def validar_config(config, modo):
    minimo = 1 if modo == "simulado" else 10
    if (
        not isinstance(config, dict) or config.keys() != DEFAULTS.keys()
        or type(config["intervalo_s"]) is not int
        or not minimo <= config["intervalo_s"] <= 86400
        or type(config["automatico"]) is not bool
    ):
        raise ValueError(f"Interval must be an integer between {minimo} and 86400 seconds.")
    return config


def validar_optica(config):
    def numero(valor, minimo, maximo):
        return type(valor) in (int, float) and math.isfinite(valor) and minimo <= valor <= maximo

    def entero(valor, minimo, maximo):
        return type(valor) is int and minimo <= valor <= maximo

    if not isinstance(config, dict) or config.keys() != OPTICAL_DEFAULTS.keys():
        raise ValueError("Incomplete optical settings.")
    roi = config["roi"]
    if not isinstance(roi, dict) or roi.keys() != {"x1", "y1", "x2", "y2"}:
        raise ValueError("ROI must contain four coordinates.")
    if not all(entero(roi[k], 0, 1280 if k[0] == "x" else 800) for k in roi):
        raise ValueError("ROI coordinates must be within 1280 × 800.")
    if roi["x2"] - roi["x1"] < 2 or roi["y2"] - roi["y1"] < 2:
        raise ValueError("ROI must be at least 2 × 2 pixels.")
    if (
        not numero(config["exposure_ms"], 0.01, 200)
        or not numero(config["analogue_gain"], 1, 16)
        or config["pixel_format"] not in ("raw10", "processed8")
        or not entero(config["replicates"], 1, 100)
        or type(config["cooldown_enabled"]) is not bool
        or not entero(config["cooldown_after"], 1, 100)
        or not entero(config["cooldown_seconds"], 0, 3600)
        or (config["as7265x_gain"] is not None and config["as7265x_gain"] not in (1, 3.7, 16, 64))
        or type(config["as7265x_gain"]) is bool
        or (config["as7265x_integration"] is not None and not entero(config["as7265x_integration"], 0, 255))
    ):
        raise ValueError("Optical settings are outside the allowed range.")
    return config


class Almacen:
    def __init__(self, directorio, modo, inicial):
        self.archivo = directorio / "cruz.sqlite3"
        self.modo = modo
        with self.conexion() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS despliegue (
                    id INTEGER PRIMARY KEY CHECK (id=1), modo TEXT NOT NULL, config TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS ciclos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, inicio_utc TEXT NOT NULL,
                    fin_utc TEXT, duracion_ms INTEGER, estado TEXT NOT NULL,
                    config TEXT NOT NULL, datos TEXT
                );
                CREATE TABLE IF NOT EXISTS ajustes_opticos (
                    id INTEGER PRIMARY KEY CHECK (id=1), config TEXT NOT NULL
                );
            """)
            columnas = {col["name"] for col in db.execute("PRAGMA table_info(ciclos)")}
            if "optica" not in columnas:
                db.execute("ALTER TABLE ciclos ADD COLUMN optica TEXT")
            db.execute("INSERT OR IGNORE INTO ajustes_opticos VALUES (1, ?)",
                       (json.dumps(OPTICAL_DEFAULTS),))
            optica_guardada = json.loads(db.execute(
                "SELECT config FROM ajustes_opticos WHERE id=1"
            ).fetchone()["config"])
            if "cooldown_enabled" not in optica_guardada:
                optica_guardada["cooldown_enabled"] = True
                db.execute("UPDATE ajustes_opticos SET config=? WHERE id=1",
                           (json.dumps(optica_guardada),))
            self.optica = validar_optica(optica_guardada)
            anterior = db.execute("SELECT modo, config FROM despliegue WHERE id=1").fetchone()
            if anterior is None:
                db.execute("INSERT INTO despliegue VALUES (1, ?, ?)", (modo, json.dumps(inicial)))
                self.config = inicial
            elif anterior["modo"] != modo:
                raise ValueError("La carpeta pertenece al otro modo. Usa una carpeta distinta.")
            else:
                self.config = validar_config(json.loads(anterior["config"]), modo)
            db.execute("UPDATE ciclos SET estado='interrumpido' WHERE estado='en_curso'")

    @contextmanager
    def conexion(self):
        with closing(sqlite3.connect(self.archivo, timeout=4)) as db, db:
            db.row_factory = sqlite3.Row
            db.execute("PRAGMA synchronous=FULL")
            yield db

    def guardar_config(self, config):
        with self.conexion() as db:
            db.execute("UPDATE despliegue SET config=? WHERE id=1", (json.dumps(config),))

    def guardar_optica(self, config):
        with self.conexion() as db:
            db.execute("UPDATE ajustes_opticos SET config=? WHERE id=1", (json.dumps(config),))

    def ciclo(self, config, optica=None):
        inicio = time.monotonic()
        with self.conexion() as db:
            id_ciclo = db.execute(
                "INSERT INTO ciclos (inicio_utc, estado, config, optica) VALUES (?, 'en_curso', ?, ?)",
                (utc(), json.dumps(config), json.dumps(optica or self.optica)),
            ).lastrowid
        try:
            datos = simulada(id_ciclo) if self.modo == "simulado" else ambiental()
        except Exception as exc:
            datos = {"errores": {"ciclo": f"{type(exc).__name__}: {exc}"}}
        estado = "completo"
        if datos["errores"]:
            estado = "parcial" if "temperatura" in datos or "conductividad" in datos else "fallido"
        with self.conexion() as db:
            db.execute(
                "UPDATE ciclos SET fin_utc=?, duracion_ms=?, estado=?, datos=? WHERE id=?",
                (utc(), round((time.monotonic() - inicio) * 1000), estado,
                 json.dumps(datos, ensure_ascii=False, allow_nan=False), id_ciclo),
            )
        return id_ciclo, estado

    def recientes(self):
        with self.conexion() as db:
            filas = db.execute(RESUMEN_SQL + " ORDER BY id DESC LIMIT 120").fetchall()
            return [{**fila, "errores": json.loads(fila["errores"] or "{}")} for fila in filas]

    def detalle(self, id_ciclo):
        with self.conexion() as db:
            fila = db.execute("SELECT * FROM ciclos WHERE id=?", (id_ciclo,)).fetchone()
            if fila is None:
                return None
            return {**fila, "modo": self.modo, "reloj": "sistema_no_verificado",
                    "config": json.loads(fila["config"]), "optica": json.loads(fila["optica"] or "null"),
                    "datos": json.loads(fila["datos"] or "null")}

    def csv(self):
        salida = io.StringIO(newline="")
        writer = csv.writer(salida)
        writer.writerow(["ciclo", "modo", "inicio_utc", "fin_utc", "duracion_ms", "estado",
                         "temperatura_c", "conductividad_us_cm", "errores_json"])
        with self.conexion() as db:
            for fila in db.execute(RESUMEN_SQL + " ORDER BY id"):
                writer.writerow([fila["id"], self.modo, *tuple(fila)[1:]])
        return salida.getvalue()

    def espectro_csv(self, id_ciclo):
        detalle = self.detalle(id_ciclo)
        if not detalle or not detalle["datos"] or "as7265x" not in detalle["datos"]:
            return None
        salida = io.StringIO(newline="")
        writer = csv.writer(salida)
        writer.writerow(["cycle", "mode", "wavelength_nm_nominal", "channel",
                         "dark_raw", "blue_raw", "dark_factory_calibrated_simulated",
                         "blue_factory_calibrated_simulated"])
        for canal in detalle["datos"]["as7265x"]["canales"]:
            writer.writerow([id_ciclo, detalle["modo"], canal["nm_nominal"], canal["canal"],
                             canal["oscuro_crudo"], canal["azul_crudo"],
                             canal["oscuro_calibrado_fabricante_simulado"],
                             canal["azul_calibrado_fabricante_simulado"]])
        return salida.getvalue()


class Monitor:
    def __init__(self, almacen):
        self.almacen = almacen
        self.config = almacen.config
        self.optica = almacen.optica
        self.condicion = threading.Condition()
        self.fin = threading.Event()
        self.siguiente = time.monotonic()
        self.midiendo = False
        self.pendiente = False
        self.error = None

    def configurar(self, config):
        validar_config(config, self.almacen.modo)
        with self.condicion:
            self.almacen.guardar_config(config)
            self.config = config
            self.siguiente = time.monotonic() + config["intervalo_s"]
            self.condicion.notify()

    def pedir(self):
        with self.condicion:
            if self.midiendo or self.pendiente or self.error or self.fin.is_set():
                return False
            self.pendiente = True
            self.condicion.notify()
            return True

    def configurar_optica(self, config):
        validar_optica(config)
        with self.condicion:
            self.almacen.guardar_optica(config)
            self.optica = config

    def estado(self):
        with self.condicion:
            ciclos = self.almacen.recientes()
            ultimo = next((c for c in ciclos if c["estado"] != "en_curso"), None)
            optica = None
            if self.almacen.modo == "simulado" and ultimo and ultimo["estado"] == "completo":
                optica = self.almacen.detalle(ultimo["id"])["datos"]
            return {
                "modo": self.almacen.modo, "config": self.config, "midiendo": self.midiendo,
                "pendiente": self.pendiente, "error": self.error, "reloj": "sistema_no_verificado",
                "en_s": (max(0, math.ceil(self.siguiente - time.monotonic()))
                         if self.config["automatico"] and not self.error else None),
                "ciclos": ciclos, "optica": optica, "ajustes_opticos": self.optica,
            }

    def parar(self, *_):
        with self.condicion:
            self.fin.set()
            self.condicion.notify_all()

    def ejecutar(self):
        while True:
            with self.condicion:
                while not self.fin.is_set():
                    espera = self.siguiente - time.monotonic()
                    if self.pendiente or (self.config["automatico"] and espera <= 0):
                        break
                    self.condicion.wait(espera if self.config["automatico"] else None)
                if self.fin.is_set():
                    return
                self.pendiente = False
                self.midiendo = True
                config = self.config
                optica = self.optica
                vencimiento = time.monotonic() + config["intervalo_s"]
                self.siguiente = vencimiento
            try:
                self.almacen.ciclo(config, optica)
            except (sqlite3.Error, OSError, ValueError) as exc:
                with self.condicion:
                    self.midiendo = False
                    self.error = f"Acquisition stopped: {exc}"
                return
            with self.condicion:
                self.midiendo = False
                ahora = time.monotonic()
                if self.siguiente == vencimiento and ahora >= vencimiento:
                    intervalo = config["intervalo_s"]
                    self.siguiente += (1 + int((ahora - vencimiento) / intervalo)) * intervalo


class Panel(BaseHTTPRequestHandler):
    def setup(self):
        self.request.settimeout(5)
        super().setup()

    def enviar(self, codigo, contenido, tipo="application/json; charset=utf-8"):
        cuerpo = (json.dumps(contenido, ensure_ascii=False, allow_nan=False)
                  if tipo.startswith("application/json") else contenido).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(cuerpo)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        if tipo.startswith("text/csv"):
            self.send_header("Content-Disposition", 'attachment; filename="cruz.csv"')
        self.end_headers()
        self.wfile.write(cuerpo)

    def host_local(self):
        return self.headers.get("Host") in {
            f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}",
        }

    def do_GET(self):
        if not self.host_local():
            self.enviar(403, {"error": "Use the local Cruz dashboard."})
            return
        ruta = urlsplit(self.path).path
        almacen = self.server.monitor.almacen
        if ruta == "/":
            self.enviar(200, self.server.html, "text/html; charset=utf-8")
        elif ruta == "/api/estado":
            self.enviar(200, self.server.monitor.estado())
        elif ruta == "/exportar.csv":
            self.enviar(200, almacen.csv(), "text/csv; charset=utf-8")
        elif ruta.startswith("/espectro/") and (num := ruta.rsplit("/", 1)[1]).isascii() and num.isdigit() and len(num) <= 18:
            espectro = almacen.espectro_csv(int(num))
            if espectro is None:
                self.enviar(404, {"error": "Spectrum not available for this cycle."})
            else:
                self.enviar(200, espectro, "text/csv; charset=utf-8")
        elif ruta.startswith("/api/ciclos/") and (num := ruta.rsplit("/", 1)[1]).isascii() and num.isdigit() and len(num) <= 18:
            detalle = almacen.detalle(int(num))
            self.enviar(200 if detalle else 404, detalle or {"error": "Measurement not found."})
        else:
            self.enviar(404, {"error": "Page not found."})

    def do_POST(self):
        origen = self.headers.get("Origin")
        if not self.host_local() or (origen and origen != "http://" + self.headers["Host"]):
            self.enviar(403, {"error": "Changes are only accepted from the local dashboard."})
            return
        monitor = self.server.monitor
        try:
            longitud = int(self.headers.get("Content-Length", "0"))
            if self.headers.get_content_type() != "application/json" or not 0 < longitud <= 4096:
                raise ValueError("The request must contain a small JSON object.")
            cuerpo = json.loads(self.rfile.read(longitud))
            if self.path == "/api/config":
                monitor.configurar(cuerpo)
                self.enviar(200, {"ok": True})
            elif self.path == "/api/optica":
                monitor.configurar_optica(cuerpo)
                self.enviar(200, {"ok": True})
            elif self.path == "/api/medir" and cuerpo == {}:
                if monitor.pedir():
                    self.enviar(202, {"ok": True})
                else:
                    self.enviar(409, {"error": "A measurement is in progress or acquisition has stopped."})
            else:
                self.enviar(404, {"error": "Operation not found."})
        except ValueError as exc:
            self.enviar(400, {"error": str(exc)})
        except sqlite3.Error:
            self.enviar(503, {"error": "Could not save the settings."})

    def log_message(self, *_):
        pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    familia = parser.add_mutually_exclusive_group()
    familia.add_argument("--simulate", action="store_const", const="simulado", dest="modo")
    familia.add_argument("--sensors", action="store_const", const="ambiental", dest="modo")
    parser.set_defaults(modo="simulado")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--config", type=Path, help="Configuración inicial de una carpeta nueva")
    parser.add_argument("--cycles", type=int, help="Ejecutar N ciclos consecutivos sin panel ni espera")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    if args.cycles is not None and (args.cycles < 1 or args.modo != "simulado"):
        parser.error("--cycles requiere un entero positivo y modo simulado")
    if not 0 <= args.port <= 65535:
        parser.error("Puerto fuera de rango.")
    directorio = args.output or Path.home() / ".local/share/cruz" / args.modo
    try:
        inicial = json.loads(args.config.read_text()) if args.config else DEFAULTS
        validar_config(inicial, args.modo)
        directorio.mkdir(parents=True, exist_ok=True)
        with (directorio / ".lock").open("a+") as bloqueo:
            try:
                fcntl.flock(bloqueo, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                raise ValueError("Ya hay una instancia de Cruz usando esa carpeta.") from None
            almacen = Almacen(directorio, args.modo, inicial)
            monitor = Monitor(almacen)
            signal.signal(signal.SIGINT, monitor.parar)
            signal.signal(signal.SIGTERM, monitor.parar)
            if args.cycles is not None:
                for _ in range(args.cycles):
                    if monitor.fin.is_set():
                        break
                    ciclo, estado = almacen.ciclo(almacen.config)
                    print(f"{args.modo} · ciclo {ciclo}: {estado}", flush=True)
                return
            with ThreadingHTTPServer(("127.0.0.1", args.port), Panel) as server:
                server.monitor = monitor
                server.html = (BASE / "panel.html").read_text()
                web = threading.Thread(target=server.serve_forever, daemon=True)
                trabajo = threading.Thread(target=monitor.ejecutar)
                web.start()
                trabajo.start()
                print(f"Cruz ({args.modo}) · http://127.0.0.1:{server.server_port} · {directorio}", flush=True)
                monitor.fin.wait()
                trabajo.join()
                server.shutdown()
    except (OSError, ValueError, sqlite3.Error) as exc:
        parser.exit(1, f"Cruz: {exc}\n")


if __name__ == "__main__":
    main()
