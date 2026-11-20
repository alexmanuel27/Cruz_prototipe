# Cuerpo de PVC horizontal con tapa acrílica — revisión D45

> **ARCHIVO D49, 30 oct:** PVC descartado por Alex. La [base vigente es acrílica horizontal](IMPLANTACION_ACRILICO_HORIZONTAL.md). Este texto y su dibujo se conservan como historial.

**21 de octubre de 2026.** Alex vuelve al cuerpo de PVC, dispone el instrumento horizontalmente y pide una tapa acrílica atornillada con silicona y argollas para los pesos. Confirma que la cámara auxiliar **mira hacia delante por la tapa**, no verticalmente hacia el fondo del agua. Este documento sustituye como base mecánica a la implantación vertical de cuerpo acrílico D39/D40.

[Boceto del conjunto](drawings/pvc-horizontal-v1.png) · [SVG editable](drawings/pvc-horizontal-v1.svg).

## 1. Qué queda fijado y qué se conserva como referencia

| Aspecto | Base vigente |
|---|---|
| Cuerpo | Tubo de PVC; se recupera como candidato dimensional el [WitWay 998087, Ø160 exterior / pared 4 mm / interior 152 mm / suministro 1 m](https://witway.be/pvc-buis-glad-160-x-4-0mm-sn4-lengte-1-meter/), de la versión anterior |
| Longitud | **330 mm como referencia provisional de encaje**, conservada del último diseño; Alex no ha fijado una nueva longitud al volver a PVC. No cortar todavía. El PVC anterior usaba 300 mm: ese valor no se reactiva automáticamente |
| Despliegue | Eje longitudinal horizontal; comprobar orientación estable con el lastre |
| Visión auxiliar | Hacia delante por una tapa/ventana de acrílico; retirar el requisito de visión a través de la pared curva del cuerpo |
| Cierre transparente | Tapa acrílica sujeta por tornillos y silicona. Se propone interpretar la silicona como **junta plana maciza recortada y comprimida**, desmontable; no se ha seleccionado un sellante ni aprobado una unión pegada |
| Otro extremo | Cierre y distribución final por resolver. Propuesta: concentrar servicios en el extremo opuesto a la cámara, con acceso al bastidor |
| Pesos | Argollas para sujeción del lastre; cantidad, posición, fijación y masas por dimensionar |
| Instrumentación | Conservar OV9281, AS7265x, cámara USB auxiliar, cubeta, fuentes, batería y bomba ya tratadas |
| Puerto eléctrico | Bulgin de ocho contactos y dirección RS-485; previsión de boya sin introducir nuevas compras de electrónica |
| Driver/potencia | Aplazados hasta terminar y probar el diseño, según D44 |

Precio consultado del tubo candidato: **13,48 EUR con IVA** (11,14 EUR sin IVA), por el suministro de un metro. No es un presupuesto del cuerpo completo. El precio de 122 EUR del tubo acrílico retirado deja de pertenecer al subtotal vigente.

## 2. Tapa de acrílico y silicona

Diseñar un apoyo rígido y continuo alrededor de la abertura. La junta propuesta forma un **anillo que deja libre la zona de visión**. Distribuir el apriete con tornillos y apoyos adecuados, con control de compresión; no fijar espesor de junta o acrílico, patrón de agujeros ni par de apriete por el dibujo.

La unión entre el apoyo y el tubo de PVC, y la retención de la tapa, siguen por diseñar. No se presupone que roscar directamente en una pared de PVC de 4 mm o en el acrílico resuelva las cargas. Los cuatro tirantes, tóricas y Ø200 de la versión anterior dejan de ser cotas o cantidades de pedido vigentes. Pueden estudiarse si la solución lo necesita, pero Alex aún no ha elegido el mecanismo detallado de retención de este cierre.

Los manguitos y tapones roscados de la antigua lista PVC se conservan como referencias. No se añaden automáticamente dos de cada uno, porque el nuevo extremo transparente cambia el cierre. Si se integra una ventana en un tapón o se usa otra solución de apoyo, documentar sus interfaces y sellos en el plano antes de comprar accesorios.

## 3. Cámara, óptica y agua

La cámara USB auxiliar mira por la tapa de un extremo hacia delante. Reservar su soporte, enfoque, conector/cable y apertura útil; comprobar imagen a través de acrílico plano sumergido, reflejos y luz de los instrumentos. Conservar protección local de los módulos espectrales.

Reorganizar el bastidor para el tubo horizontal; **no basta girar el dibujo vertical**. Proponer que la cubeta conserve entrada inferior y salida superior, con paso ascendente para gestionar burbujas. La geometría relativa de los ejes ópticos permanece; ubicarla sin modificar los 60 mm de referencia, rendija de 0,5 mm ni disposición de detectores/fuentes acordada. Posiciones y alturas concretas por comprobar con componentes reales.

Recorrido fijo: toma → cubeta → bomba → descarga. La bomba permanece después de medir la muestra y su motor en seco. Ubicarla y trazar tubos en el nuevo bastidor; la indicación anterior «bomba arriba» pasa a ser una preferencia de posición relativa, no un nivel axial de la vieja torre. No fijar nuevos tiempos, volúmenes o consumo en este cambio.

## 4. Argollas y lastre

**Confirmación de Alex, 30 oct (D47): pesos sujetos a varillas laterales exteriores**, con el equipo horizontal y la cámara hacia delante. Propuesta de apoyo: dos abrazaderas/collares que distribuyan las cargas sobre el PVC y soporten las varillas. Cantidad, sección, longitud, material y separación definitivos dependen del peso y del centro de masas. No asignar masa de lastre por estimación visual ni considerar estas varillas como los cuatro tirantes del cierre acrílico anterior.

Proponer pesos por debajo del eje del tubo, repartidos longitudinalmente y retenidos para que no se deslicen ni giren. Mantener libre la ventana frontal, toma y descarga. Las cargas de lastre se transmitirán al soporte exterior; no confiar su soporte al acrílico. El boceto D45 muestra collares y lastre conceptual; aún no representa el detalle de las varillas añadido en D47.

Comprobar tracción de argollas, tornillos y soportes; deslizamiento y giro de collares; resistencia del PVC a carga local; orientación con masas reales; y distancia de cámara/toma al fondo. El lastre debe mantener estable el conjunto horizontal sin ocultar la visión o cargar mangueras. La pared de presión no se perfora para añadir las argollas en esta propuesta. La recuperación tendrá un camino de carga definido; no atribuir automáticamente a una argolla de lastre capacidad de izado.

## 5. Próximo diseño y ensayo

1. Medir piezas reales y cerrar longitud/diámetro; 160 × 4 y 330 mm siguen siendo referencias de implantación por confirmar para esta revisión.
2. Dibujar el apoyo PVC–tapa, junta de silicona, tornillos y cierre del otro extremo. Resolver posiciones de puertos y acceso al bastidor.
3. Dimensionar resistencia, sellado y fijación de lastre. SN4 no equivale a una presión exterior admisible y la nueva tapa no hereda los cálculos del tubo acrílico anterior.
4. Ensayar envolvente con sus interfaces, orientación horizontal, lastre y testigos, **sin electrónica ni batería el 30 de octubre**. Mantener registro fotográfico y resultado.
5. Solo después de terminar y probar el diseño, retomar la selección del driver y la electrónica de potencia. Sin compras ni fabricación ejecutadas en esta revisión.
