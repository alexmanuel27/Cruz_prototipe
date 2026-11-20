# Chasis interior de Cruz · R3

Cartucho premontable para el tubo acrílico **Ø172 interior × Ø180 exterior × 380 mm**. Las mitades integran aros Ø167, largueros, guiado del empate y asientos de los módulos. La cubierta sale para limpiar y acceder a la cubeta y a la CSI. La bandeja sale con el PCB y deja acceso vertical a bomba, batería y conexiones. **Cuatro piezas impresas en total.**

## Impresión

| STL | Pieza | Cant. | X × Y × Z | ASA con borde y soportes | Soportes |
| --- | --- | ---: | --- | ---: | ---: |
| [01_DELANTERO.stl](01_DELANTERO.stl) | Mitad delantera | 1 | 167 × 167 × 208 mm | 450,5 g | 45 g |
| [02_TRASERO.stl](02_TRASERO.stl) | Mitad trasera | 1 | 167 × 167 × 208 mm | 441,2 g | 57,5 g |
| [03_BANDEJA.stl](03_BANDEJA.stl) | Bandeja PCB | 1 | 170,2 × 118 × 16,6 mm | 49,1 g | 0,4 g |
| [04_CUBIERTA.stl](04_CUBIERTA.stl) | Cubierta óptica | 1 | 165 × 150 × 66,8 mm | 156 g | 51 g |

Carga un STL por cama, en milímetros, y conserva la orientación incluida. Usa **Original Prusa i3 MK3S & MK3S+**, volumen **250 × 210 × 210 mm**, boquilla **0,4 mm**, **0,20 mm QUALITY @MK3** y **Prusament ASA**. Activa seis perímetros, relleno rectilíneo al 100 %, cama a 105 °C en primera capa y 110 °C después, boquilla a 260 °C y borde exterior de 6 mm. Usa una impresora cerrada para controlar el alabeo de los aros. Consumo laminado total aproximado de **1097 g**.

Activa soportes orgánicos con umbral de 45°, desde cualquier superficie, separación Z de 0,20 mm y dos capas de interfaz. El 02 se lamina con su centro en **X125, Y113 mm** para dejar margen a los soportes. Centra los demás en 125, 105 mm. En 01 y 02 los soportes sostienen cierres transversales, asientos, orejas y primeras capas de las diagonales. Retíralos por la abertura de la carcasa óptica y entre largueros. En 03 sostienen las orejas y los labios de apoyo. En 04 sostienen el techo y el refuerzo de la Pi. Sácalos por la boca inferior antes de fijar la placa.

## Tornillería y montaje

- **Empate.** 4 M4 × 35 de cabeza botón ISO 7380, 8 arandelas Ø9 mm y 4 tuercas M4. Allen de 2,5 mm y llave de 7 mm. Evita que los extremos de los tornillos sobresalgan hacia el tubo.
- **Cubierta y bandeja.** 8 M3 × 16, 16 arandelas Ø7 mm y 8 tuercas M3. Usa un vaso fino de 5,5 mm bajo las orejas.
- **PCB y Pi.** 4 M3 × 25, 4 tuercas M3, 4 arandelas inferiores Ø7 mm y 4 arandelas superiores Ø11–11,5 mm para retener el PCB en el borde. Usa 4 M2,5 × 16 con arandelas y tuercas para la Pi. Presenta las placas reales y comprueba salientes de soldadura y conectores antes de apretar.
- **Módulos.** Prepara 14 bridas de hasta 3 mm. Usa dos por cámara, batería, bomba y módulo Atlas, tres para el conjunto óptico, una para el bloque de temperatura y una por cada cuna de espuma de la sonda EC. Usa apoyo fino de goma bajo la cámara y la bomba, espuma de célula cerrada en las cunas de EC y cinta negra opaca para la junta entre mitades del recinto óptico.

1. Retira los soportes y rebabas de asientos, ranuras, apoyos de arandela, taladros y guía del empate. Comprueba que ambas mitades deslicen entre sí y que cada aro pase por el tubo real sin forzar. Haz este ajuste en seco, con el tubo horizontal.
2. Coloca el módulo Atlas por el aro trasero de 02 antes de los módulos voluminosos. Entra con el módulo unos 36 mm hacia el centro respecto a su posición final, avanza hacia delante y desplázalo hacia la placa lateral. Sujétalo por sus apoyos. Pasa las bridas inferiores antes de instalar la sonda.
3. Coloca el conjunto EC premontado en la mitad 01 desde el lado del empate, con el bloque delantero sobre su cuna. Deja sin conectar la manguera procedente del bloque de temperatura. Desliza 02 axialmente sobre la sonda hasta enganchar la guía. Pon los cuatro M4 desde fuera hacia el centro, con arandela en ambas caras. Asienta la unión sobre una mesa y aprieta alternando lados hasta que las caras asienten, sin marcar el ASA. Fija ambos apoyos de EC.
4. Baja la cámara auxiliar con la lente hacia la tapa frontal. Sujétala a su asiento con dos bridas. Baja el conjunto óptico sobre las cunas y deja la cubeta con ambos puertos verticales. Baja la bomba verticalmente sobre su ventana y fija batería y bloque de temperatura. Conecta la toma, temperatura, EC, cubeta, bomba y descarga en ese orden. Pasa la manguera de cubeta a bomba por el recorte de 03 y evita pellizcos en el empate.
5. Monta la Raspberry en 04 en el banco. Conecta la CSI y presenta la cubierta desde arriba. Cierra con cuatro M3 y cubre la junta del recinto óptico con cinta negra. Monta el PCB en 03 en el banco. Baja la bandeja recta, con el recorte hacia la manguera de cubeta a bomba, y fíjala con los otros cuatro M3. Ajusta el cableado y recorta las puntas de brida.
6. Sostén el cartucho por debajo de ambos largueros, aproximadamente a 100 y 285 mm de la tapa frontal. Introduce el conjunto alineado con el tubo. Conecta tapa y pasamuros al final. Para extraerlo, desconecta los pasamuros y apoya el cartucho en la boca del tubo y con la mano a medida que sale. Sustituye el apoyo de la boca por el segundo apoyo manual una vez fuera.

## Comprobación

- En Fusion v16, la primera pasada encontró choque de mangueras y bandeja, un elemento de la cubierta desconectado y una sección débil bajo la bomba. Se corrigieron los pasos, se integró el refuerzo de la cubierta y se dejó un cordón continuo bajo el motor. En la pasada de montaje se comprobó la interferencia de los cuatro sólidos con las referencias vigentes, las tapas y el tubo Ø172 mm.
- Con las mallas exportadas se repitieron la comprobación de sólidos cerrados, la inserción axial del empate y del conjunto EC, las bajadas de óptica, bomba, batería, cubierta y bandeja cargada, el paso del Atlas por el aro y los accesos con galgas de tornillo, arandela y herramienta. Radio exterior máximo nominal 83,5 mm. Holgura del aro a la pared del tubo 2,5 mm por lado. Las envolventes de módulos comerciales y curvas reales de cables requieren comprobación de banco.
- Cálculo de flexión con secciones de malla cada 1 mm, masa conservadora de 3,17 kg incluyendo módulos y ASA, y capas transversales a X. Se usó un módulo efectivo de 0,9 GPa y límite de trabajo de 4 MPa para la dirección entre capas, frente al valor de 11 ± 1 MPa de la ficha. A 2 g con ambos aros apoyados, el máximo calculado fue 3,77 MPa y 2,11 mm. La carga nominal calculada del empate fue de 99 N por fijación, unos 1,9 MPa de aplastamiento medio en el apoyo plástico de 13 mm con vástago de 4 mm. El modelo asigna el par a las fijaciones y al guiado sin atribuir resistencia a la fricción. A 2 g con dos puntos de apoyo manual, 0,46 MPa y 0,06 mm. Con un solo aro en voladizo se calculó 7,35 mm aun a 1 g, por lo que se requieren dos apoyos durante la extracción. Las cifras son calculadas. Quedan pendientes el encaje y la rigidez del conjunto impreso, el cierre contra luz lateral y el sellado. [Ficha técnica de Prusament ASA](https://prusament.com/wp-content/uploads/2022/10/ASA_Prusament_TDS_2022_16_EN.pdf).
