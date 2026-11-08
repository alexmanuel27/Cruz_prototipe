# Revisión de modelos STEP — 3 de noviembre de 2026

## Resultado

Copia actual: **[CROSS_MODELOS_CATALOGO_2026-11-03.f3d](CROSS_MODELOS_CATALOGO_2026-11-03.f3d)**. El documento activo `Cross_M2_horizontal_design` se ha modificado; no se ha guardado en la nube. Se exportó una copia F3D. No se hizo commit ni push.

Se incorporaron seis tipos de referencias CAD: Raspberry Pi 4, Atlas ISCCB Gen 2, Pololu 2814, motor MOONS de familia MS11HS5P, WetLink JPT y tuerca WetLink. La sonda Atlas oficial ya estaba incorporada. **La Raspberry es comunitaria; el motor no es la variante personalizada exacta.** La procedencia y las limitaciones de cada componente están en [MODELOS_3D.md](../componentes/MODELOS_3D.md).

Los siete conjuntos aproximados sustituidos y el conjunto temporal de importación se retiraron del navegador mediante operaciones Remove, conservando las dependencias del historial. Las nuevas piezas están en los subconjuntos existentes, no duplicadas en la raíz. Los grupos de importación tienen nombres del componente y fabricante. V8 sigue siendo la única PCB de estudio del navegador; no está lista para fabricar ni energizar.

## Posición y ajustes

- **Raspberry:** conserva placa X118–203, Y4–60, Z42–43,6 mm. El STEP detallado añade los puertos reales de su modelo, chips, GPIO y conectores de cinta. Se giró y trasladó, sin escalar ni reflejar. Permanece sobre la cubierta óptica, junto a la PiCam; recorrido, orientación y longitud de la cinta CSI real todavía deben comprobarse.
- **Bandeja `P_TOP`:** se retiró una pequeña pestaña obsoleta que chocaba con el conector de pantalla de la Pi. Se eliminó toda esa porción desconectada, no se dejó una punta flotante.
- **Regulador azul `EL_LED_B`:** reserva desplazada 3,5 mm en X mediante edición del sólido base. Quedan 1,05 mm nominales hasta el conector Pi y 1 mm hasta la reserva RTC. Son holguras entre los modelos, no tolerancias aprobadas para piezas compradas.
- **Motor:** el CAD de familia conserva eje del cabezal y posición de bomba aguas abajo de la cubeta. Rebaje en chasis trasero X248,75–255, Y23–41, Z−56 a −45,5 mm para conector y salida de cables. El eje, piloto y unión al cabezal real no están dimensionados definitivamente.
- **Atlas Gen 2:** colocado sobre el soporte lateral seco existente, conservando separadores y SMA del modelo. Envolvente centrada aproximadamente en X342, Z0 mm; pies sobre Y−70 mm. La generación de la placa física y su placa hija EZO-EC siguen por confirmar; las cinchas de montaje son provisionales.
- **Pololu:** modelo oficial colocado dentro de la reserva electrónica, con mando y terminales detallados.
- **WetLink:** dos conjuntos con tuerca, apoyados en la tapa trasera de 10 mm. Se conservó el STEP de origen, incluido su conducto interno simplificado.
- **Webcam y cabezal:** se añadieron atributos con los nuevos enlaces exactos de Alex. Sin STEP ni cotas verificables, sus envolventes no se alteraron a partir de una fotografía. Solo el color ámbar del cabezal sigue la foto del producto.

Se mantienen tubo Ø180/170 × 380 mm, tapas PMMA de 10 mm, ranura de junta de 3 mm en las tapas, tubo liso y cierre de cuatro varillas. Esta revisión no recalcula presión ni consumo.

## Comprobación del encaje modelado

[COMPROBACION_MODELOS_CATALOGO_2026-11-03.json](COMPROBACION_MODELOS_CATALOGO_2026-11-03.json) contiene el análisis completo:

- 330 cuerpos BRep en el montaje; 325 sólidos físicos incluidos en el cálculo.
- Se excluyen una reserva no física para enchufes Pi y cuatro superficies no sólidas del CAD del motor.
- **Cero interferencias externas sin explicar**, tras corregir bandeja, chasis y regulador.
- 98 intersecciones internas de los archivos de catálogo: pines embebidos en PCB y detalles superpuestos de encapsulados.
- Ocho intersecciones de roscas M8 simplificadas y dos de roscas modeladas WetLink/tuerca.
- Una intersección de eje/piloto del motor con la reserva del cabezal: no equivale a verificar su acoplamiento real.
- Dos intersecciones de la manguera continua con una zona cerrada del conducto en el STEP público WetLink, unos 0,202 cm³ cada una. Se conserva el archivo oficial sin perforarlo artificialmente; este CAD no permite certificar el paso interior del tubo ni su sellado.

Las clasificaciones de piezas importadas se basan en atributos del componente nativo: Fusion devuelve cuerpos nativos en algunos resultados de interferencia. No se compara la cadena `entityToken`, que puede cambiar. La ausencia de choques externos no valida medidas compradas, radios de curvatura, disipación, óptica o estanqueidad.

## Historial del diseño original

La revisión recursiva de 977 elementos del historial registra **cinco advertencias y un error** en los grupos `Diseno original…` de la raíz, no en las nuevas importaciones:

- `Sketch2`, `Sketch12`, `Sketch34` y `Sketch35`: referencias/plano perdidos, uso de caché.
- `Extrude5`: referencia de cuerpo perdida, geometría en caché.
- `Combine5`: cuerpo objetivo perdido.

No se eliminaron esas operaciones del diseño original para silenciar los avisos. Los sólidos activos exportados se comprobaron con el análisis anterior; la regeneración completa de ese historial no queda aprobada. Detalle: [EXPORTACION_MODELOS_CATALOGO_2026-11-03.json](EXPORTACION_MODELOS_CATALOGO_2026-11-03.json).

## Vistas nativas

- [Montaje completo](STEP_MONTAJE_CATALOGO_2026-11-03.png).
- [Raspberry, conectores y bandeja](STEP_DETALLE_RASPBERRY_2026-11-03.png): carcasa y varillas ocultas para inspección.
- [Motor, cabezal y zona Atlas](STEP_DETALLE_MOTOR_ATLAS_2026-11-03.png): además se ocultan batería, bandeja superior y PCB V8 para ver el interior. No representa piezas retiradas del montaje definitivo.

La vista final de Fusion restaura carcasa, varillas, batería, bandeja y V8. Cuatro superficies auxiliares del motor y la reserva de enchufes Pi permanecen ocultas.

## Fuentes de la modificación

- `instalar_modelos_catalogo.py`: colocación de las importaciones y retirada de referencias sustituidas.
- `ajustar_holguras_modelos_catalogo.py`: rebajes, reserva del regulador y atributos de las fotos.
- `comprobar_modelos_catalogo.py`: interferencias del conjunto.
- `exportar_vistas_modelos_catalogo.py`: restauración de visibilidad, copia F3D, vista general y revisión del historial.
- [Manifiesto de archivos](../componentes/MANIFIESTO_ARCHIVOS_2026-11-03.json): tamaños y SHA-256 de los STEP conservados.

Siguiente paso físico: contrastar cámara, cabezal, motor personalizado y revisiones Atlas con las piezas recibidas antes de cerrar sus fijaciones. Para el EN3, obtener el CAD del fabricante mediante cuenta o medir y usar el plano oficial; no se ha entrado en cuentas durante esta revisión.
