# Organización del montaje en Fusion

## Revisión actual de componentes de catálogo — 3 de noviembre de 2026

Usar **[CROSS_MODELOS_CATALOGO_2026-11-03.f3d](CROSS_MODELOS_CATALOGO_2026-11-03.f3d)**. Se sustituyeron referencias simplificadas por modelos detallados de Raspberry, Atlas, Pololu, motor de familia MOONS y pasamuros WetLink; se ajustaron bandeja, chasis y posición del regulador. Hay 330 cuerpos BRep, 325 sólidos físicos comprobados y cero choques externos sin explicar. Los solapes de catálogo y seis incidencias del historial original se detallan en [REVISION_STEP_2026-11-03.md](REVISION_STEP_2026-11-03.md). Webcam/cabezal y otras piezas siguen aproximados. Las secciones siguientes conservan revisiones anteriores.

## Revisión de tapas para CNC — 3 de noviembre de 2026

Copia vigente: `CROSS_TAPAS_10MM_RANURA_3MM_2026-11-03.f3d`. Ambas tapas son de PMMA de 10 mm, con ranura interior de 3 mm y 7 mm de material debajo. Tubo liso; cierre, conectores y holguras ajustados. Ver `TAPAS_CNC.md`. La comprobación mantiene 185 cuerpos, sin interferencias no previstas; la resistencia y la estanqueidad siguen pendientes de ensayo. La copia limpia del apartado siguiente es la revisión anterior.

## Versión vigente: montaje limpio, 2 de noviembre de 2026

Usar `CROSS_MONTAJE_LIMPIO_2026-11-02.f3d`. Se retiraron del navegador las PCB anteriores, los modelos originales duplicados, el ESP32, las envolventes electrónicas sustituidas por V8, las mangueras anteriores, la cámara larga de conductividad y los soportes ya integrados en el chasis. No quedan conjuntos antiguos ocultos que puedan reactivarse con la bombilla.

El navegador pasó de 384 a 206 ocurrencias. Los 185 cuerpos conservados tienen los mismos volúmenes y límites espaciales antes y después de la limpieza. Se mantienen las 19 piezas impresas actuales. Las retiradas están agrupadas al final de la línea de tiempo para conservar las dependencias de construcción; no se borró el historial que produce la geometría actual. V8 sigue siendo una placa de estudio, no fabricable.

Detalle y comprobación: `LIMPIEZA_RESULTADO_2026-11-02.json`. Copia previa: `CROSS_ANTES_LIMPIEZA_2026-11-02.f3d`. Los apartados siguientes describen revisiones anteriores; sus referencias a piezas ocultas o PCB archivadas ya no corresponden al navegador actual. El documento activo de Fusion tiene cambios sin guardar.

En el navegador, despliega `M2_GENERATED` para acceder a los conjuntos:

1. **CARCASA_Y_TAPAS:** tubo, tapas y juntas.
2. **VARILLAS_Y_CIERRES:** varillas, tuercas y arandelas.
3. **CHASIS_Y_SOPORTES:** chasis, bandejas y soportes impresos.
4. **OPTICA_REFERENCIAS:** cubeta, cámara y elementos ópticos de referencia.
5. **ELECTRONICA_REFERENCIAS:** batería y electrónica de referencia.
6. **AGUA_Y_SENSORES:** mangueras, conexiones y sensores.
7. **LASTRE:** abrazaderas y fijaciones.

En la línea de tiempo inferior, despliega cada grupo para editar sus operaciones. Hay grupos separados para cada varilla, cada tramo de manguera, conductividad, temperatura y los demás conjuntos. Las primeras operaciones del diseño original están agrupadas por orden porque su función no está identificada por completo. Las versiones anteriores del PCB siguen identificadas como borradores.

El archivo `CROSS_ORGANIZADO_2026-11-02.f3d` es una copia exportada del montaje organizado; `CROSS_ANTES_ORGANIZAR_2026-11-02.f3d` es la copia anterior. El diseño activo en Fusion tiene cambios sin guardar. La organización no resuelve las interferencias conocidas ni convierte el PCB en fabricable.

## Subconjuntos en el navegador

- `02_VARILLAS_Y_CIERRES`: cada varilla está junto a sus arandelas, tuercas y separador.
- `03_CHASIS_Y_SOPORTES`: cuatro subgrupos `3D` reúnen chasis y aros, bandejas, soportes ópticos y soportes de batería, bomba y sensores. `REFERENCIAS_DE_CONSTRUCCION_OCULTAS` contiene geometría usada para construir el chasis.
- `06_AGUA_Y_SENSORES`: entrada/salida, mangueras internas, conductividad, temperatura y puertos de bomba/cubeta.
- `07_LASTRE`: abrazaderas candidatas a impresión y placas metálicas de referencia.

Las piezas marcadas `3D` son candidatas a imprimir, no una orden de fabricación: comprobar encaje, medidas y materiales. Algunas piezas se mantienen ocultas como estaban antes de organizar. Despliega cada subconjunto y usa la bombilla para mostrar u ocultar piezas.

Copia más reciente: `CROSS_NAVEGADOR_ORGANIZADO_2026-11-02.f3d`; copia previa: `CROSS_ANTES_ORDENAR_NAVEGADOR.f3d`. El documento abierto en Fusion sigue sin guardar.

## Revisión de encaje y PiCam

La revisión más reciente es `CROSS_ENCAJE_REVISADO_PICAM_2026-11-02.f3d`. Ver `ENCAJE_Y_FIJACIONES_2026-11-02.md`. La Raspberry aparece en su propio subconjunto junto a la PiCam, V8 es la única PCB visible y las versiones anteriores están archivadas. Las guías se han integrado en el chasis y en la cubierta; usar la lista actual de 19 piezas para impresión, no las referencias ocultas.

La revisión de conductividad vigente es `CROSS_EC_PUNTA_HUMEDA_2026-11-02.f3d`: sonda en `03_CONDUCTIVIDAD_SOLO_PUNTA_HUMEDA`; la cámara larga está descartada y oculta. Ver `CONDUCTIVIDAD_PUNTA_HUMEDA.md`.
