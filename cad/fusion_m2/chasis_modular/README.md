# Chasis interior modular R2

El chasis se monta como un cartucho de **Ø167 × 374 mm** para el tubo de **Ø172 mm interior**. El bastidor son seis piezas. Las placas y puentes se atornillan al bastidor por separado. En Fusion v16 está en `03_CHASIS_Y_SOPORTES → 01_CHASIS_R2_MODULAR`.

[Montaje Fusion editable](CROSS_CHASIS_R2_MODULAR.f3d) · [Vista del bastidor](CHASIS_R2.png) · [Vista con los módulos](CHASIS_R2_MONTADO.png)

## Qué imprimir

| Grupo | Pieza | Cantidad | Huella × altura de impresión |
| --- | --- | ---: | --- |
| Bastidor | [01 Base delantera](01_BASE_DELANTERA.stl) · [STEP](01_BASE_DELANTERA.step) | 1 | 182 × 126 × 7 mm |
| Bastidor | [02 Base trasera](02_BASE_TRASERA.stl) · [STEP](02_BASE_TRASERA.step) | 1 | 174 × 128 × 7 mm |
| Bastidor | [03 Aro centrador](03_ARO.stl) · [STEP](03_ARO.step) | 2 | 167 × 167 × 17 mm |
| Bastidor | [04 Pletina de empate](04_EMPATE.stl) · [STEP](04_EMPATE.step) | 2 | 30,8 × 12 × 5 mm |
| Placas | [05 Placa de cámara](05_CAMARA.stl) · [STEP](05_CAMARA.step) | 1 | 61 × 119 × 4,5 mm |
| Placas | [06 Separador de cámara](06_SEPARADOR_CAMARA.stl) · [STEP](06_SEPARADOR_CAMARA.step) | 4 | 8,2 × 8,2 × 18 mm |
| Placas | [07 Placa óptica](07_OPTICA.stl) · [STEP](07_OPTICA.step) | 1 | 144 × 123 × 3,5 mm |
| Placas | [08 Placa de batería, bomba y temperatura](08_SERVICIOS.stl) · [STEP](08_SERVICIOS.step) | 1 | 92 × 120 × 4 mm |
| Electrónica | [09 Puente delantero](09_PUENTE_DELANTERO.stl) · [STEP](09_PUENTE_DELANTERO.step) | 1 | 151,6 × 83 × 8 mm |
| Electrónica | [10 Puente trasero](10_PUENTE_TRASERO.stl) · [STEP](10_PUENTE_TRASERO.step) | 1 | 142 × 83 × 8 mm |
| Electrónica | [11 Escuadra Atlas](11_ESCUADRA_ATLAS.stl) · [STEP](11_ESCUADRA_ATLAS.step) | 2 | 9,8 × 28 × 7,6 mm |

Los STL ya están orientados en milímetros con su cara de impresión en Z=0. Coloca cada base y cada aro en su propia cama. Puedes agrupar las piezas pequeñas con la función de organizar del laminador. Los apoyos ópticos, la cubierta superior y la bandeja PCB con sus clips están en sus respectivos grupos del montaje Fusion.

## Orden de montaje

1. **Bastidor.** Empata 01 y 02 con las dos pletinas 04 por debajo. Usa cuatro M4 × 18 con tuercas y arandelas. Monta un aro 03 en cada extremo con las pestañas hacia dentro y abajo. Gira el segundo aro 180° en planta. Usa dos M4 × 20 por aro. Prueba que el bastidor entre y salga del tubo en seco.
2. **Placas.** Monta 05 sobre los cuatro separadores 06 con M3 × 35. Fija 07 y 08 a las bases con M3 × 16. Las cuatro ventanas redondas de 07 dejan acceso a los tornillos de las pletinas. Sujeta la cámara y la batería con dos bridas por módulo. Centra la bomba en su abertura y abrázala por el cuerpo, con apoyo blando. Pasa las bridas de la sonda y del bloque de temperatura por las ranuras y deja libres los puertos de manguera.
3. **Electrónica.** Instala la óptica, pasa la cinta CSI y cierra la cubierta antes de atornillar el puente delantero 09. El 10 va detrás y sus dos ventanas dejan pasar las mangueras. Usa M3 × 20 en los pies de ambos puentes y de las escuadras 11. Une la placa lateral Atlas a las escuadras con M3 × 12 y sujeta el módulo con sus bridas. Instala la bandeja y los clips del PCB sobre los puentes.
4. **Cierre.** Comprueba que cables, puntas de tornillo y bridas queden dentro del perfil de los aros. Ajusta los apoyos blandos con las tapas cerradas. En la óptica, usa una placa opaca y comprueba en banco el cierre contra luz lateral al montar la cubierta.

Usa tuercas y arandelas en los pasantes. Las ranuras pequeñas admiten bridas de hasta 3 mm. Confirma el largo de los tornillos de la bandeja con sus clips y el PCB reales.

## Verificación

Las 11 mallas son sólidas y cerradas. Cada una se laminó por separado en **PrusaSlicer 2.9.6**, con el perfil **Original Prusa i3 MK3S & MK3S+**, boquilla 0,4 mm, **Prusament ASA**, capa **0,15 mm SPEED**, cuatro perímetros, 15 % de relleno, borde de 5 mm y soportes desactivados. El juego de 17 piezas tiene un consumo estimado de **238 g**, incluido el borde. La prueba en seco sigue pendiente con el tubo y los módulos físicos. Comprueba las curvas de la CSI y el ajuste de los componentes comerciales antes de cerrar. [Medidas, encaje y laminado](VERIFICACION_R2.json).
