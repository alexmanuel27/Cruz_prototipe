# Chasis interior R1

> Revisión histórica. La versión actual para fabricar es el [chasis modular R2](../chasis_modular/README.md).

Chasis extraíble de **374 mm de largo y Ø167 mm máximo** para el tubo acrílico de **Ø172 mm interior × 380 mm**. La holgura radial nominal es de **2,5 mm**. Los dos extremos llevan bisel de entrada y alojamientos poco profundos para apoyos blandos opcionales. El espesor de estos apoyos se ajusta al medir el juego con ambas tapas cerradas.

Guardado como **v14** de `Cross_M2_horizontal_design`. En Fusion, el chasis está en `M2_GENERATED → 03_CHASIS_Y_SOPORTES → 01_CHASIS_BASE_DESMONTABLE`. El montaje completo incluye el soporte óptico, la cubierta, la bandeja y las referencias de los módulos.

| Pieza | Archivo de impresión | Sólido CAD | Dimensiones sobre la cama |
| --- | --- | --- | --- |
| Mitad delantera | [STL](01_DELANTERO.stl) | [STEP](01_DELANTERO.step) | 167 × 167 × 196 mm |
| Mitad trasera | [STL](02_TRASERO.stl) | [STEP](02_TRASERO.step) | 167 × 167 × 183 mm |

[Montaje Fusion editable](CROSS_CHASIS_R1.f3d) · [Vista del chasis](CHASIS_R1.png) · [Vista con módulos](CHASIS_R1_MONTADO.png) · [Verificación geométrica](VERIFICACION_CAD.json).

## Montaje

1. Inserta dos tuercas M4 en los alojamientos abiertos hacia arriba de la mitad delantera. Enfrenta ambas mitades fuera del tubo, desliza las dos lengüetas en sus alojamientos y une con dos tornillos Allen M4 × 16 y arandelas M4 de Ø9 mm. Las cabezas se alcanzan desde el lado trasero de la unión.
2. Monta la cámara frontal en su cuna y los apoyos ópticos sobre el chasis. Coloca las sondas, la cubeta y la bomba antes de cerrar con la cubierta. Sujeta la cubeta sobre sus apoyos blandos y deja las mangueras sin tensión.
3. Pasa la cinta CSI por la cubierta y monta la Raspberry Pi junto a la PiCam. Instala el travesaño desmontable, la batería y la bandeja superior con sus clips. La interfaz Atlas va en la placa lateral y las mangueras pasan por el travesaño trasero y por la ranura inferior. Las cunas de batería, bomba y cámara admiten bridas.
4. Prueba el deslizamiento del conjunto en el tubo en seco. Comprueba la holgura en ambos extremos y ajusta los apoyos blandos si hace falta. Comprueba que la cinta, cables y mangueras queden dentro de la envolvente de paso. Para fijar el lastre de la siguiente revisión, pesa el conjunto montado.

## Impresión y verificación

Los STL están en milímetros, con el aro exterior de cada mitad apoyado en Z=0. Laminar en dos trabajos, con soportes para travesaños y repisas internas. Las dos mitades se laminaron en PrusaSlicer 2.9.7 con un perfil genérico de PETG, capa de 0,20 mm, cuatro perímetros, relleno del 30 %, soportes orgánicos y borde de 8 mm. El perfil estimó **511 g para la delantera y 461 g para la trasera**, incluidos soportes y borde. Usa el perfil de tu impresora para obtener sus tiempos y consumo. Comprueba que la cama admita la huella Ø167 mm más el borde de adhesión y que haya 196 mm de recorrido vertical.

Fusion confirmó un sólido conectado por mitad. La comprobación con 285 cuerpos de referencia incluyó cubeta, óptica, cámara, mangueras, batería, sensores y electrónica. El chasis queda libre en la comprobación con el tubo CAD de Ø170 mm interior y con las dos tapas de referencia. La tornillería y los volúmenes de acceso de la herramienta quedaron libres de interferencias. Ambos STL tienen mallas cerradas y un solo componente. La prueba en seco con las piezas reales determinará el ajuste final de bomba, cámara, batería y cinta CSI. Las envolventes comerciales y la PCB V8 siguen en revisión.
