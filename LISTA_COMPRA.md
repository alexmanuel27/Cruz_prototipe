# Lista de compra — faltantes del prototipo

**30 de octubre de 2026 · revisión D52; conector confirmado en D51.** Esta es la lista de lo que falta comprar. La relación amplia anterior se conserva como [referencia de materiales](LISTA_MATERIALES.md). Se conservan los números originales para discutirlos; los huecos corresponden a elementos retirados del pedido.

Base: tubo acrílico transparente horizontal, cámara hacia delante por la tapa, junta plana de silicona y varillas laterales M8. Alex autoriza ahora cerrar la electrónica e incorporarla al mismo pedido. Se reutilizan A4988 y tres DC/DC de 5 A disponibles; no comprar otros. Selección técnica y comprobaciones en [Electronics V1](electronica/DISENO_ELECTRICO_V1.md).

## 1. Compras previstas

| Nº anterior | Cantidad | Comprar | Enlace y observación |
|---:|---:|---|---|
| 1 | 1 suministro | **Tubo acrílico Ø150 exterior / Ø140 interior, pared 5 mm** | [Amazon diconfa B0DCTW22XJ](https://www.amazon.com.be/-/en/dp/B0DCTW22XJ). Cortar tramo de referencia de **330 mm**, tras comprobar el encaje. **122 EUR comunicados por Alex**, sin nueva cotización ni porte confirmado. Verificar variante antes de pedir. |
| 2 | 1 retal, dimensiones por plano | **Plancha de acrílico para las tapas** | Compra local/fablab, **sin enlace por indicación de Alex**. Espesor y tamaño del retal después de dimensionar apoyos, visión y perforaciones. |
| 3 | Según plano de cierres | **Junta plana maciza de silicona, a medida** | Propuesta: [Greendale Rubber, Países Bajos — corte y troquelado a medida](https://www.greendalerubber.nl/en/punching). Declara corte de silicona según dibujo y suministro de piezas sueltas. Pedir presupuesto al disponer del plano; no se ha identificado si es la empresa que mencionó el tutor. Se conserva como alternativa ya tratada la [lámina maciza Rubbermagazijn BE](https://www.rubbermagazijn.be/rubber-platen/silicone/) para recortar. Espesor, dureza y compresión por cerrar. |
| 4, incluye antiguo 31 | 4 tramos M8; 8 tuercas; 8 arandelas | **Varillas roscadas M8, tuercas ciegas abombadas y arandelas, todo inox A4** | [Varilla M8 × 1 m — Vis-Express BE, 8900000818](https://www.vis-express.be/tige-filetee-1-metre-inox-a4-din-975/21861-808153-tige-filetee-m8-longueur-1-metre-inox-a4-3663072175693.html) · [Tuerca ciega M8 DIN 1587, 8728000818](https://www.vis-express.be/ecrou-borgne-inox-a4-din-1587/21060-ecrou-borgne-m8-inox-a4-3663072201569.html) · [Arandela ancha M8 × 22 × 1,5 mm, 8934000818](https://www.vis-express.be/rondelle-plate-serie-l-large-inox-a4-nfe-25513/22221-rondelle-plate-m8x22x15-l-inox-a4-3663072175969.html). Ocho tuercas se interpretan como dos por varilla. Provisión: dos barras de 1 m si los cuatro tramos finales caben a menos de 500 mm incluyendo la pérdida de corte; confirmar longitud antes de pedir/cortar. Se necesitan ocho tuercas y ocho arandelas; comparar formatos de diez para evitar pagar ocho unidades sueltas más caras. |
| 9 | 2 | **Pasos hidráulicos WetLink JPT, M10 / 5.5 HC** | [Blue Robotics — JPT, BR-107163-155](https://bluerobotics.com/store/cables-connectors/penetrators/wetlink-penetrator-jpt/). Candidato conservado: OD de tubo 4,7–5,3 mm, para el tubo de 5 mm exterior. Comprobar material y compresión sin obstruir el agua. **No añadir otro juego de juntas/tuercas del antiguo 14: viene con estos pasos.** Referencia previa: **13 USD/u**, sin nueva cotización. |
| 15, sustituye antiguos 15–20 | 1 conjunto | **Conector único de carga/datos: Switchcraft EN3, ocho contactos ya montados, macho + hembra + tapa** | **Conjunto confirmado por Alex (D51)**, desglosado en la sección siguiente. No comprar contactos sueltos ni el conjunto Bulgin anterior. Conector de panel macho y contraparte de cable hembra. Comprobar montaje en la tapa antes del pedido. |
| 21 | 1 kit | **Batería CITYORK 24 V / 3 Ah anunciados, con BMS y cargador** | [Amazon B0FQ583Q2J](https://www.amazon.com.be/-/en/dp/B0FQ583Q2J). Opción conservada por Alex. **43,99 EUR observados anteriormente**, no precio actualizado. Comprobar etiquetas y tensiones reales al recibir. No añadir otro BMS ni cargador. |
| 27 | 1 paquete de 2 láminas | **Red de difracción de transmisión, 1000 líneas/mm** | [Edmund Optics **stock #40-267**](https://www.edmundoptics.eu/p/25400-linesinch-6quot-x-12quot-sheets-2pack/4621/). Dos láminas de **152,4 × 304,8 mm**, 25 400 líneas/pulgada = 1000 líneas/mm, ángulo de dispersión indicado 36°. Referencia enlazada en el MonoSpectro, para recortar y colocar junto a la lente. **19,75 EUR sin IVA**, consultado el 30 oct. El número 4621 de la URL es el identificador de página, no el stock comercial. |

La ficha de la red declara 400–700 nm; el alcance acordado del instrumento sigue siendo 420–780 nm. La reutilización de esta referencia no convierte el tramo 700–780 nm en una garantía del proveedor: se comprobará con la calibración del conjunto, como en el MonoSpectro.

## 2. Una sola propuesta de conector completo — ítem 15

**Switchcraft EN3 con terminales de soldadura integrados, confirmado por Alex el 30 de octubre (D51).** Cada mitad se suministra con sus ocho contactos: no hay que comprar ni insertar pines. Hay que soldar los cables y montar el cierre del cable según las instrucciones. Son tres referencias del mismo conjunto, disponibles en el catálogo de DigiKey Bélgica:

| Pieza | Cantidad | Referencia y compra | Precio sin IVA, 30 oct |
|---|---:|---|---:|
| Macho de panel, ocho contactos | 1 | [EN3P8MX — DigiKey](https://www.digikey.be/en/products/detail/switchcraft-inc/EN3P8MX/2080473) | 23,03 EUR |
| Hembra de cable, ocho contactos | 1 | [EN3C8FX — DigiKey SC259-ND](https://www.digikey.be/en/products/detail/switchcraft-inc/EN3C8FX/2080464) | 30,35 EUR |
| Tapa estanca con anillo de bloqueo, para panel | 1 | [EN3IPCAPX — DigiKey SC2851-ND](https://www.digikey.be/en/products/detail/switchcraft-inc/EN3IPCAPX/4248698) | 5,28 EUR |
| **Total de las tres piezas** | | | **58,66 EUR sin IVA; 70,98 EUR con 21 %**, sin portes |

- [Fabricante: EN3P8MX](https://www.switchcraft.com/en3-harsh-environment-panel-mount-8-contact-male/en3p8mx/) y [tapa EN3IPCAPX](https://www.switchcraft.com/en3-series-ip68-rated-panel-mount-or-cable-to-cable-connector-cap-with-lock-ring/en3ipcapx/). El fabricante identifica EN3C8FX como contraparte del EN3P8MX.
- Ocho contactos, corriente nominal de ficha **6,5 A** y cierre de bayoneta. Verificar corriente del conjunto con sección, temperatura y funciones reales; conservar reserva de carga, alimentación externa y RS-485.
- La variante de cable enlazada admite **OD 4,06–6,73 mm**. El cable se preparará con material disponible que cumpla ese rango y las secciones de ficha; no se añade otra compra de cable por defecto.
- Sellado declarado IP68 **con la contraparte o tapa montada**. No convertirlo en una profundidad/duración certificada del instrumento: validar el montaje para el objetivo actual de 1 m y su tiempo de despliegue. Conectar/desconectar en seco.
- Esta solución invierte el género respecto al Bulgin anterior: **macho en equipo y hembra en cable**. Evitar contactos de alimentación expuestos energizados al estar desenchufado; cerrar el pinout y la gestión eléctrica antes de cablear.
- Confirmar dimensiones, espesor admisible y retención en la tapa antes de perforar. No usar las cotas del Bulgin anterior.

## 3. Ítems consultados: recomendación pendiente de Alex

### 12. Tapón de ventilación manual

**Recomendación: conservar uno manual**, [Blue Robotics BR-100783](https://bluerobotics.com/store/watertight-enclosures/enclosure-tools-supplies/vent-asm-r1/), **12 USD** consultados el 30 oct. Incluye pasamuros, tapón, tuerca y juntas. Permite igualar la presión interior antes de abrir y conectar un ensayo de vacío si se dispone del equipo de taller. No añade resistencia a presión exterior y no es indispensable para que una junta plana selle. Tampoco libera automáticamente sobrepresión: no equivale a una PRV. Se retira la PRV automática de las opciones de este pedido; la manual queda por confirmar con Alex.

Referencia: [guía Blue Robotics sobre ventilación de cavidades secas](https://bluerobotics.com/learn/watertight-enclosure-wte-assembly-new/). Es una recomendación de mantenimiento aplicada a nuestro diseño; la tapa plana atornillada no comprime el aire del mismo modo que su cierre de inserción.

### 13. Lubricante: no sustituir automáticamente por vaselina común

**Compra condicionada a que no haya lubricante compatible en el taller.** La compatibilidad depende del elastómero: vaselina de petróleo no es un sustituto universal de grasa para juntas. [Sea-Bird desaconseja Vaseline en sus juntas sumergibles](https://www.seabird.com/faqs/faq000084); no trasladar esa advertencia a todos los cauchos como si fueran iguales.

Para las juntas originales de los puertos Blue Robotics, conservar como referencia [Molykote 111](https://bluerobotics.com/store/watertight-enclosures/enclosure-tools-supplies/molykote/) en el formato mínimo, si lo necesitan y no hay equivalente compatible disponible. La ficha del [vent manual](https://bluerobotics.com/store/watertight-enclosures/enclosure-tools-supplies/vent-asm-r1/) identifica Buna-N y Molykote 111. **No aplicar esa grasa de silicona por defecto a la junta plana de silicona:** seguir la indicación de su fabricante; puede montarse limpia y seca si así lo especifica. No sustituir compresión y geometría por lubricante.

## 4. Fuera de esta compra

Retirados por Alex: **5–8, 10–11, 14, 22–26, 28–30 y 32–37**. El antiguo **31** se integra en **4**; los antiguos **16–20** se sustituyen por el conjunto completo de **15**. Retirar de compra no significa que cada pieza esté recibida ni que deje de formar parte del instrumento.

**Profundidad: no se incorpora sensor en esta versión**, por indicación expresa de Alex. Se mantiene el requisito mecánico de profundidad de servicio de 1 m; eso no es una medida del equipo. Temperatura y conductividad continúan previstas con las piezas disponibles, sin compra nueva.

## 5. Electrónica añadida — D52, 30 oct 2026

**Propuesta para revisión del técnico**, con los dos LED elegidos por Alex. Precios unitarios en EUR **con IVA belga del 21 %**, consultados el 30 de octubre; no incluyen portes. TinyTronics ya muestra 21 %: no se vuelve a añadir. En DigiKey, RS y Ledrise se calcula desde el precio neto. El Pololu es Marketplace con envío separado.

| ID | Cantidad | Comprar | Enlace | EUR/u con IVA |
|---|---:|---|---|---:|
| E01 | 1 | Nichia NF2W757GT-F1 Optisolis white LED on star PCB, 5000 K, SKU 32724 | [Ledrise](https://www.ledrise.eu/nichia-nf2w757gt-f1-optisolis-smd-led-with-star-pcb-23lm-5000-kelvin-cri-98-sku-32724.html) | 2.24 |
| E02 | 1 | ILS 430 nm PowerStar LED, ILH-XC01-S420-SC211-WIR200., RS 0283199 | [RS Belgium](https://benl.rs-online.com/web/p/uv-leds/0283199) | 8.68 |
| E03 | 1 | LEOTRO PLD333 constant-current LED driver, AL8860, SKU 007287 | [TinyTronics](https://www.tinytronics.nl/en/power/voltage-converters/buck-(step-down)-converters/power-led-driver-constant-current-333-667ma) | 3.75 |
| E04 | 1 | LM317T adjustable regulator, TO-220, SKU 000235 | [TinyTronics](https://www.tinytronics.nl/en/components/voltage-regulators/lm317t-adjustable-voltage-regulator) | 0.50 |
| E05 | 2 | 2N3904 NPN transistor, TO-92 | [TinyTronics](https://www.tinytronics.nl/nl/schakelaars/transistoren-en-mosfet%27s/transistoren/npn-transistor-2n3904) | 0.15 |
| E06 | 1 | 1% metal-film resistor assortment, 10 ohm to 1 Mohm, 0.25 W | [TinyTronics](https://www.tinytronics.nl/en/components/resistors/resistors/10%CF%89-1m%CF%89-resistor-set) | 5.00 |
| E07 | 1 | Pololu 2814 Big MOSFET Slide Switch MP, 2183-2814-ND | [DigiKey Belgium](https://www.digikey.be/en/products/detail/pololu/2814/10450362) | 6.68 |
| E08 | 1 | Open-Smart DS3231 RTC with backup battery, SKU 005386 | [TinyTronics](https://www.tinytronics.nl/nl/sensoren/tijd/open-smart-ds3231-rtc-module-met-eeprom-i2c) | 4.00 |
| E09 | 1 | DFRobot DFR0845 isolated RS485-to-UART module | [TinyTronics](https://www.tinytronics.nl/en/communication-and-signals/serial/rs-485/dfrobot-gravity-active-isolated-rs485-to-uart-signal-adapter-module) | 19.75 |
| E10 | 1 | Waveshare USB TO RS485 (B) adapter, CH343G, model 22456 | [TinyTronics](https://www.tinytronics.nl/en/communication-and-signals/serial/rs-485/waveshare-industrial-bi-directional-usb-to-rs485-converter-ch343g) | 9.00 |
| E11 | 1 | TI SN74LVC245AN bus buffer, PDIP-20 | [DigiKey Belgium](https://www.digikey.be/en/products/detail/texas-instruments/SN74LVC245AN/377483) | 1.96 |
| E12 | 1 | G2RL-2 DC5 DPDT relay, 5 V coil | [DigiKey Belgium](https://www.digikey.be/en/products/detail/aratas-formerly-omron-components/G2RL-2-DC5/1789837) | 5.13 |
| E13 | 1 | Lite-On LTV-817 optocoupler, DIP-4 | [DigiKey Belgium](https://www.digikey.be/en/products/detail/lite-on-inc/LTV-817/385836) | 0.42 |
| E14 | 2 | 1N4007 rectifier diode, DO-41 | [TinyTronics](https://www.tinytronics.nl/en/components/diodes/diode-1n4007) | 0.10 |
| E15 | 2 | MPD BF353 covered inline ATO/ATC fuse holder, 16 AWG | [DigiKey Belgium](https://www.digikey.be/en/products/detail/mpd-memory-protection-devices/BF353/8119223) | 4.45 |
| E16 | 2 | Littelfuse 0287003.PXCN ATO blade fuse, 3 A, 32 VDC | [DigiKey Belgium](https://www.digikey.be/en/products/detail/littelfuse-inc/0287003-PXCN/3102553) | 0.47 |
| E17 | 2 | Littelfuse 0287002.PXCN ATO blade fuse, 2 A, 32 VDC | [DigiKey Belgium](https://www.digikey.be/en/products/detail/littelfuse-inc/0287002-PXCN/3102552) | 0.50 |
| E18 | 6 | AISHI ERS1HM470E110T electrolytic capacitor, 47 uF, 50 V | [TinyTronics](https://www.tinytronics.nl/en/components/capacitors/aishi-elektrolytic-capacitor-47uf-50v) | 0.13 |
| E19 | 2 | AISHI ERS1EM331F12OT electrolytic capacitor, 330 uF, 25 V | [TinyTronics](https://www.tinytronics.nl/en/components/capacitors/aishi-elektrolytic-capacitor-330uf-25v) | 0.15 |
| E20 | 6 | Vishay K104K15X7RF5TL2 ceramic capacitor, 100 nF, 50 V | [DigiKey Belgium](https://www.digikey.be/en/products/detail/vishay-beyschlag-draloric-bc-components/K104K15X7RF5TL2/286538) | 0.34 |
| E21 | 1 | Internal leak detection board, 3.3 V operation, SKU 001093 | [TinyTronics](https://www.tinytronics.nl/en/sensors/liquid/water-level-sensor) | 1.50 |

**Subtotal de electrónica propuesta: 83.07 EUR con IVA**, sin portes. Incluye ambos LED; retirar del pedido el que ya se tenga. El conjunto mecánico mantiene sus importes y presupuestos pendientes; no se mezcla USD con EUR.

- **Optisolis E01:** Alex confirma que hay que comprarlo. La ficha de Ledrise anuncia producción de 6–12 semanas y no se ha encontrado stock inmediato verificado del mismo conjunto 5000 K sobre estrella. Mantener la referencia presupuestada y dejar su pedido pendiente de resolver la entrega; no tratarla como entrega de una semana.
- **Motor/convertidores:** Alex confirma A4988 y DC/DC de 5 A. Se asignan un A4988 y tres convertidores; quedan fuera de compra. El A4988 se aprueba para el montaje solo tras comprobar corriente por fase y temperatura. Los convertidores admiten 30 V de entrada: medir la carga completa del pack antes de conectarlos.
- **E04/E06:** fuente blanca lineal a unos 62,5 mA desde 9 V, con dos resistencias de 10 Ω en serie. E03 es exclusivamente para el azul a 333 mA. No conectar el blanco al módulo azul ni reutilizar la hipótesis energética de 100 mA como especificación del LED.
- **E06 y E18–E20:** material de montaje no confirmado en inventario. Descontarlo si el técnico dispone de los mismos valores y tensiones; se incluye para que el pedido no omita pasivos necesarios. La placa de montaje, cables y disipador se preparan con material del taller previamente retirado del pedido por Alex.
- **E12/E13/E15–E17:** propuesta de aislamiento de la carga mediante relé normalmente abierto de dos polos y detección de cable. Conservar el cargador y BMS originales. Fusibles provisionales de 3 A y 2 A; cotejar cargador, cables y BMS antes del cableado. Pinout EN3 todavía no liberado para soldar.
- **RTC:** se propone DS3231 de 4 EUR; ARES también enumera DS1307, sin disponibilidad confirmada ni revisión de sus pull-ups. No se compra una segunda placa aisladora de conductividad: viene en el kit Atlas.
- Solo hay referencias cerradas para blanco y azul. Los otros LED y las nuevas magnitudes futuras se incorporarán cuando estén definidos; no se compran módulos para corrientes desconocidas.

## 6. Documentos para el técnico

- [Electronics V1 — distribución, conexiones funcionales y comprobaciones](electronica/DISENO_ELECTRICO_V1.md).
- [Lista única en Excel, en inglés y con enlaces/precios numéricos con IVA](outputs/01a0de94-9b4a-7771-b367-25a5e993f29d/Cruz_Shopping_List_EN_2026-10-30.xlsx).

## 7. Presupuesto energético conservado

[Presupuesto previo y sus limitaciones](docs/PRESUPUESTO_ENERGETICO.md), trasladado sin recalcular. No se mezcla con el importe de esta compra. Los precios históricos de tubo/batería y las referencias en USD no constituyen un total actualizado del pedido.
