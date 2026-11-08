# PCB V4 — carga con batería de terminales comunes

**Estado: borrador incompleto. No fabricar, soldar ni energizar.** V4 conserva el trabajo V3 en una carpeta aparte e incorpora el ramal de carga solicitado el 2 de noviembre de 2026.

## Cambios incorporados en KiCad

- `J13`: entrada del par común del pack. La alimentación y la carga comparten el mismo positivo (`VBAT_RAW`) y el mismo negativo (`GND`).
- `F1`: fusible provisional del ramal de consumo. `J14` lleva su salida a un interruptor de potencia que aún debe diseñarse; `J11` recibe por separado la salida conmutada. **J14 y J11 no están conectados entre sí en esta placa**.
- `F2`: fusible provisional de carga, en la rama positiva entre batería y el contacto común de `K1`.
- `K1`: relé bipolar G2RL-2 de bobina 5 V; los contactos normalmente abiertos conectan `J15` a los dos bornes del pack cuando se excita. `Q2`, resistencias y diodo de rueda libre representan el control de la bobina.
- `J16`, `U3`, resistencias y diodo: circuito provisional de detección del bucle de presencia del cable. `J16` representa las dos señales de presencia, no la asignación física definitiva del conector exterior. La Raspberry lee el estado mediante GPIO25; GPIO24 controla el relé mediante Q2.
- `J17` es únicamente una entrada provisional de `5V_AON` para el relé y el piloto: **su fuente no está diseñada en esta versión**. El encendido de la Raspberry para modo servicio no está resuelto.

La apertura de K1 con la pérdida del cable depende de software y de que la Raspberry esté operativa: **no hay un enclavamiento cableado independiente ni garantía de liberación ante cuelgue**. No hay firmware de control, detector de fugas integrado, prueba de interbloqueo ni solución para cargar con batería agotada. El pinout de ocho contactos del puerto exterior, polaridad del pack, corriente del cargador, BMS, características definitivas de fusibles, conexión a la futura boya y verificación de interruptores/pistas siguen pendientes. El circuito propuesto no sustituye el cargador original ni puentea el BMS.

Las huellas de conectores/fusibles son provisionales. Se eligieron clips 5 × 20 mm y relé G2RL-2 DC5 para poder estudiar el montaje; no se ha aprobado su compra ni determinado si son adecuados para corriente, capacidad de corte DC y condiciones térmicas reales. Los pines de J15/J16 **no son el pinout del conector exterior EN3**. La placa Atlas J9 conserva una propuesta de cinco pines y necesita comprobación de revisión, orientación y soporte.

## Comprobaciones de KiCad

- Se compararon las redes exportadas por el esquema con las conexiones previstas de la placa. Durante la generación se detectó y corrigió una unión indebida de 5 V con masa, y se restauró el pin de bobina `K1.A2`. Esta comparación no valida el circuito ni la seguridad de los componentes.
- DRC con paridad: **106 conexiones sin trazar**, **25 avisos de serigrafía** y **0 diferencias de paridad**. La placa no es fabricable.
- ERC: **126 incidencias**: 2 errores de alimentación no declarada, 81 avisos de puntos fuera de la rejilla y 43 avisos de discrepancia de símbolos. Se requiere revisar y ordenar el esquema, resolver ERC y comprobar visualmente cada conexión.
- No se han calculado pistas ni verificado rutas de corriente, ventilación o temperatura. No hay pruebas físicas.

## Fusion

El STEP de referencia es [`PCB_V4_BORRADOR_NO_FABRICAR.step`](../../cad/fusion_m2/PCB_V4_BORRADOR_NO_FABRICAR.step). Se importó como `PCB_V4_CARGA_BORRADOR_NO_FABRICAR` al documento activo `Cross_M2_horizontal_design`; se ocultó la referencia V3 sin borrarla. **El documento de Fusion quedó sin guardar.** La colocación es provisional, sin taladros de fijación ni cálculo de interferencias. Actualización 3D: se incorporaron modelos de referencia del relé y A4988, zócalos y envolventes aproximadas de disipador y fusibles. Procedencia, hipótesis y componentes aún pendientes en [modelos 3D](modelos_3d/README.md). Los componentes y conectores no están aprobados. Los DC/DC y otros módulos de potencia tampoco se han integrado.

Fuentes: [ficha Omron G2RL](https://omronfs.omron.com/en_US/ecb/products/pdf/en-g2rl.pdf), [AO3400A](https://www.aosmd.com/products/mosfets/low-voltage-mosfets-12v-30v/ao3400a), [DFR1015](https://www.dfrobot.com/product-2599.html), [Atlas carrier Gen 2](https://files.atlas-scientific.com/electrically-isolated-ezo-carrier-board.pdf).


**Actualización de Fusion:** el STEP más reciente es `PCB_V4_REFERENCIAS_3D_BORRADOR.step`; la versión anterior quedó oculta sin borrar. Se mantienen las limitaciones y solapamientos de referencias previos. La placa sigue sin rutear ni validar.
