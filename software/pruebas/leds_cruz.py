"""Prueba de banco de los dos LED adicionales en la Pi 5."""

import argparse
import signal
import time

from gpiozero import OutputDevice


def cancelar(_signum, _frame):
    raise KeyboardInterrupt


def main():
    parser = argparse.ArgumentParser(description="Enciende un LED durante dos segundos.")
    parser.add_argument("led", choices=("naranja", "ir"))
    args = parser.parse_args()
    signal.signal(signal.SIGTERM, cancelar)

    try:
        with (
            OutputDevice(16, initial_value=False) as naranja,
            OutputDevice(20, initial_value=False) as infrarrojo,
        ):
            salida = naranja if args.led == "naranja" else infrarrojo
            try:
                salida.on()
                time.sleep(2)
            finally:
                salida.off()
    except KeyboardInterrupt:
        parser.exit(130, "Prueba interrumpida. Salidas desactivadas.\n")

    print(f"Prueba de {args.led} terminada. Ambas salidas desactivadas.")


if __name__ == "__main__":
    main()
