# Modelos 3D de componentes comerciales

Revisión: **3 de noviembre de 2026**. Montaje: `Cross_M2_horizontal_design`.

Los archivos del fabricante se conservan como referencias de terceros. «Oficial» identifica la procedencia del archivo; no acredita que la variante comprada sea idéntica. No se han escalado los modelos para hacerlos encajar. Ver [revisión del montaje](../fusion_m2/REVISION_STEP_2026-11-03.md).

## Modelos incorporados a Fusion

| Componente | Fuente | Modelo y alcance |
|---|---|---|
| Raspberry Pi 4 Model B | [MGS-CAD-Files](https://github.com/multigamesystem/MGS-CAD-Files/blob/main/STEP%20files%20with%20images/Raspberry%20Pi%204%20Model%20B%20v4.step) | **Comunitario, no oficial Raspberry Pi**. PCB de 85 × 56 mm, conectores y componentes detallados. Archivo en `raspberry_pi4_community/`. Se cotejó la envolvente de placa; medir puertos y conectores reales. La [documentación oficial](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html) ofrece dibujos mecánicos PDF/DXF de Pi 4; no se localizó un STEP oficial de Pi 4. No se sustituyó por Pi 5. |
| Sonda Atlas EC K=1.0 | [STEP Atlas](https://files.atlas-scientific.com/ENV-40-EC-K-1.0.zip) | Oficial de generación anterior, publicado en 2021. Ya estaba incorporado. En `atlas_conductividad/`; el cable rígido se recortó en el montaje, no en el archivo de origen. Confirmar generación de la sonda entregada. |
| Interfaz aislada Atlas Gen 2 | [Atlas ISCCB Gen 2](https://atlas-scientific.com/carrier-boards/electrically-isolated-ezo-carrier-board-gen-2/) · [CAD](https://files.atlas-scientific.com/Electrically-Isolated-EZO-Carrier-Board.zip) | Oficial Gen 2, en `atlas_isolated_carrier/`. Incluye placa, componentes, SMA y separadores. La revisión del kit físico y la placa hija EZO-EC siguen por confirmar. |
| Pololu 2814 | [Pololu recursos](https://www.pololu.com/product/2814/resources) · [STEP](https://www.pololu.com/file/0J1406/big-mosfet-slide-switch-with-reverse-voltage-protection.step) | Oficial de la familia Big MOSFET Slide Switch. Archivo conservado en `../../electronica/cross_v8_raspberry/modelos_3d/Pololu_2814_fabricante.step`. |
| Motor MOONS MS11HS5 | [MOONS MS11HS5P4100](https://www.moonsindustries.com/jp/p/nema-11-standard-hybrid-stepper-motors/ms11hs5p4100-000004611110015856) | **Oficial de familia MS11HS5P**, no del MS11HS5L410C-01 personalizado. En `moons_ms11hs5/`. Eje, conector y acoplamiento con el cabezal son provisionales. Cuatro superficies no sólidas de roscas/taladros permanecen ocultas. |
| Dos pasamuros WetLink JPT M10 5,5 mm | [Blue Robotics](https://bluerobotics.com/store/cables-connectors/penetrators/wetlink-penetrator-jpt/) · [CAD compartido X55](https://cad.bluerobotics.com/WLP_JPT_M10_5.5MM_BR-107163-X55.zip) | Oficial; archivo etiquetado LC055 en descarga compartida X55. La variante HC155 seleccionada comparte referencia exterior publicada, pero su sello específico no está representado. En `bluerobotics_wetlink_jpt/`. |
| Tuercas WetLink M10 | [CAD Blue Robotics](https://cad.bluerobotics.com/WL-M10-NUT-R1.zip) | Oficial, con rosca modelada; dos instancias. Mismo directorio. |
| A4988 | [Pololu A4988](https://www.pololu.com/product/1182/resources) | La referencia 3D Pololu ya incluida en V8 representa otra placa de la misma familia, no certifica la geometría del clon WJMY comprado. Disipador/zócalos permanecen aproximados. |

## Referencias todavía aproximadas

| Componente | Fuente revisada | Estado en el montaje |
|---|---|---|
| Webcam auxiliar IMX179 | [Enlace exacto de Alex](https://www.fruugo.be/industriele-4k-usb-webcam-met-8mp-autofocus-en-imx179-sensor/p-478437047-992136824) | Ficha sin marca de modelo mecánico, cotas exteriores ni STEP verificable. Foto de caja metálica negra con lente saliente. `O04` conserva su envolvente provisional; la ficha no permite aprobar su soporte. No es la cámara espectral. |
| Cabezal de bomba | [Enlace exacto de Alex](https://www.fruugo.be/small-peristaltic-dosing-water-pump-with-stepper-motor-12v24v-3-rotors-silicone-for-lawn-irrigation/p-550072799-1112187245) | Foto con etiqueta KAS-SF-B063, 24 V / 20 W; apariencia de familia KAS. Sin STEP ni plano dimensional exactos verificados. Reserva `H_PUMP_HEAD`: Ø50 × 15 mm; color ámbar basado en foto. Posición de boquillas y acoplamiento pendientes de medición. El enlace no confirma el tubo ni el sufijo de motor; se mantiene el 3 × 5 mm confirmado por Alex. |
| Conector Switchcraft EN3P8MX | [Fabricante](https://www.switchcraft.com/en3-harsh-environment-panel-mount-8-contact-male/en3p8mx/) · [dibujo de panel](https://www.switchcraft.com/assets/1/24/en3p_m_cd.pdf?7687) | Los enlaces DXF/3D llevan al acceso de cuenta del fabricante. No se obtuvo STEP público; se conserva `EL_EN3` aproximado. No se accedió a cuentas ni se creó ninguna. |
| PiCam Arducam OV9281 y conjunto lente/red | [Arducam ficha](https://www.arducam.com/downloads/modules/RaspberryPi_camera/OV9281_MIPI_Camera_Module_DS_v2.pdf) | Sin STEP exacto verificado del conjunto comprado. Se conservan óptica, ángulo y distancia existentes. No se sustituyó por otra PiCam. |
| AS7265x de AliExpress | [Módulo de Alex](https://nl.aliexpress.com/item/1005012953628864.html) | Reserva 45 × 36 × 4,5 mm ya aceptada por Alex. Una placa SparkFun no demuestra las medidas de esta placa. |
| Cubeta NEXACULE | [Variante comprada](https://www.nexacule.com/collections/flow-cuvettes/products/quartz-flow-cuvette-brownloo-quartz-flow-cells-two-ends-open-nexacule?variant=46090230005978) | Modelo dimensional provisional; puertos y cuarzo deben medirse. |
| Buck de 5 A / DFR1015 candidato | [TinyTronics](https://www.tinytronics.nl/en/power/voltage-converters/buck-(step-down)-converters/dc-dc-adjustable-step-down-buck-converter-5a-3.3v-5v-9v-12v) | Sin STEP exacto verificado de la unidad disponible. La envolvente de V8 no certifica zócalos ni disipación. |
| RS-485 DFR0845 | [DFRobot](https://wiki.dfrobot.com/dfr0845/) | Se localizaron planos dimensionales; no STEP exacto. Reserva conservada. |
| RTC DS3231 OpenSmart | Módulo existente | Sin modelo exacto verificado; reserva conservada. |
| Optisolis y LED 430 nm sobre PCB estrella | [Optisolis](https://www.ledrise.eu/nichia-nf2w757gt-f1-optisolis-smd-led-with-star-pcb-23lm-5000-kelvin-cri-98-sku-32724.html) · [RS LED 430](https://benl.rs-online.com/web/p/uv-leds/0283199) | No se verificó STEP del conjunto exacto sobre estrella. Un STEP del chip solo no sustituye la placa, disipador y fijación. |
| Batería CITYORK | [Pack seleccionado](https://www.amazon.com.be/dp/B0FQ583Q2J) | Sin CAD verificado; reserva basada en dimensiones publicadas. Medir pack y salida de cable. |
| DS18B20 encapsulado, imán/reed, racores de punta, tornillería y mangueras | Piezas de compra / reservas de montaje | Geometría simplificada. No se atribuye origen de fabricante ni tolerancia a estos sólidos. |

## Trazabilidad

`MANIFIESTO_ARCHIVOS_2026-11-03.json` registra tamaño y SHA-256 de los STEP utilizados. Los archivos de terceros conservan sus atribuciones y condiciones de uso; su presencia aquí no establece una licencia nueva de redistribución. En particular, la autoría original y licencia de la Raspberry comunitaria no se han verificado por completo.
