# Implantación interior y tapa de servicio — propuesta 01

> **ARCHIVO D45:** esta implantación vertical en tubo acrílico está sustituida por [PVC horizontal](IMPLANTACION_PVC_HORIZONTAL.md). Sus niveles, Ø200, tóricas y tirantes no son cotas de compra vigentes.

**21 de octubre de 2026 · Para discutir con Alex.** Desarrolla las dimensiones aceptadas en D39; la distribución y las reservas nuevas de este documento todavía son propuestas. No demuestra encaje, resistencia ni estanqueidad; no es un plano de taladros o fabricación. No modifica el presupuesto energético.

## Bocetos

- [Distribución longitudinal, cruz y cámara auxiliar — PNG](drawings/implantacion-interior-v1.png) · [SVG editable](drawings/implantacion-interior-v1.svg).
- [Tapa superior y puertos — PNG](drawings/tapa-servicios-v1.png) · [SVG editable](drawings/tapa-servicios-v1.svg).
- [Generador reproducible de SVG](../cad/implantacion/generar_bocetos.py).
- [Concepto de cierre aceptado](drawings/cierre-acrilico-boceto-v1.png).

## 1. Base fija y sistema de coordenadas

Tubo de PMMA transparente: **150 mm exterior / 140 mm interior / 5 mm de pared / 330 mm de altura de tubo**. Las tapas añaden altura; el largo de los tirantes depende de sus espesores, arandelas y tuercas. En este documento, `z = 0` corresponde al extremo inferior del tubo y `z = 330` al superior. Las cotas no incluyen las tapas.

Equipo vertical. Tapa superior de servicio, con dos racores de agua, un único conector de carga/datos y un vent o PRV. Tapa inferior ciega y desmontable. Mantener una junta axial por tapa y cuatro tirantes exteriores, sin taladrar la pared curva.

## 2. Distribución longitudinal propuesta

Las alturas siguientes son **presupuestos de espacio**, no cotas verificadas de los componentes. Las líneas discontinuas separan zonas funcionales; **no representan mamparos estancos**.

| Zona | Altura z, mm | Reserva | Criterio y límite |
|---|---:|---:|---|
| Fondo | 0–15 | 15 mm | Testigo/sensor de fuga, canal de recogida y separación respecto a la bandeja de batería. No constituye un depósito estanco ni una garantía de protección de la batería. |
| Batería | 15–80 | 65 mm | Pack en soporte independiente y elevado; fusible accesible junto al pack. Dimensiones anunciadas del pack 70 × 37,5 × 56 mm, pendientes de comprobar. Incluir DC5521, cable y aislamiento. |
| Paso/servicio | 80–90 | 10 mm | Guiado y separación; ajustar después de comprobar radios y fijaciones. |
| Óptica | 90–165 | 75 mm | Cubeta vertical y dos ejes ópticos transversales. Resguardo opaco local desmontable; fuente caliente sobre soporte adecuado. Puertos axiales de la cubeta libres. |
| Separación | 165–170 | 5 mm | Holgura provisional entre niveles, no barrera hidráulica. |
| Adquisición y potencia | 170–255 | 85 mm | Pi orientada longitudinalmente, supervisor, RTC, drivers y DC/DC en soportes próximos. CSI e I²C interiores. Reserva muy ajustada al añadir conectores: puede requerir mover placas. |
| Cámara auxiliar | Dentro de 170–255 | Compartida | En lado opuesto a la Pi, mirando radialmente hacia fuera a través del acrílico. No se suma otra franja axial. Envolvente, cable y enfoque pendientes de medir. |
| Transición | 255–260 | 5 mm | Ajuste entre soportes; puede necesitar ampliación. |
| Bomba | 260–315 | 55 mm | Bomba completa arriba, motor seco. **55 mm es una reserva arbitrada para estudiar el encaje, no una dimensión de MS11HS5L410C-01**. Faltan cuerpo, motor, cable, tornillos y orientación de mangueras. |
| Conexiones de tapa | 315–330 | 15 mm | Reserva inicial para interiores de los puertos. Puede ser insuficiente para tuercas, conector y curvas; medir antes de cerrar niveles. |

La placa de la Pi 4 mide aproximadamente **85 × 56 mm**, según la [documentación oficial de Raspberry Pi](https://www.raspberrypi.com/documentation/computers/sbcs.html) y su [ficha mecánica](https://pip-assets.raspberrypi.com/categories/545-raspberry-pi-4-model-b/documents/RP-008341-DS-1-raspberry-pi-4-datasheet.pdf). Esta medida **no incluye** el volumen necesario para conectar USB/CSI/alimentación, refrigeración y soporte. Los bocetos muestran reservas funcionales, no modelos del fabricante.

## 3. Cruz y límite de encaje

Conservar la óptica acordada: halógena → muestra → rendija de 0,5 mm → red junto a lente gran angular → OV9281; LED 430 nm → muestra → AS7265x en el eje transversal. El rojo dibujado parte de la muestra y termina en el detector. La transmisión se mide antes de la fluorescencia. Mantener el ángulo de dispersión de 36° del montaje validado y la referencia de 60 mm de rendija a cámara; confirmar el plano físico de esa referencia antes de mecanizar.

La vista B **no es un trazado óptico ni reproduce el ángulo de la cámara**. Usa cajas orientativas para estudiar ocupación dentro del círculo. La red/lente lleva una pequeña franja de colores; no se dibuja dispersión libre entre rendija y red ni se añade colimador.

Propuesta de posición en planta, en mm respecto al eje del tubo:

| Referencia | x | y | Estado |
|---|---:|---:|---|
| Centro de cubeta | −22 | 0 | Desplazamiento propuesto para dar longitud al brazo de cámara |
| Rendija | −10 | 0 | Posición ilustrativa; comprobar alojamiento y separación a cubeta |
| Plano de referencia cámara/red-lente | +50 | 0 | 60 mm respecto a la rendija en la vista esquemática; plano real por confirmar |
| Fuente halógena | −54 | 0 | Centro de reserva; portalámparas y aislamiento por medir |
| AS7265x | −22 | +35 | Centro de reserva; PCB y campo de recepción por medir |
| LED 430 nm | −22 | −35 | Centro de reserva; otros cuatro LED y montaje aún pendientes |

**Punto crítico:** la reserva de cámara acaba cerca del límite interior del tubo. No se ha comprobado el conjunto inclinado, carcasa opaca, tornillos, disipación ni holguras de ajuste. Tampoco se ha verificado el volumen de los otros cuatro LED. El cabezal anterior de 207 × 160 mm no entra directamente. Antes de dar el encaje por válido, medir la óptica real completa y preparar envolventes 3D con soportes y cables; no acortar la distancia de 60 mm para forzar el cierre.

## 4. Agua y separación funcional

`Exterior → H1 → entrada inferior de cubeta → salida superior de cubeta → bomba → H2 → exterior`.

H1 está en la tapa superior, pero su conducto baja por un lateral hasta la base de la cubeta. El agua asciende por la cubeta y después llega a la bomba, situada arriba. En el croquis, los pasos hacia/desde la cabeza de bomba son simbólicos; orientación real pendiente de ficha y medición. Mantener la manguera peristáltica **3 mm interior / 5 mm exterior** y comprobar radios y resistencia a succión.

Guiar las mangueras en un canal independiente de las placas y del campo visual de la cámara, con retención en sus conexiones. Prever desvío de goteo hacia el testigo inferior sin atravesar la bandeja de batería. Las bandejas impresas no se consideran barreras estancas. Con la envolvente en una sola cavidad, una fuga sigue siendo un riesgo compartido: el sensor debe disparar parada y registro, con aislamiento de potencia según diseño eléctrico.

La toma exterior se prolonga y separa de la descarga; no son necesarios dos extremos de tubo abiertos cerca uno del otro. Mantener cubeta/conductos llenos entre ciclos; renovar varios volúmenes antes de medir. Blanco previo al despliegue en memoria; sin blanco a bordo ni caudalímetro.

## 5. Tapa superior: reservas para elegir componentes

**Contorno provisional Ø200 mm**, para dibujar los tirantes exteriores y su acceso. No es un diámetro final de compra. Espesor, diámetro de tirantes, arandelas, apriete y resistencia por calcular. La tórica se muestra centrada provisionalmente sobre la pared; hay que dimensionar ranura, sección y tolerancias dentro de sus 5 mm reales.

Coordenadas vistas desde fuera, x a derecha, y hacia arriba. Las coordenadas son propuestas de implantación; no autorizan perforación.

| Puerto | Centro x/y, mm | Diámetro de reserva, mm | Función |
|---|---|---:|---|
| H1 | −30 / +25 | 24 | Entrada, racor para manguera ID3 con sello de panel |
| H2 | +30 / +25 | 24 | Descarga desde bomba, segundo racor de panel |
| V1 | −30 / −25 | 20 | Un vent manual **o** una PRV; selección pendiente |
| E1 | +20 / −25 | 36 | Único conector de datos y carga, con contraparte y tapón estanco |

Los diámetros reservan **ocupación de tuerca, sello y herramienta**, no indican rosca ni taladro. Tras elegir modelos, comprobar el conjunto de arandelas/tuercas, capuchón, acceso por ambos lados, espesores admisibles y radios de cable/manguera. Si la herramienta no cabe, mover puertos antes de mecanizar.

Cuatro tirantes ilustrativos a radio 87 mm y ángulos de 45°, 135°, 225° y 315°. Radio, agujeros y distancias a bordes por verificar estructuralmente; los puntos grises no especifican un diámetro de taladro. Mantener todos los puertos dentro de la zona seca interior a la línea de sello.

## 6. Bastidor y mantenimiento

Proponer dos guías longitudinales y bandejas modulares impresas, desmontables. Fijar cada pieza pesada por su propio soporte; no cargar cubeta ni placas con masa de batería/bomba. Usar fijaciones cautivas donde faciliten servicio, sin depender de roscas en acrílico para soportar cargas.

Extracción propuesta por la tapa inferior, conservando la tapa superior de puertos. Requiere conexiones internas accesibles y desconectables; comprobar recorrido, holgura, longitud de servicio y que la extracción no tire de boquillas de cuarzo, CSI o USB. No basta dibujar una bandeja: hay que comprobar la secuencia de desmontaje antes de llamarla extraíble.

## 7. Siguiente cierre de diseño

1. Medir bomba completa, cámara USB con cable y óptica existente; fotografiar con regla.
2. Verificar las envolventes reales y los conectores dentro de ID140 × 330, manteniendo la óptica validada. Cambiar la distribución si las reservas no alcanzan.
3. Seleccionar las cuatro interfaces de tapa, con sus planos de montaje.
4. Dimensionar tapas de PMMA, junta axial sobre pared de 5 mm y tirantes; comprobar presión exterior e interior, flexión, fluencia y ligamentos entre agujeros.
5. Generar CAD del bastidor y del cierre y revisar montaje/desmontaje. Mantener el ensayo del **30 de octubre con lastre y sin electrónica ni batería**, con todas las interfaces finales.

No se han hecho pedidos, taladros, impresión ni ensayos al preparar estos bocetos.
