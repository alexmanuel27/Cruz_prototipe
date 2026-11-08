# AS7265x — referencia mecánica de Fusion

**2 de noviembre de 2026.** Alex indica usar las dimensiones del sensor que ya está en Fusion para el diseño. Se consultó en modo de solo lectura el documento activo `Cross_M2_horizontal_design`, que tenía cambios sin guardar.

## Envolvente y ubicación

- Componente del montaje: `M2_GENERATED / 04_OPTICS_REFERENCES / O02 AS7265x 18-channel detector APPROX`.
- Cuerpo local: **45 × 36 × 4,5 mm**, medidas del modelo; es la envolvente de referencia aceptada por Alex para esta fase.
- En el montaje, su caja envolvente está orientada aproximadamente **45 × 4,5 × 36 mm** respecto a los ejes X, Y y Z. La pequeña diferencia (0,02 mm) en las medidas de caja de Fusion es tolerancia geométrica, no espesor adicional.
- Caja del montaje: X 103,99–149,01 mm; Y 54,49–59,01 mm; Z −19,93–16,09 mm. La cubeta de referencia ocupa X 120,24–132,76 mm; Y −6,26–6,26 mm; Z −20,01–20,01 mm. El eje transversal de la cubeta y el centro X del sensor coinciden aproximadamente; la separación entre las cajas en Y es aproximadamente 48,23 mm. Es una lectura de implantación, no una distancia óptica validada.
- Fuente azul de referencia: al lado opuesto de la cubeta, en Y negativa. El centro de su envolvente coincide aproximadamente con el centro X de la celda.

## Uso en el diseño

Reservar esta envolvente en el soporte óptico y conservar una trayectoria despejada hacia la cara lateral de la cubeta. Prever la conexión con el PCB principal sin impedir el montaje y mantenimiento. Alex confirmó que el módulo se conecta mediante cuatro cables: alimentación, masa, SDA y SCL. El conector J8 del esquema corresponde a estas cuatro señales: pin 1 = 3V3_PI, pin 2 = GND, pin 3 = SDA y pin 4 = SCL. Este es el orden propuesto en el PCB, no el orden demostrado en el módulo; cada cable debe identificarse por su función. Alex confirmó que el módulo acepta alimentación y niveles I²C de 3,3 V. Comprobar las resistencias pull-up y la conexión efectiva durante la puesta en marcha. El componente modelado no define la posición de los tres detectores, el conector físico, los agujeros ni la longitud de cable. Comprobar orientación, soportes y componentes sobresalientes al integrar.

Las posiciones anteriores proceden del **documento activo**, no de una nueva exportación ni de una versión guardada. La implantación, ausencia de colisiones, alineación óptica y señal de fluorescencia necesitan comprobación; no se ha modificado ni guardado Fusion en esta consulta. El PCB sigue incompleto y sin trazado.
