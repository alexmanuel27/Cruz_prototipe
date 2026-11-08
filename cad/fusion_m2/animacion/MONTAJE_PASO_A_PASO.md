# Montaje del instrumento — animación desde Fusion

Revisión propuesta, 3 de noviembre de 2026.

## Archivos

- Vídeo: `CROSS_MONTAJE_ORDEN_REAL_2026-11-03.mp4` (1920 × 1080, 24 fps, sin audio).
- Modelo de revisión: `../CROSS_MONTAJE_ACCESIBLE_2026-11-03.f3d`.
- Original preservado: `CROSS_ANTES_ANIMACION.f3d` y `ESTADO_ORIGINAL_ANTES_CORREGIR_ACCESOS.json`.
- Vista general de etapas: `SECUENCIA_MONTAJE.png`.
- Piezas impresas de esta revisión: `../PIEZAS_IMPRESAS_MONTAJE_2026-11-03.json` (20 referencias; fuentes en F3D, no orden de fabricación).

El vídeo usa imágenes del modelo real de Fusion. Los movimientos se generan con las transformaciones de sus componentes. **No se ha creado una línea de tiempo editable en el espacio Animation de Fusion.** El plan, las posiciones originales y los scripts de generación quedan junto al vídeo.

## Cambios para permitir el montaje

La comprobación de trayectorias mostró que algunas piezas encajaban en su posición final, pero no podían entrar siguiendo una trayectoria recta. Se preparó una revisión que conserva el original guardado por Alex:

1. Travesaño del chasis en X216 convertido en pieza desmontable `P_TRAV216`, con dos M3 × 16 avellanados y dos tuercas cautivas. Se coloca después de la cubierta y antes de la bandeja.
2. Canal axial inferior para introducir la sonda EC desde atrás: radio 15,3 mm en Y0/Z−60, con alivio lateral para el racor. Espesor geométrico ideal mínimo de 8,7 mm hasta el exterior del chasis; pendiente tolerancia de impresión.
3. Alivio estrecho para el racor inferior de temperatura, manteniendo la inserción axial.
4. Paso abierto para la salida lateral del motor y pequeño alivio de la interfaz Atlas. No se desplazan las piezas comerciales.
5. Extremo de bandeja recortado hasta X371,9 y placa lateral Atlas hasta X371,7 para liberar el aro posterior. Permanecen los apoyos y fijaciones existentes.

Estos cambios se aplican a las piezas impresas interiores; no cambian tubo, tapas, ranuras de junta, posiciones ópticas ni dimensiones de cierre. La revisión añade una pieza impresa, dos tornillos y dos tuercas. Los 335 BRep incluyen superficies auxiliares y modelos de catálogo: no equivalen al número de piezas de compra.

La comprobación geométrica es discreta y no sustituye una prueba física. Confirmar acceso de herramientas, juego de montaje y orientación de impresión antes de fabricar.

## Comprobación de trayectorias

`VALIDACION_MONTAJE.json`: revisión completa de 31 etapas con 2.756 intersecciones y siete posiciones discretas por entrada. `VALIDACION_CIERRE_FINAL.json`: otras 703 comprobaciones de las ocho etapas finales tras corregir el orden de collares y arandelas. En ambas solo se detecta el contacto previsto entre tuerca M8 y varilla, con roscas simplificadas. Comprobar en piezas reales la profundidad útil de las tuercas ciegas. La prueba se detiene ante el primer choque de una etapa: no valida todas las superficies de esa excepción ni simula colisiones continuas, flexión o acceso de herramientas.

## Orden y tiempos

| Inicio | Paso | Operación |
| --- | ---: | --- |
| 00:03 | 1 | Unir las dos mitades del chasis |
| 00:06 | 2 | Introducir la sonda de conductividad |
| 00:11 | 3 | Introducir la sonda de temperatura |
| 00:14 | 4 | Fijar los apoyos ópticos |
| 00:18 | 5 | Instalar el módulo óptico premontado |
| 00:22 | 6 | Instalar la cubeta de flujo |
| 00:26 | 7 | Montar la cámara auxiliar |
| 00:29 | 8 | Instalar la bomba completa |
| 00:33 | 9 | Fijar la interfaz Atlas en seco |
| 00:37 | 10 | Colocar la cubierta óptica |
| 00:42 | 11 | Introducir las dos tuercas cautivas |
| 00:46 | 12 | Asentar el travesaño desmontable |
| 00:49 | 13 | Fijar el travesaño con dos M3 |
| 00:53 | 14 | Sujetar la batería |
| 00:57 | 15 | Bajar la bandeja antes de la Raspberry |
| 01:02 | 16 | Montar la Raspberry junto a la PiCam |
| 01:06 | 17 | Instalar PCB y módulos en la bandeja |
| 01:10 | 18 | Colocar los retenedores laterales |
| 01:14 | 19 | Preparar y apoyar la tapa trasera |
| 01:18 | 20 | Conectar las mangueras inferiores |
| 01:22 | 21 | Conectar cubeta y bomba por arriba |
| 01:27 | 22 | Revisar el conjunto todavía abierto |
| 01:31 | 23 | Deslizar el tubo desde el frente |
| 01:36 | 24 | Introducir las cuatro varillas desde atrás |
| 01:39 | 25 | Colocar las arandelas interiores traseras |
| 01:43 | 26 | Colocar los limitadores de compresión |
| 01:47 | 27 | Deslizar los dos conjuntos de lastre |
| 01:52 | 28 | Colocar las arandelas interiores delanteras |
| 01:56 | 29 | Presentar junta y tapa frontal |
| 02:00 | 30 | Cerrar alternando las diagonales |
| 02:05 | 31 | Comprobar el montaje terminado |

## Instrucciones de cada etapa

### 01. Unir las dos mitades del chasis

Colocar tuercas cautivas y fijar la unión M4. Dejar desmontado el travesaño de X216.

### 02. Introducir la sonda de conductividad

Entrar desde atrás por el canal axial y fijar con apoyos blandos. Chasis transparente solo para mostrar este acceso.

### 03. Introducir la sonda de temperatura

Entrar desde atrás con el bloque de flujo premontado. Vista transparente para mostrar el acceso bajo el chasis.

### 04. Fijar los apoyos ópticos

Montar y comprobar los apoyos antes de colocar el cuarzo.

### 05. Instalar el módulo óptico premontado

En banco: montar PiCam, AS7265x y ambos LED en el portador. Después bajar el conjunto y fijarlo.

### 06. Instalar la cubeta de flujo

Apoyos blandos; no transmitir esfuerzos de las mangueras al cuarzo.

### 07. Montar la cámara auxiliar

Orientar la lente hacia la futura tapa transparente frontal.

### 08. Instalar la bomba completa

Motor y cabezal premontados. La muestra se mide antes de pasar por la bomba.

### 09. Fijar la interfaz Atlas en seco

Premontar placa lateral y carrier; dejar acceso a tornillos y bridas.

### 10. Colocar la cubierta óptica

Conectar CSI a la PiCam y sacar su extremo libre. Pasar también la manguera superior, aún sin conectar.

### 11. Introducir las dos tuercas cautivas

Deslizar las M3 en los alojamientos laterales del chasis, antes de cerrar el travesaño.

### 12. Asentar el travesaño desmontable

Apoyar ambos extremos en las ménsulas del chasis; no cargar la cubierta óptica.

### 13. Fijar el travesaño con dos M3

Tornillos avellanados M3 × 16; cabezas enrasadas y acceso libre antes de instalar la bandeja.

### 14. Sujetar la batería

Mantenerla desconectada y preparar el cableado antes de cubrir el compartimento.

### 15. Bajar la bandeja antes de la Raspberry

Bandeja vacía y separadores; extremo trasero recortado para que entre sin chocar con el aro.

### 16. Montar la Raspberry junto a la PiCam

Conectar la cinta CSI sin tensarla y fijar la Pi sobre la cubierta. Mantener libres sus puertos.

### 17. Instalar PCB y módulos en la bandeja

V8 todavía de estudio. Colocar las placas con el equipo sin alimentación y sin forzar conectores.

### 18. Colocar los retenedores laterales

Entrar desde ambos lados, encajar las ranuras en el borde y fijar con M3.

### 19. Preparar y apoyar la tapa trasera

Premontar juntas, pasamuros y conector EN3 fuera del tubo; dejar la tapa accesible.

### 20. Conectar las mangueras inferiores

Con el tubo retirado, conectar sensores y pasamuros. Fijar rutas sin radios cerrados ni pellizcos.

### 21. Conectar cubeta y bomba por arriba

Recuperar el extremo que se pasó por la cubierta y conectarlo a la bomba. Revisar ambos extremos.

### 22. Revisar el conjunto todavía abierto

Comprobar fijaciones, CSI, cables y circuito hidráulico. Validar la electrónica antes de energizar.

### 23. Deslizar el tubo desde el frente

Guiarlo hasta la junta trasera sin rozar componentes; comprobar que ningún cable quede en el cierre.

### 24. Introducir las cuatro varillas desde atrás

Tuercas y arandelas exteriores traseras premontadas; todavía sin comprimir las tapas.

### 25. Colocar las arandelas interiores traseras

Deslizarlas desde los extremos delanteros libres; no atraviesan los taladros de la tapa.

### 26. Colocar los limitadores de compresión

Deslizarlos sobre las varillas desde delante hasta las arandelas traseras.

### 27. Deslizar los dos conjuntos de lastre

Primero el collar trasero, después el delantero. Deslizar sobre tubo y limitadores antes de poner arandelas delanteras.

### 28. Colocar las arandelas interiores delanteras

Presentarlas contra los extremos de los limitadores.

### 29. Presentar junta y tapa frontal

Junta en la ranura de la tapa; limpiar, alinear y evitar retorcerla durante el cierre.

### 30. Cerrar alternando las diagonales

Colocar arandelas y tuercas exteriores; apretar por etapas y comprobar compresión uniforme.

### 31. Comprobar el montaje terminado

Revisar fijaciones, visión de cámara y lastre. El ensayo de estanqueidad se hace aparte, sin electrónica.

## Supuestos y límites

- El módulo óptico se prepara en banco: portador, PiCam, AS7265x y LED. Su inserción se representa como una unidad. Apretar sus fijaciones con los ejes ópticos alineados; la película no reproduce cada tornillo.
- La interfaz Atlas entra lateralmente elevada 8 mm y después desciende. Las conexiones se realizan con acceso abierto.
- La manguera superior se pasa por la cubierta antes de asentarla. Se deja libre mientras se montan batería, bandeja y placas; se conecta a la bomba al terminar. Las mangueras aparecen en su ruta final: no se simula flexión ni se presupone que atraviesen piezas.
- Los collares se deslizan axialmente, primero el trasero y luego el delantero, después de arandelas traseras y limitadores. Sus pasos de Ø15 mm dejan pasar los limitadores Ø14; las arandelas anchas Ø22 se colocan fuera de esos pasos. Comprobar las holguras reales de impresión (tubo Ø180 frente a alojamiento Ø180,6).
- En las etapas 2 y 3 el chasis se hace semitransparente únicamente para mostrar el montaje de las sondas inferiores; su material no cambia.
- Cables, bridas, algunas fijaciones, adhesivos y herramientas no están representados. Los rótulos indican cuándo deben instalarse.
- Las juntas se muestran en su geometría de trabajo. No se simula compresión ni se prescribe un par de apriete que todavía no se ha ensayado.
- Webcam y cabezal peristáltico siguen siendo envolventes aproximadas. El STEP del motor es de familia MOONS, no de la variante exacta; Pi comunitaria y revisión Atlas según el manifiesto de modelos.
- PCB V8 sigue sin terminar eléctricamente. El vídeo no autoriza fabricar ni energizar la placa.
- El ensayo de estanqueidad se realiza por separado, con lastre y sin electrónica. No se registra aquí ningún ensayo físico como realizado.
- Permanecen las incidencias previas del historial de Fusion; no se ha reparado ni ocultado su estado.
- Documento activo restaurado a la posición armada al terminar cada lote. No se ha guardado una nueva versión en la nube ni se ha hecho commit/push.
