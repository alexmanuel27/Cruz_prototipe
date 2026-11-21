"""Prueba de banco: 20 pulsos lentos con habilitación activa en bajo."""

import time

from gpiozero import OutputDevice


def main():
    enable = OutputDevice(27, active_high=False, initial_value=False)
    try:
        with OutputDevice(17, initial_value=False) as step, OutputDevice(18, initial_value=False):
            enable.on()
            for _ in range(20):
                step.on()
                time.sleep(0.1)
                step.off()
                time.sleep(0.1)
    finally:
        enable.off()
        enable.close()


if __name__ == '__main__':
    main()
    print('Prueba terminada: 20 pulsos enviados; ENABLE desactivado.')
