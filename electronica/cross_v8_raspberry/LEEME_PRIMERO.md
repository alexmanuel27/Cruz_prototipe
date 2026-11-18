# V8 — esquema corregido y ensayo de trazado. NO FABRICAR NI ENERGIZAR

El proyecto continúa en desarrollo. El esquema y la placa sin rutear coinciden eléctricamente en la comprobación de paridad de KiCad. Las 52 redes con más de un terminal del esquema exportado coinciden por nombre y por terminales con las redes previstas en la V7. Esta comprobación **no prueba que los circuitos sean adecuados ni seguros**.

El 18 de noviembre de 2026 se organizó el esquema en nueve bloques funcionales. Las conexiones siguen representadas mediante etiquetas de red; la comparación de las 77 redes antes y después resultó idéntica. ERC de KiCad 9: 80 incidencias antes y después (77 discrepancias con biblioteca y 3 entradas de alimentación sin fuente identificada).

## Archivos

- `cross_v8_draft.kicad_sch`: esquema con las conexiones accidentales de V7 corregidas. Componentes separados con etiquetas de red.
- `cross_v8_draft.kicad_pcb`: colocación sin rutear, 170 × 68 mm. Las dimensiones de las huellas, conectores y módulos deben comprobarse.
- `modelos_3d/Pololu_2814_fabricante.step`: modelo oficial Pololu descargado de [recursos del fabricante](https://www.pololu.com/product/2814/resources); el módulo todavía no está colocado en la placa ni su huella y conexiones están definidas.
- `REVISION_ERC.txt`, `REVISION_DRC_SIN_TRAZAR.txt`, `REVISION_DRC_EXPERIMENTAL.txt`: informes de KiCad del 2 de noviembre de 2026.
- `generar_esquema_corregido.py` y `comprobar_redes.py`: instrumentos históricos de desarrollo; el generador requiere restaurar V7 desde Git y adaptar las rutas antes de reutilizarlo.

## Resultados de revisión

- Esquema: 83 incidencias ERC, entre ellas 3 entradas de alimentación que KiCad no identifica como alimentadas porque las fuentes se representan con conectores pasivos. No se han marcado como resueltas con indicadores de alimentación ficticios; revisar fuente y retorno reales.
- Placa sin rutear: 199 conexiones sin trazar, 57 avisos/incidencias DRC y cero diferencias de paridad con el esquema.
- Placa con trazado experimental: 20 conexiones sin trazar y 77 incidencias, incluida una separación de cobre insuficiente al borde. Los recorridos de alimentación no están dimensionados. Es una prueba, no una placa completa.

## Pendiente para terminar

1. Completar y validar el encendido magnético, la inicialización al conectar la batería, el reloj, el apagado ordenado y el modo apagado. El CD4013 no tiene garantizado el estado inicial; el firmware aún no existe. Un toque de imán y un corte de alimentación no están demostrados.
2. Diseñar y montar en placa la interfaz del Pololu 2814 con las protecciones frente a transitorios, fijaciones y conexiones de potencia correspondientes. El interruptor físico del módulo debe estar en la posición apropiada para el control externo según su fabricante. No se ha instalado en la placa.
3. Completar detector de fuga y comportamiento seguro, carga y bloqueo de contactos, selección de fusibles y tensión/corriente admisibles. Confirmar polaridad y vista real de los 8 pines y el cargador original antes de conexión: datos comerciales de baterías similares no identifican de forma inequívoca la unidad de Alex.
4. Confirmar huellas reales y corriente admisible de tres DFR1015, A4988 WJMY, Atlas y cable de alimentación USB-C. Los módulos DFR1015 tienen una envolvente aproximada y el fabricante recomienda entrada inferior a 24 V, pese a declarar 7,5–30 V: confirmar tensión real, transitorios, caída y temperatura. Confirmar corriente y cableado del motor para ajustar el A4988: 24 V y 20 W de alimentación no determinan la corriente por fase.
5. Completar modelos 3D y conexiones físicas para los módulos aún ausentes; verificar la orientación de Atlas. El AS7265x tiene su referencia dimensional en el Fusion del proyecto, pero va cableado; no confundir su envolvente con un conector validado.
6. Terminar la colocación y trazado con anchuras, planos, distancias, montaje y serigrafía correctos. Pasar ERC y DRC y revisar el esquema y la placa manualmente. Solo entonces preparar una versión para la comprobación de Alex en Fusion y posteriores ensayos en banco.

Las tres salidas de DFR1015 son una propuesta: 5 V siempre activos, 5 V para Raspberry y 9 V para óptica. No hay medición de consumo en reposo ni de duración de batería para esta electrónica. El sistema permanece parcialmente alimentado aunque esté apagado.
