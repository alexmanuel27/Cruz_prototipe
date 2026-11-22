import sqlite3
import csv
import io
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from adquisicion import atlas_ec_oem
from cruz import Almacen, DEFAULTS, OPTICAL_DEFAULTS, Monitor, validar_config, validar_optica


class MonitorTest(unittest.TestCase):
    def setUp(self):
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.carpeta = Path(carpeta.name)

    def test_datos_inmutables_y_recuperacion(self):
        almacen = Almacen(self.carpeta, "simulado", DEFAULTS)
        ciclo, estado = almacen.ciclo(DEFAULTS)
        self.assertEqual(estado, "completo")
        detalle = almacen.detalle(ciclo)
        self.assertEqual(detalle["modo"], "simulado")
        self.assertEqual(len(detalle["datos"]["camara"]["transmision_por_pixel"]), 128)
        canales = detalle["datos"]["as7265x"]["canales"]
        self.assertEqual(len(canales), 18)
        self.assertEqual([c["canal"] for c in canales[8:12]], ["R", "I", "S", "J"])
        self.assertIn("azul_calibrado_fabricante_simulado", canales[0])
        self.assertIn("simulado", almacen.csv())
        espectro = list(csv.DictReader(io.StringIO(almacen.espectro_csv(ciclo))))
        self.assertEqual(len(espectro), 18)
        self.assertEqual(espectro[8]["channel"], "R")
        self.assertEqual(espectro[8]["wavelength_nm_nominal"], "610")
        self.assertEqual(espectro[8]["blue_raw"], str(canales[8]["azul_crudo"]))
        self.assertIsNone(almacen.espectro_csv(999))
        with almacen.conexion() as db:
            pendiente = db.execute(
                "INSERT INTO ciclos (inicio_utc, estado, config) VALUES ('t', 'en_curso', '{}')"
            ).lastrowid
        config = {"intervalo_s": 140, "automatico": False}
        almacen.guardar_config(config)
        reinicio = Almacen(self.carpeta, "simulado", DEFAULTS)
        self.assertEqual(reinicio.config, config)
        self.assertEqual(detalle, reinicio.detalle(ciclo))
        self.assertEqual(reinicio.detalle(pendiente)["estado"], "interrumpido")
        with self.assertRaisesRegex(ValueError, "otro modo"):
            Almacen(self.carpeta, "ambiental", DEFAULTS)

    def test_configuracion_estricta(self):
        for malo in (True, 0, 86401, 1.1, float("nan"), "5"):
            with self.subTest(malo=malo), self.assertRaises(ValueError):
                validar_config({"intervalo_s": malo, "automatico": True}, "simulado")
        with self.assertRaises(ValueError):
            validar_config({"intervalo_s": 9, "automatico": True}, "ambiental")

    def test_fallo_parcial_conserva_el_otro_sensor(self):
        almacen = Almacen(self.carpeta, "ambiental", DEFAULTS)
        datos = {"temperatura": {"valor": 23.25}, "errores": {"conductividad": "desconectado"}}
        with patch("cruz.ambiental", return_value=datos):
            ciclo, estado = almacen.ciclo(DEFAULTS)
        self.assertEqual(estado, "parcial")
        self.assertEqual(almacen.detalle(ciclo)["datos"], datos)

    def test_un_solo_ciclo_y_config_aplicada_despues(self):
        inicial = {"intervalo_s": 900, "automatico": False}
        almacen = Almacen(self.carpeta, "simulado", inicial)
        monitor = Monitor(almacen)
        entro = threading.Event()
        salir = threading.Event()
        captura = []

        def lento(config, optica):
            captura.append((config, optica))
            entro.set()
            salir.wait(3)

        with patch.object(almacen, "ciclo", side_effect=lento):
            hilo = threading.Thread(target=monitor.ejecutar)
            hilo.start()
            try:
                self.assertTrue(monitor.pedir())
                self.assertTrue(entro.wait(2))
                self.assertFalse(monitor.pedir())
                monitor.configurar({"intervalo_s": 7, "automatico": False})
            finally:
                monitor.parar()
                salir.set()
                hilo.join(3)
        self.assertFalse(hilo.is_alive())
        self.assertEqual(captura, [(inicial, OPTICAL_DEFAULTS)])
        self.assertEqual(Almacen(self.carpeta, "simulado", DEFAULTS).config["intervalo_s"], 7)

    def test_fallo_de_almacenamiento_frena_monitor(self):
        almacen = Almacen(self.carpeta, "simulado", DEFAULTS)
        monitor = Monitor(almacen)
        with patch.object(almacen, "ciclo", side_effect=sqlite3.OperationalError("disco lleno")):
            monitor.ejecutar()
        self.assertIn("disco lleno", monitor.estado()["error"])
        self.assertFalse(monitor.pedir())

    def test_optica_persiste_y_se_guarda_con_cada_ciclo(self):
        almacen = Almacen(self.carpeta, "simulado", DEFAULTS)
        monitor = Monitor(almacen)
        anterior, _ = almacen.ciclo(DEFAULTS)
        cambio = {**OPTICAL_DEFAULTS, "roi": {**OPTICAL_DEFAULTS["roi"], "x1": 150},
                  "exposure_ms": 35.5, "replicates": 12}
        monitor.configurar_optica(cambio)
        nuevo, _ = almacen.ciclo(DEFAULTS, monitor.optica)
        self.assertEqual(almacen.detalle(anterior)["optica"], OPTICAL_DEFAULTS)
        self.assertEqual(almacen.detalle(nuevo)["optica"], cambio)
        self.assertEqual(Almacen(self.carpeta, "simulado", DEFAULTS).optica, cambio)

    def test_optica_rechaza_roi_y_valores_invalidos(self):
        for cambios in ({"roi": {"x1": 300, "x2": 200, "y1": 0, "y2": 400}},
                        {"exposure_ms": float("nan")}, {"replicates": True},
                        {"as7265x_gain": True}, {"as7265x_integration": 256}):
            with self.subTest(cambios=cambios), self.assertRaises(ValueError):
                validar_optica({**OPTICAL_DEFAULTS, **cambios})

    def test_base_previa_se_abre_sin_perder_ciclos(self):
        archivo = self.carpeta / "cruz.sqlite3"
        with sqlite3.connect(archivo) as db:
            db.executescript("""
                CREATE TABLE despliegue (id INTEGER PRIMARY KEY, modo TEXT, config TEXT);
                CREATE TABLE ciclos (id INTEGER PRIMARY KEY, inicio_utc TEXT, fin_utc TEXT,
                    duracion_ms INTEGER, estado TEXT, config TEXT, datos TEXT);
                INSERT INTO despliegue VALUES (1, 'simulado', '{"intervalo_s":900,"automatico":true}');
                INSERT INTO ciclos VALUES (1, 'original', NULL, NULL, 'interrumpido', '{}', NULL);
            """)
        almacen = Almacen(self.carpeta, "simulado", DEFAULTS)
        self.assertEqual(almacen.optica, OPTICAL_DEFAULTS)
        self.assertEqual(almacen.detalle(1)["inicio_utc"], "original")
        self.assertIsNone(almacen.detalle(1)["optica"])


class AtlasTest(unittest.TestCase):
    def test_registros_y_reposo_ante_fallo(self):
        for fallo in (False, True):
            with self.subTest(fallo=fallo):
                lecturas = {
                    0x00: "0x04 0x05", 0x08: "0x00 0x0a", 0x06: "0x00", 0x07: "0x01",
                    0x14: "0x00 0x00 0x09 0xc4 0x00 0x00 0xee 0x56", 0x0f: "0x00",
                }
                escrituras = []
                registro = None

                def transferir(args, **kw):
                    nonlocal registro
                    if args[3].startswith("w1"):
                        registro = int(args[4], 16)
                        return SimpleNamespace(stdout="")
                    if args[3].startswith("w2"):
                        escrituras.append(tuple(int(v, 16) for v in args[4:]))
                        return SimpleNamespace(stdout="")
                    if fallo and registro == 0x14:
                        raise OSError("bus desconectado")
                    return SimpleNamespace(stdout=lecturas[registro])

                with patch("adquisicion.subprocess.run", side_effect=transferir):
                    if fallo:
                        with self.assertRaises(OSError):
                            atlas_ec_oem()
                    else:
                        datos = atlas_ec_oem()
                        self.assertEqual(datos["valor"], 610.14)
                        self.assertEqual(datos["temperatura_compensacion_c"], 25)
                self.assertEqual(escrituras, [(0x07, 0), (0x06, 1), (0x06, 0)])


if __name__ == "__main__":
    unittest.main()
