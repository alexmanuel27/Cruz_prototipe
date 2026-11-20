# Registro de ensayos y fotografías

**26 de septiembre de 2026. Estado inicial: ningún ensayo físico de Cruz ejecutado en esta tarea. No hay fotografías de montaje ni resultados experimentales nuevos.**

## Ensayos programados

| ID | Fecha prevista | Objeto | Estado | Datos / foto / resultado |
|---|---|---|---|---|
| OPT-01…07 | 7–12 oct | Espectro, emisión, geometría e interferencia | Planificado | Pendientes |
| EST-01 | **30 oct** | Inmersión con lastre, sin electrónica, todas las interfaces | **Planificado; fecha dura** | Pendientes |
| EST-02 | 30 oct–2 nov | Inmersión prolongada de 72 h sin electrónica | Planificado | Pendientes |
| HID-01…05 | Durante integración; cierre antes del 17 nov | Renovación, arrastre, burbujas y fallos de bombeo | Planificado | Pendientes |
| AUT-01…04 | 13–16 nov y pruebas de fallos durante X3 | Autonomía, deriva y recuperación | Planificado | Pendientes |
| BAN-01 | 17–19 nov | Comparación contra espectrofotómetro | Planificado | Pendientes |
| BAN-02 | 17–19 nov | Fluorescencia y clorofila frente a referencias | Planificado | Pendientes |
| CAM-01 | 24 nov | Campo varias horas y pares contemporáneos | Planificado | Pendientes |

Los criterios se encuentran en [Validación y calibración](VALIDACION_Y_CALIBRACION.md). Una fecha prevista no es un resultado aprobado.

## Simulación de amarre y lastre · 20 de noviembre de 2026

Modelo Fusion `Cross_M2_horizontal_design` v13. El grupo `08_ESTUDIO_AMARRE` muestra los dos ramales superiores, los pesos inferiores, los vectores de fuerza y la postura perturbada a 15°. Los topes metálicos son envolventes para verificar espacio. El cálculo hidrostático y el FEM local se realizaron con la geometría exportada de Fusion.

### Masa y lastre

El cálculo usa el tubo real Ø172/180 × 380 mm, tapas Ø230 × 10 mm, cuatro tramos M8 con sus casquillos, y dos aros R3 de PETG macizo equivalente. Los volúmenes del CAD se combinaron con densidades y masas estimadas de piezas comerciales. La masa sin lastre calculada es **7,40 kg** con un rango de escenarios de **6,29–8,71 kg**. El volumen desplazado estanco es **11,64 L**. De los 7,40 kg, 1,98 kg corresponden al acrílico y tóricas, 1,96 kg a herrajes exteriores y topes, 1,14 kg a los aros, 0,91 kg al chasis y 1,42 kg a batería, bomba, óptica, electrónica y cableado. [Densidad de PMMA](https://www.plexiglas.de/en/contact) · [Ficha de PETG](https://prusament.com/wp-content/uploads/2022/10/PETG_Prusament_TDS_2021_10_EN.pdf)

| Montaje | Agua | Acero para flotabilidad neutra | Lastre de prueba | Tensión vertical total en el cabo |
|---|---|---:|---:|---:|
| 4 tramos M8 | Dulce, 1 000 kg/m³ | 4,86 kg | 6,0 kg | 9,7 N |
| 4 tramos M8 | Mar, 1 025 kg/m³ | 5,21 kg | 6,5 kg | 11,0 N |
| 2 tramos M8 opuestos | Dulce, 1 000 kg/m³ | 5,76 kg | 7,0 kg | 10,6 N |
| 2 tramos M8 opuestos | Mar, 1 025 kg/m³ | 6,12 kg | 7,0 kg | 7,5 N |

Con densidades en kg/L, el lastre de acero se calcula como `(densidad_agua × volumen_L − masa_equipo + margen_equivalente_kg) / (1 − densidad_agua / 7,85)`. Con cuatro tramos M8, conviene disponer de hasta 7,5 kg de lastre modular, para ajustar tras el pesaje del equipo. Dos tramos eliminan unos 0,90 kg de herraje y reducen el volumen desplazado unos 0,11 L. Las densidades son escenarios. La del agua de bahía depende de la salinidad y temperatura. [Densidad del agua en NOAA](https://www.nodc.noaa.gov/OC5/woa13/woa-info.html)

En el escenario marino de cuatro tramos y 6,5 kg, el equilibrio horizontal requiere aproximadamente **3,46 kg delante y 3,04 kg detrás**. Un reparto 50/50 produce unos 4,3° de cabeceo en el modelo. Con el reparto corregido, una perturbación de balanceo de 15° produce **1,83 N·m** en sentido recuperador. Se supusieron ramales tensos y cargas verticales equivalentes aplicadas en las orejas. El cálculo es estático y depende de la distribución real de masas.

### Iteraciones del aro

Criterio del estudio estático de prototipo **≤6 MPa de von Mises y ≤1 mm de desplazamiento**. Se aplicaron **250 N a una oreja**, en el plano del aro y a 30° fuera del plano, con cuatro casquillos o dos opuestos como apoyo. Se usó un modelo elástico lineal isotrópico de PETG macizo equivalente, E = 1,2 GPa y ν = 0,36. El caso con topes aplica la componente axial en la franja de contacto de las caras. La geometría se malló con Gmsh y se resolvió localmente mediante elementos tetraédricos lineales. Se comprobaron reacciones y campo de deformación uniforme.

| Iteración | Cambio | Pico más alto | Desplazamiento máximo | Dictamen |
|---|---|---:|---:|---|
| v12, 20 mm | Aro inicial | 19,60 MPa | 2,54 mm | Fuera de criterio |
| R1, 40 mm | Mayor espesor y radio en la oreja | 6,12 MPa | 0,81 mm | Fuera de criterio |
| R2, 46 mm | Resaltes de casquillo reforzados | 6,43 MPa | 0,73 mm | Fuera de criterio |
| R3, 48 mm | Aro más ancho y radios de transición mayores | 4,79 MPa | 0,39 mm | Dentro del criterio |

R3 pasó las mallas de 100 661 y 163 522 tetraedros. El caso de topes con caras planas de despeje, en la malla fina, dio **3,30 MPa y 0,392 mm**. Se comprobó el encaje CAD con el tubo, las tapas, las varillas, los casquillos y los ocho topes de referencia. El [STL R3](../cad/fusion_m2/ARO_AMARRE_M8_REFORZADO_R3.stl) mide **238 × 206 × 48 mm**. Su masa estimada es **0,57 kg por aro** en la hipótesis maciza.

El dictamen permite avanzar a una prueba física del prototipo con lastre. Quedan pendientes el peso real, la resistencia de la impresión y de los topes sobre los casquillos, la estanqueidad y la respuesta a corriente, oleaje, fatiga y fluencia. El cálculo tampoco asigna una carga nominal de izado.

### Relleno y material del primer aro R3

Para la primera prueba de carga se propone imprimir el aro en PETG, plano y con 100 % de relleno. Es el ajuste de laminado más cercano al sólido continuo del FEM. Los perímetros, la orientación y la unión entre capas también afectan a la resistencia real. Para reducir masa, conviene conservar material sólido alrededor de los pasacabos, los casquillos y sus transiciones y repetir la comprobación de carga con el nuevo laminado. [Relleno y perímetros según Prusa](https://help.prusa3d.com/article/infill_42)

Prusament publica una adhesión entre capas de 18 ± 4 MPa para su PETG y 11 ± 1 MPa para su ASA bajo el método del fabricante. El PETG se deforma poco al imprimir piezas grandes. El ASA tiene estabilidad UV y mayor temperatura de deflexión térmica, con más tendencia a deformarse en piezas grandes. Las fichas describen esos filamentos y probetas. La resistencia de los aros impresos, en especial bajo inmersión y carga sostenida, se comprobará con las piezas reales. [Ficha PETG](https://prusament.com/wp-content/uploads/2022/10/PETG_Prusament_TDS_2021_10_EN.pdf) · [Ficha ASA](https://prusament.com/wp-content/uploads/2022/10/ASA_Prusament_TDS_2022_16_EN.pdf) · [Impresión con PETG](https://prusament.com/materials/prusament-petg/) · [Impresión con ASA](https://prusament.com/materials/prusament-asa/)

### Archivo reproducible

El [archivo de la simulación](../cad/fusion_m2/simulacion_amarre_2026-11-20/) incluye el montaje Fusion v13, los STEP exactos de v12/R1/R2/R3, los volúmenes y centros exportados de Fusion v12, las salidas originales JSON y los scripts. El cálculo hidrostático usa ese inventario y sustituye los aros por el volumen de cada revisión. Las salidas hidrostáticas intermedias R1 y R2 se regeneraron con sus volúmenes exportados. El archivo `resultados/campo_r3_250N_30grados.npz` contiene la malla, las fuerzas nodales, las restricciones, los desplazamientos y las tensiones del caso R3 con topes en D. El campo se regeneró desde el STEP archivado y se cotejó con el resumen original. Los índices de tetraedros y de grados de libertad comienzan en cero. Las seis componentes de tensión siguen el orden `xx, yy, zz, xy, yz, xz`.

Desde la carpeta del archivo, con Python 3.14 y las versiones indicadas en `requirements.txt`, se pueden repetir los cálculos. Las salidas de los siguientes comandos se guardan aparte de las originales.

```sh
python -m pip install -r requirements.txt
python hidro.py 448.606663 4 48 hidro_r3_4_repetido.json
python hidro.py 448.606663 2 48 hidro_r3_2_repetido.json
python fea.py geometria/aro_v12.step 4.2 20 fea_v12_repetido.json
python fea.py geometria/aro_r1.step 4.2 40 fea_r1_repetido.json
python fea.py geometria/aro_r2.step 3.1 46 fea_r2_repetido.json topes
python fea.py geometria/aro_r3.step 4.2 48 fea_r3_gruesa_repetido.json topes
python fea.py geometria/aro_r3.step 3.1 48 fea_r3_fina_repetido.json topes
python fea.py geometria/aro_r3.step 3.1 48 fea_r3_topes_d_repetido.json topes_d campo_r3_repetido.npz
shasum -a 256 -c SHA256SUMS
```

Para el futuro artículo, identificar estas cifras y figuras como resultados de simulación. Añadir al acta de carga las mediciones de la pieza impresa, lote de filamento, archivo de laminado, orientación, masa y condiciones de inmersión y carga.

## Plantilla del acta de cada ensayo

Copiar esta estructura en `docs/ensayos/AAAA-MM-DD_ID.md` al ejecutar el trabajo:

- **ID, fecha y operador:**
- **Objetivo y requisito comprobado:**
- **Estado:** iniciado / completado / interrumpido.
- **Versiones:** CAD, electrónica, software, calibración y configuración real.
- **Instrumentos y patrones:** referencia, número de serie, lote, calibración, unidades.
- **Muestras:** ID, preparación, conservación, edad y volumen.
- **Condiciones:** temperatura, profundidad/presión, alimentación y ajustes.
- **Criterio de aceptación fijado antes del ensayo:**
- **Procedimiento realmente seguido y desviaciones:**
- **Datos originales y archivos de configuración:** enlaces relativos.
- **Fotografías:** antes, durante y después; cada una con pie, fecha y componente visible.
- **Resultados:** valores, dispersión, incertidumbre pertinente y observaciones.
- **Dictamen:** APROBADO / FALLIDO / INCONCLUSO, con razón.
- **Acciones:** reparación, repetición requerida y vínculo a la decisión.
- **Revisión:** responsable y fecha.

## Fotografías que deben tomarse mientras aún son posibles

| Etapa | Fotografías mínimas |
|---|---|
| Inventario | Etiquetas de cámara, lente, LED/lámpara, placa AS7265x y filtro; regla junto a rendija |
| Fabricación | Pieza y versión, acabado de ranuras, medidas críticas y defectos |
| Sellado | Junta en su ranura antes de cerrar; ventana, cada pasamuros y racor; vista de conjunto |
| EST-01 | Interior seco y lastre; testigos identificados; profundidad/montaje; apertura e inspección final |
| Electrónica | Conexiones de potencia, fusible/protecciones, polaridad, rutas de cables y fijación antes de ocultarlas |
| Óptica | Muestra central, fuentes, detectores, filtro, baffles y ajustes de alineación |
| Hidráulica | Toma, orientación de celda, bomba y descarga; posición de burbujas/fugas si aparecen |
| Campo | Lugar, fijación, profundidad, toma/descarga y estado al recuperar |

Guardar originales en `docs/fotos/AAAA-MM-DD/` con nombres como `EST-01_junta_tapa_antes_01.jpg`. Conservar metadatos y relacionarlos con el acta. Un render CAD o una imagen ilustrativa no sustituye una fotografía de montaje. Los fallos también se fotografían.

## Verificación CAD del chasis interior R1 · 20 de noviembre de 2026

Se revisaron las dos mitades del chasis para el tubo Ø172/180 × 380 mm. Se retiraron los bloques sueltos de la unión, se añadió acceso a dos tornillos M4 y se ajustaron los pasos de manguera. Ambas mitades pasan la comprobación de encaje CAD y la verificación de mallas STL cerradas. Las dos se laminaron por separado en PrusaSlicer 2.9.7 con soportes orgánicos y un perfil genérico de PETG, con una estimación conjunta de 972 g de filamento. La masa, el encaje y la secuencia de montaje se verificarán con las piezas impresas. [Archivos históricos de R1 en Git](https://github.com/alexmanuel27/Cruz_prototipe/tree/6ccc63f/cad/fusion_m2/chasis_interior).

## Chasis modular R2 · 20 de noviembre de 2026

Se sustituyeron las dos mitades altas por dos bases planas, dos aros iguales, dos pletinas de empate y placas separadas para los módulos. Se guardó la v16 de Fusion. Pasaron la comprobación de interferencias de las piezas nuevas y la verificación de los ejes de los pasantes. Los 11 STL se laminaron por separado en MK3S+ con perfil Prusament ASA y soportes desactivados. La masa estimada de las 17 piezas, con borde de adhesión, es 238 g. Quedan pendientes el montaje real, la comprobación de luz lateral y el pesaje del conjunto. [Archivos históricos de R2 en Git](https://github.com/alexmanuel27/Cruz_prototipe/tree/6ccc63f/cad/fusion_m2/chasis_modular).


## Verificación del chasis interior R3 · 20 de noviembre de 2026

- **Primera pasada en Fusion v16.** El solape horizontal reducía la altura resistente de los largueros. Se cambió a un empate lateral con guía longitudinal y cuatro M4 pasantes. El primer cálculo con empate lateral detectó 8,32 MPa a 2 g en la ventana de la bomba. También aparecieron interferencias de mangueras y bandeja y dos volúmenes en la cubierta. Se añadió un cordón continuo bajo el motor, se dieron pasos a las mangueras, se cambiaron las orejas delanteras de la bandeja y se unió el refuerzo de la cubierta.
- **Segunda pasada en Fusion.** Se compararon los cuatro sólidos definitivos con los cuerpos vigentes de cámara, óptica, electrónica e hidráulica, entre sí, con las tapas y con el tubo real de Ø172 mm interior. Se repitió la prueba con las cuatro piezas en su posición de montaje. Resultados sin interferencias positivas por encima de 0,01 mm³.
- **Revisión de los STL.** Se verificaron mallas cerradas, una pieza conectada por archivo y trayectorias de inserción, retirada y acceso. El Atlas entra vía el aro trasero y se desplaza hacia la placa lateral. El EC entra antes del empate. Se reubicó la retención delantera izquierda del PCB y se abrió una escotadura para retirar la bandeja con la manguera montada. Los cuatro archivos definitivos se laminaron por separado en PrusaSlicer 2.9.6 con MK3S+, Prusament ASA y boquilla de 0,4 mm. Se desplazó 8 mm hacia el fondo la mitad trasera para mantener incluso sus soportes dentro de la cama. [Piezas, parámetros y montaje](../cad/fusion_m2/chasis_r3/README.md).
- **Cálculo.** Flexión a partir de las secciones netas de los STL cada 1 mm y de las masas máximas de módulos del estudio de amarre, con 3,17 kg totales. Módulo efectivo 0,9 GPa y límite de trabajo 4 MPa entre capas, con capas normales al eje del tubo. Con ambos aros apoyados a 2 g en el giro crítico, 3,77 MPa y 2,11 mm. En extracción con apoyo doble, 0,46 MPa y 0,06 mm a 2 g. Se estimaron unos 100 N por fijación para transmitir el par en el empate. El caso de voladizo sobre un único aro dio 6,46 MPa y 7,35 mm a 1 g. Se requiere manipular con dos apoyos. Quedan pendientes las pruebas físicas de ajuste, carga y cierre óptico. [Ficha técnica de ASA](https://prusament.com/wp-content/uploads/2022/10/ASA_Prusament_TDS_2022_16_EN.pdf).
