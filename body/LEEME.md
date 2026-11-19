# Tapa común para Shaper Origin

[TAPA_SHAPER_230_PROTOTIPO.svg](TAPA_SHAPER_230_PROTOTIPO.svg) contiene una sola tapa a escala 1:1 en milímetros. Coloca el mismo diseño dos veces sobre la placa de acrílico de 800 × 400 × 10 mm, con espacio para la fresa, la fijación y la cinta de seguimiento. El lado que se fresa para la junta es la cara interior.

| Geometría | Modo en Shaper | Cota |
| --- | --- | --- |
| Ranura anular | Pocket (gris) | Ø170,8 interior y Ø181,2 exterior. Ancho 5,2 mm. Profundidad de prueba 3,2 mm. |
| Cuatro agujeros de varillas M8 | Inside (blanco con borde negro) | Ø9 mm pasante. Círculo de centros Ø202 mm, con los agujeros a 45° respecto a los ejes. |
| Perfil de la tapa | Outside (negro) | Ø230 mm pasante. |

Al cargar el SVG, comprueba el Ø230 mm y que el modo Pocket seleccione solo la franja anular. La profundidad de cada operación se introduce en la Shaper. Para los pasantes, mide el espesor real de la placa y usa una base de sacrificio. En cada tapa, realiza primero las operaciones interiores y recorta el perímetro al final. Una fresa para acrílico de Ø3 mm deja margen para vaciar la ranura de 5,2 mm. [Tipos de corte](https://support.shapertools.com/hc/en-us/articles/115002721473-cut-type-encoding) · [Fresado de bolsillos](https://support.shapertools.com/hc/en-us/articles/360005473253-pocketing-procedure)

## Ranura de prueba

La tórica es de Ø172 mm interior con cordón de 4 mm. Su diámetro medio de Ø176 mm coincide con el centro de la ranura. La profundidad nominal de 3,2 mm daría un 20 % de compresión si el extremo del tubo quedara al ras con la cara interior de la tapa.

El tubo mide Ø172/180 mm y tiene 4 mm de pared radial, frente a los 5,2 mm de la ranura. El borde del tubo puede entrar en el bolsillo. Antes de fresar las dos tapas, prueba un tramo de la ranura en un retal y comprueba el centrado y el apoyo. El montaje necesita topes que limiten el cierre a la compresión prevista. Valida el conjunto con el ensayo de estanqueidad con lastre y sin electrónica. [Guía de juntas estáticas Parker](https://www.parker.com/content/dam/Parker-com/Literature/Praedifa/Catalogs/Catalog_O-Ring-Handbook_PTD5705-EN.pdf)

Los pasamuros de la tapa trasera se taladran aparte con las piezas reales. Si se usa el EN3P8MX, comprueba el espesor admisible de panel antes de perforar. La ficha indica un máximo de 0,188 pulgadas (4,78 mm), por lo que con la placa de 10 mm hay que resolver su alojamiento. [Catálogo Switchcraft](https://www.switchcraft.com/assets/1/6/hec_2013_catalog_hires_b.pdf)
