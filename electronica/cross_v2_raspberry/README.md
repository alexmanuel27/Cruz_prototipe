# CROSS V2: Raspberry Pi carrier — borrador de trabajo

**Existe una revisión posterior:** [V3 de trabajo](../cross_v3_raspberry/README.md), también incompleta y no fabricable.

**Estado: INCOMPLETO. NO FABRICAR, NO SOLDAR, NO ENERGIZAR.**

Este primer archivo editable permite estudiar la interfaz de la Raspberry, el A4988 y algunos sensores. No es un PCB terminado ni una definición mecánica válida para cerrar el diseño en Fusion. Conserva aparte el proyecto anterior `electronica/cross/`.

## Archivos

- `cross_v2.kicad_sch`: esquema parcial KiCad 9.
- `cross_v2.kicad_pcb`: colocación preliminar de 170 × 68 mm, sin pistas ni taladros de fijación. Se tomó como referencia solo la bandeja de 177 × 70 mm de los parámetros de Fusion guardados en disco; esa versión mecánica tiene comprobaciones fallidas y no necesariamente refleja el documento abierto. No están colocadas las dimensiones reales de las placas enchufables.
- `cross_v2_erc.txt` y `cross_v2_drc.txt`: informes brutos de KiCad, no aprobaciones.

## Qué incluye el borrador

Interfaz GPIO a la Pi con alimentación de la Pi prevista por USB-C independiente; zócalo lógico A4988 y conector de bobinas; circuito provisional del LED blanco con LM317 y transistor; interfaz incompleta al driver del LED azul; conectores lógicos I²C y DS18B20; divisor de tensión y puntos para un ADS1115. El rango `VBAT_SW` todavía no está aprobado y el esquema no contiene una batería ni su cargador conectados.

Los conectores que representan placas son **provisionales**: J6 y J7 no representan el zócalo físico real del ADS1115, J4/J5 no son el zócalo real del driver azul, y los conectores de sensores son interfaces para revisión, no selección de conectores. El A4988 debe compararse con el módulo real: la huella muestra la geometría nominal del portador, no el volumen de sus zócalos ni un modelo 3D de su placa. No se ha diseñado el montaje enchufable de los tres convertidores, el driver azul, el ADS ni las demás placas. Los conectores de batería y motor necesitan dimensiones y corriente aprobadas, y pueden ser distintos de los pines de 2,54 mm que aparecen como marcadores.

## Pendiente antes de una placa fabricable

1. Encendido y apagado autónomos con intervalo configurable, hora conservada y apagado seguro de Linux. La Pi 4 no ofrece un modo de sueño profundo equivalente al ESP32. Un temporizador de intervalo fijo no cumple por sí mismo la programación desde configuración. Evaluar el circuito RTC con alarma y enclavamiento o un módulo comercial adecuado; comprobar consumo en reposo, arranque por cable y que la Pi no reciba tensión por señales cuando esté apagada.
2. Esquema completo de batería, protección, distribución, convertidores, accionamiento del rail del motor y carga mediante el conector de servicio. Confirmar tensión máxima real y terminales de carga del pack, así como corriente y tensión del cargador. La tensión nominal «24 V» no especifica la tensión máxima. Verificar el margen de los convertidores de 30 V y la corriente asignada a fusibles, conectores, interruptor y pistas.
3. Integra RS485 y la asignación real de pines del conector de ocho contactos, además del detector de fugas y el despertador. Con la Pi apagada, el detector conectado a su ADC no vigilaría continuamente: la protección autónoma debe diseñarse si se exige actuación inmediata.
4. Medir módulos y conectores que Alex ya tiene, comprobar la numeración real de sus pines y diseñar sus zócalos, su altura, separación y soporte. Comprobar que los interfaces y fuentes I²C funcionen a 3,3 V y que no haya retroalimentación de placas apagadas. Verificar el estado apagado del driver azul: el esquema todavía no incorpora la resistencia ni el circuito de inhibición necesarios.
5. Identificar pares y corriente por fase del motor, resistencia de sensado y ajuste del A4988; confirmar su compatibilidad térmica. El condensador de entrada es provisional y debe situarse cerca de VMOT. El fabricante advierte no conectar ni desconectar el motor con el controlador alimentado.
6. Revisar el esquema visual y eléctricamente, hacer coincidir esquemático y PCB en KiCad, colocar mecánicamente piezas reales, rutear con reglas de corriente y separación justificadas, revisar ERC/DRC completos, preparar BOM y solo después exportar STEP y archivos de fabricación.

## Comprobaciones realizadas el 2 de noviembre de 2026

- KiCad 9.0.7 abre y exporta el esquema y ejecuta ambas comprobaciones.
- Comparación automática entre los conjuntos de pines conectados del esquema exportado y los de la placa: coinciden. KiCad también informa **0 diferencias de paridad** entre esquema y placa; esto no sustituye una revisión eléctrica.
- ERC: **29 incidencias**: 2 errores de entrada de alimentación no declarada y 27 avisos de diferencias entre símbolos insertados y biblioteca. No está aprobado. La generación automática también colocó incorrectamente una masa sobre un GPIO; se retiró, junto con R7, al detectarse. Falta diseñar de nuevo la inhibición del LED azul.
- DRC con comprobación de paridad: **73 conexiones sin trazar**, 0 diferencias de paridad y ninguna otra incidencia en la colocación actual. Las huellas y reglas son provisionales, por lo que este resultado no demuestra que el PCB sea fabricable ni seguro.
- No hay montaje, pruebas eléctricas, ensayo de estanqueidad, validación térmica ni ensayo de campo registrados para esta placa.

El documento anterior `DISENO_ELECTRICO_V1.md` contiene decisiones con ESP32 y queda superado allí donde contradiga esta revisión. Su lista de compra necesita actualización cuando se cierre el nuevo circuito; no usarla como BOM definitivo de V2.

## Referencias aportadas por Alex — 2 de noviembre

- **A4988:** [WJMY B08R64Y7V7](https://www.amazon.com.be/-/en/WJMY-Stepper-Motor-Driver-Module/dp/B08R64Y7V7). Amazon no entregó la ficha a esta consulta; [otra ficha del mismo ASIN](https://www.bol.com/nl/nl/p/stappenmotor-driver-modul-stepstick-stappenmotor-driver-met-warmteverdeler-voor-3d-printer/9300000394436602/) indica 20 × 15 × 11 mm. Confirmar orden de pines, dimensiones del zócalo, sentido de inserción y resistencia de sensado del ejemplar; la referencia no demuestra compatibilidad eléctrica ni corriente por fase.
- **DC/DC confirmado por Alex:** [DFRobot DFR1015](https://www.dfrobot.com/product-2599.html). Su fabricante indica 7,5–30 V de entrada pero recomienda menos de 24 V; solo da una salida seleccionada cada vez y declara los 5 A con disipación adecuada. No aceptar su uso con el pack hasta confirmar el modelo y medir la tensión de carga completa y transitorios.
- **Placas de sensores:** Alex indica usar las dimensiones del AS7265x que ya existe en Fusion: envolvente 45 × 36 × 4,5 mm ([referencia y posición](REFERENCIA_SENSOR_FUSION.md)); la página de AliExpress no fue accesible para verificar conectores y la del [kit Atlas K1.0](https://atlas-scientific.com/kits/conductivity-k-1-0-kit/). El kit actual incluye interfaz aislada Gen 2 de 56,2 × 32 mm; confirmar la revisión física recibida. [Modelo 3D de referencia](../../cad/componentes/atlas_isolated_carrier/README.md). El termómetro y la sonda permanecen conectados mediante cable. La óptica del AS7265x debe mirar la cubeta y puede requerir una ubicación distinta a la placa principal.

### Corrección importante de J9 (2 noviembre)

**J9 es un conector lógico de 4 pines; no coincide con la conexión física de 5 pines del Atlas y NO es un zócalo para enchufar el módulo.** No conectarlo directamente. La interfaz Gen 2 documentada por Atlas tiene VCC, OFF, GND, TX/SDA y RX/SCL; alimentar el lado anfitrión a 3,3 V, configurar el EZO en I²C y dejar OFF sin conectar o a VCC, según el fabricante. La disposición física y la orientación se incorporarán al esquema y a la placa después de confirmar la revisión y su montaje. Mantener aisladas las masas de sonda y anfitrión. El A4988, DFR1015 y las demás huellas tampoco han sido verificados físicamente.

Fuentes: [manual de la placa Atlas](https://files.atlas-scientific.com/electrically-isolated-ezo-carrier-board.pdf) y [datos del DFR1015](https://www.dfrobot.com/product-2599.html).

### Conexión AS7265x confirmada por Alex

El sensor usa cuatro cables: alimentación, masa, SDA y SCL. En el esquema J8 propone, respectivamente, 3V3_PI, GND, SDA y SCL en los pines 1–4. Este orden pertenece al conector provisional del PCB, no establece el orden físico en el módulo. Alex confirmó alimentación e I²C a 3,3 V; comprobar las resistencias pull-up y el cableado durante la puesta en marcha. El conector J8 sigue siendo una huella provisional sin rutear.
