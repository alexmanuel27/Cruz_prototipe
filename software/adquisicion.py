"""Lecturas sintéticas y primera adquisición ambiental en el banco de Cruz."""

import math
import re
import subprocess
import time
from pathlib import Path


CANALES = tuple(zip(
    (410, 435, 460, 485, 510, 535, 560, 585, 610, 645, 680, 705, 730, 760, 810, 860, 900, 940),
    "ABCDEFGHRISJTUVWKL",
))


def simulada(ciclo):
    fase = ciclo / 5
    cambio = math.sin(fase)
    oscuro = [10] * 128
    transmision = [round(10 + 480 * math.exp(-((i - 64) / 39) ** 2) * (0.93 + cambio * 0.05)) for i in range(128)]
    canales = []
    for i, (nm, letra) in enumerate(CANALES):
        fondo = 14 + i % 4
        iluminado = fondo + round((310 + 40 * cambio) * math.exp(-((nm - 680) / 38) ** 2))
        canales.append({
            "nm_nominal": nm, "canal": letra,
            "oscuro_crudo": fondo, "azul_crudo": iluminado,
            "oscuro_calibrado_fabricante_simulado": round(fondo * 0.74, 2),
            "azul_calibrado_fabricante_simulado": round(iluminado * 0.74, 2),
        })
    return {
        "temperatura": {"valor": round(20.5 + 0.6 * cambio, 3), "unidad": "°C"},
        "conductividad": {"valor": round(610 + 17 * math.cos(fase), 2), "unidad": "µS/cm"},
        "camara": {"oscuro_por_pixel": oscuro, "transmision_por_pixel": transmision},
        "as7265x": {"canales": canales},
        "secuencia": ["purga", "reposo", "oscuros", "transmision", "azul", "sensores_ambientales"],
        "errores": {},
    }


def ds18b20():
    sondas = sorted(Path("/sys/bus/w1/devices").glob("28-*/w1_slave"))
    if len(sondas) != 1:
        raise ValueError(f"Se esperaba un DS18B20 y se encontraron {len(sondas)}")
    archivo = sondas[0]
    crudo = subprocess.run(
        ["cat", str(archivo)], check=True, capture_output=True, text=True, timeout=3,
    ).stdout
    lineas = crudo.splitlines()
    if len(lineas) != 2 or not lineas[0].endswith(" YES"):
        raise ValueError("CRC del DS18B20 incorrecto")
    encontrado = re.search(r"\bt=(-?\d+)\b", lineas[1])
    if encontrado is None:
        raise ValueError("El DS18B20 no devolvió temperatura")
    return {
        "valor": int(encontrado[1]) / 1000, "unidad": "°C",
        "id": archivo.parent.name, "crudo": crudo,
    }


def atlas_ec_oem():
    # El OEM necesita un STOP entre seleccionar el registro y leerlo.
    def transferir(*args):
        return subprocess.run(
            ["i2ctransfer", "-y", "1", *args], check=True,
            capture_output=True, text=True, timeout=2,
        ).stdout

    def leer(registro, cantidad):
        transferir("w1@0x64", hex(registro))
        datos = bytes(int(b, 16) for b in transferir(f"r{cantidad}@0x64").split())
        if len(datos) != cantidad:
            raise ValueError(f"Respuesta incompleta del Atlas en {registro:#04x}")
        return datos

    def escribir(registro, valor):
        transferir("w2@0x64", hex(registro), hex(valor))

    identidad, firmware = leer(0x00, 2)
    if identidad != 0x04:
        raise ValueError(f"0x64 respondió con ID {identidad:#04x}, se esperaba EC-OEM")
    k = int.from_bytes(leer(0x08, 2), "big")
    if k != 10:
        raise ValueError(f"El Atlas guarda K{k / 100:g}; la sonda de banco es K0.1")
    estado_anterior = leer(0x06, 1)[0]
    if estado_anterior not in (0, 1):
        raise ValueError(f"Modo del Atlas inesperado: {estado_anterior:#04x}")
    try:
        escribir(0x07, 0)
        escribir(0x06, 1)
        limite = time.monotonic() + 2.5
        while leer(0x07, 1) != b"\x01":
            if time.monotonic() >= limite:
                raise TimeoutError("El Atlas no entregó una lectura nueva")
            time.sleep(0.1)
        crudo = leer(0x14, 8)
    finally:
        escribir(0x06, estado_anterior)
    return {
        "valor": int.from_bytes(crudo[4:], "big", signed=True) / 100,
        "unidad": "µS/cm", "k": k / 100, "firmware": firmware,
        "temperatura_compensacion_c": int.from_bytes(crudo[:4], "big") / 100,
        "registro_calibracion": leer(0x0F, 1)[0],
        "crudo_hex": crudo.hex(),
    }


def ambiental():
    datos = {"errores": {}}
    for nombre, leer in (("temperatura", ds18b20), ("conductividad", atlas_ec_oem)):
        try:
            datos[nombre] = leer()
        except (OSError, ValueError, subprocess.SubprocessError) as exc:
            datos["errores"][nombre] = (getattr(exc, "stderr", None) or str(exc)).strip()
    return datos
