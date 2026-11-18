# Tapas del cuerpo — corte inicial

Dos archivos SVG a escala 1:1 en milímetros: `tapa_delantera.svg` y `tapa_trasera.svg`. Cada uno contiene solo el contorno Ø230 mm y cuatro agujeros pasantes Ø9 mm para varillas M8, en círculo de centros Ø202 mm y a 45° respecto a los ejes. Son geometrías nominales: aplicar compensación de herramienta en CAM, no escalar.

`LASER_DOS_TAPAS_800x400.svg` reúne las dos tapas en la placa nominal: margen mínimo 10 mm y separación entre contornos 10 mm. Verificar área útil, sujeción y compensación de corte según la máquina.

## Fabricación prevista

1. **Láser:** cortar el contorno y los cuatro agujeros pasantes de cada tapa. Confirmar que la máquina admite PMMA de 10 mm y hacer una prueba para ajustar el corte y la holgura de los agujeros.
2. **CNC:** el archivo `CNC_RANURA_ESTUDIO_NO_MECANIZAR.svg` contiene los límites de un bolsillo anular de estudio para ambas tapas, en su cara interior. Profundidad propuesta 3,2 mm (no está codificada en el SVG). Usar un útil de referencia para centrar la tapa respecto a los cuatro agujeros. **No mecanizar el bolsillo hasta resolver y verificar los topes y el apoyo de la junta.**
3. **Después:** Alex hará con el taladro los dos agujeros de manguera y el del conector de carga/datos, usando las piezas reales; no están incluidos en los SVG. Ensayar el cierre sin electrónica.

Material recibido: placa acrílica 800 × 400 × 10 mm; tubo Ø exterior 180 mm, Ø interior 172 mm, largo 380 mm. Las dos tapas caben en la placa; prever separación para la herramienta, sujeción y márgenes.

**Pendiente antes del montaje estanco:** diseñar la ranura de la junta tórica Ø interior 172 mm y cordón 4 mm, y los topes de compresión. La ranura anterior correspondía a una junta plana y no se debe utilizar. El tubo tiene solo 4 mm de pared radial; el apoyo del extremo, tolerancias y compresión de la junta deben verificarse juntos. No hay profundidad de ranura aprobada en estos SVG.

**Tapa trasera:** los taladros para mangueras, conector y sensores no están incluidos porque faltan las cotas definitivas de los pasamuros. No utilizar las reservas antiguas como medidas de fabricación.

Confirmar las medidas con calibre, planitud y espesor reales; verificar sujeción y trayectoria en la máquina antes de cortar. Hacer ensayo de estanqueidad con lastre y sin electrónica antes de usar el equipo sumergido.

## Estudio de la ranura — no liberado para mecanizado

Junta nominal: diámetro interior 172 mm, cordón 4 mm; diámetro medio 176 mm, centrado sobre la pared nominal del tubo (172–180 mm). Los dos círculos del SVG de estudio representan los límites del bolsillo: Ø170,8 y Ø181,2 mm, ancho radial 5,2 mm. Una profundidad de 3,2 mm produciría teóricamente un 20 % de compresión si el extremo del tubo llegara al plano de la tapa. Es una hipótesis de diseño, no una medida liberada.

El bolsillo es más ancho que la pared del tubo de 4 mm, por lo que el extremo del tubo no tendrá apoyo plano continuo a ambos lados. Se necesitan topes mecánicos que controlen la posición de la tapa y un análisis del confinamiento de la tórica ante la presión exterior. No basta con apretar las tuercas hasta que parezcan firmes. Verificar tolerancias reales del tubo y la junta, dureza/material, mecanizado y ensayo de estanqueidad antes de aceptar la geometría. Los archivos de corte láser siguen siendo solo para el contorno y los cuatro agujeros M8.

El conector previsto EN3P8MX requiere revisar su alojamiento: Switchcraft especifica espesor máximo de panel de 0,188 pulgadas (aprox. 4,78 mm). La tapa es de 10 mm y precisaría un rebaje local u otra solución; comprobar el modelo realmente disponible antes de taladrar. Fuente: https://www.switchcraft.com/assets/1/6/hec_2013_catalog_hires_b.pdf
