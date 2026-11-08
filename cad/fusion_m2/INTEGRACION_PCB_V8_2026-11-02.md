# Integración provisional de PCB V8 en Fusion

## Estado

Se importó `PCB_V8_ESTUDIO_NO_FABRICAR.step`, exportado de la placa V8 de KiCad sin rutear, como `PCB_V8_ESTUDIO_NO_FABRICAR` en el documento activo `Cross_M2_horizontal_design`. La placa y sus módulos son referencias para estudiar espacio; el PCB no está listo para fabricar ni para energizar. Se ocultó la referencia de PCB V4, sin borrarla.

Alex dio libertad para elegir las dimensiones con menor riesgo de espacio. Para este estudio se mantuvo el modelo existente en Fusion de **180 mm exterior, 170 mm interior y 380 mm de largo**. La opción anterior de compra de 150/140 × 330 mm no corresponde a esta geometría. Esto no certifica la resistencia a presión ni equivale a una selección de tubo comprado.

Se ocultaron referencias obsoletas duplicadas en `05_ELECTRONICS_REFERENCES`: ESP32 (descartado), tres DFR1015, A4988, relé y regulador blanco. Las referencias del RTC, RS-485, driver azul y bloque de potencia permanecen como envolventes aproximadas porque sus módulos no están integrados en la placa. Ninguna referencia antigua fue borrada.

Se exportó el estado activo a `CROSS_M2_PCB_V8_ESTUDIO_NO_FABRICAR.f3d`, como copia de intercambio; el documento activo quedó con cambios sin guardar. La geometría importada es una referencia STEP, no una placa editable de Fusion Electronics.

## Ubicación y comprobaciones

- Posición de inserción de la placa: traslación X = 199 mm, Y = 34 mm, Z = 55 mm, sobre la zona de la bandeja superior. Su envolvente total aproximada, incluidos componentes, queda en X = 198,98–369,02 mm; Y = −34,02–34,02 mm; Z = 46,825–75,39 mm. La bandeja existente está por debajo; no se han diseñado fijaciones de la V8.
- `Design.analyzeInterference`: cero intersecciones entre el conjunto PCB y tubo acrílico, bandeja, piezas del chasis frontal y trasero, batería, motor, cabezal de bomba, cubierta óptica superior, portaelectrónica Atlas y pasamuros de entrada/salida examinados.
- La manguera cubeta → bomba interseca la PCB o sus componentes en seis volúmenes; la manguera bomba → descarga en dos. Las mangueras son propuestas aproximadas, con boquillas de bomba aún sin cotejar. La bandeja también interseca ambas mangueras en la geometría existente.
- Una colocación lateral positiva interseca el cabezal de la bomba y la sección trasera del chasis; lateral negativa interseca batería, referencia Atlas y chasis. Las variantes probadas sobre la óptica presentaron interferencia con el tubo o con la manguera de la cubeta. Estos ensayos no son una búsqueda exhaustiva.

## Pendiente antes de fabricación

1. Rediseñar la colocación y el recorrido hidráulico completo sin cruces con PCB, bandeja, bomba y envolvente; mantener entrada → cubeta → bomba → salida, con radios de curvatura verificables y sin cargar la cubeta. Dimensionar a partir de la bomba, la cubeta y sus conexiones físicas.
2. Diseñar soportes y fijaciones de la placa, reserva para cableado, extracción, refrigeración y conexión a módulos externos. La PCB V8 no tiene disposición de fijación validada.
3. Terminar el diseño electrónico, definir y medir todos los componentes y actualizar el modelo 3D de la placa.
4. Resolver la estanqueidad: tapa de acrílico, juntas, superficies, compresión limitada, pasamuros y conductos, presión y ensayos. Los componentes y las dimensiones marcadas HOLD en M2 siguen sin validar. Realizar el ensayo con lastre y sin electrónica.
5. Repetir interferencias con todas las piezas finales, despeje de mangueras y cables, cámara y accesorios; validar estabilidad, pesos, sujeción, material y fabricación. No usar este archivo como plano de producción.
