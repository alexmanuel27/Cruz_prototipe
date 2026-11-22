# Adquisición y control de Cruz: revisión y primera iteración

**Monitor local · 22/11/2026.** La [primera versión](../software/README.md) incluye adquisición periódica, almacenamiento por ciclo, configuración local de la cadencia, vistas del último ciclo e historial, y exportación CSV/JSON. El modo simulado cubre el recorrido óptico sintético. El modo ambiental integra DS18B20 y Atlas EC-OEM K0.1 a partir de las pruebas de banco, pendiente de verificación en la Pi. La hora se toma del sistema y se marca como no verificada. La lectura óptica real, los actuadores, el RTC y el corte de alimentación quedan para la integración.

**Interfaz eléctrica vigente:** [tabla BCM/pines, polaridades y estados de arranque](../electronica/cross_v8_raspberry/REVISION_BANCO_2026-11-21.md#tabla-vigente-para-software). Las cuatro fuentes son activas altas y requieren `OPT_ARM` en BCM21/pin 40. El programa de banco de tres LED conserva su cableado ensayado y no controla esa señal nueva. Alex confirmó que probó los sensores desde los 3V3 de la Raspberry y eligió esa alimentación: se retiró U10 del diseño; el aislamiento físico del EC-OEM está incorporado en el diseño mediante R05CT05S e ISO1540D, pendiente de montaje y ensayo. [Cierre y pendientes eléctricos de PCB](../electronica/cross_v8_raspberry/CIERRE_PCB_2026-11-21.md). [Estado de PCB del 22/11](../electronica/cross_v8_raspberry/LEEME_PRIMERO.md): sin trazado ni puentes W, esquema reorganizado y GPIO conservados; U11 SN74CBTLV3125D SOIC para señales de 3,3 V. No energizar V8 a partir de los ensayos separados.

**Geometría actual, D55 y D56 · 21/11/2026:** iluminación compartida desde un brazo con halógena y LED azul, rojo e infrarrojo seleccionables; cámara en transmisión y AS7265x a 90°. Mantener transmisión primero y excitación azul después; orden, tiempos y datos derivados para las excitaciones adicionales pendientes de definir. El software debe identificar fuente y ajustes por lectura, guardar los 18 canales y originales, y mantener la exclusión de fuentes y apagado seguro. Esta decisión no valida la respuesta de fluorescencia ni cambia el PCB o el CAD.

## Conmutación de las fuentes en banco

Alex probó la halógena de **12 V / 10 W** con la fuente de banco. También alimentó a 12 V el circuito del azul con LM317 y 10,4 Ω y reportó que se mantiene el ajuste de **110 mA**. Probar una línea de 12 V común:

| Rama | Camino de potencia |
| --- | --- |
| Halógena | +12 V → lámpara → drenador del IRLZ44N → fuente del MOSFET → negativo del DC/DC |
| Azul | +12 V → LM317 (10,4 Ω entre OUT y ADJ) → LED azul → IRLZ44N → GND |
| Naranja | +12 V → LM317 (10,4 Ω entre OUT y ADJ) → LED naranja → IRLZ44N → GND |
| Infrarrojo | +12 V → 220 Ω / 1 W → LED TSHG6410 → IRLZ44N → GND |

Alex comprobó que el naranja de 620 nm y el infrarrojo de 850 nm encienden en banco con DC/DC a 12 V y reportó aproximadamente 3 V y 110 mA. Falta identificar el punto de medida de esos 3 V. Los 110 mA del naranja quedan dentro del rango publicado por [ILS](https://docs.rs-online.com/c025/A700000015828598.pdf). Para el [Vishay TSHG6410](https://www.vishay.com/docs/81870/tshg6410.pdf), 110 mA excede el máximo continuo de 100 mA a 25 °C. Para el IR usar 220 Ω / 1 W en serie desde la línea regulada de 12 V. Con Vf alrededor de 1,5–1,6 V se esperan 47–48 mA y alrededor de 0,5 W de disipación en la resistencia. Azul y naranja conservan un LM317 por rama. Medir la corriente en serie y la tensión directamente entre las patas del IR antes de la prueba GPIO.

La prueba de la halógena queda para más adelante. Demanda 10 W / 12 V ≈ 0,83 A en régimen. El [filamento frío](https://www.ushio.com/files/catalog/qih/qih-lamp-characteristics.pdf) demanda más al arrancar. Probar el DC/DC real desde frío, verificar que la lámpara arranca y que los 12 V se recuperan y se mantienen. El pico real requiere instrumentación con resolución temporal suficiente. Medir cuánto tarda la luz en estabilizarse antes de fijar la espera para transmisión.

Si los 12 V llegan directamente a IN del LM317, el aumento de 8 a 12 V agrega unos 0,44 W de calor a 110 mA. Medir temperatura y corriente con el tiempo de encendido previsto. Si hace falta reducir el calor, se puede conservar la línea de 12 V y bajar solo la entrada del LM317. [Cálculo térmico del LM317](https://www.ti.com/lit/ds/symlink/lm317.pdf#page=23).

GPIO propuestos para la Pi 5 en un montaje separado de V8. Verificar disponibilidad en la Pi antes de cablear. La tabla de V8 más abajo describe otra interfaz.

| Fuente | GPIO BCM | Pin físico | Activa en banco |
| --- | --- | --- | --- |
| Halógena | 22 | 15 | Alto |
| Azul | 23 | 16 | Alto |
| Naranja (rojo de 620 nm) | 16 | 36 | Alto |
| Infrarrojo | 20 | 38 | Alto |

Probar primero el azul. El cátodo pasa al drenador del IRLZ44N y la fuente del MOSFET va al negativo del DC/DC. Usar un [74AHCT125](https://www.ti.com/lit/ds/symlink/sn74ahct125.pdf) alimentado con los 5 V de la Pi para adaptar las cuatro señales de 3,3 V. Unir GND de Pi, adaptador y DC/DC, con el retorno de potencia directo al convertidor. Para el azul, llevar GPIO23 a 1A y llevar 1Y a la puerta a través de 470 Ω. Para la halógena, usar GPIO22, 2A y 2Y de la misma forma. Poner una resistencia de 10 kΩ a GND en cada entrada usada y unir su OE a GND. Poner 120 kΩ entre puerta y fuente y 100 nF de desacoplo entre VCC y GND del adaptador. Deshabilitar y fijar las entradas de los canales que aún no se usan. Verificar apagado en reposo, arranque y reinicio, VGS de al menos 4,5 V al encender y corriente del LED con el interruptor instalado. El [IRLZ44N](https://www.infineon.com/part/IRLZ44N) tiene resistencia de encendido garantizada a partir de la condición publicada de 4,5 V. Probar una fuente a la vez.

### Prueba de los tres LED desde la Pi

Mantener la halógena apagada durante esta prueba. En cada rama, llevar el cátodo a su drenador IRLZ44N y la fuente del MOSFET al negativo del DC/DC. Mantener los 12 V comunes y un limitador de corriente por rama. La tierra de la Pi y la del convertidor se unen, con retorno de potencia directo al convertidor.

| LED | GPIO BCM / pin físico Pi | Entrada / salida del 74AHCT125 de 14 pines | OE a GND |
| --- | --- | --- | --- |
| Azul | GPIO23 / 16 | 1A (2) / 1Y (3) | 1OE (1) |
| Naranja | GPIO16 / 36 | 3A (9) / 3Y (8) | 3OE (10) |
| IR | GPIO20 / 38 | 4A (12) / 4Y (11) | 4OE (13) |

Usar la misma adaptación de nivel, desacoplo y resistencias que en el azul. Comprobar primero las tres puertas con la alimentación de los LED apagada. Dejar las entradas sin usar en GND y sus OE en 5 V si no hay nada conectado a esos canales. En la Pi, comprobar que los tres GPIO estén libres con `pinctrl get 23,16,20`. Copiar [leds_cruz.py](../software/pruebas/leds_cruz.py) a `/tmp/cruz-leds.py` en la Pi y ejecutar un LED por vez:

```sh
sudo env GPIOZERO_PIN_FACTORY=lgpio python3 /tmp/cruz-leds.py azul
sudo env GPIOZERO_PIN_FACTORY=lgpio python3 /tmp/cruz-leds.py naranja
sudo env GPIOZERO_PIN_FACTORY=lgpio python3 /tmp/cruz-leds.py ir
```

Alex confirmó el 21 de noviembre que probó la conmutación de los tres LED desde la Pi y funcionó bien. Cada comando está diseñado para encender solo el canal indicado durante dos segundos y apagarlo al terminar o recibir Ctrl+C o SIGTERM. Confirmar que el canal queda libre y apagado al salir. Los GPIO controlan la conmutación. La corriente depende del limitador físico. El ajuste del IR a unos 48 mA debe verificarse antes de darle alimentación para ejecutar su prueba.

### Webcam submarina USB (O04)

Alex indica que es la última cámara por probar en esta ronda. Ensayar en seco con la cámara en el interior, orientada hacia la tapa acrílica. Verificar los modos que anuncia la propia cámara y anotar la resolución realmente capturada.

```sh
lsusb
v4l2-ctl --list-devices
```

Elegir el nodo de captura del bloque USB de la webcam. Cuando exista un enlace inequívoco bajo `/dev/v4l/by-id/`, se puede usar ese nombre estable. Algunas cámaras exponen también un nodo de metadatos. Confirmar formatos antes de capturar. Sustituir `/dev/videoN` por el nodo real.

```sh
cam=/dev/videoN
v4l2-ctl -d "$cam" --list-formats-ext
prueba=$(mktemp -d "$HOME/cruz-webcam-XXXXXX")
timeout 15s ffmpeg -hide_banner -nostdin -f v4l2 -i "$cam" -ss 1 -frames:v 1 -update 1 "$prueba/webcam.jpg"
ls -lh "$prueba"
```

Si falla el modo predeterminado, elegir uno de los anunciados por la cámara antes de repetir. Comprobar en el JPEG detalle, foco y orientación. Después repetir a través de la tapa para comparar reflejos y nitidez. Alex confirmó enumeración USB como `32e6:9281 icSpring icspring camera`, con `/dev/video0` y `/dev/video1` en su propio bloque y el CSI por separado. `/dev/video0` expone captura MJPEG y anuncia modos de 640 × 480 a 3264 × 2448 a 30 fps. Alex capturó un JPEG de 3264 × 2448 (248 KiB) con FFmpeg en `/home/alex/cruz-webcam-4D5cIu/webcam.jpg`. Quedan pendientes revisión visual, captura a través de la tapa y cualquier prueba de vídeo sostenido. [Captura Video4Linux2 con FFmpeg](https://www.ffmpeg.org/ffmpeg-devices.html#video4linux2_002c-v4l2).

### Conductividad Atlas K0.1

La foto de Alex muestra una sonda Atlas K0.1 con cable sin conector y un módulo verde con dos filas de cinco contactos. El tamaño relativo y los tres integrados coinciden con el **Atlas EC-OEM**. Falta un adaptador de montaje. La [OEM Simple Development Board (OEM-SDB)](https://files.atlas-scientific.com/oem-dev-board.pdf) es el adaptador de banco del fabricante y se entrega sin ensamblar. Para integrar la medición en el instrumento, aislar alimentación y señales I²C. La portadora EZO de cinco pines es de otra familia.

Confirmar la orientación con la [vista superior de Atlas](https://files.atlas-scientific.com/EC_oem_datasheet.pdf#page=7) antes de soldar. Mirando el lado de los chips, orientar el integrado rectangular abajo a la derecha. Alex propone soldar cables directamente para el ensayo. Fijar el módulo a una base aislante, soldar con la Pi desconectada y comprobar que no haya puentes ni corto entre VCC y GND. Cableado de banco:

| EC-OEM | Conexión Pi 5 |
| --- | --- |
| 1 SDA | GPIO2, pin físico 3 |
| 3 VCC | 3,3 V, pin físico 1 |
| 6 GND | GND, pin físico 14 |
| 8 SCL | GPIO3, pin físico 5 |

Para la sonda, separar el vivo del coaxial y la malla. Llevar el vivo al pad 4 (PRB) y la malla al pad 5 (PRB G). No tender un puente de la malla a GND de la Pi. La primera prueba de comunicación se puede hacer con la sonda desconectada. INT y NC quedan libres. Mantener 3,3 V y bus de 100 kHz. Para identificar el circuito en la dirección predeterminada 0x64, enviar primero solo el puntero de registro y terminar la transacción. Leer en una segunda transacción:

```sh
sudo i2ctransfer -y 1 w1@0x64 0x00
sudo i2ctransfer -y 1 r2@0x64
```

Alex obtuvo `0x04 0x05` en la Pi 5. El primer byte confirma el EC-OEM y el segundo es el valor del registro de versión. La comunicación I²C en 0x64 está comprobada. Alex comprobó la adquisición de tres muestras nuevas.

Antes de medir, leer la constante K guardada:

```sh
sudo i2ctransfer -y 1 w1@0x64 0x08 &&
sudo i2ctransfer -y 1 r2@0x64
```

Interpretar los dos bytes como entero sin signo, primero el byte alto, dividido por 100. Alex obtuvo `0x00 0x64`, que corresponde a K1.0. Para la sonda K0.1, escribir `0x00 0x0a` y verificar el resultado:

```sh
sudo i2ctransfer -y 1 w3@0x64 0x08 0x00 0x0a &&
sudo i2ctransfer -y 1 w1@0x64 0x08 &&
sudo i2ctransfer -y 1 r2@0x64
```

K permanece al apagar. Con la sonda conectada y sumergida en un vaso separado, borrar la marca de lectura anterior (0x07), activar la medida (0x06), esperar a que 0x07 sea 0x01 y leer cuatro bytes desde 0x18 en una transacción separada. Interpretar MSB primero y dividir por 100. Volver a hibernar con 0x06 = 0x00. Primera prueba funcional sin calibrar. [Registros del EC-OEM](https://files.atlas-scientific.com/EC_oem_datasheet.pdf#page=8).

Resultados de Alex: `00 00 ee 56`, `00 00 ee 84`, `00 00 ee 8d`, equivalentes a 610,14, 610,60 y 610,69 µS/cm. Media 610,48 µS/cm, diferencia máximo–mínimo 0,55 µS/cm (≈0,09 % de la media). Las tres lecturas seguidas muestran estabilidad a corto plazo. Alex confirmó el ajuste K0.1 leyendo `0x00 0x0a`. Quedan por comprobar muestra, temperatura y exactitud frente a un patrón.

## Traspaso al chat del PCB · pruebas de banco del 21 de noviembre de 2026

Plataforma de banco: Raspberry Pi 5 con Trixie. D55 fija una geometría en T con iluminación común y AS7265x a 90°. D56 fija la halógena para transmisión. La tabla distingue resultados de banco y propuestas para revisar el esquema.

| Elemento | Interfaz y resultado comprobados | Pendiente para el PCB o el ensayo integrado |
| --- | --- | --- |
| Cámara espectral OV9281 | FFC en CAM/DISP 1. La Pi guardó JPEG y DNG de 1280 × 800 con el sensor en modo RAW10. | Reservar acceso y espacio de la cinta. Calibración y respuesta óptica pendientes. |
| Webcam del entorno O04 | USB icSpring 32e6:9281. Captura desde `/dev/video0`, JPEG de 3264 × 2448. | Reservar USB y ruta interior del cable hacia la tapa. Validar foco y reflejos a través del acrílico. El nodo Linux puede cambiar. |
| AS7265x | Bus I²C 1, SDA GPIO2/pin físico 3 y SCL GPIO3/pin 5. Dirección 0x49. Los 18 canales respondieron a luz frente a tapado. | Verificar el bus con todos los periféricos y validar blancos, señal a 90° y rangos de exposición. |
| Temperatura DS18B20 | 1-Wire por GPIO4/pin 7 a 3,3 V, pull-up previsto de 4,7 kΩ. Lecturas 20,875 y 32,750 °C con CRC correcto. | Comparar con una referencia y revisar orden de hilos y alimentación en el conector final. |
| Conductividad Atlas EC-OEM + K0.1 | Módulo de diez pads. Bus I²C 1, 0x64. ID 0x04, versión 0x05. K0.1 confirmado por lectura. Tres lecturas consecutivas con media reportada de 610,48 µS/cm. | Incorporar huella OEM y aislamiento de alimentación e I²C si se conserva este módulo. Definir terminación del coaxial. Verificar con patrón y temperatura antes de usar los valores para salinidad. |
| Bomba Kamoer y A4988 | Conjunto nominal 24 V/20 W, dos bobinas de 2,9 Ω, placa con R050. BCM17/18/27 (pines 11/12/13) para STEP, DIR y ENABLE activo bajo. Se obtuvieron 10 mL en 15,981 s con 9.333 pulsos a ~640 Hz programados. | Confirmar corriente por fase, margen de VMOT, apagado por defecto, temperatura y repetibilidad con la hidráulica real. Conservar configuración de banco como punto de partida. |
| LED azul y naranja | Alex confirma que ambos conmutaron desde la Pi. Azul con LM317 a 110 mA medidos, ajuste conservado con 12 V de entrada al circuito. Naranja de 620 nm también reportado a 110 mA. | Comprobar disipación del LM317 y apagado durante el arranque y reinicio. |
| LED infrarrojo y control de LED | Alex confirma que el TSHG6410 de 850 nm también conmutó desde la Pi. | Propuesta para IR: 220 Ω / 1 W desde 12 V, ~48 mA. Falta registrar la corriente con esa resistencia. Para banco se propusieron BCM23/16/20 (pines 16/36/38), activos en alto, por 74AHCT125 a 5 V hacia tres IRLZ44N. La V8 guardada tiene lógica previa distinta para el azul. |
| Halógena | 12 V / 10 W. Encendió con la fuente de banco. | Validar arranque en frío con el DC/DC, conmutación, tiempo de estabilización y temperatura antes de cerrar el dimensionado. El canal blanco de V8 estaba diseñado para un LED. |

Los GPIO de banco son una referencia para revisión. La etapa de potencia y las conexiones definitivas siguen pendientes del chat del PCB.

## Pruebas de banco · 21 de noviembre de 2026

- **Pi 5 y cámara:** Alex corrigió la orientación de la cinta; la OV9281 Arducam se detecta en CAM/DISP 1 con `camera_auto_detect=0` y `dtoverlay=ov9281,arducam`. `rpicam-still` guardó JPEG y DNG de 1280 × 800 con sensor RAW10; el JPEG muestra señal, con zonas blancas saturadas visualmente. DNG, linealidad, saturación real y calibración aún sin evaluar. Los archivos de prueba se guardaron temporalmente en la Pi.
- **AS7265x:** Alex conectó el módulo a la Pi 5; bus I²C 1 y respuesta en `0x49`. El tipo leído fue `0x40` y el registro de selección `0x30` indicó presencia de los dos sensores asociados. Se obtuvieron crudos y valores calibrados de fabricante en 18 canales. La prueba inicial consultaba dos veces DATA_RDY: corregida en la copia temporal para tomar la primera señal de listo. Biblioteca SparkFun Python 2.0.0 con `smbus2`; prueba con 64× y registro de integración 49, ajustes predeterminados de la biblioteca, sin calibrar para Cruz. El LED azul externo no se activó; la biblioteca enciende brevemente y luego apaga su indicador interno.
- **DS18B20:** Alex conectó la sonda a Pi 5 según la prueba propuesta: 3,3 V en pin físico 17, datos en GPIO4/pin 7 y masa en pin 9, con resistencia pull-up de 4,7 kΩ solicitada entre datos y 3,3 V; conexiones y resistencia aún sin inspección independiente. Tras habilitar 1-Wire y reiniciar, apareció `28-0122120493cd`. Lectura original `4e 01 55 00 7f ff 0c 10 38`, `crc=38 YES`, `t=20875`: 20,875 °C. Al sujetar la punta, Alex obtuvo `0c 02 55 00 7f ff 0c 10 b0`, `crc=b0 YES`, `t=32750`: 32,750 °C; evidencia de respuesta térmica, sin tiempo cronometrado. Exactitud y repetibilidad pendientes. No confundir resolución numérica con exactitud.
- **Bomba, identificación visual:** foto aportada por Alex muestra etiqueta Kamoer `KAS-SE-B083`, `U:24V`, `P:20W`. Es la referencia del conjunto de bomba; no demuestra por sí sola la referencia ni la corriente por fase del motor. Alex corrigió su identificación inicial y confirmó aproximadamente 2,9 Ω entre 1A–1B y entre 2A–2B en el conector mostrado; circuito abierto entre bobinas y 0 Ω con puntas juntas. La foto parece mostrar 2B rojo, 2A azul, 1A verde y 1B negro; colores por verificar visualmente antes de conectar. Indica `R050` en ambas resistencias del A4988: 0,05 Ω cada una, pendiente de inspección detallada. Corriente nominal por fase y fuente pendientes; no deducir corriente nominal de resistencia ni de 24 V/20 W. Sin prueba de accionamiento ni conexiones a la Pi.
- **Prueba A4988 preparada:** `software/pruebas/bomba_a4988.py` envía 20 pulsos lentos por GPIO17, dirección GPIO18 y habilita temporalmente mediante GPIO27 activo bajo. Alex indicó 12 V en VMOT, VDD 3,3 V y Vref correctos; ajuste experimental solicitado: 0,40 V con R050, pendiente registrar medición exacta. Pull-up externo de ENABLE a 3,3 V indicado; conexiones sin inspección independiente. Prueba lógica con dispositivos simulados en éxito/error. Alex ejecutó la prueba en banco: la bomba se movió y reportó consumo no superior a 400 mA (se interpreta como lectura de fuente, por confirmar). No se midió la corriente por bobina. Paro ante pérdida de alimentación, temperaturas, sentido de flujo, caudal y límites reales pendientes; mantener la fuente accesible.
- **Prueba a 24 V:** Alex sustituyó el condensador de 25 V por uno identificado como 36 V y confirmó Vref. Ejecutó 100 pulsos a 5 pulsos/s (aprox. 20 s); informó giro correcto pero lento y corriente no superior a 300 mA, solicitada en la fuente. No es corriente de fase. Valor exacto de Vref, picos de VMOT, temperatura, caudal, sentido y operación continua sin medir; 1 A por fase sigue siendo ajuste experimental no validado. 36 V deja menos margen que el condensador de 50 V recomendado.
- **Segunda velocidad a 24 V:** Alex informó giro estable, algo más rápido, con 200 pulsos programados a ~20 Hz y corriente de fuente sin aumento respecto al ensayo anterior (~300 mA). Los pulsos son comandos; giro, pasos perdidos, caudal y temperatura no se midieron cuantitativamente.
- **Tercera velocidad a 24 V:** Alex ejecutó 400 pulsos programados a ~80 Hz y valoró el resultado como «espectacular». No comunicó corriente, tiempo cronometrado, temperatura, pasos perdidos o volumen; la respuesta observada no verifica caudal ni calibración.
- **Primer ensayo de caudal:** a 24 V y ~80 pulsos/s, Alex informó que la primera muestra, 3,5 mL en 20,478 s, incluía agua previa en el vaso: se excluye del cálculo. Dos repeticiones con vaso vacío y 1.600 pulsos enviados: 2,8 mL en 20,470 s (8,21 mL/min) y 2,9 mL en 20,476 s (8,50 mL/min). Media: 2,85 mL por 1.600 pulsos, 8,35 mL/min y 1,78 µL/pulso enviado. Dos repeticiones técnicas, sin caudal, temperatura, alturas, tiempo y volumen de cebado, precisión de vasos ni pasos perdidos validados; no establece una calibración para el montaje final ni la purga efectiva.
- **Objetivo de bomba:** Alex fijó mover 10 mL en el menor tiempo viable. Se propone aumentar la frecuencia por etapas, midiendo volumen, tiempo y estabilidad; la estimación inicial con 2,85 mL/1.600 pulsos es ~5.600 pulsos para 10 mL, no validada a velocidades superiores. No se ha establecido el caudal máximo ni un volumen dosificado garantizado.
- **Ensayo de velocidad ~160 Hz:** Alex reportó giro suave, 5.600 pulsos enviados, 6 mL en 35,978 s a 24 V. Caudal medio 10,01 mL/min y 1,071 µL/pulso, frente a ~1,781 µL/pulso de dos ensayos a ~80 Hz: ~40 % menos volumen por pulso. Posibles pasos perdidos u otras condiciones hidráulicas; causa no verificada. No se alcanzaron los 10 mL objetivo; repetir y comparar antes de calibrar. Corriente, temperaturas y picos no medidos para este ensayo.
- **Ensayo de velocidad ~320 Hz:** Alex reportó 5.600 pulsos enviados, 6 mL y `real 18,461 s`, a 24 V. Caudal medio calculado 19,50 mL/min; ~1,071 µL/pulso enviado. La medición coincide en volumen con el ensayo a ~160 Hz, pero es una sola repetición por velocidad; caudal máximo, pérdidas de pasos, temperatura y picos siguen sin validar.
- **Velocidad elegida para primera dosificación:** a ~640 Hz programados, Alex observó giro rápido y satisfactorio: 5.600 pulsos, 6 mL en 9,696 s (~37,13 mL/min). Estimación proporcional para 10 mL: ~9.333 pulsos; falta medir la dosis real, repeticiones, temperatura, pulsos perdidos y margen eléctrico. Tiempo por pulso de Python es orientativo; no se ha medido eléctricamente la frecuencia.
- **Primera dosis objetivo de 10 mL:** Alex observó 10 mL en 15,981 s con 9.333 pulsos enviados a ~640 Hz programados, 24 V y A4988; ≈37,54 mL/min y ≈1,0715 µL/pulso enviado. El script confirmó ENABLE desactivado. Una prueba con vaso graduado y mangueras de banco; quedan por verificar repetibilidad, resolución del vaso, temperatura, pasos perdidos, picos eléctricos y renovación real de cubeta y mangueras. El capacitor utilizado se indicó de 36 V, por debajo del margen de 50 V recomendado para 24 V.
- **Driver alternativo fotografiado:** Pololu blanco `md22a / 0J7097`, identificado por su fabricante como DRV8834: VMOT 2,5–10,8 V, no conectar directamente a batería nominal de 24 V. No usa alimentación lógica VDD como A4988; con resistencias originales 0,1 Ω, Pololu indica Vref = Ilímite/2: 0,5 V para 1 A. La selección de 1 A es de prueba propuesta por Alex; corriente nominal del motor desconocida. Sustitución en V8 y ensayo no aprobados ni probados. [Pololu](https://www.pololu.com/product/2134).
- **Respuesta a iluminación:** una lectura con el sensor tapado y otra con la luz del móvil; sin distancias ni espectro controlados. Todos los canales respondieron. Cuentas crudas, en orden 410, 435, 460, 485, 510, 535, 560, 585, 610, 645, 680, 705, 730, 760, 810, 860, 900 y 940 nm:
  - Tapado: `0, 1, 0, 1, 0, 2, 1, 1, 6, 0, 1, 1, 0, 0, 0, 0, 0, 0`.
  - Móvil: `38, 348, 331, 1008, 1406, 1135, 2617, 5012, 33624, 5595, 6514, 1525, 5284, 2776, 2654, 447, 127, 120`.
- **Originales:** Alex indicó que los CSV con crudos y valores calibrados quedaron en `/home/alex/cruz-sensor-DR8T91/` de la Pi. `luz-ambiental.csv` corresponde a luz del móvil. No se han copiado ni verificado los archivos en el repo; la prueba Python y la biblioteca están en `/tmp/cruz-as7265x` de la Pi y son temporales. No hay medición de intensidad de fuente, réplicas, blanco, saturación, repetibilidad ni validación de fluorescencia. La respuesta óptica no demuestra concentraciones ni calibración del conjunto.
- **Siguiente paso:** comprobar la lectura de temperatura DS18B20 o la conductividad Atlas según el material disponible, verificando módulo, terminales, alimentación y bus antes de cablear. Tras las pruebas se entregarán al chat de PCB únicamente interfaces y resultados comprobados.

**20 de noviembre de 2026 · Revisión y plan de pruebas, sin control de hardware habilitado.**

La Raspberry Pi gobierna el instrumento. **Prioridad posterior fijada por Alex:** seleccionar y probar los componentes reales, sus conexiones y funciones básicas; integrar después y trasladar al chat del PCB los resultados verificados. El ciclo simulado de §3 se conserva como propuesta posterior para probar integración y fallos, sin preceder a esas pruebas básicas. No se modifica mecánica, esquema, PCB ni software de los instrumentos anteriores.

Alex dispone de una Raspberry Pi 5 y de la Pi 4 de MonoSpectro. Recomendación pendiente de ensayo: evaluar la Pi 5 con una tarjeta de sistema independiente y conservar la Pi 4 como referencia. Empezar por Pi 5 + OV9281, alimentación de banco conocida y V8 desconectada; comprobar detección, RAW, ajustes manuales y guardado. Después, verificar cada sensor y actuador por separado, revisando antes su interfaz eléctrica. No hay cambio definitivo de controlador ni incorporación del ESP32 aprobados todavía.

La selección energética comparará energía por ciclo completo y espera, incluyendo convertidores y periféricos. Para la Pi 5 se evaluará el despertar por su RTC y el estado de bajo consumo documentados en la [guía oficial](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#real-time-clock-rtc). El ESP32 queda como candidato a supervisor si aporta una mejora medida; leer el AS7265x desde la Pi no requiere conservar el firmware ESP32. No se exportan todavía propuestas al chat del PCB.

## 1. Qué existe y qué reutilizar

La búsqueda del árbol de Cruz, incluidos archivos ocultos salvo Git, no encontró adquisición, servicio de arranque ni firmware unificado. Los programas Python existentes pertenecen al CAD, simulación o generación/comprobación histórica de KiCad. No son controladores del instrumento. Entrada de requisitos: [especificación, §§2–8](../ESPECIFICACION.md), [calibración](VALIDACION_Y_CALIBRACION.md) y [decisión D53](../DECISIONES.md#d53--raspberry-pi-como-controlador-principal-2026-11-02).

| Origen revisado | Reutilización concreta | Adaptación necesaria para Cruz |
| --- | --- | --- |
| `MonoSpectro/app.py`: `manual`, `unpack_raw10`, `start_camera`, `collect`, `same_settings` | Captura PiCam mediante Picamera2; RAW10; ROI; exposición y ganancia manuales; promediado y detección de saturación; compatibilidad de referencias | Extraer únicamente captura y validación, sin importar la app: inicializa cámara e hilos al importar. Guardar cada réplica, metadatos efectivos y original sin pérdida. Plazo total finito aun si llegan cuadros a destiempo. Exigir RAW para fotometría validada; el fallback ISP de 8 bits queda solo diagnóstico identificado. |
| `MonoSpectro/app.py`: `wavelength_axis`, carga de JSON y exportación CSV | Polinomio píxel–λ y formato legible con ajustes de adquisición | El ROI es semiabierto: usar índices reales `x1 … x2−1`, no el `linspace(x1,x2,n)` actual. No asignar una escala espectral ficticia sin calibración. Referencias persistentes: `refs` vive en RAM y el CSV se descarga por HTTP. |
| `MonoSpectro/spectro_math.py`: `absorbance`, `apply_response`, `savgol` | Ecuaciones y corrección opcional separadas de la interfaz | No copiar `absorbance` tal cual: impone un suelo de una cuenta y usa un solo oscuro. Cruz necesita D de muestra y D₀ del blanco; señales no positivas quedan inválidas. `apply_response` recorta a cero: conservar absorbancia aparente negativa y guardar aparte cualquier corrección declarada y validada. No transferir coeficientes del otro montaje. |
| `Fluorometer/Spectro18_V_Flu/Spectro18_V_Flu.ino` | Mapa explícito de los 18 canales; adquisición de réplicas; separación de muestra, oscuro y blanco | El firmware ESP32 no se ejecuta en la Pi. Lee `getCalibrated*`, no cuentas crudas; las muestras guardan medias/SD de 18 canales y réplicas individuales solo de 435/645 nm. Cruz guardará todas las réplicas crudas y calibradas, configuración y tiempos. |
| `Fluorometer/Spectro18_V_Flu/WhiteReference.h`, `SpectrumStats.h` | Referencia de 10×18 y estadística de Welford, con comprobación de guardado fallido | Reutilizar comportamiento y casos de prueba en Python; no portar NVS ni exigir señal en 435/645 para validar cualquier blanco. Ceros de oscuro son legítimos. No heredar tiempos térmicos ni número de réplicas como calibrados. |

Rutas de origen: `/Users/alex/Nube /repos/MonoSpectro` y `/Users/alex/Nube /repos/Fluorometer`. No se importarán por rutas absolutas ni se dependerá en producción de repos vecinos. Al incorporar fragmentos, conservar atribución y licencia aplicable; MonoSpectro incluye MIT, y debe revisarse la autorización de los archivos concretos de Fluorometer antes de distribuirlos.

La ecuación de firmware `−2,7924·ln(I645)+20,1264` no usa el blanco ni el oscuro en su resultado. Las calibraciones de extractos del repo Fluorometer tampoco validan agua natural ni la geometría de Cruz. En esta primera entrega, clorofila y salinidad derivada permanecerán sin valor si no existe un modelo válido para ese dominio; se conservan las señales y conductividad originales.

Para el controlador Python del AS7265x existe una opción del propio fabricante de la placa: [SparkFun Qwiic AS7265x](https://github.com/sparkfun/qwiic_as7265x_py/blob/master/qwiic_as7265x.py), con lecturas crudas y calibradas separadas. Es candidata, no dependencia instalada o validada aquí. Su `take_measurements()` puede volver por timeout sin excepción: no interpretar retorno como lectura nueva. Comprobar disponibilidad/frescura, errores de bus y plazo total. Usar adquisición sin los emisores integrados; la excitación externa es 430 nm. La [documentación oficial de Raspberry Pi](https://www.raspberrypi.com/documentation/accessories/camera-software.html) mantiene la pila moderna de cámara; el sensor OV9281 concreto y su soporte RAW se verificarán en la Pi real.

## 2. Instantánea de interfaces V8 anterior a la edición del 21 de noviembre

Esta tabla conserva la exportación anterior de 75 componentes y 77 redes; **ya no describe la rama de sensores ni las fuentes ópticas guardadas**. Para trabajar con la edición nueva, usar la [tabla eléctrica vigente](../electronica/cross_v8_raspberry/REVISION_BANCO_2026-11-21.md#tabla-vigente-para-software) y el [estado V8](../electronica/cross_v8_raspberry/LEEME_PRIMERO.md). Los números de la instantánea siguiente son pines físicos de J1, no BCM ni autorización de cableado.

| Función | Conexión observada | Pendiente que bloquea su uso real |
| --- | --- | --- |
| PiCam espectral / cámara auxiliar | CSI / USB previstos por especificación; no representados en J1 | Modelo de Pi/OS, enumeración y soporte OV9281, formato/stride RAW, metadatos; modos reales de la USB. Cámara auxiliar aplazada hasta definir función/cadencia. |
| Bus I²C sensores | J1.3=`SDA`, J1.5=`SCL`; J8 AS7265x, J9 Atlas, J6 ADS1115 y adaptación hacia RTC | Direcciones reales, modo I²C de Atlas, pull-ups conjuntos, niveles, cableado y ausencia de alimentación parásita con Pi apagada. No hacer barridos sobre V8 sin revisión. |
| AS7265x | J8: 1=`3V3_PI`, 2=GND, 3=SDA, 4=SCL | Orden del módulo/cable, alimentación y emisores desactivados; ajustes y saturación. La alimentación dedicada de 3,3 V acordada aún no aparece. |
| Atlas EC | J9: 1=`3V3_PI`, 2=sin conectar, 3=GND, 4=SDA, 5=SCL | Orientación y función real del zócalo Gen 2, alimentación dedicada, modo/dirección, respuesta/status, unidades, K, calibración y compensación térmica. No interpretar el quinto contacto por analogía con otro módulo. |
| DS18B20 | J10: 1=`3V3_PI`, 2=GND, 3=`TEMP_1WIRE`; J1.7; R10=4,7 kΩ | Alimentación dedicada, orden real de hilos, identidad 1-Wire, CRC y conversión completada dentro del plazo. Conservar lectura/status original; fallos no son 0 °C. |
| Bomba A4988 | `M_STEP`=J1.11→U1.7; `M_DIR`=J1.12→U1.8; `M_ENABLE_N`=J1.13→U1.1; J2 bobinas | Correspondencia del carrier WJMY, corriente por fase, microstepping, reset/sleep, dirección, arranque deshabilitado y forma de generar pulsos con tiempo definido. Caudal/volumen efectivo y purga requieren ensayo; no inferirlos de 24 V/20 W. |
| Fuente blanca | `WHITE_EN`=J1.15→R5/Q1; J3 LED, U2 LM317 | Polaridad efectiva, estado al arrancar y al caer la Pi, corriente/driver, estabilización, fuente real disponible y disipación. |
| Excitación azul | `BLUE_EN`=J1.16→D8; `BLUE_GATE`→Q7; `BLUE_CTRL`=J5.1, J4 alimentación de driver | Hay inversión por D8/Q7: no asumir que HIGH equivale a luz. Verificar CTRL del driver y ausencia de encendido durante arranque, reset y Pi apagada. |
| Batería/ADC | J6 interfaz ADS1115; J7.1=`BAT_SENSE` desde divisor R8=100 kΩ/R9=10 kΩ de `VBAT_SW` | Módulo, dirección, rango, ganancia y referencia ADC; tensión máxima real y divisor/calibración; umbrales para terminar escritura. Mide rama conmutada, no batería permanentemente. |
| RS-485 | J1.8=`UART_TX`→J19.2; J1.10=`UART_RX`→J19.1; J19.3=GND, .4=`3V3_PI`; J20.3=A, .4=B, .2=REF | Módulo/transceptor real, dirección de transmisión, compatibilidad lógica, aislamiento, terminación, UART/console Linux y formato serie. No aparece DE/RE dedicado en J1. |
| Puerto exterior EN3 | J18.1/.2 carga, .3 sin conectar, .4 GND, .5=A, .6=B, .7=REF, .8=PILOT en este borrador | El símbolo dice `ASSIGNMENT_VERIFY`: no es un pinout físico aprobado. La reserva de alimentación externa de la especificación no está resuelta; no asignar sus cavidades ni unir retornos. |
| Despertador RTC | J24: 1=`3V3_AON`, 2=GND, 3=`RTC_SDA`, 4=`RTC_SCL`, 5=`WAKE_N`; Q3/Q4 hacia I²C de Pi | Modelo, dirección, batería/reserva, interrupción, alarma y aislamiento entre dominios. No hay prueba de despertar autónomo ni de reloj UTC confiable. |
| Corte de Pi | `HOLD_PI`=J1.37→U8.4 **R**; U8.1 Q→`POWER_ON`→J26.1 | El nombre HOLD no determina la acción: la red llega al reset del biestable. Verificar circuito, estado inicial, señales durante shutdown y corte solo después de escritura y apagado completos; no implementarlo como simple “mantener HIGH”. |
| Imán / cable / carga | `SW_SENSE`=J1.29; `PILOT_SENSE`=J1.22; `CHARGE_CTRL`=J1.18→R11/Q2/K1, inhibición Q6 | Polaridades, interbloqueos, debounce, latencia y comportamiento con Pi sin alimentación; contactos energizados y cargador. No controlar carga en la primera iteración. |
| Fuga, humedad y temperatura interior | No se identifica sensor/interfaz dedicado entre los componentes y redes exportados | Definir sensor, señal, alimentación, umbral y reacción de potencia independiente del programa. Tampoco hay realimentación de caudal/presión identificada. El software no puede certificar ausencia de fuga/obstrucción sin esas señales. |

Conexiones reservadas no equivalen a interfaces validadas. El documento V8 registra 199 conexiones sin trazar, tres errores ERC de alimentación y revisión eléctrica pendiente. Esos resultados se citan, no se han repetido ERC/DRC ni paridad en esta tarea. No fabricar ni energizar V8 a partir de este informe.

El [puerto de servicio](../electronica/PUERTO_SERVICIO_Y_BOYA.md) fija RS-485 como enlace y propone Modbus RTU, pero no hay mapa de registros, baud rate, dirección de equipo ni protocolo de archivos aprobado. RS-485 no proporciona por sí solo descarga de espectros/imágenes. Esa implementación queda después de medir el volumen de datos y cerrar electrónica. La extracción final será por el conector físico, con integridad y reanudación; no se sustituye por Wi-Fi.

### Comparación con los instrumentos de origen · 22 de noviembre

MonoSpectro parte de ROI (100,300)–(1100,420), exposición manual de 50 ms, ganancia 11 y preferencia por RAW10. Conserva las referencias de oscuro y blanco asociadas al ROI y a la exposición/ganancia. El fluorómetro toma 10 lecturas por adquisición, guarda oscuridad y blanco para los 18 canales y prevé enfriamiento de 60 s tras tres adquisiciones iluminadas. No fija explícitamente ganancia o integración en el firmware revisado.

Estos ajustes son antecedentes para diseñar la captura real de Cruz. La geometría, corriente del LED y sensores han cambiado y requieren validar parámetros y blancos propios. El monitor aún no controla la óptica real. El panel en inglés permite guardar exposición, ganancia, ROI, formato, réplicas y enfriamiento como ajustes preparatorios. Los guarda en cada ciclo sin aplicarlos todavía al hardware. Una gráfica muestra transmisión o fluorescencia con intervalo seleccionable. Al elegir fluorescencia se puede seleccionar la fuente azul, naranja o IR. Solo se simula el azul. La tabla y CSV conservan los 18 canales.

## 3. Plan de integración y criterios de validación

La primera versión implementa ciclo autónomo, seguimiento de fallos, almacenamiento y panel. El escenario simulado nunca abre dispositivos y sus datos están separados de los ambientales. El modo explícito `--sensors` consulta únicamente al DS18B20 y al Atlas. Los apartados siguientes conservan el plan y los criterios para completar adquisición óptica, procesamiento, calibración, archivos RAW y control de actuadores.

### Archivos y alcance

- `software/cruz.py`: entrada de terminal, cadencia, SQLite y API del panel local. `software/adquisicion.py` contiene los modos de adquisición y `software/panel.html` la interfaz.
- Procesamiento pendiente: eje píxel–λ, transmitancia, absorbancia, resta de oscuro y blanco multicanal, y validaciones de calidad.
- `software/config/`: ejemplo de cadencia y estado automático. La configuración de calibración y las referencias separadas se definirán durante la integración óptica.
- `software/tests/`: comprobaciones de almacenamiento, reinicio, exclusión de ciclos, fallo parcial y lectura de registros Atlas. Las pruebas de ecuaciones y referencias llegarán con su implementación.
- `software/README.md`: instalación, comandos, formato y límites. Si se incorporan dependencias, declaración mínima de versiones verificadas; Picamera2 solo en fase Pi, desde el sistema compatible.

Los dos precursores quedan como referencia de solo lectura.

### Secuencia que debe ejecutar

1. Validar configuración, destino, espacio disponible y reloj; crear y persistir ID único del ciclo antes de cualquier actuación simulada. Registrar inicio, versión de formato/software y hashes de configuración, calibración y referencias.
2. Simular toma→celda→bomba aguas abajo→descarga. Simular renovación de varios volúmenes efectivos, parada y espera de burbujas. Tiempos/volumen del ejemplo son sintéticos; no parámetros para la bomba real. Sin inversión ni repurga automática en esta entrega.
3. Ambas fuentes apagadas: adquirir oscuros de cámara y AS7265x con los ajustes de cada detector.
4. Solo visible encendido: estabilización, réplicas PiCam y apagado. Solo después, azul 430 nm encendido: estabilización, réplicas de los 18 canales y apagado. Conservar tiempos individuales para evaluar separación entre modalidades en el mismo llenado.
5. Adquirir temperatura y conductividad originales y sus estados; registrar compensación aplicada y tiempo. Recoger estado instrumental disponible. En simulación indicar su origen sintético; para señales no implementadas usar ausencia explícita, nunca valores normales inventados.
6. Procesar y guardar calidad por dato/modalidad y estado global. Un detector fallido no borra lo adquirido por el otro. Tiempo máximo por operación y por ciclo con reloj monótono; UTC para trazabilidad. Concluir siempre con intención de fuentes/bomba apagadas. Si una llamada bloquea, el controlador deberá tener un mecanismo externo que haga cumplir el plazo en fase hardware: un `finally` o un hilo con timeout no cubren un proceso colgado.
7. Cerrar durablemente el ciclo; esperar hasta el próximo vencimiento (15 min inicial configurable). Una sola ejecución a la vez. Si el ciclo excede la cadencia, registrar vencimiento perdido sin superponer ni acumular ciclos de recuperación. No hay corte de alimentación ni programación RTC en esta entrega.

Cada estado y fallo queda en un registro por ciclo. Si en el futuro es necesario repurgar, cerrar el intento fallido e iniciar otro ID, enlazado al anterior. No reutilizar el ID con otra muestra.

### Configuración y procesamiento

Separar `operation.json` (adquisición, cadencia, réplicas, tiempos, límites), `calibration.json` (coeficientes, unidades, método, dominio e identidad del montaje) y `references/` (blanco y oscuro de cada blanco con sus metadatos y datos originales). Guardar una copia inmutable de los archivos activos dentro del despliegue. Un cambio de configuración se aplica entre ciclos, con nueva identificación; nunca a mitad de una medida.

Validar esquema/versión, números finitos, dimensiones, identidades, ROI, formato y profundidad de bits, exposición/ganancia/integración efectivas, mapa de canales, fuente/celda y rango calibrado. El objetivo es 420–780 nm; informar cobertura útil real y enmascarar fuera del dominio comprobado. Sin coeficientes reales se guardan intensidad frente a píxel y estado sin calibrar; no inventar longitudes de onda. Blanco ausente/incompatible impide derivados afectados, sin impedir conservar originales en una adquisición diagnóstica explícita. Una configuración estructuralmente inválida bloquea el ciclo antes de actuar.

Para transmisión calcular, por píxel válido:

`T = (I − D) / (I₀ − D₀)`; `A_aparente = −log10(T)`.

Conservar I, D, I₀ y D₀ separados. Denominador o numerador no positivo, no finito, o saturación: resultado ausente y motivo; no suelo de una cuenta. T>1/A<0 se conserva con su diagnóstico de ruido/deriva, sin recorte. Una corrección fotométrica opcional no sustituye T/A originales. El blanco predespliegue no se mide automáticamente dentro del equipo; conservar edad y verificar deriva al recuperar.

Para fluorescencia, conservar por réplica los 18 enteros crudos y los 18 flotantes calibrados del fabricante, antes de corrección. Guardar `F_neta = (F_on − F_dark) − (B_on − B_dark)` cuando las referencias/configuraciones sean compatibles, en la misma escala y con unidad declarada. Conservar negativos; medias y SD son derivados adicionales. No normalizar por ganancia/integración ni convertir a concentración sin un método validado.

Mapa heredado que debe comprobar el adaptador real, en nm y letra de canal: `410:A, 435:B, 460:C, 485:D, 510:E, 535:F, 560:G, 585:H, 610:R, 645:I, 680:S, 705:J, 730:T, 760:U, 810:V, 860:W, 900:K, 940:L`. Los 18 se almacenan aunque el análisis use solo parte; no confundir el rango del AS7265x con el objetivo de transmisión.

### Archivos de salida y reinicios

Un directorio por despliegue, con manifiesto, metadatos del montaje y copias de configuración/referencias. Un subdirectorio por ID de ciclo con:

| Archivo propuesto | Contenido |
| --- | --- |
| `cycle.json` | Estado iniciado/completo/fallido/interrumpido; UTC y reloj confiable o no; IDs de equipo/celda/muestra/despliegue; versión de software/calibración; ajustes efectivos, fuentes, purga, sensores, alarmas, referencias, unidades y motivos de invalidez. |
| `events.jsonl` | Transiciones, intentos, fallos y tiempos. No reemplaza el manifiesto de integridad. |
| `camera.csv` | Réplica/tipo (oscuro/muestra), UTC, índice de píxel e intensidad antes de corrección. Guardar originales RAW sin pérdida y metadatos por captura para auditar ROI/saturación; calcular su tamaño real antes de dimensionar despliegues. |
| `as7265x.csv` | Réplica/tipo, UTC, canal/letra/λ nominal, cuenta cruda, valor calibrado del fabricante y ajustes. |
| `environment.csv` | Respuesta original y status/CRC disponibles, temperatura, conductividad con unidad y compensación, batería/otros sensores disponibles. Valor ausente y causa si faltan. |
| `processed.csv` | T/A aparente, fluorescencia neta, medias/SD, máscaras de calidad y versiones/métodos. Concentraciones ausentes salvo calibración validada. |

Archivos nuevos sin sobrescribir ciclos previos. Crear marca de inicio durable; escribir cada archivo temporal en el mismo sistema de archivos, vaciar buffers y sincronizar, renombrar y sincronizar directorio; publicar `complete` solo tras cerrar y verificar todos los archivos esperados y hashes. Esto reduce escrituras incompletas; no garantiza contra fallo físico de tarjeta/controlador. Al arrancar, conservar cualquier original parcial y registrar como interrumpidos los inicios sin cierre válido; empezar con ID nuevo, sin completar artificialmente datos ausentes. Bloqueo de ejecución única para evitar dos procesos sobre el mismo destino. Con disco lleno, conservar lo existente y detener nuevos ciclos; registrar causa si queda espacio.

No se borran datos tras exportar. El manifiesto permitirá comprobar una futura copia íntegra por el conector. El presupuesto de espacio se calcula con el formato medido, incluido RAW, para ≥7 días con margen ×2.

### Pruebas de aceptación de esa entrega

1. Caso numérico conocido: I=60, D=10, I₀=120, D₀=20 → T=0,5 y A≈0,30103. Detecta usar por error D en ambos términos. Casos no positivos, saturación y T>1; cero oscuro permitido.
2. Blanco incompatible por ROI, exposición, ganancia, integración, fuente o celda: originales conservados, derivados bloqueados y motivo explícito. Configuración corrupta/no finita: ciclo rechazado antes de actuaciones.
3. Réplicas de cámara y **18 crudos + 18 calibrados por réplica** recuperables, mapa correcto (incluidos R/I/S), sin clorofila inventada. Verificar resta separada de oscuro/blanco con un caso conocido.
4. Traza de acciones: bomba detenida antes de óptica; visible antes de azul; nunca ambas fuentes encendidas; apagado tras fallo. Fallos inyectados de cámara/sensor y plazo vencido no dejan un ciclo completo falso.
5. Interrupción durante cada fase de escritura y reinicio: datos previos intactos, ciclo interrumpido identificable y siguiente ID distinto. Simular disco lleno y segunda instancia, con rechazo seguro. Una prueba de proceso no demuestra resistencia a corte físico de energía.
6. Serie acelerada de 24 ciclos simulados sin superposición y con un fallo inyectado; exportación CSV/JSON recargable y recomputación de resultados desde originales y referencias. Registrar tamaño por ciclo, disponibilidad y todos los fallos. No contar esta serie como validación del instrumento o de su autonomía.

Comandos disponibles para la primera versión:

```sh
python3 -m unittest discover -s software/tests
python3 software/cruz.py --simulate --cycles 1 --config software/config/operation.example.json --output /tmp/cruz-sim
```

## 4. Siguiente conexión al hardware: puertas de entrada

| Paso | Prueba concreta | Condición previa |
| --- | --- | --- |
| A. Pi + cámara aisladas | Enumerar OV9281, confirmar RAW lineal y captura/ROI/metadatos; oscuro/blanco/muestra en banco con iluminación controlada externamente | Alimentación y cámara por conexiones conocidas; V8 desconectada. No habilita GPIO de potencia. |
| B. Sensores uno a uno | AS7265x: crudos/calibrados y plazos; DS18B20: CRC; Atlas: respuesta/unidad/compensación | Cableado, niveles, alimentación y bus revisados para cada módulo. No energizar una interfaz desconocida para identificarla. |
| C. Control con cargas de prueba | Confirmar niveles lógicos, arranque/reset, fallo de programa, exclusión de fuentes y pulsos del motor | Revisión eléctrica cerrada para esas señales, estados de fallo medidos y límite independiente para actuadores. Después, calibrar bomba y tiempos reales. |
| D. Servicio físico y autonomía | Transferir archivos completos con hash y reanudar descarga interrumpida; medir tiempo real por ciclo/descarga; apagado y siguiente despertar | Transceptor y EN3 verificados; definir protocolo tras medir volumen. Validar RTC/corte/guardado y fuga/batería antes de pruebas autónomas. |

Para D, propuesta a cerrar: Modbus RTU para consulta/estado/configuración y una operación de lectura por bloques de archivos con identificador, tamaño, offset e integridad, compatible con reanudación. No fijar registros, velocidad, direcciones, tamaño de bloque ni pines sin comprobar la electrónica real. La Pi apagada no sirve archivos: la sesión de servicio requiere un despertar y alimentación mantenida verificados.

El monitor actual permite probar cadencia y persistencia. El despliegue autónomo aún requiere captura óptica real, actuadores, supervisión independiente, fuga/batería, servicio físico, calibración y ensayo integrado. El panel se ofrece localmente y se puede consultar por túnel SSH. La interfaz final por el conector físico queda pendiente.

## 5. Evidencia de esta revisión

- Netlist XML exportada con KiCad CLI desde V8 a un archivo temporal; se inspeccionaron componentes, referencias y redes. No se alteró el diseño. Para repetir: `kicad-cli sch export netlist --format kicadxml --output /tmp/cruz-v8.xml electronica/cross_v8_raspberry/cross_v8_draft.kicad_sch`.
- Comprobaciones existentes ejecutadas: `MonoSpectro/spectro_math.py`, `Fluorometer/tests/check_white.py` y `Fluorometer/tests/check_firmware.py`: todas pasan. La primera comprueba las ecuaciones actuales, incluidos sus recortes; la segunda ejecuta C++ con dispositivos simulados; la tercera comprueba principalmente estructura/texto y fórmula del firmware. No demuestran validez óptica ni compatibilidad con Pi.
- No se ejecutó una adquisición ni se instaló software en la Pi. Sin hardware activado, sin descarga física, sin pruebas de corte eléctrico. No se modificó ni recompiló firmware ESP32. Sin commit ni push.

Identificación de las fuentes locales leídas (SHA-256; HEAD orientativo, el hash de archivo identifica el contenido revisado):

| Fuente | SHA-256 |
| --- | --- |
| V8 esquema | `d2a346aeb1e3ee872ee54396d219a7cd4b42f6284495c0c0832b75d14ea90863` |
| V8 PCB | `1c81c5b83dc3ce8274b2ce2147d3c1f0fb1775d53a8852257a7018e004bbaf1a` |
| MonoSpectro `app.py` (HEAD `65af45a`) | `80f98575bbc6f7c085074f58ec61191ebfe79ea363b290f1b14f0b5611206d1d` |
| MonoSpectro `spectro_math.py` | `a18d3aad9b54bf1f4f68edbbe4af82ec35d9c20fde597ddb87479d9c150f844c` |
| Fluorometer `Spectro18_V_Flu.ino` (HEAD `f2cdedf`) | `d92809bafaec65f469ed563e159c1b481de33873a30606bbee781af6ff1a0934` |
