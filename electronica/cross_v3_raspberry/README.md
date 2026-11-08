# PCB Raspberry — V3 de trabajo, no fabricable

**Revisión posterior:** [PCB V4 con ramal de carga](../cross_v4_raspberry/README.md), también incompleta y no fabricable.

**Estado: borrador incompleto. No fabricar ni energizar.**

Esta versión continúa `cross_v2_raspberry`. Alex pidió terminar el PCB e incorporarlo a Fusion; se ha avanzado en la conexión Atlas y se ha incorporado una representación mecánica, pero el esquema, la alimentación y el trazado no están terminados.

## Cambio en J9

El conector lógico de cuatro pines V2 se sustituye por un zócalo provisional de cinco pines para la interfaz Atlas Scientific aislada Gen 2. Según la [ficha del fabricante](https://files.atlas-scientific.com/electrically-isolated-ezo-carrier-board.pdf):

| Pin en el borrador | Señal | Red en PCB |
|---:|---|---|
| 1 | VCC | 3V3_PI |
| 2 | OFF | Sin conectar (el fabricante permite dejarlo libre) |
| 3 | GND anfitrión | GND |
| 4 | TX/SDA | SDA |
| 5 | RX/SCL | SCL |

El EZO debe configurarse en I²C. La correspondencia refleja la señalización publicada para Gen 2, **no una comprobación de la placa de Alex ni de la orientación del zócalo al enchufarlo**. Comprobar revisión real, pin 1, orientación, paso, altura, fijaciones, aislamiento, espacio del conector SMA y posición del conjunto 56,2 × 32 mm. La placa Atlas necesita soporte mecánico: un zócalo no basta para demostrar que soporta los esfuerzos.

## Ficheros y comprobaciones

- `cross_v3_draft.kicad_sch` y `cross_v3_draft.kicad_pcb`: archivos editables de KiCad 9. La alimentación, carga, despertador configurable, puerto y varias huellas siguen sin diseñar.
- `erc.txt`: 29 incidencias (2 entradas de alimentación no declaradas, 27 avisos de discrepancia de símbolos). Necesita revisión eléctrica completa.
- `drc.txt`: sin errores de colocación según las reglas provisionales y sin diferencias de paridad; **73 conexiones sin trazar**. No prueba seguridad ni fabricabilidad.
- Se compararon las conexiones de pines exportadas desde el esquema y desde la placa: coinciden. Es una verificación de consistencia, no una validación del circuito.
- [`PCB_V3_BORRADOR_NO_FABRICAR.step`](../../cad/fusion_m2/PCB_V3_BORRADOR_NO_FABRICAR.step) es el modelo exportado del borrador. KiCad no encontró el modelo 3D de U1 (A4988); convertidores, control de alimentación y otras placas aún faltan. Los modelos de conectores y componentes son provisionales.

## Fusion

Se incorporó `PCB_V3_BORRADOR_NO_FABRICAR` al documento activo `Cross_M2_horizontal_design` el 2 noviembre de 2026, sin guardar el documento. El componente de PCB mide aproximadamente 170 × 68 mm en planta y se colocó sobre el área de la bandeja; su cara inferior queda a unos 8 mm de la cara superior de la bandeja según las cajas de Fusion. No hay separadores ni taladros de fijación aprobados.

**Hay solapamientos de cajas envolventes** con las referencias antiguas de los convertidores, A4988, RTC, RS485, relé y otros componentes. Son referencias de una implantación anterior: no se eliminó ni ocultó la geometría del usuario. Reubicar las piezas reales, diseñar sus zócalos y soportes y volver a ejecutar una comprobación de interferencias antes de dar por válido el montaje. El ensamblaje conserva cambios sin guardar; esta operación no guardó ni sustituyó el documento.

## Pendiente crítico

1. Definir y verificar el encendido autónomo con intervalo configurable, hora, apagado seguro y gestión de fugas durante el reposo. La Raspberry no tiene sueño profundo equivalente a un microcontrolador.
2. Diseñar batería, protección, conmutación, DFR1015 y carga. Confirmar tensión real de batería y salida del cargador y disposición de terminales. DFRobot recomienda menos de 24 V a la entrada del DFR1015 aunque declara un intervalo de 7,5–30 V: no se ha demostrado que el pack cumpla esa recomendación cargado.
3. Completar interfaz aislada RS485, conexión de carga y pinout de servicio, driver de LED azul con estado seguro, protección eléctrica y vigilancia de batería/fugas.
4. Comprobar dimensiones y correspondencia de pines de módulos reales; integrar sus envolventes y zócalos. Verificar corriente de fase del motor y resistencias de sensado/ajuste del A4988.
5. Revisar ERC, rutear según corriente y dimensiones reales, realizar DRC y ensayos eléctricos y térmicos. Probar estanqueidad sin electrónica antes del montaje.

No se ha hecho prueba eléctrica, de estanqueidad ni de campo. La lista de compra de D52 no es una BOM definitiva para esta revisión.

## Datos de alimentación confirmados por Alex

Alex corrigió su respuesta: el cargador indica **25,6 V**, y el pack tiene **un solo par de conexiones para carga y alimentación**. La conexión funcional revisada y sus comprobaciones pendientes están en [Alimentación y carga](ALIMENTACION_Y_CARGA.md). La cifra 14,2 V queda descartada. El circuito de carga todavía no está incluido en el KiCad.
