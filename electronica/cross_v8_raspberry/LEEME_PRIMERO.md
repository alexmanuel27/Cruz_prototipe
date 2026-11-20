# PCB V8 · estado de trabajo

La V8 es el proyecto editable. El esquema está agrupado en nueve bloques funcionales. Abre el archivo de proyecto para cargar sus huellas y modelos STEP locales. **El PCB requiere completar el diseño y la revisión eléctrica antes de fabricarlo o energizarlo.**

## Archivos del proyecto

- [Proyecto KiCad](cross_v8_draft.kicad_pro).
- [Esquema](cross_v8_draft.kicad_sch) y [placa sin rutear](cross_v8_draft.kicad_pcb), con un contorno de 170 × 68 mm. Las dimensiones de huellas y módulos siguen pendientes de validar.
- [Huellas locales](Cross.pretty/) y [modelos 3D](modelos_3d/). El modelo oficial `Pololu_2814_fabricante.step` sirve de referencia para la huella y conexiones que faltan. [Recursos del fabricante](https://www.pololu.com/product/2814/resources).
- [Informes, scripts y copias históricas](../../archivo/electronica/cross_v8_raspberry/). Los resultados de trazado experimental corresponden a otra revisión.

## Comprobación en KiCad 9.0.7 · 20 de noviembre de 2026

| Comprobación | Resultado |
| --- | --- |
| ERC | 77 avisos de discrepancia con biblioteca y 3 errores por entradas de alimentación de U2 y U7 sin fuente reconocida. |
| DRC | 199 conexiones por rutear y 57 avisos de serigrafía. |
| Paridad esquema–PCB | 0 diferencias. |

Para la revisión conjunta de alimentación y control, U7 pertenece a la alimentación permanente aunque figura dentro de Motor. La alimentación dedicada de 3,3 V para AS7265x, DS18B20 y Atlas es el ítem 23 acordado y está pendiente de implementar. En este borrador, J8, J9 y J10 siguen unidos a `3V3_PI`.

## Pendiente para terminar

1. Completar y validar el encendido magnético, la inicialización al conectar la batería, el reloj, el apagado ordenado y el modo apagado. El CD4013 no tiene garantizado el estado inicial; el firmware aún no existe. Un toque de imán y un corte de alimentación no están demostrados.
2. Diseñar y montar en placa la interfaz del Pololu 2814 con las protecciones frente a transitorios, fijaciones y conexiones de potencia correspondientes. El interruptor físico del módulo debe estar en la posición apropiada para el control externo según su fabricante. No se ha instalado en la placa.
3. Completar detector de fuga y comportamiento seguro, carga y bloqueo de contactos, selección de fusibles y tensión/corriente admisibles. Confirmar polaridad y vista real de los 8 pines y el cargador original antes de conexión: datos comerciales de baterías similares no identifican de forma inequívoca la unidad de Alex.
4. Confirmar huellas reales y corriente admisible de tres DFR1015, A4988 WJMY, Atlas y cable de alimentación USB-C. Los módulos DFR1015 tienen una envolvente aproximada y el fabricante recomienda entrada inferior a 24 V, pese a declarar 7,5–30 V: confirmar tensión real, transitorios, caída y temperatura. Confirmar corriente y cableado del motor para ajustar el A4988: 24 V y 20 W de alimentación no determinan la corriente por fase.
5. Completar modelos 3D y conexiones físicas para los módulos aún ausentes; verificar la orientación de Atlas. El AS7265x tiene su referencia dimensional en el Fusion del proyecto, pero va cableado; no confundir su envolvente con un conector validado.
6. Terminar la colocación y trazado con anchuras, planos, distancias, montaje y serigrafía correctos. Pasar ERC y DRC y revisar el esquema y la placa manualmente. Solo entonces preparar una versión para la comprobación de Alex en Fusion y posteriores ensayos en banco.

Las tres salidas de DFR1015 son una propuesta: 5 V siempre activos, 5 V para Raspberry y 9 V para óptica. No hay medición de consumo en reposo ni de duración de batería para esta electrónica. El sistema permanece parcialmente alimentado aunque esté apagado.
