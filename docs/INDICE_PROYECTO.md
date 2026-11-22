# Índice del proyecto

## Trabajar en el prototipo

| Área | Archivo de entrada |
| --- | --- |
| Requisitos y decisiones | [Especificación funcional](../ESPECIFICACION.md) · [Registro de decisiones](../DECISIONES.md) |
| Óptica y arquitectura | [Diseño óptico](DISENO_OPTICO.md) · [Análisis de arquitectura](ANALISIS_ARQUITECTURA.md) |
| CAD mecánico | [Guía CAD](../cad/README.md) |
| Corte de tapas e impresión | [Tapa Shaper](../body/TAPA_SHAPER_230_PROTOTIPO.svg) · [Guía de mecanizado](../body/LEEME.md) · [Aro R3](../cad/fusion_m2/ARO_AMARRE_M8_REFORZADO_R3.stl) · [Chasis interior R5 para Prusa MINI](../cad/fusion_m2/chasis_r5/README.md) |
| KiCad | [Proyecto V8](../electronica/cross_v8_raspberry/cross_v8_draft.kicad_pro) · [Estado y pendientes](../electronica/cross_v8_raspberry/LEEME_PRIMERO.md) |
| Adquisición y control | [Monitor local y puesta en marcha](../software/README.md) · [Pruebas de banco e interfaces V8](SOFTWARE_ADQUISICION.md) |
| Compras | [Lista fechada](../compras/LISTA_COMPRA.md) · [Excel para el técnico](../compras/Cruz_Shopping_List_EN_2026-10-30.xlsx) |

El PCB V8 vigente está sin trazado, sin zonas de cobre y sin puentes W; conserva su contorno de 132 × 102 mm y 209 conexiones pendientes. El esquema está reorganizado por bloques. El requisito de pistas en una cara para Bantam sigue pendiente de resolver. El cuerpo usa el tubo acrílico recibido de Ø180/172 × 380 mm. D55 cambia la óptica a un brazo de iluminación común y AS7265x a 90°; la integración en CAD está pendiente de revisar. La simulación R3 está documentada. Los ensayos físicos de estanqueidad y carga siguen pendientes en el registro. El monitor local ya ejecuta ciclos y guarda sus resultados en simulación. El modo ambiental de banco queda por ejecutar en la Pi.

## Validación y datos

- [Registro de ensayos y fotografías](REGISTRO_ENSAYOS.md) · [validación y calibración](VALIDACION_Y_CALIBRACION.md) · [plan de trabajo](PLAN_TRABAJO.md).
- [Estudio reproducible de amarre y lastre](REGISTRO_ENSAYOS.md#archivo-reproducible) · [cálculos, modelos y datos](../cad/fusion_m2/simulacion_amarre_2026-11-20/).

## Referencias de ingeniería

- [Puerto de carga/datos y futura boya](../electronica/PUERTO_SERVICIO_Y_BOYA.md).
- [Pasamuros y revisión de ensuciamiento](ANTIFOULING_Y_PASAMUROS.md).
- [Presupuesto energético del 30 de octubre](PRESUPUESTO_ENERGETICO.md), previo a los cambios de electrónica.
- [Modelos 3D de componentes](../cad/componentes/MODELOS_3D.md).
- [Archivo histórico](../archivo/README.md) con revisiones CAD, vídeo de montaje, dibujos de concepto y listas anteriores.
