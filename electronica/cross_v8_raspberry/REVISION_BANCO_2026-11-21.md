# Adaptación de V8 a los ensayos de banco

21 de noviembre de 2026 · Codex GPT-6 · Esquema y placa editados, sin energizar hardware.

La V8 incorpora la plataforma de banco Pi 5, halógena de transmisión y tres LED de excitación conforme a D55/D56 y al [traspaso de banco](../../docs/SOFTWARE_ADQUISICION.md#traspaso-al-chat-del-pcb--pruebas-de-banco-del-21-de-noviembre-de-2026). La disposición óptica es en T: brazo común y AS7265x a 90°. Se conservan los ensayos como resultados comunicados por Alex; esta edición no añade una validación física del circuito integrado.

## Cambios en el esquema

| Parte | Cambio guardado |
| --- | --- |
| U6 | Salida propuesta de **12 V**, sustituye `9V_OPT`. DFR1015 conservado como candidato, capacidad de arranque y térmica pendientes. |
| Halógena | J3 para 12 V/10 W; Q1 ahora **IRLZ44N**, conmutación por el retorno. Se retira el driver anterior del Optisolis. |
| Azul | J4 para LED 420–430 nm; **U2 LM317**, R4/R42/R43 = 26 Ω ∥ 26 Ω ∥ 52 Ω; Q7 ahora IRLZ44N. Se elimina D8 y la inversión anterior. |
| Naranja | J5 para LED de 620 nm; **U14 LM317**, R44/R45/R46 con la misma red de 10,4 Ω; Q8 IRLZ44N. |
| IR | J27 para TSHG6410; **R47 = 220 Ω/1 W**, Q9 IRLZ44N. Corriente final sin medir. |
| Buffer | **U9 SN74AHCT125N**, alimentado desde 5V_PI; cuatro canales activos altos. C7 = 100 nF; entradas con 10 kΩ a GND, puertas con 470 Ω en serie y 120 kΩ a fuente. |
| Armado óptico | **Q10/R30/R31/R32** controlan conjuntamente las cuatro entradas OE de U9. `OPT_ARM` bajo o flotante deshabilita salidas. GPIO adicional BCM21/pin 40; sin conflicto con los GPIO conservados. |
| Regulador 23 | **U10 AP2112K-3.3**, propuesta 5V_PI → 3V3_SENS; C8/C9 = 1 µF X7R. EN sigue 3V3_PI, no toma la corriente de los sensores de esa salida de la Pi. Térmica y consumo conjunto pendientes. |
| Sensores | J8 y J10 reciben 3V3_SENS. R10, pull-up de 1-Wire de 4,7 kΩ, también pasa a esa rama. |
| Desconexión de señales | **U11 SN74CB3Q3125PW**, alimentado por 3V3_PI, separa SDA/SCL/1-Wire de los sensores cuando la Pi pierde esa alimentación, según su característica Ioff. C10 = 100 nF. No es aislamiento galvánico. |
| Conductividad | Se retira J9 Gen 2. **U12 EC-OEM** de diez pads, huella local `Cross:Atlas_EC_OEM_10pad`, según ficha v3.4, p. 35. J28 representa la terminación de sonda, aún por cotejar con el coaxial real. |
| Aislamiento EC | **U13** representa exclusivamente el requisito de aislar alimentación y SDA/SCL. Está excluido de BOM y placa, **sin componente físico seleccionado**. Dominios 3V3_EC_ISO/GND_EC_ISO; no se unen a 3V3_SENS/GND. |
| Interfaz de Pi | J1 pasa a cabecera IDC 2×20, paso 2,54 mm, para cinta GPIO. Pines de 5 V de J1, 2/4, siguen sin conectar en la PCB; alimentación de Pi por J23/cable USB-C. |

Las fuentes se representan mediante conectores para los emisores externos. La halógena no pasa por LM317; azul y naranja sí. Se mantienen los identificadores de los componentes existentes cuando cambia su función, para facilitar el contraste con el montaje anterior. El bloque 06 contiene ahora el buffer, el 10 las etapas ópticas y el 11 el regulador y las interfaces de sensores; las demás posiciones del esquema se conservan. Hoja ampliada a A0 para incluir estos bloques.

R26/R27 son pull-ups de I²C del lado de sensores marcados DNP hasta comprobar las resistencias existentes en AS7265x y en el aislador seleccionado. R28/R29 son los pull-ups del lado aislado EC; deben coordinarse con ese aislador. El bus compartido se prevé a **100 kHz**, compatible con el límite documentado del EC-OEM.

## Corrientes y alimentación que siguen abiertas

La red de **10,4 Ω** tiene una consigna ideal LM317 de `1,25/10,4 ≈ 120 mA`. Alex comunicó **110 mA medidos** en azul y naranja; se conserva la red ensayada, sin declarar ambas cifras equivalentes. Comprobar tensión OUT–ADJ, resistencias y corriente en el montaje final. Cada resistencia de 26 Ω disiparía unos 0,060 W y la de 52 Ω unos 0,030 W a 1,25 V. El LM317 puede disipar del orden de 1 W desde 12 V según la caída del LED; seleccionar disipación a partir de temperatura medida dentro del cuerpo. No hay condensador de salida cargado conectado en paralelo al LED. [Aplicación LM317](https://www.ti.com/lit/ds/symlink/lm317.pdf)

Para el IR, `(12−Vf−VDS)/220` da aproximadamente 48 mA con Vf alrededor de 1,4 V; la resistencia disipa aproximadamente 0,51 W. Su potencia de 1 W necesita margen térmico en la envolvente. El límite continuo de 100 mA de la ficha no es una consigna. [Vishay TSHG6410](https://www.vishay.com/docs/81870/tshg6410.pdf)

La halógena requiere **0,83 A nominales en régimen**, con arranque en frío sin medir con U6. Con los cuatro canales encendidos simultáneamente, el consumo estacionario previsto en 12 V sería aproximadamente 1,12 A usando las consignas ideales de los LED, antes de pérdidas y tolerancias; el pico de arranque puede dominar. El circuito no impide por hardware encender varios canales: software debe seleccionar la fuente y el dimensionado debe contemplar errores de operación.

Las pestañas metálicas de los IRLZ44N están conectadas a sus drenadores, y las de LM317 a OUT. No unirlas eléctricamente mediante un disipador compartido: verificar aislamiento de pestañas y tornillos si comparten soporte térmico.

U10 es una selección de esquema pendiente de comprobar térmicamente: `P ≈ (5−3,3)×I`. Su capacidad eléctrica de 600 mA no implica poder disipar 1,02 W en SOT-23-5 dentro del instrumento. Los emisores integrados del AS7265x deben permanecer desactivados salvo ensayo explícito. [AP2112](https://www.diodes.com/datasheet/download/AP2112.pdf)

El EC-OEM especifica 10,6–26 mA a 3,3 V según conductividad; no corresponde al consumo del EZO/Gen 2 anterior. Añadir las pérdidas de la etapa aislada y los demás sensores antes de cerrar U10. El aislador debe soportar I²C bidireccional, sus umbrales y capacidad de bus, entregar alimentación regulada dentro del rango OEM y mantener la separación de retornos. INT no se utiliza. Pad 4 PRB y pad 5 PRBG van solo a la sonda; PRBG **no se conecta a GND_EC_ISO**. [Atlas, pp. 6–7, 31 y 35](https://files.atlas-scientific.com/EC_oem_datasheet.pdf)

U5 queda marcado para revisar con Pi 5, OV9281, webcam USB, U9 y U10. Pi 5 puede arrancar con 5 V/3 A, pero la documentación reduce el presupuesto USB a 600 mA si no se dispone de la alimentación de 5 A correspondiente. La webcam detectada no acredita consumo bajo todas las condiciones. Verificar el cable USB-C, la identificación de la fuente y la tensión en Pi bajo carga; no limitarse a la marca «5 A» del convertidor. [Raspberry Pi](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#power-supply)

**Inventario corregido por Alex después de esta edición:** solo hay un DC/DC disponible para 24 V → 12 V. Los tres módulos dibujados son propuestas funcionales, no existencias confirmadas. Se necesita otra conversión a la alimentación de 5,1 V recomendada para Pi 5; 12 V directos no son admisibles. La alternativa batería → 5,1 V separa la conversión de Pi de la carga de la halógena, pero exige margen para el pack cargado y transitorios. La alternativa 12 V → 5,1 V exige que el DC/DC de 12 V soporte también la potencia de Pi. No se cambia aún el esquema ni se da por cerrado el suministro permanente.

Batería comunicada: 24 V/3 Ah, carga 25,2 V, salida 22–25 V (5–8 A); cargador 25,2 V/2 A. Siguen pendientes tolerancia, máximo medido y límites continuos/pico del BMS. F1/F2 continúan sin calibre: F2 no se cierra copiando los 2 A del cargador. U4 AON queda antes del Pololu; su protección de polaridad y los transitorios de batería/interruptor aún no están resueltos. Los tres DFR1015 siguen por encima de la recomendación de entrada inferior a 24 V. TVS y clamp necesitan un cálculo con la tensión máxima y el componente más débil; no se ha añadido una TVS de valor arbitrario.

Para bomba se mantiene A4988, C1 = 100 µF/50 V y los GPIO de banco. R050 implica `I_tripmax = Vref/0,4`; no se fija un Vref final sin corriente nominal por fase. Dos bobinas de 2,9 Ω y potencia de conjunto de 20 W no determinan ese límite. El DRV8834 blanco queda descartado para la rama de 24 V. Margen de VMOT, picos, disipación y repetibilidad siguen abiertos.

## Tabla vigente para software

BCM y pin físico no son intercambiables. Las señales descritas son las guardadas en esta revisión, pendientes de ensayo integrado.

| Señal | BCM | Pin físico J1 | Estado eléctrico |
| --- | ---: | ---: | --- |
| SDA / SCL | 2 / 3 | 3 / 5 | I²C 1, 3,3 V; sensores tras U11. AS7265x 0x49, EC-OEM 0x64 tras aislamiento pendiente. |
| TEMP_1WIRE | 4 | 7 | DS18B20 tras U11; pull-up R10 a 3V3_SENS. |
| M_STEP / M_DIR | 17 / 18 | 11 / 12 | Paso/dirección conservados. R2/R3 a GND. |
| M_ENABLE_N | 27 | 13 | **Bajo habilita**; R1 de 10 kΩ mantiene deshabilitado con la lógica alimentada. |
| HAL_EN | 22 | 15 | **Alto enciende** la halógena si OPT_ARM=1. Sustituye WHITE_EN. |
| BLUE_EN | 23 | 16 | **Alto enciende** el azul si OPT_ARM=1. Eliminada la inversión de V8 anterior. |
| ORANGE_EN | 16 | 36 | **Alto enciende** naranja si OPT_ARM=1. GPIO de banco conservado. |
| IR_EN | 20 | 38 | **Alto enciende** IR si OPT_ARM=1. GPIO de banco conservado. |
| OPT_ARM | 21 | 40 | **Alto habilita** las cuatro salidas del buffer. Bajo/flotante inhibe mediante Q10 y R30. Nueva señal de V8. |
| CHARGE_CTRL | 24 | 18 | Alto solicita relé de carga, sujeto al bloqueo del piloto. Sin cambios. |
| PILOT_SENSE | 25 | 22 | Bajo detecta piloto; verificar umbrales. Sin cambios. |
| SW_SENSE | 5 | 29 | Bajo detecta imán. Sin cambios. |
| HOLD_PI | 26 | 37 | **Alto solicita corte**, llega a RESET de U8. No es una señal de mantener alimentación. |
| UART_TX / UART_RX | 14 / 15 | 8 / 10 | RS-485 mediante DFR0845; puerto Linux y consola por verificar para Pi 5. |

Secuencia prevista: iniciar OPT_ARM=0 y las cuatro órdenes a 0; configurar bomba deshabilitada; habilitar OPT_ARM solo al estar listo. Entre fuentes, poner todas a cero antes de seleccionar la siguiente y respetar la estabilización medida. Al apagar, desarmar y desactivar bomba, cerrar archivos, programar/liberar RTC y emitir HOLD_PI únicamente en la etapa final del apagado.

Con GPIO flotantes, los pull-downs fijan entradas y puertas; R30 eleva OE y Q10 queda apagado. Si la Pi pierde 3V3_PI, U10 se deshabilita y descarga su salida y U11 ofrece desconexión Ioff de las señales de sensores. Esto es una revisión de esquema basada en fichas, **no un ensayo de rampas**: comprobar arranque, reset, brownout, caída relativa de 12/5/3,3 V, tensión en puertas y corriente hacia la Pi apagada. USB externo, ADC y otras interfaces también requieren revisar alimentación parásita; U11 no protege por sí solo todos los puertos del instrumento. [SN74CB3Q3125](https://www.ti.com/lit/ds/symlink/sn74cb3q3125.pdf), [SN74AHCT125](https://www.ti.com/lit/ds/symlink/sn74ahct125.pdf)

El programa de banco `software/pruebas/leds_cruz.py` corresponde al cableado ensayado de tres canales; no configura OPT_ARM ni controla la halógena. Se conserva sin modificar como evidencia de ese ensayo. No usarlo como controlador final de esta PCB. El 74AHCT125 debe ser la variante AHCT; no sustituirlo por AHC a 5 V suponiendo los mismos umbrales.

El encendido magnético y el RTC externos conservan sus pendientes: U8 no dispone de un reset inicial definido; un SET mantenido por imán, piloto o alarma puede impedir el corte. Tampoco hay un watchdog externo o detector de fuga que desconecte potencia con Linux bloqueado. Esta revisión no declara resueltos esos fallos.

## Cinta GPIO y reservas de cámaras

Alex propone el [kit TinyTronics 000883](https://www.tinytronics.nl/nl/development-boards/accessoires/adapter-boards/raspberry-pi-40-pins-gpio-extension-kit): incluye cinta de **40 contactos y 20 cm**. Se prevé usar solo la cinta entre Pi 5 y J1, sin la placa de protoboard. J1 usa `Connector_IDC:IDC-Header_2x20_P2.54mm_Vertical`; antes de cerrar orientación y montaje, verificar conectores reales, muesca, pin 1 y continuidad 1:1 de los 40 contactos. No confiar solo en la raya del cable o en rótulos del adaptador. Validar el bus a 100 kHz con el cable y todas las cargas de señal instaladas. La cinta transporta señales y referencias lógicas; bomba, lámparas y alimentación principal de Pi usan sus conexiones de potencia propias.

Se reserva CAM/DISP 1 para la OV9281 Arducam, ya ensayada a 1280×800/RAW10, y una ruta USB interior para O04 icSpring 32e6:9281, que produjo JPEG 3264×2448. Son reservas de interfaz, no conectores FFC/USB añadidos a esta PCB. Coordinar con CAD la cinta GPIO, FFC, acceso USB y enfoque a través de tapa; no modificar el montaje mecánico desde esta revisión.

## Comprobaciones y estado de la placa

- **ERC: cero errores y 29 avisos de biblioteca.** Se han actualizado cinco definiciones compartidas de componentes después de comprobar idénticos números, tipos eléctricos y posiciones de pines. No se han silenciado reglas. Los módulos DFR1015 declaran ahora su salida de potencia; las referencias externas de 3V3_PI y GND están explicitadas. U13 sigue siendo un bloque funcional no implementado aunque suministre referencias en el esquema.
- **Paridad: cero diferencias** entre esquema y placa. 113 huellas, incluidas R26/R27 DNP; U13 excluido físicamente. No se ha creado una huella ficticia para el aislador pendiente.
- **DRC: 283 conexiones pendientes y 50 avisos de serigrafía.** Sin otros errores de colocación en la comprobación final. Esto no valida una placa fabricable: 43 huellas nuevas o sustituidas, incluido el IDC J1 más grande, están aparcadas fuera del contorno y marcadas para colocar. Las otras 70 conservan posición y orientación. Contorno 170×68 mm y ausencia de trazado conservados; cabida del conjunto pendiente.
- Se verificaron las redes de todas las referencias ajenas al cambio sin diferencias. La comprobación [comprobar_conexiones.py](../revision_banco_2026-11-21/comprobar_conexiones.py) exporta el esquema actual y verifica señales, polaridades por pin, resistencias en paralelo, separación de retornos EC y alimentación de sensores. No simula transitorios ni térmica.

Informes y huellas SHA256 en [revision_banco_2026-11-21](../revision_banco_2026-11-21/). Respaldo anterior recuperable fuera del repo: `/Users/alex/.codex/backups/Cruz/2026-11-21_antes_banco`. No se usaron los generadores históricos para sustituir el diseño; se preservaron los elementos ajenos a esta edición.

Antes de fabricar: seleccionar e integrar físicamente el aislamiento EC, cerrar U5/U6 y fusibles con ensayos, resolver protecciones y enclavamiento, confirmar conectores/huellas y hacer colocación, trazado y nueva revisión completa.
