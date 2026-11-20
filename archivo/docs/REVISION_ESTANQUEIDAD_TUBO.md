# Tubo acrílico y tapas: revisión de viabilidad

> **ARCHIVO D49:** cálculo del cuerpo acrílico anterior, con otro cierre y orientación. Aunque D49 recupera acrílico, la [base horizontal actual con silicona y varillas de lastre](IMPLANTACION_ACRILICO_HORIZONTAL.md) requiere verificar de nuevo cargas, retención y sellado. No trasladar capacidades ni ranuras.

> **Antecedente D39, 21 oct:** tubo acrílico transparente **Ø150 exterior / Ø140 interior / pared 5 mm y altura de tubo 330 mm**, con cámara USB auxiliar. Alex acepta tapas de PMMA colado, una tórica axial por tapa y cuatro tirantes exteriores. Se actualizan las cargas preliminares; espesores, ranuras, apriete, puertos y retención siguen por calcular y ensayar. Ver [lista vigente](../../compras/LISTA_COMPRA.md#1-cuerpo-y-consumibles).

**21 de octubre de 2026 · Análisis preliminar, sin ensayo físico ni certificación.**

## 1. Respuesta a la duda sobre imprimir la tapa

Una tapa impresa **puede ser viable para estudiar el servicio inicial de 1 m**, pero la resistencia y estanqueidad del conjunto concreto siguen sin demostrarse. No hay base para afirmar que cualquier tapa PETG gruesa o con relleno del 100 % servirá durante días. Tampoco hay razón para descartar toda impresión 3D sin diseñar y probar el cierre.

**Antecedente anterior a D38/D39:** se recomendó estudiar un cierre híbrido con superficies de sellado mecanizadas y piezas impresas para soporte, protección y retención según cálculo. Una tapa/tapón completo de POM-C mecanizado es una alternativa directa; aluminio mecanizado y protegido es otra. La preferencia de Alex por imprimir todo o casi todo el cuerpo sigue registrada: **D39 acepta ahora tapas de PMMA colado con cierre axial; las demás opciones quedan como alternativas**.

Los ensayos publicados por [Prusa sobre recipientes impresos](https://blog.prusa3d.com/watertight-3d-printing-part-2_53638/) muestran que la impresión puede funcionar bajo agua, pero que los cierres, defectos, acabado y deformación condicionan el resultado. Sus piezas y parámetros no califican nuestra tapa. El [manual de Parker](https://www.parker.com/content/dam/Parker-com/Literature/O-Ring-Division-Literature/ORD-5700.pdf), capítulo de sellado estático, es la referencia para diseñar ranuras, compresión, holguras y acabado; una ranura FDM sin acabado no hereda la tolerancia de una mecanizada.

## 2. Geometría real pendiente de confirmar

Alex fija **150 mm exteriores, 140 mm interiores y 330 mm de altura de tubo**. La pared radial es `(150 − 140) / 2 = 5 mm`. La altura total del instrumento incluirá tapas y retención. El [enlace de familia diconfa](https://www.amazon.com.be/-/en/dp/B0DCTW22XJ) procedía de la variante 134/124; Alex comunica 122,00 EUR de precio; no se ha podido verificar la referencia exacta 150/140, longitud de suministro, porte ni entrega.

Antes del plano de fabricación medir en ambos extremos: ID/OD en varios ángulos, ovalización, espesor mínimo, rayas en el alojamiento de juntas y perpendicularidad del corte. La ficha comercial de PMMA no proporciona tolerancia diametral ni profundidad admisible. La resistencia del tubo a presión exterior depende también del largo libre, apoyos e imperfecciones; no se deduce de la carga sobre la tapa.

## 3. Carga de presión: cálculo reproducible

Hipótesis: aire interior inicialmente a presión atmosférica, agua dulce de densidad `ρ = 1000 kg/m³`, `g = 9,81 m/s²` y **diámetro efectivo de sellado provisional 145 mm**, situado a mitad de la pared de 5 mm para estimar cargas del concepto axial. No fija el diámetro comercial de la tórica ni la ranura: en el CAD se sustituirá por el diámetro efectivo real y se comprobará el espacio disponible en la pared. `h` es la profundidad de la tapa considerada; la posición más profunda gobierna.

```text
Δp = ρ g h
A = π D² / 4 = π × 0,145² / 4 = 0,016513 m²
F = Δp A
```

| Profundidad / diferencia | Diferencia de presión | Fuerza por tapa | Equivalente de peso orientativo |
|---|---:|---:|---:|
| 1 m agua dulce | 9,81 kPa | 162,0 N | 16,5 kgf |
| 2 m agua dulce, solo comparación | 19,62 kPa | 324,0 N | 33,0 kgf |
| Vacío interior de 10 kPa en superficie | 10 kPa | 165,1 N | 16,8 kgf |
| Vacío interior de 34 kPa en superficie | 34 kPa | 561,4 N | 57,2 kgf |
| Sobrepresión interior de 0,8 bar | 80 kPa | 1321,0 N **hacia fuera** | 134,7 kgf |

En agua de mar con `ρ = 1025 kg/m³`, la carga a 1 m aumenta a unos **166,0 N**. Un tubo vertical largo puede poner la tapa inferior bastante más profunda que la superior: el límite de 1 m se refiere al punto más profundo, no solo a la toma.

Estos valores son **cargas**, no capacidades resistentes. No incluyen apriete, golpes, tracción del anclaje, esfuerzos de manguera, tensiones locales de puertos ni cambios térmicos del aire interior. La flexión de una placa circular varía fuertemente con diámetro libre y espesor; agujeros, nervios y apoyo cambian el resultado. Sin geometría, material impreso caracterizado, orientación y condiciones de apoyo no se puede fijar un espesor seguro con estos números solos.

## 4. Qué suele gobernar el cierre

| Modo de fallo | Consecuencia de diseño |
|---|---|
| Flexión de tapa / fluencia con horas de carga | Conservar compresión de junta bajo carga sostenida y temperatura real de lámpara/batería. Dimensionar diámetro libre, nervios y apoyo. |
| Poros o unión entre capas | Ensayar proceso y pieza final; relleno del 100 % no demuestra ausencia de vías de agua. Un recubrimiento tampoco sustituye resistencia estructural. |
| Ranura rugosa, ovalizada o con medidas erróneas | Superficies continuas y controladas, tóricas comerciales y compresión dentro del rango del compuesto/sección. Evitar rayas que crucen la línea de sello. |
| Roscas e insertos arrancados / plástico aplastado | Transmitir cargas con apoyo positivo y tornillería/retención calculada. No confiar el cierre a fricción de la junta ni a roscas FDM sin calificar. |
| Racores y válvula sobre una zona flexible | Zona local rígida y plana; junta del componente correctamente apoyada, suficiente rosca para tuerca y margen entre agujeros/ranuras. |
| Grietas o cargas puntuales en PMMA | Apoyos amplios y control de apriete; evitar perforar la pared para sujetar tirantes si se puede retener externamente. |
| Fuga del circuito de muestra dentro del tubo | Bandeja/recorrido separado de batería, retención de tubos y detector de fuga en la zona baja. La envolvente exterior no evita esta fuga interna. |

## 5. Alternativas para cerrar el tubo

| Opción | Ventaja | Límite / trabajo necesario | Estado |
|---|---|---|---|
| Tapa/tapón íntegramente FDM con juntas comerciales | Máxima fabricación propia, iteración rápida y geometría libre | Caracterizar impresión, acabar sellos, dimensionar resistencia/fluencia y puertos; validar cada cambio de proceso. Riesgo de iteraciones antes del 30 oct. | Abierta según preferencia de Alex |
| Híbrida: pieza impresa y portajuntas/placa estanca mecanizada | Conserva piezas impresas y controla las superficies críticas | Cada unión añadida es otro sello; el diseño debe identificar qué pieza recibe presión y cuál sella. Una placa metálica sobre un anillo FDM poroso no basta. | Alternativa previa a D39 |
| Tapón completo mecanizado en POM-C | Ranuras repetibles, aislante y sin corrosión metálica | Dimensionar fluencia, espesor y apoyo; obtener material/mecanizado en plazo. No es presión nominal garantizada. | Alternativa para reducir riesgo de fabricación |
| Tapa/flange mecanizados en aluminio protegido | Mayor rigidez y puertos robustos | Protección frente al agua y aislamiento de pares con inoxidable para uso futuro en bahías; fabricación y coste por cotizar. | Alternativa |
| Flange comercial Blue Robotics | Diseño comercial documentado | No asumir compatibilidad por llamarse «5 pulgadas»: el tubo propio Ø140 interior requiere cotejar planos y tolerancias. | No comprar sin cotejo dimensional |

### Concepto de cierre aceptado; dimensiones por calcular

- Dos discos de **PMMA colado**, cada uno con **una tórica axial comercial** en ranura mecanizada; cuatro tirantes exteriores retienen ambas tapas. Véase [boceto actualizado](drawings/cierre-acrilico-boceto-v1.png). Sustituye la propuesta inicial de doble sello radial.
- Apoyo directo del extremo plano del tubo contra la tapa; controlar profundidad de ranura y compresión de junta. Dimensionar para la pared de **5 mm**, comprobar tolerancias y evitar cargas puntuales. Los tirantes pasan por fuera del tubo sin taladrar su pared.
- Una tapa de servicio con dos racores de agua, un puerto combinado de datos/carga y una PRV o vent. Otra tapa preferentemente ciega. Comprobar que la distribución cabe sin interferir con juntas y soporte.
- Superficies de sellado mecanizadas/controladas y chaflán de entrada que no corte tóricas. Compuesto y dimensiones finales se seleccionan con el manual de juntas y mediciones.
- Soportes de óptica, cubeta, motor y batería desmontables e imprimibles. La cruz conserva sus ejes ópticos aunque se reorganice dentro del tubo.

No se ha fijado aún espesor, diámetro/sección de junta, tamaño de tirantes/tornillos, apriete ni posición de puertos. El método de retención aceptado utiliza cuatro tirantes exteriores. Es el siguiente plano que debe resolverse; los STL de tres cajas del M1 anterior no sirven para este cierre.

## 6. Válvula y penetraciones

La [PRV de Blue Robotics](https://bluerobotics.com/store/watertight-enclosures/enclosure-tools-supplies/prv-m10-asm/) permite aliviar presión interna, ventilar manualmente y acoplar el adaptador de vacío. Su umbral es aproximadamente **0,8 ± 0,2 bar**, muy superior a los 0,098 bar de diferencia hidrostática a 1 m. **No es un compensador de profundidad.** El caso de presión interior y la retención de tapa deben analizarse por separado. La [guía de instalación](https://bluerobotics.com/learn/pressure-relief-valve-installation-and-usage/) debe acompañar su plano de montaje; no copiar un par de apriete destinado a una tapa comercial rígida sobre plástico impreso sin comprobarlo.

El [vent manual](https://bluerobotics.com/store/watertight-enclosures/enclosure-tools-supplies/vent-asm-r1/) es una alternativa de compra si la PRV no llega, pero **no tiene alivio automático**. No son funciones equivalentes. Las decisiones finales de válvula y retención siguen pendientes.

Para cables, seguir la [selección de WetLink](https://bluerobotics.com/learn/how-to-choose-a-wetlink-penetrator/) y [su instalación](https://bluerobotics.com/learn/wetlink-penetrator-installation-guide/): elegir sello para el cable concreto, no para varios conductores sueltos. Si usamos conector estanco de panel, ese puerto puede resolver por sí solo la penetración eléctrica. Los racores de agua deben estar especificados para manguera y presión/depresión del circuito.

## 7. Verificación necesaria antes de electrónica

La [prueba de vacío de Blue Robotics](https://bluerobotics.com/learn/using-the-vacuum-test-plug/) es una comprobación útil tras montar o intervenir juntas. En nuestro tubo, limitar primero la diferencia a la carga de diseño calculada; el vacío de 34 kPa de algunos protocolos supone una carga mayor que el servicio inicial de 1 m. El vacío no reproduce humedad, envejecimiento ni todos los modos de fallo en agua. No hacer una prueba de sobrepresión con aire para «ver si salta» la PRV.

Secuencia propuesta, complementaria al [protocolo general](../../docs/VALIDACION_Y_CALIBRACION.md):

1. Medir y fotografiar tubo, ranuras, juntas, puertos y retención. Registrar material, versión CAD y parámetros de impresión/mecanizado de cada tapa.
2. Revisar resistencia y carga de prueba antes de fijar una presión de aceptación superior a servicio. Si se adopta un margen, justificarlo en el plano y protocolo; aquí no se declara que 2 m estén aprobados.
3. Comprobar cierre y fugas por vacío controlado, con manómetro adecuado al rango y temperatura estabilizada. Registrar presión y tiempo; corregir efectos térmicos antes de atribuir una caída a fuga.
4. **30 oct: inmersión con lastre, todas las interfaces finales y sin electrónica ni batería**, a profundidad registrada que cubra el servicio inicial. Usar testigos absorbentes y peso antes/después; fotografiar y registrar duración, fuga, deformación y estado de juntas. Una prueba sin electrónica se denomina aquí «en seco» por el contenido, aunque la envolvente se sumerja.
5. Solo instalar electrónica tras aprobar el criterio del protocolo. La inmersión corta del día 30 no prueba por sí sola 72 h: hacer después ensayo prolongado de envolvente, ciclos de apertura/cierre y prueba de autonomía según la duración realmente buscada.

**Riesgo de calendario:** la entrega anterior era 28–30 oct para otra variante; el suministro 150/140 sigue por confirmar. Si llega el 30, no queda margen garantizado para medir, ajustar tapas y ensayar ese mismo día. Necesitamos suministro confirmado anterior o un tramo equivalente disponible localmente; no registrar el ensayo como superado por el mero hecho de que llegue la fecha.
