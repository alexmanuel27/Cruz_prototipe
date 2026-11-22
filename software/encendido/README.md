# Pulsador de Cruz

U17 (ATtiny1604-SS) permanece alimentado por 5V_AON. J25 admite un pulsador momentáneo normalmente abierto entre los contactos 1 (BUTTON_N) y 2 (GND). El tiempo de pulsación es de aproximadamente 5 s, con 30 ms para rechazar rebotes. El oscilador interno del ATtiny determina la tolerancia.

- Con el equipo apagado, después de 5 s de pulsación, U17 habilita el Pololu por J26. Soltar el pulsador antes de la siguiente orden.
- Con el equipo encendido, tras otra pulsación de 5 s, U17 manda un pulso bajo al GPIO BCM5 (pin físico 29). Raspberry Pi OS solicita el apagado. Al finalizar, BCM26 (pin físico 37) pasa a alto y U17 corta la alimentación principal. Si Linux no confirma, la alimentación permanece activa.
- Una nueva alarma del DS3231 por J24.5 puede encender Cruz. La alarma sostenida no impide el corte ni vuelve a encender el equipo. Programar la próxima alarma y limpiar sus banderas antes de apagar.

## Preparación del ATtiny

`encendido.hex` contiene el firmware de `main.c` y `control.h`. Grabarlo con un programador UPDI apto para lógica de 5 V y objetivo ATtiny1604. J29 tiene 1 = 5V_AON, 2 = UPDI, 3 = GND. Con la placa alimentada por su propia rama permanente, usar el pin 1 como referencia de tensión del programador. Mantener la salida principal desconectada durante la programación y comprobar que el programador no inyecta otra alimentación de 5 V.

Compilación con AVR-GCC con soporte para ATtiny1604:

```sh
avr-gcc -mmcu=attiny1604 -std=c11 -Wall -Wextra -Werror -Os main.c -o encendido.elf
avr-objcopy -O ihex -R .eeprom encendido.elf encendido.hex
```

## Preparación de Raspberry Pi OS

Con la placa montada y el ATtiny grabado, copiar `cruz-encendido.txt` a `/boot/firmware/` e incluir la línea `include cruz-encendido.txt` dentro de `[all]` en `/boot/firmware/config.txt`. Reiniciar y comprobar que la política del botón de encendido de Raspberry Pi OS inicia un apagado. El comportamiento previsto es el de Raspberry Pi OS Lite con su política de apagado para `KEY_POWER`. Comprobar el ciclo completo con el circuito antes de operar el instrumento sin supervisión. [Documentación de las dos opciones de arranque](https://github.com/raspberrypi/firmware/blob/master/boot/overlays/README).

Patillaje de U17:

| Pin | Puerto | Señal |
| --- | --- | --- |
| 1 / 14 | Alimentación | 5V_AON / GND |
| 10 | PA0 | UPDI |
| 11 | PA1 | Pulsador J25, activo bajo |
| 12 | PA2 | Alarma DS3231, activa baja |
| 13 | PA3 | Habilitación del Pololu, activa alta |
| 2 | PA4 | Solicitud de apagado, drenador abierto |
| 3 | PA5 | Confirmación de apagado a 5 V desde U16 |

`test_control.c` verifica en un ordenador las pulsaciones cortas, los 5 s, la liberación del botón, la confirmación de Linux y el despertar por alarma.
