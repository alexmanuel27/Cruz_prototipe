# Chasis interior de Cruz · R5 para Prusa MINI

Cartucho para el tubo acrílico de **Ø172 mm interior, Ø180 mm exterior y 380 mm de largo**. Las piezas 01 y 02 conservan los centradores, los apoyos de los módulos y sus posiciones. El puente 06 completa el tramo central y guía las dos uniones laterales. La cuna de óptica, la cubierta y la bandeja PCB salen por separado para acceder a los módulos.

## Impresión

| STL | Cant. | X × Y × Z | Soporte | ASA total |
| --- | ---: | --- | ---: | ---: |
| [01_DELANTERO.stl](01_DELANTERO.stl) | 1 | 166 × 167 × 120,5 mm | 2,8 g | 270,6 g |
| [02_TRASERO.stl](02_TRASERO.stl) | 1 | 166 × 167 × 120,5 mm | 4,2 g | 326,9 g |
| [03_BANDEJA.stl](03_BANDEJA.stl) | 1 | 170,2 × 118 × 16,6 mm | 0,1 g | 49,1 g |
| [04_CUBIERTA.stl](04_CUBIERTA.stl) | 1 | 165 × 150 × 37 mm | 6,2 g | 111,7 g |
| [05_CUNA_OPTICA.stl](05_CUNA_OPTICA.stl) | 1 | 165 × 150 × 44 mm | 7,4 g | 155,2 g |
| [06_PUENTE_CENTRAL.stl](06_PUENTE_CENTRAL.stl) | 1 | 104,3 × 119 × 19,5 mm | 1,3 g | 81,7 g |

Carga una pieza por cama y conserva la orientación de cada STL. Usa el perfil **Original Prusa MINI & MINI+**, boquilla de **0,4 mm**, **0,20 mm QUALITY @MINI** y **Prusament ASA @MINI**. Los seis STL se laminaron en una cama de **180 × 180 × 180 mm**, con seis perímetros, 100 % rectilíneo, borde de 4 mm, sin falda, boquilla a 260 °C y cama a 100 °C. Usa recinto para el ASA. El consumo estimado con borde y soportes es de **995 g**.

Centra las piezas en X90/Y90 mm. Usa soportes a 45° desde cualquier superficie, separación Z de 0,20 mm y dos capas de interfaz. Activa **Orgánico** en 01, 02, 03 y 06. Usa **Ajustado (Snug)** en 04 y 05 para que los soportes queden dentro de la cama. Retira los soportes bajo las orejas, los rebajes y los pasos laterales antes de presentar el chasis. [Volumen de impresión y temperaturas de la Prusa MINI+](https://www.prusa3d.com/es/producto/original-prusa-mini-3/).

## Tornillería

| Unión | Cantidad | Material por fijación |
| --- | ---: | --- |
| Mitades al puente 06 | 8 | M4 × 35 de cabeza botón ISO 7380, dos arandelas Ø9 y una tuerca M4 |
| Cuna a 01 | 2 | M4 × 16 de cabeza botón, dos arandelas Ø9 y una tuerca M4 |
| Cuna a 02 | 2 | M4 × 30 de cabeza botón, dos arandelas Ø9 y una tuerca M4 |
| Cubierta y bandeja | 8 | M3 × 16, dos arandelas Ø7 y una tuerca M3 |
| PCB a la bandeja | 4 | M3 × 25, arandela superior Ø11–11,5, arandela inferior Ø7 y tuerca M3 |
| Raspberry Pi a la cubierta | 4 | M2,5 × 16, separador de 5 mm, arandelas y tuerca |

Prepara 14 bridas de hasta 3 mm, dos por cámara, batería, bomba y módulo Atlas, tres para el conjunto óptico, una para temperatura y una para cada apoyo de espuma de EC. Usa goma fina bajo la cámara y la bomba y una junta fina opaca entre cuna y cubierta.

## Montaje

1. Apoya 06 en la mesa con el paso del racor superior de EC hacia la mitad 01. Encaja 01 y 02 sobre las guías de 06 deslizando ambas axialmente. Coloca cuatro M4 × 35 en cada extremo del puente, dos por larguero. Introduce los tornillos desde fuera, pon arandelas en ambas caras y aprieta alternando lados hasta que asienten.
2. Introduce el circuito EC desde abajo con el racor superior desmontado. Sujeta el bloque y la sonda sobre la espuma y coloca el racor superior desde arriba a través de la escotadura de 06. Instala el Atlas por el centrador trasero de 02, unos 36 mm hacia el centro respecto a su posición final. Una vez dentro, desplázalo hacia su apoyo lateral.
3. Baja 05 sobre los largueros y atorníllala antes de montar la óptica. Usa los M4 × 16 delante y los M4 × 30 detrás. Deja las cabezas botón con arandela arriba y las tuercas accesibles desde abajo. Monta la cámara con la lente hacia la tapa frontal, los apoyos ópticos y la cubeta con los puertos verticales. Fija bomba, batería y temperatura. Conecta toma, temperatura, EC, cubeta, bomba y descarga.
4. Fija la Raspberry a 04 en el banco. Conecta la CSI y baja la cubierta. Cierra con cuatro M3. Monta el PCB en 03, baja la bandeja con su recorte hacia la manguera de cubeta a bomba y fíjala con los cuatro M3 restantes. Recoge el cableado y recorta las puntas de brida dentro de la envolvente de los centradores.
5. Prueba el cartucho en el tubo horizontal, con dos apoyos bajo los largueros, aproximadamente en X100 y X285 mm desde el frente. Conecta tapa y pasamuros al final. Para extraerlo, desconecta los pasamuros y usa la boca del tubo como apoyo hasta poder sostenerlo con ambas manos.

## Comprobación

- En Fusion se confirmaron las posiciones de los módulos, el Ø167 exterior nominal de los centradores y el encaje de los seis sólidos con el tubo y las tapas. Se redondearon **48 raíces con radios de 1 a 3 mm** en empates, travesaños, centradores y apoyos. Los planos de apoyo y las guías conservan sus holguras de montaje.
- Se volvieron a verificar las mallas, las trayectorias de montaje y los accesos a tornillos y tuercas. Los recorridos de extrusión, borde y soportes incluidos, quedan dentro de la MINI.
- Cálculo con secciones netas de los STL, masa cargada de **3,15 kg** y módulo efectivo de **1,3 GPa** para el ASA con capas longitudinales en los largueros. A 2 g con ambos centradores apoyados, **5,47 MPa y 1,91 mm**. Con dos apoyos manuales a 2 g, **0,05 mm**. El modelo reparte el par entre los pasantes y no asigna resistencia a la fricción de las caras. Quedan pendientes las pruebas de rigidez, ajuste y luz lateral con piezas impresas. [Ficha técnica del ASA](https://prusament.com/wp-content/uploads/2022/10/ASA_Prusament_TDS_2022_16_EN.pdf).
