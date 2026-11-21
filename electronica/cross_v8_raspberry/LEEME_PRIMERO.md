# PCB V8 · estado de trabajo

La V8 es el proyecto editable. Conserva los bloques anteriores y añade los de potencia óptica y rama de sensores. Abre el archivo de proyecto para cargar sus bibliotecas locales. **El PCB requiere completar el diseño y la revisión eléctrica antes de fabricarlo o energizarlo.**

**Revisión vigente del 21 de noviembre:** [adaptación a los ensayos de banco y tabla de señales](REVISION_BANCO_2026-11-21.md). Pi 5, halógena 12 V/10 W y tres LED activos altos; rama propia de 3,3 V y EC-OEM de diez pads. Esta revisión sustituye la óptica Optisolis/PLD333 y el zócalo Atlas Gen 2 anteriores.

## Archivos del proyecto

- [Proyecto KiCad](cross_v8_draft.kicad_pro).
- [Esquema](cross_v8_draft.kicad_sch) y [placa sin rutear](cross_v8_draft.kicad_pcb), con un contorno de 170 × 68 mm. Las dimensiones de huellas y módulos siguen pendientes de validar.
- [Huellas locales](Cross.pretty/) y [modelos 3D](modelos_3d/). El modelo oficial `Pololu_2814_fabricante.step` sirve de referencia para la huella y conexiones que faltan. [Recursos del fabricante](https://www.pololu.com/product/2814/resources).
- [Informes, scripts y copias históricas](../../archivo/electronica/cross_v8_raspberry/). Los resultados de trazado experimental corresponden a otra revisión.

## Comprobación en KiCad 9.0.7 · 21 de noviembre de 2026

| Comprobación | Resultado |
| --- | --- |
| ERC | 0 errores y 29 avisos de discrepancia con biblioteca. No se han silenciado reglas. |
| DRC | 283 conexiones por rutear y 50 avisos de serigrafía. |
| Paridad esquema–PCB | 0 diferencias. |
| Colocación | 113 huellas; 43 nuevas o sustituidas fuera del contorno, pendientes de colocar. Las otras 70 conservan posición y orientación. |

U7 sigue en Motor y pertenece a alimentación permanente. El ítem 23 es ahora U10 AP2112K-3.3, propuesta de regulador para `3V3_SENS` con carga y térmica por comprobar. J8/J10/R10 pasan a esa rama; U11 desconecta SDA/SCL/1-Wire con Pi sin 3,3 V. J9 se sustituye por U12 EC-OEM con huella local. U13 es solo un bloque de requisito de aislamiento de alimentación e I²C, excluido de BOM/PCB: **todavía no hay aislamiento físico seleccionado ni integrado**.

La [revisión de 01 y 02 del 20 de noviembre](REVISION_01_02.md) conserva la numeración histórica de 23 ítems. Alex transcribe batería 24 V/3 Ah, entrada 25,2 V, salida 22–25 V (5–8 A), cargador 25,2 V/2 A y motor 20 W. Máximo medido y corriente por fase siguen pendientes. `HOLD_PI` alto solicita corte y una señal SET mantenida puede impedir apagar. `OPT_ARM` BCM21/pin 40 habilita la óptica; las cuatro órdenes son ahora activas altas.

## Pendiente para terminar

1. Completar y validar el encendido magnético, la inicialización al conectar la batería, el reloj, el apagado ordenado y el modo apagado. El CD4013 no tiene garantizado el estado inicial; el control autónomo unificado no está probado. Un toque de imán y un corte de alimentación no están demostrados en el conjunto.
2. Diseñar y montar en placa la interfaz del Pololu 2814 con las protecciones frente a transitorios, fijaciones y conexiones de potencia correspondientes. El interruptor físico del módulo debe estar en la posición apropiada para el control externo según su fabricante. No se ha instalado en la placa.
3. Completar detector de fuga y comportamiento seguro, carga y bloqueo de contactos, selección de fusibles y tensión/corriente admisibles. Confirmar polaridad y vista real de los 8 pines y el cargador original antes de conexión: datos comerciales de baterías similares no identifican de forma inequívoca la unidad de Alex.
4. Confirmar capacidad, huellas y corriente admisible de tres DFR1015, A4988 WJMY, lámpara y cable USB-C para Pi 5. Los DFR1015 tienen envolvente aproximada y recomiendan entrada inferior a 24 V, pese a declarar 7,5–30 V. Medir máximo y transitorios de batería, arranque en frío de halógena y térmica antes de cerrar valores. R050 y dos bobinas de 2,9 Ω no determinan la corriente nominal por fase del motor.
5. Elegir e integrar físicamente aislamiento EC de alimentación y SDA/SCL, sin unir GND_EC_ISO con GND ni conectar PRBG a masa. Confirmar orientación del OEM, coaxial y el IDC40 de J1 para la cinta propuesta de 20 cm; reservar CAM/DISP 1 y USB interior para las cámaras. Comprobar apagado durante rampas y reset, consumo de sensores y térmica del regulador y drivers. Completar modelos locales y conexiones de módulos ausentes.
6. Terminar la colocación y trazado con anchuras, planos, distancias, montaje y serigrafía correctos. Pasar ERC y DRC y revisar el esquema y la placa manualmente. Solo entonces preparar una versión para la comprobación de Alex en Fusion y posteriores ensayos en banco.

Las tres salidas de DFR1015 son una propuesta: 5 V permanentes, 5 V para Pi 5 y 12 V para óptica. No hay medición de consumo en reposo ni de autonomía integrada. El sistema permanece parcialmente alimentado aunque esté apagado. ERC sin errores y paridad correcta no validan el aislador pendiente, la colocación, el dimensionado o la fabricación.

**Disponibilidad aclarada por Alex el 21 de noviembre:** solo dispone de un DC/DC para batería de 24 V → 12 V. U4/U5/U6 son funciones propuestas; no representan tres módulos disponibles. Falta seleccionar la alimentación de 5,1 V para Pi 5. Puede obtenerse con otro buck desde batería o desde 12 V; esta última opción suma la carga de Pi a la del convertidor de 12 V. La topología y el suministro permanente siguen por cerrar. No alimentar la Pi directamente a 12 V.
