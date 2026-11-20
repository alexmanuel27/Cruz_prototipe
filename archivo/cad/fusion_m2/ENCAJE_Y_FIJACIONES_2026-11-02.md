> Actualización: el montaje de conductividad se ha sustituido por punta húmeda y cuerpo seco. La copia vigente es `CROSS_EC_PUNTA_HUMEDA_2026-11-02.f3d`; ver `CONDUCTIVIDAD_PUNTA_HUMEDA.md`. Las menciones a la cassette larga en este documento describen la revisión anterior.

# Encaje y fijaciones — revisión del 2 de noviembre de 2026

## Montaje actual

Copia completa: `CROSS_ENCAJE_REVISADO_PICAM_2026-11-02.f3d`. El documento activo de Fusion tiene cambios sin guardar. La versión V8 es la única PCB visible y está dentro de `M2_GENERATED / 05_ELECTRONICA_REFERENCIAS`. V3 y V4 están archivadas y ocultas en `90_PCB_ANTERIORES_NO_USAR`.

La PCB V8 continúa siendo un borrador electrónico sin terminar. Esta revisión corrige su integración mecánica; no autoriza fabricar ni alimentar esa placa.

La Raspberry se encuentra en `05_ELECTRONICA_REFERENCIAS / 01_RASPBERRY_PI_4_JUNTO_PICAM`, sobre la cubierta óptica, próxima al MonoSpectro. Su placa ocupa X=118–203, Y=4–60, Z=42–43,6 mm. Los puertos y el GPIO tienen envolventes separadas. El paso CSI está en X=185, Y=−15, en la cubierta superior: cerrar la ranura con espuma negra tras montar la cinta. Comprobar con la PiCam y la cinta reales la posición del conector, la longitud disponible y las curvas; no se ha modelado la cinta flexible completa.

La bomba está 20 mm más baja y 14 mm desplazada lateralmente respecto al montaje anterior. El flujo sigue: entrada → temperatura → conductividad → cubeta, de abajo hacia arriba → bomba → salida. Se añadió el tramo antes ausente entre temperatura y conductividad. Los recorridos anteriores están archivados dentro de las mangueras.

## Fijaciones sencillas

| Elemento | Solución | Tornillería o retención propuesta |
|---|---|---|
| Raspberry Pi | Cuatro postes de 5 mm integrados en la cubierta óptica; patrón 58 × 49 mm | 4 M2.5 × 12, arandelas y tuercas; colocar las tuercas antes de cerrar la cubierta |
| PCB y bandeja | Cuatro clips de borde; ranura de 2 mm para FR4 de 1,6 mm; topes longitudinales en la bandeja | 4 M3 × 25 con arandela; tuercas M3 cautivas en los travesaños. Los mismos tornillos sujetan clips y bandeja |
| Electrónica de conductividad | Placa lateral extraíble, separada de la batería | 2 M3 × 20 con tuercas y arandelas; 2 bridas para el módulo |
| Batería | Cuna integrada en el chasis | Dos bridas por las ranuras existentes |
| Bomba | Asiento rebajado integrado en el chasis, con topes laterales | Dos bridas de 2,5 mm; verificar sujeción y temperatura con la bomba física |
| Cámara auxiliar | Cuna frontal integrada en el chasis | Bridas por las ranuras existentes |
| Sonda/celda de conductividad | Dos apoyos de espuma de 2 mm sobre los nervios del chasis | Dos bridas alrededor de la cassette y los nervios; no cargar ni deformar las juntas |
| Tee de temperatura | Repisa integrada con paso inferior para el tubo | Dos bridas |
| Guías de mangueras | Integradas en cubierta óptica y chasis trasero | Sin tornillos ni piezas independientes |
| Módulos electrónicos externos | Sobre la bandeja ranurada, conservando sus reservas de espacio | Bridas; sus envolventes y conectores siguen siendo aproximados |

La longitud final de los tornillos se comprobará con arandelas y piezas impresas reales, evitando puntas sobresalientes hacia la óptica. La tornillería no está representada por completo en el modelo.

## Qué se imprime en esta revisión

Las 19 piezas visibles se enumeran con sus dimensiones en `PIEZAS_IMPRESAS_ACTUALES_2026-11-02.json`:

- Dos mitades de chasis.
- Una bandeja electrónica y cuatro separadores.
- Una cubierta óptica superior, ahora con postes de Raspberry y guía de retorno integrados.
- Dos apoyos ópticos.
- Una placa lateral para conductividad.
- Cuatro clips de PCB.
- Cuatro medias abrazaderas exteriores.

Las cunas, guías y soportes originales que están fusionados en esas piezas se mantienen ocultos como fuentes. No imprimirlos por separado. Los apoyos `ESPUMA_180` y `ESPUMA_300` se cortan en espuma; no son impresiones.

## Comprobación

`COMPROBACION_ENCAJE_PICAM_2026-11-02.json` registra el análisis de **195 cuerpos visibles**: **cero intersecciones no previstas**. Las ocho intersecciones restantes son las parejas varilla–tuerca, con roscas simplificadas. Se incluyeron las envolventes visibles de conectores.

Se corrigió la representación sobredimensionada de los pasamuros: cuello M10 para los taladros de 10,2 mm existentes. Referencia: [instalación WetLink JPT](https://bluerobotics.com/learn/wetlink-penetrator-jpt-assembly-and-installation/). Sigue siendo una envolvente simplificada: cotejar modelo comprado, espesor de montaje, asiento de junta y compatibilidad con la manguera.

El patrón de montaje de la Pi se contrastó con la [documentación mecánica oficial Raspberry Pi 4](https://pip.raspberrypi.com/categories/545-raspberry-pi-4-model-b). La forma de los componentes y conectores es aproximada.

Los radios de las rutas principales son 15 mm; el lazo temperatura–conductividad tiene dos curvas de 12,35 mm, pendientes de verificar con la manguera real. Este análisis no incluye todas las tolerancias, movimiento de cables, tornillos, disipación ni estanqueidad. Las dimensiones de bomba, celda y sondas marcadas como aproximadas siguen requiriendo cotejo físico.

Las matrices del antiguo explosionado corresponden al montaje anterior. Para esta revisión, usar las posiciones del informe de encaje y la copia F3D actual.
