# Lista de materiales — referencia anterior al recorte de compra

**Archivo de referencia, 30 de octubre de 2026.** Conserva la lista amplia anterior a D50 y su presupuesto energético. No es un inventario de recepción ni el pedido actual. Para comprar prevalece [LISTA_COMPRA.md](LISTA_COMPRA.md); sus retiradas de componentes y la exclusión de profundidad sustituyen los estados anteriores.

# Lista de compra — cuerpo acrílico horizontal

**Actualizada: 30 de octubre de 2026 · D49.** Cuerpo **acrílico transparente en posición horizontal**, tapa acrílica atornillada con junta plana de silicona y varillas laterales para sujetar pesos. Cámara USB hacia delante por la tapa. Se recuperan **Ø150 exterior / Ø140 interior / pared 5 mm y tramo de 330 mm** como última referencia del acrílico, pendiente de verificar encaje horizontal. PVC descartado. Se mantienen sensores D46, retirada del Honeywell D48 y driver aplazado. [Base mecánica vigente](docs/IMPLANTACION_ACRILICO_HORIZONTAL.md).

## Alcance de esta revisión

**Solo los componentes y opciones que hemos tratado con Alex.** La electrónica de potencia queda para después: **no seleccionar ni comprar driver del motor hasta terminar y probar el diseño**. El 30 oct Alex acepta añadir temperatura DS18B20 y conductividad Atlas K1.0. Se registra profundidad como función a incorporar, con sensor candidato aún sin seleccionar. No añadir otros sensores ni módulos por iniciativa del asistente. El protocolo, pinout y funciones previstas del conector no constituyen una compra de esos circuitos.

## Cómo usar esta lista

**Para discutir componentes, usar los números 1–37.** Se conservan los números 1–34; los sensores añadidos son 35–37. Los códigos originales se conservan para las referencias técnicas. El conjunto I01 agrupa los ítems 15–20 y no es una compra adicional.

- **Seleccionado:** opción aceptada; comprobar variantes, dimensiones y condiciones indicadas antes del pedido. No significa que esté comprado ni ensayado.
- **Candidato / catálogo:** enlace para elegir o cotizar; no es una referencia aprobada de compra.
- **Reutilizar / inventariar:** revisar existencias antes de duplicar material.
- **Fabricar:** fuente editable o boceto del proyecto; no comprar la pieza comercial equivalente por defecto. Los bocetos aún no son planos de fabricación.
- **Comprado:** solo se marca cuando Alex lo ha confirmado; actualmente consta la cubeta.

Los enlaces se identifican como **compra**, **fabricante**, **catálogo**, **ficha** o **diseño**. Se conservan precios con su moneda y procedencia; los campos pendientes no se sustituyen por estimaciones. No se realizan pedidos desde esta revisión.

**Enlaces completados el 30 de octubre de 2026.** Se priorizan Superplastic (Lieja), Manutan Bélgica y Farnell Bélgica; se mantienen también proveedores habituales como TinyTronics (Países Bajos) y Mouser. Rubbermagazijn se enlaza mediante su tienda para Bélgica. Un catálogo o un material para fabricar no fija todavía referencia, dimensiones ni cantidad de compra. En los ítems 22 y 37 sigue faltando, respectivamente, una fuente verificable de la bomba exacta y una solución de profundidad elegida.

## 1. Cuerpo y consumibles

| Nº | ID | Cantidad | Componente y enlaces | Estado / qué falta cerrar | Precio de referencia |
|---: |---|---:|---|---|---:|
| 1 | M01 | 1 suministro; cortar tramo de referencia 330 mm | **Tubo acrílico transparente Ø150 exterior / Ø140 interior** · [Amazon diconfa B0DCTW22XJ](https://www.amazon.com.be/-/en/dp/B0DCTW22XJ) | **Acrílico confirmado por Alex en D49.** Pared radial 5 mm. Comprobar variante exacta, suministro y encaje antes de cortar. | **122 EUR comunicados anteriormente por Alex**; precio actual y porte sin verificar |
| 2 | M02 | 1 tapa transparente; otro cierre en M08 | **PMMA colado para tapa atornillada** · [Catálogo belga Superplastic](https://www.superplastic.be/fr/catalogue/?id=plcot&ssfamille=transparent) · [Concepto vigente](docs/IMPLANTACION_ACRILICO_HORIZONTAL.md#2-tapas-y-sellado) | **Tapa acrílica atornillada seleccionada.** Espesor, apoyo, abertura de visión, contorno y patrón de tornillos por diseñar; PMMA colado como material propuesto. Cámara mirando hacia delante. No trasladar Ø200 ni los cuatro tirantes del cuerpo acrílico como cotas de compra. | Pendiente de plano |
| 3 | M03 | 1 junta para tapa transparente + recambio; resto según cierre | **Lámina maciza de silicona para junta plana recortada** · [Catálogo de silicona maciza — Rubbermagazijn BE](https://www.rubbermagazijn.be/rubber-platen/silicone/) · [Diseño de interfaz](docs/IMPLANTACION_ACRILICO_HORIZONTAL.md#2-tapas-y-sellado) | **Solución aceptada: junta plana comprimida y desmontable.** Espesor, dureza y sección por cerrar; solicitar recorte o formato pequeño, no una bobina por defecto. Elegir material macizo («volrubber»), no espuma ni cinta adhesiva. Las tóricas de la versión anterior no son pedido vigente. | Pendiente |
| 4 | M04 | Según diseño del cierre | **Tornillos, tuercas, arandelas y apoyos de tapas** · [Catálogo de ferretería — Manutan Bélgica](https://www.manutan.be/fr/mab/quincaillerie) · [Requisitos mecánicos](docs/IMPLANTACION_ACRILICO_HORIZONTAL.md#2-tapas-y-sellado) | Cantidad/diámetro/material por calcular; consultar inox A4 para las piezas exteriores, sin fijar aún referencia. Retención y reparto de apriete por diseñar; no confiar cargas a rosca directa sobre pared de 5 mm. No se recuperan automáticamente los antiguos cuatro tirantes de cierre. | Pendiente |
| 5 | M05 | Consumibles de taller | **Limpieza y acabados compatibles con PMMA y silicona** · [Paños de microfibra — Manutan Bélgica](https://www.manutan.be/fr/mab/chiffon-microfibre-manutan) · [Guía de limpieza del fabricante PLEXIGLAS](https://www.plexiglas.de/en/service/processing/cleaning-plexiglas) · [Plan de fabricación y ensayo](docs/IMPLANTACION_ACRILICO_HORIZONTAL.md#5-próximo-diseño-y-ensayo) | Inventariar. Paño suave limpio y agua como punto de partida. Adhesivos/limpiadores se elegirán solo cuando se defina una unión que los requiera y su compatibilidad. El enlace del paño no valida ningún producto químico. | Reutilizar / pendiente |
| 6 | M06 | 1 conjunto | **Soporte de cámara frontal y protección óptica local** · [Material candidato: filamento PETG — TinyTronics, NL](https://www.tinytronics.nl/en/3d-printing/filament/1.75mm-filament/petg) · [Implantación](docs/IMPLANTACION_ACRILICO_HORIZONTAL.md#3-cámara-óptica-y-agua) | Fabricación propia tras comprobar medidas; el enlace es material de impresión, no un soporte terminado. Material/color y compatibilidad con impresora por cerrar; protección óptica opaca. Reservar enfoque y paso de USB; mantener la vista libre por la tapa. | Fablab |
| 7 | M07 | Uso de taller | **Corte guiado, acabado y medición** · [Catálogo de calibres — Manutan Bélgica](https://www.manutan.be/fr/mab/pied-a-coulisse) · [Taller de corte y mecanizado — Superplastic, Lieja](https://www.superplastic.be/) · [Verificaciones](docs/IMPLANTACION_ACRILICO_HORIZONTAL.md#5-próximo-diseño-y-ensayo) | Reutilizar herramientas del fablab; catálogo/servicio como respaldo. Comprobar rango del calibre para cuerpo y tapas. Comprobar todos los componentes y cierres antes de cortar o mecanizar acrílico. | Reutilizar |
| 8 | M08 | 1 cierre posterior | **Tapa posterior y soporte de puertos** · [Material candidato: PMMA — Superplastic, Lieja](https://www.superplastic.be/fr/catalogue/?id=plcot&ssfamille=transparent) · [Diseño vigente](docs/IMPLANTACION_ACRILICO_HORIZONTAL.md#2-tapas-y-sellado) | Fabricación propia; el enlace corresponde al material. Solución y material definitivo por dimensionar para el tubo acrílico. Reservar pasos de agua, conector, válvula y sensores. Los manguitos y tapones PVC quedan fuera de compra. | Pendiente |

**Visión:** cuerpo transparente y cámara auxiliar frontal por tapa acrílica. Probar reflejos/enfoque bajo agua y conservar pantallas opacas locales de los módulos espectrales.

## 2. Agua, puertos y ventilación

**Manguera de bomba confirmada:** ID **3,0 mm**, OD **5,0 mm**, pared **1,0 mm**. Su material/referencia exactos siguen pendientes. Esa dimensión no obliga a usar el mismo material blando en el paso de tapa.

| Nº | ID | Cantidad | Componente y enlaces | Estado / qué falta cerrar | Precio de referencia |
|---: |---|---:|---|---|---:|
| 9 | H01 | 2 | **Pasos hidráulicos de tapa: WetLink JPT** · [Fabricante: Blue Robotics](https://bluerobotics.com/store/cables-connectors/penetrators/wetlink-penetrator-jpt/) · [Evaluación local](docs/ANTIFOULING_Y_PASAMUROS.md#pasamuros-candidato) | **Candidato profesional.** BR-107163-155, M10 / 5.5 HC, rango OD 4,7–5,3 mm. Tubo continuo; validar material, compresión, paso de agua y montaje en tapa. No sustituir por WetLink estándar. | **13 USD/u; 26 USD por dos**, catálogo |
| 10 | H02 | Según trazado + recambio de tramo bombeado | **Mangueras, uniones y recambio de bomba** · [Catálogo de tubo de silicona — Superplastic, Lieja](https://www.superplastic.be/fr/catalogue/?id=a0u70llgc6&ssfamille=silicone) · [Guía de selección: Saint-Gobain](https://fluidtransfer.saint-gobain.com/sites/hps-mac3-lifesciences-fluid-transfer/files/2022-10/food-and-beverage-tubing-selection-guide-saint-gobain.pdf?cache=jX9abyQG) · [Requisitos hidráulicos](ESPECIFICACION.md#5-renovación-de-agua-y-blancos) | **Referencia por elegir.** Consultar ID 3 / OD 5 mm; no se confirma esa variante ni su aptitud peristáltica mediante el catálogo. La guía no acredita compatibilidad con MS11HS5L410C-01. Conservar recambio autorizado para su cabeza. Uniones por elegir tras medir boquillas de cuarzo, radios de curvatura y resistencia a succión. | Pendiente |
| 11 | H03 | 1 toma + 1 descarga + fijaciones | **Toma con rejilla gruesa, guías y separación de descarga** · [Material candidato para piezas impresas — TinyTronics, NL](https://www.tinytronics.nl/en/3d-printing/filament/1.75mm-filament/petg) · [Diseño del recorrido](docs/IMPLANTACION_ACRILICO_HORIZONTAL.md#3-cámara-óptica-y-agua) | **Fabricar / ajustar.** Catálogo de material, no toma terminada. Sin filtro fino; tamaño de abertura y material por definir. El estudio de cobre y limpieza automática queda aplazado, por indicación de Alex. | Fablab / pendiente |
| 12 | H04 | 1, elegir una opción | **Válvula de la cavidad seca** · [Vent manual BR-100783](https://bluerobotics.com/store/watertight-enclosures/enclosure-tools-supplies/vent-asm-r1/) **o** [PRV automática BR-100804](https://bluerobotics.com/store/watertight-enclosures/enclosure-tools-supplies/prv-m10-asm/) | **Por decidir.** Manual: igualación y prueba de vacío. PRV: añade alivio automático. No son equivalentes. Verificar interfaz con tapa y disponibilidad. | Manual **12 USD** / PRV **32 USD**, catálogo |
| 13 | H05 | 1 envase pequeño si falta | **Lubricante de juntas** · [Molykote 111 — Blue Robotics](https://bluerobotics.com/store/watertight-enclosures/enclosure-tools-supplies/molykote/) | Elegir formato pequeño y comprobar compatibilidad con compuesto de junta y PMMA. Usar existencias compatibles si las hay. | Referencia previa **4–32 USD**, según formato |
| 14 | H06 | Solo lo que no venga incluido | **Juntas y tuercas de cada interfaz; tapones de ensayo** · [Contenido de JPT](https://bluerobotics.com/store/cables-connectors/penetrators/wetlink-penetrator-jpt/) · [Interfaces por diseñar](docs/IMPLANTACION_ACRILICO_HORIZONTAL.md#2-tapas-y-sellado) | Descontar lo incluido en H01/H04/I01. Repuestos y tapones solo después de comprobar el plano. | Pendiente |

**Orden de agua:** exterior → toma → cubeta → bomba → descarga. La muestra se mide antes de pasar por la bomba. Cubeta y tubos permanecen llenos; renovar varios volúmenes antes de medir. Blanco previo al despliegue en memoria; sin caudalímetro ni depósito de blanco.

**Puertos:** se mantienen dos pasos de agua, un conector eléctrico y una válvula. Propuesta: extremo opuesto a la cámara; posiciones y cierre por resolver en [la revisión horizontal](docs/IMPLANTACION_ACRILICO_HORIZONTAL.md). La distribución de puertos del antiguo montaje vertical queda como antecedente.

## 3. Un conector exterior para carga y datos

**Aceptado por Alex:** Bulgin Buccaneer 400 de **ocho contactos**, con tapón estanco y previsión de futura boya. [Arquitectura de puerto y funciones reservadas](electronica/PUERTO_SERVICIO_Y_BOYA.md). Pinout, cable y esquemático aún por cerrar.

| Nº | ID | Cantidad | Pieza / referencia y enlaces | Estado / observación |
|---: |---|---:|---|---|
| — | I01 | 1 conjunto, desglosado debajo | **Puerto combinado completo** · [Ficha de familia Bulgin](https://www.bulgin.com/products/pub/media/bulgin/data/400_power.pdf) | No contar I01 como compra adicional a I01a–I01f. Familia de 8 contactos aceptada; completar variantes antes de pedir. |
| 15 | I01a | 1 | **Panel hembra PX0412/08S** · [Compra: Mouser](https://www.mouser.com/ProductDetail/Bulgin/PX0412-08S?qs=xh6E4zEJdPkMSk3FcmL2ig%3D%3D) · [Ficha Bulgin](https://www.bulgin.com/pdf/pdf.php?sku=PX0412%2F08S) | Cuerpo sin contactos. Comprobar junta de panel, rosca, espesor de tapa y acceso de tuerca. Precio del conjunto por cotizar. |
| 16 | I01b | 1 | **Contraparte macho PX0410/08P**, sufijo según cable · [Ejemplo 6065 y ficha del fabricante](https://www.bulgin.com/us/products/flex-cable-connector-px0410-series-8-contact-plug-6-0mm-6-5mm-cable.html) · [Catálogo Farnell Bélgica](https://be.farnell.com/c/connectors/circular-connectors-components/circular-industrial-connectors?brand=bulgin-limited&product-range=buccaneer-400-series) | **No fijar aún /6065:** esa opción admite cable OD 6,0–6,5 mm. Elegir sufijo después del cable. Cuerpo sin contactos. |
| 17 | I01c | 1 | **Tapón de panel PX0480** · [Ficha Bulgin](https://www.bulgin.com/pdf/pdf.php?sku=PX0480) · [Compra: Farnell](https://es.farnell.com/bulgin/px0480/sealing-cap-chassis/dp/3841285) | Mantiene el sellado del puerto sin cable. Enlace comercial de ES; confirmar oferta para Bélgica. Referencia observada: **4,20 EUR sin IVA**, no cotización BE. |
| 18 | I01d | 1 paquete de 10; usar 8 | **Contactos hembra para soldar SA3347/1** · [Compra: Farnell Bélgica](https://be.farnell.com/en-BE/bulgin/sa3347-1/solder-socket-22-26awg-pk10/dp/3841390) · [Compatibilidad Bulgin](https://www.bulgin.com/products/pub/media/bulgin/data/400_power.pdf) | Para el cuerpo de panel. Referencia observada en catálogo: **21,82 EUR sin IVA por paquete de 10**, no por contacto. |
| 19 | I01e | 1 paquete de 10; usar 8 | **Contactos macho para soldar SA3348/1** · [Ficha Bulgin](https://www.bulgin.com/pdf/pdf.php?sku=SA3348%2F1) · [Compra: Farnell Francia](https://fr.farnell.com/bulgin/sa3348-1/broche-a-souder-22-26awg/dp/3841406) | Para la contraparte de cable. Confirmar precio regional y paquete; soldar con cable dentro del rango de ficha. |
| 20 | I01f | 1 cable de servicio | **Cable de servicio para carga y datos** · [Catálogo multiconductor — Farnell Bélgica](https://be.farnell.com/fr-BE/c/cables-fils-cables-assembles/cables-multiconducteurs) · [Catálogo multipar — Farnell Bélgica](https://be.farnell.com/fr-BE/c/cables-fils-cables-assembles/cables-multipaires) · [Criterios del puerto](electronica/PUERTO_SERVICIO_Y_BOYA.md#funciones-reservadas-sin-números-de-pin-asignados) | Catálogos, cable aún no seleccionado. Definir ocho conductores, longitud, sección, par de datos y diámetro compatible con I01b al cerrar el diseño. Comprobar rango 22–26 AWG de los contactos y corriente admisible del conjunto; no elegir cualquier cable de ocho hilos. Preparar ramales externos hacia cargador y adaptador de datos. |

Reserva funcional: **2 contactos de carga + 2 de alimentación externa regulada + 3 de RS-485/referencia + 1 de reserva**. No asignar números ni unir retornos hasta revisar BMS y aislamiento. Datos para PC mediante adaptador; futura boya mediante registrador compatible. Un panel solar necesitará controlador y carga compatibles con el pack. Conexión/desconexión en seco; sellado con contraparte o tapón montados según fabricante.

## 4. Componentes del instrumento ya tratados

| Nº | ID | Cantidad | Componente y enlaces | Estado / observación |
|---: |---|---:|---|---|
| 21 | C01 | 1 kit | **Batería CITYORK, 24 V / 3 Ah anunciados, BMS y cargador** · [Amazon B0FQ583Q2J](https://www.amazon.com.be/-/en/dp/B0FQ583Q2J) | **Seleccionada. 43,99 EUR**, observados previamente el 21 oct. No añadir otro cargador/BMS. Datos reales por comprobar al recibirla. |
| 22 | C03 | 1 | **Bomba MS11HS5L410C-01** · [Datos y mediciones pendientes](docs/IMPLANTACION_ACRILICO_HORIZONTAL.md#5-próximo-diseño-y-ensayo) | Referencia fijada por Alex; **sin enlace de proveedor/ficha verificable**. 24 V / 20 W comunicados por Alex; tubo de bomba 3 × 5 mm. No sustituir por Denash. |
| 23 | E14 | 1 | **Cámara USB auxiliar interior** · [Fruugo 478082530 / 972533366](https://www.fruugo.be/industriele-4k-usb-webcam-pc-laptops-video-8mp-autofocus-usb-camera-imx179-sensor-otg-uvc-plug-play/p-478082530-972533366?language=nl) | Seleccionada por Alex, adicional a la cámara espectral. Dimensiones, modos efectivos y precio pendientes de comprobar. |
| 24 | E15 | 1 | **Cubeta de flujo NEXACULE de cuarzo** · [Producto, variante 46090230005978](https://www.nexacule.com/collections/flow-cuvettes/products/quartz-flow-cuvette-brownloo-quartz-flow-cells-two-ends-open-nexacule?variant=46090230005978) | **Comprada.** Medir cuerpo y boquillas; no pedir otra. |

### Material de los instrumentos anteriores: inventariar y reutilizar

No son nuevas compras aprobadas:

25. **Raspberry Pi 4 y almacenamiento:** [catálogo de placas, incluye Pi 4 — TinyTronics, NL](https://www.tinytronics.nl/nl/development-boards/single-board-computers) · [referencia del fabricante](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/). Reutilizar placa y almacenamiento; capacidad/modelo de memoria por inventariar, sin sustituir por Pi 5.
26. **ESP32:** [catálogo de placas — TinyTronics, NL](https://www.tinytronics.nl/nl/development-boards/microcontroller-boards) · [documentación del fabricante](https://www.espressif.com/en/products/devkits/esp32-devkitc). Conservar la placa disponible y confirmar cuál es; el catálogo no selecciona otra variante.
27. **OV9281, lente, red, rendija y halógena del MonoSpectro:** [referencia OV9281 — Arducam](https://docs.arducam.com/cameras-for-raspberry-pi/migrated/ov9281-1mp-global-shutter-raspberrypi-camera/) · [catálogo de redes de transmisión — Edmund Optics](https://www.edmundoptics.com/c/transmissive-diffraction-gratings/1416/) · [requisitos ópticos vigentes](docs/ANALISIS_ARQUITECTURA.md). Referencias de consulta, no sustitutos de las piezas existentes. Conservar gran angular confirmado por Alex, red junto a lente, 36°, rendija 0,5 mm y referencia de 60 mm. Inventariar referencias exactas de lente, red y halógena antes de enlazar repuestos; la rendija se fabrica.
28. **AS7265x de 18 canales:** [referencia de placa completa SEN-15050 — Mouser Bélgica](https://www.mouser.be/ProductDetail/SparkFun/SEN-15050?qs=sGAEpiMZZMs50KUSuyRkplZw6Dwuduoydny2FcCw00z4BfpO%2Fco52w%3D%3D) · [documentación SparkFun](https://learn.sparkfun.com/tutorials/spectral-triad-as7265x-hookup-guide). Comprobar el sensor disponible. La ficha comercial de SEN-15050 se conserva para identificación: Mouser la marca obsoleta en su catálogo europeo, no se presenta como compra disponible. No sustituir la placa de tres sensores por un único chip de la familia.
29. **Cinco LED en total, incluido 430 nm:** [catálogo de LED violetas — Mouser](https://www.mouser.com/en/c/optoelectronics/led-lighting/leds-light-emitting-diodes/?illumination+color=Violet) · [especificación acordada](ESPECIFICACION.md). Catálogo para estudiar el emisor de 430 nm, no una referencia seleccionada: verificar longitud de onda y tolerancia en ficha. Modelos y cuatro longitudes de onda adicionales aún sin fijar; no convertir esa previsión en pedido de cinco LED idénticos. Los 4 V / 100 mA del balance energético son una hipótesis, no especificaciones de compra.

**Potencia aplazada:** los DC/DC se dimensionarán después con los datos reales. El driver del motor queda fuera de la lista de compra hasta terminar y probar el diseño, según la indicación expresa de Alex. No se selecciona ahora ningún modelo.

## 5. Soportes, anclaje y ensayo

| Nº | ID | Cantidad | Elemento y enlaces | Estado / acción |
|---: |---|---:|---|---|
| 30 | S01 | 1 conjunto modular | **Bastidor, bandejas y soportes impresos** · [Material candidato: filamento PETG — TinyTronics, NL](https://www.tinytronics.nl/en/3d-printing/filament/1.75mm-filament/petg) · [Memoria de diseño](docs/IMPLANTACION_ACRILICO_HORIZONTAL.md) | Fabricación propia tras cerrar material, medidas y verificar encaje en ID140. El enlace es material, no un bastidor terminado. Los STL antiguos de tres cajas no corresponden al tubo vigente. Fijación independiente de batería/bomba. |
| 31 | S02 | 1 conjunto; cantidades por dimensionar | **Abrazaderas exteriores y varillas laterales para sujetar lastre** · [Catálogo de varillas roscadas A4 — tienda e-Altamira BE](https://e-altamira.be/fr_BE/c/Tiges-filetees/93/3) · [Material candidato para collares impresos — TinyTronics, NL](https://www.tinytronics.nl/en/3d-printing/filament/1.75mm-filament/petg) · [Diseño mecánico vigente](docs/IMPLANTACION_ACRILICO_HORIZONTAL.md#4-varillas-y-lastre) | Alex confirma el 30 oct pesos sujetos a las varillas laterales. Propuesta: varillas sostenidas por collares que distribuyan carga; A4 como candidato para varillas, sin diámetro aprobado. Número, sección, longitud, material y retención por dimensionar; no son automáticamente los cuatro tirantes del cierre acrílico anterior. Validar resistencia de collares antes de cargar lastre. |
| 32 | S03 | 1 conjunto | **Argollas, sujeciones de pesos y lastre** · [Catálogo de argollas inox — Manutan Bélgica](https://www.manutan.be/fr/mab/anneau-de-levage-inox) · [Revisión de montaje](docs/IMPLANTACION_ACRILICO_HORIZONTAL.md#4-varillas-y-lastre) · [Protocolo de ensayo](docs/VALIDACION_Y_CALIBRACION.md) | Catálogo para argollas; lastre/sujeciones por inventariar, sin masa o referencia de compra elegida. Lastre sujeto a las varillas laterales exteriores, sin perforar pared de presión. Posición y masas por dimensionar para mantener el tubo horizontal y cámara libre. Comprobar sujeciones y camino de recuperación; la capacidad indicada para una argolla no acredita la del conjunto. |
| 33 | S04 | 1 juego | **Desecante, testigos absorbentes y registro fotográfico** · [Sobres de gel de sílice — Manutan Bélgica](https://www.manutan.be/fr/mab/sachet-de-gel-de-silice-lot-de-100-matfer) · [Protocolo y criterios](docs/VALIDACION_Y_CALIBRACION.md) | Inventariar/cotizar consumibles de laboratorio; el enlace es un lote de 100, no cantidad de compra aprobada. Usar papel absorbente limpio del laboratorio para los testigos y cámara disponible para fotos. Desecante como control de condensación, no sustituto del cierre estanco. |
| 34 | S05 | 1 equipo de taller, si falta | **Manómetro, bomba y adaptador de vacío** · [Kit Blue Robotics BR-100297](https://bluerobotics.com/store/watertight-enclosures/enclosure-tools-supplies/vacuum-pump-kit-r2-rp/) **o** [solo Vacuum Plug](https://bluerobotics.com/store/watertight-enclosures/enclosure-tools-supplies/vacuum-plug/) · [Guía](https://bluerobotics.com/learn/using-the-vacuum-test-plug/) | **Opcional.** Reutilizar equipo de fablab. Kit **98 USD**, adaptador solo **8 USD**, precios previos de catálogo. El kit incluye adaptador: no duplicar. Limitar presión al diseño. |

**Ensayo duro: 30 de octubre, con lastre y todas las interfaces finales, sin electrónica ni batería.** Registrar fotos, montaje, profundidad, duración y resultado. No se considera probado el conjunto por completar la lista. [Plan vigente de cierre y ensayo](docs/IMPLANTACION_ACRILICO_HORIZONTAL.md#5-próximo-diseño-y-ensayo).

### 5.1. Sensores añadidos el 30 de octubre — D46/D47

| Nº | ID | Cantidad | Componente y enlaces | Estado / observación |
|---:|---|---:|---|---|
| 35 | A01 | 1 | **DS18B20 encapsulado con cable de 4 m** · [Referencia ARES/TinyTronics](https://www.tinytronics.nl/en/sensors/temperature/ds18b20-to-92-thermometer-temperature-sensor-with-cable-waterproof-high-temperature-4m) · [Chip y especificaciones ADI](https://www.analog.com/en/products/DS18B20.html) | **Incorporación aceptada. Inventariar antes de comprar:** ARES_2025, Export fila 50, incluye 20 unidades, sin confirmar recepción. Comprobar temperatura contra referencia y compatibilidad del encapsulado/cable con agua marina. Objetivo: sin intervención durante despliegue; duración por demostrar. |
| 36 | A02 | 1 kit | **Atlas Scientific Conductivity K1.0 Kit** · [Referencia ARES/proveedor](https://sensorsandprobes.com/products/conductivity-k-1-0-kit) · [Fabricante](https://atlas-scientific.com/probes/conductivity-probe-k-1-0/) | **Incorporación aceptada. Inventariar:** ARES_2025, Export fila 119, incluye dos kits, sin confirmar recepción. Conservar circuito y aislamiento del kit; temperatura del agua para compensación. Guardar conductividad original, compensada y salinidad derivada con método/configuración. No duplicar con otro kit Mini. Comprobar deriva y ensuciamiento al recuperar. |
| 37 | A03 | Pendiente | **Medición de profundidad, solución por decidir** · [Especificación](ESPECIFICACION.md#2-qué-mide) | **Honeywell retirado por Alex el 30 oct; no comprar.** Sin sensor elegido. Cable graduado conservado como alternativa manual aún sin aprobar como sustituto. |

**A03 permanece abierto.** El Honeywell industrial con conexión roscada se retira de las opciones de compra por indicación de Alex. Si se retoma un sensor, definir montaje, rango útil, referencia de presión y compatibilidad con inmersión prolongada antes de seleccionarlo.

El **cable graduado queda como alternativa planteada por Alex**, sin convertirlo todavía en sustituto aprobado del sensor. Permite registrar profundidad nominal y método manual, distinguiéndolo de profundidad medida. Revisar inclinación con corriente y cambios del nivel del agua según el amarre. Mantener números de serie, coeficientes y comprobaciones antes/después del despliegue. El presupuesto energético no se recalcula en esta revisión.

## 6. Presupuesto parcial y pendientes de compra

| Grupo | Importe / tratamiento |
|---|---:|
| Tubo acrílico M01, precio comunicado anteriormente por Alex | **122,00 EUR**; variante, desglose y porte por verificar |
| Batería con BMS y cargador C01, precio previo observado | **43,99 EUR** |
| **Subtotal de esas dos referencias históricas** | **165,99 EUR**; sin portes adicionales ni cotización actual |
| Dos JPT H01, si se valida y selecciona el candidato | **26 USD**, catálogo; no sumados al subtotal EUR |
| Válvula H04, elegir una | **12 USD manual / 32 USD PRV**, catálogo |
| Bulgin I01a–I01f y medios de montaje | **Conjunto completo por cotizar**; incluir los dos paquetes de contactos y cable |
| Material/tapas, juntas, retención, bomba si falta, cámara auxiliar y consumibles tratados | **Pendiente** |

No es el total del instrumento. No convertir USD ni mezclar precios sin IVA con importes cuyo desglose no se ha verificado. Los precios comerciales son referencias históricas, no disponibilidad/plazo garantizados. Se retira el tubo PVC de 13,48 EUR del subtotal; los 122 EUR del acrílico vuelven como precio comunicado por Alex, sin nueva consulta comercial. [Historial de alternativas](docs/ANTECEDENTES_LISTA_COMPRA.md).

### Lo siguiente que debe cerrarse

1. Comprobar variante del tubo acrílico Ø150/140 y tramo de referencia 330 mm; medir bomba, cubeta, batería y cámara para el encaje horizontal.
2. Dimensionar apoyo y tapa acrílica atornillada, junta plana de silicona y abrazaderas/argollas ya aceptadas; resolver el cierre del otro extremo, elegir válvula y revisar interfaces Bulgin/JPT antes de perforar.
3. Elegir cable de servicio y sufijo de I01b; cotejar y cotizar todo el conjunto Bulgin, no solo el cuerpo de panel.
4. Registrar medidas y etiquetas de los componentes para terminar y probar el diseño. La elección del driver y la electrónica de potencia se tratará después; no forma parte de este pedido.
5. Reutilizar óptica/electrónica disponible, completar solo faltantes y ejecutar el ensayo de envolvente del 30 oct.

## 7. Presupuesto energético conservado

**Conservado sin recalcular por indicación de Alex.** El presupuesto previo no incorpora todavía la cámara auxiliar USB E14; no se presenta como cálculo completo actualizado con esa cámara.

Datos del anuncio C01: Li-ion, **24 V / 3 Ah / 72 Wh declarados**, BMS contra sobretensión, descarga profunda, cortocircuito y temperatura; uso indicado **1–3 A**; dimensiones **70 × 37,5 × 56 mm**, peso neto descrito 278 g. Son datos del vendedor, pendientes de recepción y ensayo. Otra tabla indica 157 g: registrar el peso real. No hay en el texto consultado una especificación suficiente de corriente continua/pico del BMS, número de celdas, tensión máxima/mínima ni salida del cargador.

Antes de comprar los DC/DC y el driver: fotografiar etiquetas de pack/cargador, comprobar polaridad DC5521, tensión a plena carga y límites documentados. Ensayar arranque de Pi, bomba y fuentes con el pack. El conector DC5521 suministrado queda **dentro de la envolvente seca**; no sirve como conector exterior sumergible. Usar el cargador del kit por el puerto de carga previsto; no conectar una fuente genérica de 24 V como cargador. Adaptar después la conexión al único puerto exterior de carga/datos.

Presupuesto acordado para **un ciclo cada 15 min**, todavía sin mediciones eléctricas:

| Carga | Hipótesis por ciclo | Wh en 24 h / 96 ciclos | Wh en 72 h / 288 ciclos |
|---|---|---:|---:|
| Bomba | 20 W × 30 s | 16,00 | 48,00 |
| Halógena | 10 W × 5 s | 1,33 | 4,00 |
| Cinco LED en total | Cada uno 4 V × 100 mA × 5 s | 0,27 | 0,80 |
| Pi + cámara | 5 W × 90 s; alimentación cortada entre ciclos tras apagado ordenado | 12,00 | 36,00 |
| **Subtotal** | **0,3083 Wh/ciclo; media 1,233 W** | **29,60** | **88,80** |

Los cinco LED incluyen el de 430 nm; longitudes de onda y secuencia de los otros cuatro pendientes. Estos tiempos son hipótesis energéticas, no estabilizaciones ópticas demostradas.

Con los **72 Wh declarados**, el cociente ideal es **58,4 h**. Aplicando una sola vez 20 % de reserva y rendimiento supuesto de conversión de 85 %: `72 × 0,80 × 0,85 = 48,96 Wh`, equivalentes a **39,7 h** con esas cuatro cargas. **Faltan** supervisor/RTC, AS7265x, reposos de convertidores/driver, sensores y posibles diferencias de consumo: la autonomía real será menor. Si la etiqueta nominal resulta ser 22,2 V × 3 Ah = 66,6 Wh, el mismo cálculo baja a **36,7 h**. Medir capacidad útil y energía por ciclo antes de prometer duración.

La batería pequeña es la elección para el primer prototipo por precio y plazo. **No demuestra el objetivo original de 72 h**; ese requisito queda como ampliación pendiente para esta configuración. El ensayo de campo de varias horas sigue siendo el primer objetivo operativo.

## 8. Ampliaciones y componentes descartados

**Fuera del pedido actual:** tubo, manguitos, tapones y adhesivos de PVC, panel solar, controlador de boya, registrador y transmisor. La interfaz queda prevista en [el diseño del puerto](electronica/PUERTO_SERVICIO_Y_BOYA.md), pero no hay modelos elegidos para esos equipos.

**Cobre y limpieza de toma: aplazados por Alex.** [Análisis conservado](docs/ANTIFOULING_Y_PASAMUROS.md); no se añade cobre, biocida ni mecanismo de limpieza al pedido de esta revisión.

**PVC descartado en D49; enlaces históricos, fuera del pedido:**

- [Tubo PVC d160 × 4 mm, 1 m — WitWay](https://witway.be/pvc-buis-glad-160-x-4-0mm-sn4-lengte-1-meter/).
- [Manguito d160 — WitWay](https://witway.be/pvc-lijmmof-160mm/).
- [Extremo d160 con tapa roscada — WitWay](https://witway.be/pvc-eindstuk-schroefdeksel-160-mm-prod/).

[Historial completo de listas y alternativas, con precios antiguos](docs/ANTECEDENTES_LISTA_COMPRA.md).
