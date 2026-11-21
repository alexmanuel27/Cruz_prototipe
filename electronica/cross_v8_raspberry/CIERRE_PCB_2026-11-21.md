# PCB V8 · cierre de colocación y trazado

21 de noviembre de 2026 · Codex GPT-6. Diseño de prototipo pendiente de liberación eléctrica y mecánica. No equivale a ensayo físico ni a autorización de fabricación.

## Resultado guardado

- **122 huellas colocadas dentro del contorno**, pistas y planos en ambas caras; todas las conexiones trazadas.
- **KiCad 9.0.7: DRC 0 errores, 0 avisos, 0 conexiones pendientes; paridad esquema–placa 0.** Separación 0,2 mm, borde 0,5 mm y serigrafía 0,15 mm, sin desactivar reglas para obtener este resultado.
- **ERC 0 errores / 0 avisos.** Se sincronizaron 27 definiciones de símbolos con la biblioteca instalada tras comprobar números, nombres, tipos, posición, orientación y longitud de los pines. En el CD4013, la unidad de alimentación pasa a ser común a ambos estilos de dibujo con idénticos pines. No se movieron conexiones ni se silenciaron reglas.
- Comprobación de redes actualizada para aislamiento real, alimentación permanente y convertidores externos: correcta. Estas comprobaciones no simulan el circuito ni validan las piezas físicas.

[Proyecto editable](cross_v8_draft.kicad_pro) · [cobre superior](../cierre_pcb_2026-11-21/vistas/cobre_superior.svg) · [cobre inferior, espejado](../cierre_pcb_2026-11-21/vistas/cobre_inferior.svg) · [montaje superior](../cierre_pcb_2026-11-21/vistas/montaje_superior.svg) · [montaje inferior, espejado](../cierre_pcb_2026-11-21/vistas/montaje_inferior.svg) · [BOM](../cierre_pcb_2026-11-21/bom.csv) · [conexiones externas](../cierre_pcb_2026-11-21/conectores.csv) · [posiciones](../cierre_pcb_2026-11-21/posiciones.csv) · [STEP de placa sin componentes](../cierre_pcb_2026-11-21/placa_sin_componentes.step).

El STEP representa solo sustrato y taladros, sin envolventes de componentes/cables ni validación de bandeja. La BOM identifica R26/R27 como DNP y la lista de posiciones los excluye; no son una orden de compra. Informes y hashes en [cierre_pcb_2026-11-21](../cierre_pcb_2026-11-21/).

## Alimentación acordada

Alex confirma **dos DC/DC principales cableados fuera de la PCB**. U5 y U6 son bornas de conexión, no huellas para montar convertidores. Ambas entradas reciben VBAT_SW, después del interruptor externo Pololu; no hay cascada 24→5→12.

| Borna | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| U5 · convertidor externo Pi | Entrada + desde batería conmutada | GND / entrada − | Salida regulada +5 V para Pi | GND / salida − |
| U6 · convertidor externo óptica | Entrada + desde batería conmutada | GND / entrada − | Salida regulada +12 V | GND / salida − |

Identificar **los números de pad**, sin deducirlos por la posición en una imagen. Borneras Phoenix MKDS-1,5, paso 5,08 mm. Los retornos de U5/U6 están unidos en la PCB: estas dos ramas no son aisladas.

U4 cambia a **RECOM R-78HE5.0-0.3**, pequeño convertidor permanente montado en placa (pieza adicional por adquirir). Su rango 6,5–72 V incluye los 25,2 V declarados y entrega 5 V/300 mA para U7/lógica/relé. No alimenta la Pi ni la lámpara. Entrada C21 4,7 µF/50 V y salida C20 22 µF/16 V X7R; revisar capacidad efectiva. El consumo en reposo de todo el instrumento sigue sin medir. [Ficha oficial R-78HE](https://recom-power.com/pdf/Innoline/R-78HE-0.3.pdf).

J23 lleva la alimentación de 5 V al cable USB-C de Pi. J1 mantiene sus pines 2/4 desconectados: la cinta GPIO lleva señales, 3,3 V de referencia y masas. La Pi no admite 12 V. Para comprar U5, verificar entrada con margen sobre pack cargado/transitorios y salida continua suficiente para Pi 5, cámaras y sensores. Raspberry Pi recomienda alimentación de 5,1 V/5 A; un buck rotulado «5 A» y un cable USB-C sencillo no garantizan identificación de fuente ni ese presupuesto USB. Medir tensión en Pi bajo carga y revisar negociación USB-C. [Documentación oficial](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#power-supply).

## Aislamiento de conductividad implementado

U13 deja de ser un bloque virtual: **RECOM R05CT05S** alimentado desde 5V_PI, habilitado por 3V3_PI; TRIM a GND_EC_ISO selecciona 3,3 V y SYNC a GND selecciona funcionamiento independiente. La salida regulada soporta más que los 26 mA máximos documentados del EC-OEM más la interfaz aislada. Entrada C15/C16 y salida C14/C19; C13 junto al OEM. Es una nueva pieza por adquirir, no material ya disponible. [RECOM](https://recom-power.com/en/rec-p-R05CT05S-R.html).

U15 **ISO1540D** aísla SDA/SCL. Su lado 1 (1–4, límite 80 pF) mira al pequeño bus EC y el lado 2 (5–8) al bus compartido de sensores. C17/C18 desacoplan ambos dominios. R28/R29 son los pull-ups aislados de 4,7 kΩ; R26/R27 siguen DNP hasta medir los pull-ups existentes en AS7265x. Trabajar inicialmente a 100 kHz y medir niveles/flancos y capacitancia efectiva. [Ficha TI ISO1540](https://www.ti.com/lit/ds/symlink/iso1540.pdf).

Una franja de **3,5 mm sin cobre** en ambas caras separa las masas y fuentes; solo los dos aisladores atraviesan la franja con sus cuerpos. No unir GND_EC_ISO con GND ni PRBG con ninguna masa. El coaxial de sonda va a J28: vivo PRB y retorno PRBG. Aislamiento funcional para medida, sin certificación del conjunto para seguridad eléctrica.

## Construcción y montaje

Contorno conservado de **170 × 68 mm**, dos capas, espesor propuesto 1,6 mm y cobre de 70 µm en ambas caras. No se inventan taladros de fijación: cotejar la bandeja/soportes reales antes de fabricar. La colocación nueva sustituye el aparcamiento fuera del contorno. Los DC/DC externos y sus cables, el Pololu, el motor y las fuentes ópticas requieren sus fijaciones independientes.

Resistencias lógicas 0805; red de corriente azul/naranja y R47 mantienen encapsulado axial. Pasivos de desacoplo y compuertas se montan también por la cara inferior, con espacio libre y sin apoyo directo sobre la bandeja. Consultar los planos de ambas caras y la lista de posiciones; la cara inferior se muestra espejada en su vista de montaje. No intercambiar AHCT por AHC. C4/C5 pasan a 2,2 µF X7R/16 V para dar margen de capacidad efectiva al regulador.

Reglas de trazado: señales 0,25 mm, batería/carga 1,5 mm, línea óptica/halógena 1,2 mm, fases del motor 0,8 mm y auxiliares 0,5 mm. Pi tiene ida y retorno directos de 3 mm entre U5 y J23. Separación mínima de 0,2 mm y margen de cobre al borde de 0,5 mm. Los planos de masa complementan los retornos. Son geometrías de diseño: la corriente admisible integrada necesita revisión térmica con fusibles, cables y carga reales; no se deduce de DRC.

Las pestañas de IRLZ44N son drenador y las de LM317 son OUT: no compartir disipador conductor sin aislamiento. La halógena y su calor quedan fuera de placa. Comprobar orientación y continuidad 1:1 del cable IDC40 real, no solo la raya. El [kit TinyTronics](https://www.tinytronics.nl/nl/development-boards/accessoires/adapter-boards/raspberry-pi-40-pins-gpio-extension-kit) incluye cinta de 20 cm; comprobar funcionamiento de I²C con todo el montaje.

## Condiciones pendientes antes de fabricación o alimentación del conjunto

1. **F1/F2 siguen sin calibre liberado.** Cerrar máximos y transitorios del pack/BMS, cables y convertidores reales; seleccionar protección contra inversión/transitorios compatible con el A4988. Los 25,2 V/2 A del cargador y «5–8 A» del pack no determinan los fusibles. No hay TVS seleccionada ni supresión del bus motor validada.
2. **Motor:** 24 V/20 W y bobinas de 2,9 Ω no dan la corriente nominal por fase. Medir/confirmar ese dato y ajustar el A4988 R050; no aprobar un Vref por inferencia. El DRV8834 blanco no admite batería de 24 V.
3. **Encendido/apagado:** estado inicial de U8 CD4013 sin garantizar y SET sostenido puede impedir corte; no se ha rediseñado ni probado ese control autónomo. Completar secuencia magnética/RTC, aislamiento de carga/contactos y respuesta segura. Detector de fuga y watchdog externo no incorporados.
4. **Potencia y térmica:** probar arranque en frío de halógena, caída de 5 V en Pi con USB, convertidores reales, corriente final del IR, LM317, U10 y calentamiento de pistas/vías/borneras. Los 110 mA de banco azul/naranja no equivalen a los 120 mA ideales de 10,4 Ω.
5. **Mecánica y piezas reales:** cotejar orientación, dimensiones y contactos del EC-OEM, R05CT05S, R-78HE, A4988, relé y conectores; comprobar disipadores, alturas inferiores, salida de cables y montaje en bandeja. Los dibujos de huella no constituyen una prueba de encaje.
6. Comprobar rampas, reset y brownout: fuentes apagadas, bomba deshabilitada, ausencia de alimentación parásita, funcionamiento del aislamiento y apagado ordenado. La tabla de GPIO de la [revisión de banco](REVISION_BANCO_2026-11-21.md#tabla-vigente-para-software) permanece vigente.
