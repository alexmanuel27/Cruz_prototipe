# Revisión de alimentación y control de Cruz V8

20 de noviembre de 2026 · Codex GPT-6 · Revisión del archivo guardado, sin editar esquema ni PCB.

La Raspberry Pi recibe 5 V y gobierna el instrumento; sus GPIO trabajan a 3,3 V. Batería y bomba son de 24 V nominales. Se conserva la numeración de las 22 referencias discutidas con Alex y se añade el regulador de sensores como ítem 23. Es una lista de trabajo funcional: el título real del bloque 01 es «BATERIA, CARGA Y PROTECCION» y el del 02, «CONVERSION DE ALIMENTACION». El control magnético está dibujado en 08, el reloj en 07 y el bloqueo del piloto en 09.

> **D56:** Alex elige una [halógena para transmisión](../../DECISIONES.md#d56--halógena-para-transmisión-2026-11-21). La tabla y las referencias reflejan la V8 guardada con su antiguo canal de LED blanco. La alimentación, corriente de arranque y conmutación de la lámpara deben verificarse en banco antes de revisar ese canal.

## Estado comprobado

KiCad 9.0.7, comprobaciones sobre copia. [ERC](../revision_01_02_2026-11-20/erc.json), [DRC con paridad](../revision_01_02_2026-11-20/drc.json), [redes exportadas](../revision_01_02_2026-11-20/redes.xml) y [SHA256 de las fuentes](../revision_01_02_2026-11-20/fuentes_sha256.json).

| Comprobación | Resultado |
| --- | --- |
| Componentes / redes del esquema | 75 / 77, incluyendo redes de pines sin conectar |
| ERC | 77 avisos `lib_symbol_mismatch`; 3 errores `power_pin_not_driven` |
| Pines de los errores ERC | U2.3 VI (`9V_OPT`), U7.2 VI (`5V_AON`), U7.1 GND |
| DRC | 199 conexiones pendientes y 57 avisos de serigrafía |
| Paridad esquema–PCB | 0 diferencias |
| Trazado | Sin segmentos ni vías; contorno de referencia 170 × 68 mm |

Coincide con `LEEME_PRIMERO.md`. Paridad significa que placa y esquema coinciden, no que el circuito sea correcto. Los errores de alimentación requieren modelar las salidas reales de módulos y retornos; no basta con añadir indicadores de alimentación para ocultar errores. Las discrepancias de biblioteca deben compararse antes de actualizar símbolos: pueden afectar numeración y funciones de pines.

## Lista conservada de 23 ítems

Las tensiones indican las redes del circuito, no la tensión nominal máxima admisible de cada pieza. `AON` permanece alimentado con la Pi apagada. Alex transcribe las etiquetas: batería 24 V / 3000 mAh, entrada 25,2 V, salida 22–25 V (5–8 A); cargador 25,2 V / 2 A. Falta comprobar tolerancia y máximo efectivo mediante medida.

| Nº | Referencia y valor guardado | Función y tensión | Decisión o comprobación pendiente |
| ---: | --- | --- | --- |
| 1 | J13 `BATTERY_COMMON_PAIR` | Entrada: pin 1 `VBAT_RAW`, pin 2 GND; batería 24 V/3 Ah; etiqueta salida 22–25 V, carga 25,2 V; par común | Máximo medido, polaridad, significado continuo/pico de 5–8 A y conector/cable real |
| 2 | F1 `F1_LOAD_RATING_TBD` | `VBAT_RAW` → `VBAT_FUSED`; protege consumo, incluido AON | Calibre, curva, tensión DC y poder de corte frente a pack/cables/arranque; sin valor cerrado |
| 3 | J14 `TO_SWITCH_INPUT_FUSED` | Pin 1 `VBAT_FUSED`, pin 2 GND; entrada del interruptor externo | Integración física del Pololu 2814, fijación, terminales y protección de transitorios |
| 4 | J11 `INPUT_SWITCHED_BATTERY` | Pin 1 `VBAT_SW`, pin 2 GND; retorno del interruptor, aproximadamente tensión de batería | Conector real y capacidad de corriente. La orden está en J26, fuera de estos 22 ítems |
| 5 | J18 `EN3_8PIN_ASSIGNMENT_VERIFY` | Interfaz lógica de ocho contactos para carga, RS-485 y piloto; varias tensiones | Numeración desde ambas caras del EN3 real, cable y secuencia de desconexión; no liberado para soldar |
| 6 | F2 `F2_CHARGE_RATING_TBD` | `VBAT_RAW` ↔ `CHG_FUSED`; rama de carga, cargador etiquetado 25,2 V/2 A | Revisar propuesta histórica de fusible 2 A: no seleccionarlo igualando sin más la corriente nominal del cargador; curva y coordinación DC con cable/relé |
| 7 | K1 `G2RL-2_DC5` | Bobina 5 V AON; dos contactos normalmente abiertos conectan los dos hilos de carga | Referencia exacta, carga DC admisible e intensidad de conexión; recuperación con batería/BMS agotados |
| 8 | Q2 `AO3400A` | MOSFET que conecta bobina a GND; puerta por GPIO de 3,3 V | Cotejar componente/pinout y conducción garantizada a la tensión de puerta disponible |
| 9 | D1 `1N4007` | Retorno inductivo de bobina: cátodo 5 V AON, ánodo `RELAY_LOW` | Montaje/polaridad y tiempo de liberación del relé; no es protección del bus de batería |
| 10 | R11 1 kΩ | `CHARGE_CTRL` → puerta Q2; señal 0–3,3 V | Verificar con Q6 que el bloqueo por piloto ausente domina la orden de la Pi |
| 11 | R12 47 kΩ | Puerta Q2 → GND; mantiene carga desactivada con GPIO flotante | Verificar estado durante arranque, apagado y pérdida de alimentación |
| 12 | U3 `LTV-817` | Lazo piloto a 5 V AON; salida `PILOT_ACTIVE_N` elevada a 3,3 V AON por R24 | CTR y corriente de LED reales; detectar cable no equivale a verificar cargador |
| 13 | R13 680 Ω | Limita LED de U3 desde 5 V AON | Corriente según caída del LED, tolerancia y resistencia del cable |
| 14 | D2 `1N4007_PILOT_REVERSE` | En antiparalelo con LED de U3; lazo de 5 V | Verificar orientación y protección de los contactos externos |
| 15 | R14 10 kΩ | `PILOT_SENSE` → `3V3_PI`; lectura solo con Pi encendida | D7 separa esta lectura de la señal AON; comprobar tensión baja y ausencia de alimentación por GPIO |
| 16 | U4 `DFR1015_5V_AON` | `VBAT_FUSED` → 5 V permanentes; relé, piloto y U7 | Margen de entrada real, polaridad de AON, consumo en reposo, huella y temperatura |
| 17 | C4 1 µF | Desacoplo de 5 V AON antes de U7 | Tipo, capacidad efectiva, tensión nominal y proximidad a U7; huella actual de disco |
| 18 | U7 `MCP1700_3V3_AON` | 5 V AON → 3,3 V AON para RTC y enclavamiento | Está en 03 MOTOR, posición esquema (414,02; 66,04) mm. Validar variante TO-92, carga y disipación; no conectarlo a batería |
| 19 | C5 1 µF | Desacoplo de salida 3,3 V AON de U7 | Capacidad efectiva mínima y ESR según ficha; huella actual de disco |
| 20 | U5 `DFR1015_5V_PI` | `VBAT_SW` → 5 V conmutados de Pi | Corriente conjunta Pi/cámaras/regulador 23, caída de cable, arranque y temperatura |
| 21 | J23 `PI_5V_USBC_LEAD_VERIFY` | Pin 1 `5V_PI`, pin 2 GND; alimentación mediante cable USB-C | Cable USB-C y conector de potencia reales, caída bajo carga; no inyectar por GPIO |
| 22 | U6 `DFR1015_9V_OPT` | `VBAT_SW` → 9 V para los drivers ópticos | Mantener 9 V como propuesta hasta validar corrientes, disipación, arranque y apagado de ambos drivers |
| 23 | Regulador 3,3 V de sensores, sin referencia asignada | Propuesta: entrada `5V_PI`, salida nueva `3V3_SENS` para AS7265x, DS18B20 y Atlas | No existe en esquema ni PCB. Elegir modelo por carga conjunta y térmica; incluir condensadores, huella y secuencia de alimentación |

U7 admite entrada de 2,3–6 V, salida de hasta 250 mA para esta variante y requiere al menos 1 µF efectivo de salida. No se presupone que otro MCP1700 sea suficiente para el ítem 23: un LDO disiparía `(5−3,3) × I_sensores`. [Microchip MCP1700](https://ww1.microchip.com/downloads/en/DeviceDoc/MCP1700-Data-Sheet-20001826F.pdf)

## Diferencias concretas frente a las decisiones de diseño

1. **Rama de sensores aún compartida con Pi.** J8.1 (AS7265x), J9.1 (Atlas) y J10.1 (DS18B20) están en `3V3_PI`. Al añadir el ítem 23, revisar también R10.2, el pull-up de 1-Wire: sigue en `3V3_PI`. SDA/SCL siguen siendo señales de 3,3 V de Pi; revisar pull-ups de los módulos, posibles retornos de alimentación y caídas de ambas ramas. No unir las salidas de los dos reguladores de 3,3 V.
2. **Pololu sin componente propio en placa.** J14/J11/J26 representan entrada/salida/control. El STEP local oficial no añade conexiones eléctricas ni fijaciones. U4 recibe batería protegida por F1 antes del Pololu; por tanto la protección de polaridad del Pololu no protege U4 ni la rama AON.
3. **Huellas provisionales.** J13/J14/J11/J23 son cabeceras de 2,54 mm. F1/F2 usan portafusibles 5×20 mm; la compra histórica proponía ATO/ATC en línea. Seleccionar una implementación y hacer coincidir BOM, huella y montaje. U4/U5/U6 usan `Cross:DFR1015_8pad_BORRADOR`: ocho pads físicos con cuatro números repetidos y envolvente aproximada, no un pinout físico validado.
4. **Protecciones incompletas.** Solo C1, 100 µF/50 V, está entre `VBAT_SW` y GND; no hay TVS de batería ni protección equivalente de picos negativos del interruptor. No hay corte preventivo de batería por baja tensión en AON. R8/R9 miden `VBAT_SW` mediante un ADS1115 externo representado por conectores, con Pi apagada no hay supervisión activa de batería. No aparece un detector de fuga en las 75 referencias.
5. **No hay supervisor ESP32.** El documento histórico `archivo/electronica/DISENO_ELECTRICO_V1.md` describe esa arquitectura anterior. En V8 el RTC y U8 mantienen el encendido sin Pi. Tampoco existe un watchdog externo que fuerce un comportamiento definido si Linux se cuelga.

## Batería, interruptor y puerto común

Alex comunicó el 20 de noviembre las siguientes etiquetas: **batería 24 V / 3000 mAh; entrada 25,2 V; salida 22–25 V (5–8 A); cargador 25,2 V / 2 A; motor 20 W**. Los 25,2 V sustituyen al dato de 25,6 V comunicado el 2 de noviembre. Sigue vigente el par común de carga/descarga. No se interpreta 5–8 A como una especificación inequívoca de corriente continua/pico o del umbral BMS. Registrar las medidas de cargador, pack cargado en reposo y bus durante conexión/desconexión de cargas. No deducir química ni número de celdas del rótulo «24 V». No reutilizar el techo provisional histórico de 28 V como aprobación del fabricante.

Con 25,2 V de etiqueta, quedan 4,8 V hasta los 30 V declarados del DFR1015, antes de tolerancias y transitorios; continúa por encima de la recomendación inferior a 24 V. La propuesta antigua de F2=2 A debe redimensionarse con el cargador nominal de 2 A, su corriente real y la curva/temperatura del fusible, sin elegir un nuevo calibre hasta cotejar cable, contactos y batería.

El DFR1015 declara 7,5–30 V de entrada y recomienda menos de 24 V. Entrega nominal de 5 V/3 A sin disipación añadida; hasta 5 A requiere disipación. La marca «5 A» no acredita 5 A continuos dentro del tubo. [DFRobot](https://www.dfrobot.com/product-2599.html)

El Pololu 2814 MP recomienda 4,5–32 V; su comparación térmica indica 4 A a 55 °C en las condiciones publicadas. Con interruptor local OFF, ON bajo/desconectado apaga y por encima de aproximadamente 1 V enciende. El máximo absoluto de 40 V no es una tensión de diseño. Dimensionar TVS con tensión de trabajo por encima de la máxima continua y tensión de clamp por debajo del límite de la pieza más débil, considerando corriente de pulso y cableado; una TVS etiquetada «24 V» no cierra ese cálculo. [Pololu, control y transitorios](https://www.pololu.com/product/2814)

La asignación **lógica provisional** guardada de J18 es: 1 `CHG_PLUS`; 2 `CHG_MINUS`; 3 sin conectar (reserva EXT+); 4 GND (referencia piloto/EXT−); 5 `RS485_A`; 6 `RS485_B`; 7 `RS485_REF` aislada; 8 `PILOT_LOOP`. No es todavía la numeración liberada del EN3 físico. Mantener la referencia aislada de RS-485 separada de GND. J18 es una cabecera interna; no valida el conector de panel, estanqueidad, paso por tapa ni orientación.

K1.11 recibe `CHG_FUSED` y K1.14 va a `CHG_PLUS`; K1.21 es GND y K1.24 va a `CHG_MINUS`. La bobina está en 5 V AON. Piloto presente hace `PILOT_ACTIVE_N` bajo y libera Q6; entonces `CHARGE_CTRL` alto puede accionar Q2. Piloto ausente eleva esa señal y Q6 intenta bloquear la puerta de Q2. Verificar capacidad de bloqueo, tensión de puerta y tiempo real de apertura. El circuito no demuestra contactos de conexión anticipada ni hace seguro un cortocircuito entre contactos durante inserción. K1 tampoco sustituye al cargador o al BMS.

## Estados e interfaz eléctrica para software

Conexiones extraídas del netlist; numeración BCM derivada del conector estándar de 40 pines, pendiente de contraste con la Pi y el cable reales. Son interfaces provisionales, no autorización para energizar.

| Señal | Pin físico J1 / BCM | Comportamiento guardado |
| --- | --- | --- |
| `M_STEP` / `M_DIR` | 11 / 17; 12 / 18 | Pulsos de paso / dirección; R2/R3 a GND |
| `M_ENABLE_N` | 13 / 27 | Alto deshabilita; R1 10 kΩ a 3V3_PI |
| `WHITE_EN` | 15 / 22 | Alto activa Q1 y LED blanco; R6 apaga con base flotante |
| `BLUE_EN` | 16 / 23 | Lógica invertida por D8/Q7: bajo puede encender, alto apaga. No copiar la semántica activa-alta de V1 |
| `CHARGE_CTRL` | 18 / 24 | Alto permite bobina, sujeto a Q6/piloto; R12 apaga con puerta flotante |
| `PILOT_SENSE` | 22 / 25 | Bajo indica piloto, mediante D7; umbral real por verificar |
| `SW_SENSE` | 29 / 5 | Bajo detecta imán por D5; no implementa alternancia por sí solo |
| `HOLD_PI` | 37 / 26 | **Alto resetea U8A y solicita corte**, pese al nombre HOLD; R23 100 kΩ a GND |

U8A.1 (`Q`) gobierna `POWER_ON` → J26.1. U8A.4 (`RESET`) recibe `HOLD_PI`. U8A.6 (`SET`) recibe `SET_NODE`; Q5 invierte `WAKE_N`. Imán, piloto o RTC pueden llevar WAKE_N a bajo y activar SET. CLOCK y D están a GND: un toque de imán establece encendido; otro toque no alterna automáticamente a apagado.

| Estado | Qué hace el circuito guardado | Qué queda por cerrar |
| --- | --- | --- |
| Conectar batería | U4/U7 y lógica AON arrancan; no hay reset inicial explícito de U8 | Elegir arranque apagado o encendido y garantizarlo por hardware ante rampa y reconexión |
| Imán o piloto | Activan SET y solicitan encendido; sin antirrebote explícito | Duración de pulsos, detección mantenida, desconexión de cable |
| Despertar RTC | INT bajo activa SET hasta liberar la alarma | Módulo DS3231 con INT accesible, configuración y verificación de alarma futura |
| Pi arrancando | La rama conmutada arranca junto con motor/óptica; los pull-ups/down intentan mantener cargas inactivas | Medir orden de subida de 9 V/5 V/3,3 V y estados GPIO reales |
| Apagado ordenado | `HOLD_PI` alto pide reset inmediatamente | Emitirlo únicamente en etapa final del apagado del sistema, tras guardado durable; no desde la recepción de una orden |
| Pi apagada | AON, RTC, piloto y enclavamiento permanecen activos; RS-485/ADC y sensores actuales pierden 3V3_PI | Medir consumo en reposo y alimentación por señales/cables externos |

Antes del corte, programar el siguiente despertar, limpiar las banderas de alarma y verificar INT inactivo; una alarma DS3231 queda señalada hasta limpiar su bandera. Si imán, piloto o RTC mantienen SET alto, RESET alto no constituye un corte fiable: la tabla CD4013 da Q y Q invertida altos cuando SET=RESET=1. El circuito actual no garantiza poder apagar mientras esa causa siga activa. [DS3231](https://www.analog.com/media/en/technical-documentation/data-sheets/ds3231.pdf), [tabla CD4013B](https://www.ti.com/lit/ds/symlink/cd4013b.pdf)

La ficha enlazada por el símbolo U8 es de MC14013B, mientras el valor dice CD4013. Identificar la pieza comprada antes de dar por cerrados los umbrales y corrientes a 3,3 V. Acordar un nombre claro para `HOLD_PI`, por ejemplo una señal de corte al finalizar apagado; no renombrarla unilateralmente mientras Alex edita.

## Interfaces de motor y fuentes ópticas

Estos bloques se revisarán después de 01+02, pero fijan las cargas y estados de alimentación.

- **Motor U1/J2:** 24 V y 20 W no determinan corriente por fase. Identificar modelo, parejas de bobinas, corriente nominal y Rsense de ambos canales del carrier WJMY. Para A4988, `I_tripmax = Vref/(8×Rsense)`; el modo de paso completo usa aproximadamente el 70,7 % de ese límite por bobina. VMOT está en VBAT_SW y lógica en 3V3_PI. A4988 admite bus hasta 35 V: medir picos, corriente y temperatura antes de aprobar; no trasladar prestaciones térmicas de otro carrier. [Ficha Allegro](https://www.allegromicro.com/~/media/Files/Datasheets/A4988-Datasheet.pdf)
- **Blanco:** U2 LM317, R4=20 Ω, Q1 2N3904 y J3 ya forman una fuente de corriente de unos `1,25/20 = 62,5 mA`, no un LED directo a 9 V. R4 disipa aproximadamente 0,078 W. Nichia NF2W757GT-F1: prueba a 65 mA, Vf típica 2,9 V, máximo 100 mA a Ts=25 °C sujeto a reducción térmica. Validar margen LM317 y saturación de Q1, disipación, corriente y temperatura reales. [Nichia](https://led-ld.nichia.co.jp/api/data/spec/led/NF2W757GT-F1-E%285056%29Rfa00%20Rfc00.pdf), [LM317](https://www.ti.com/lit/ds/symlink/lm317.pdf)
- **Azul:** J4 es entrada 9 V de un driver externo y J5 su CTRL; no representan una conexión directa al LED. La propuesta histórica PLD333/AL8860 con Rs=0,3 Ω y puente abierto (`0,1/0,3 ≈ 333 mA`) no corresponde al ajuste de 120 mA informado por Alex para el método de Daniela; Alex no dispone del PLD333. No energizar con esta propuesta sin revisar [D54](../../DECISIONES.md#d54--fuentes-adicionales-y-ajuste-del-azul-2026-11-21). ILS ILH-XC01-S420-SC211-WIR200 especifica bin de pico 420–430 nm, Vf 3–4 V y datos a 350 mA; requiere disipador. Para el AL8860 propuesto, CTRL flotante enciende y menos de 0,2 V apaga. D8/Q7 invierten el control en V8; comprobar estados al arranque y corte. [Diseño Leotro](https://github.com/Leotro-Engineering/Power-LED-Driver), [AL8860](https://www.diodes.com/datasheet/download/AL8860.pdf), [ILS, p. 3](https://docs.rs-online.com/3301/A700000012614806.pdf)

## Orden de trabajo con Alex

1. Ítems 1–4: identificar pack/cargador y corriente total; cerrar conectores de potencia, protección de AON y Pololu/transitorios.
2. Ítems 5–15: cerrar EN3 físico, relé, fusible de carga e interbloqueo con estados de fallo.
3. Ítems 16–23: confirmar DFR1015, U7/condensadores y elegir/añadir 3V3_SENS, incluidos pull-ups y huellas.
4. Revisar juntos 07–09: estado inicial, prioridad SET/RESET, despertar y corte final de Linux; después validar estados seguros del motor y LED.

Alex edita la fuente en `cross_v8_raspberry`. Antes de cada tanda, volver a leer los archivos guardados y comparar sus huellas SHA256 con la base revisada. Cualquier propuesta de modificación se prepara sobre esa versión; no actualizar desde los generadores históricos ni sustituir sus cambios. Las cotas mecánicas y pinouts comerciales siguen siendo interfaces por validar. Sin ensayo físico, consumo medido ni aprobación de fabricación en esta revisión.
