# Puerto único de carga/datos y futura instalación en boya

**Actualizado el 30 de octubre de 2026, D52; conector D51.** Se mantiene un único conector de ocho contactos para carga, alimentación externa y RS-485, con previsión de futura boya. Alex pide macho, hembra y tapa con los contactos montados; no comprar pines por separado. El conjunto Bulgin Buccaneer 400 anterior se retira del pedido. Modbus RTU sigue siendo una propuesta; pinout, cable, módulos y gestión de fuentes no están cerrados.

> **D52:** Alex autoriza ahora la electrónica. Se propone DFR0845 aislado, relé de carga de dos polos y detección de cable. Ver [Electronics V1](../archivo/electronica/DISENO_ELECTRICO_V1.md). No hay pinout físico liberado; verificar el pack/cargador antes de soldar.

## Conector físico — confirmado D51

**Switchcraft EN3 confirmado por Alex**, ocho contactos integrados para soldar, cierre de bayoneta y tapa estanca con anillo de bloqueo. Conjunto de compra en [LISTA_COMPRA, ítem 15](../compras/LISTA_COMPRA.md#2-una-sola-propuesta-de-conector-completo--ítem-15); pendiente comprobar su montaje en la tapa y el ensayo del conjunto.

| Pieza | Referencia y enlace | Cantidad |
|---|---|---:|
| Macho de panel, ocho contactos incluidos | [EN3P8MX — DigiKey Bélgica](https://www.digikey.be/en/products/detail/switchcraft-inc/EN3P8MX/2080473) | 1 |
| Hembra de cable, ocho contactos incluidos | [EN3C8FX — DigiKey Bélgica](https://www.digikey.be/en/products/detail/switchcraft-inc/EN3C8FX/2080464) | 1 |
| Tapa estanca de panel con bloqueo | [EN3IPCAPX — DigiKey Bélgica](https://www.digikey.be/en/products/detail/switchcraft-inc/EN3IPCAPX/4248698) | 1 |

No hay contactos sueltos en este pedido. Soldar conductores a los terminales integrados y montar el cable de acuerdo con la ficha. [Switchcraft identifica EN3C8FX como contraparte de EN3P8MX](https://www.switchcraft.com/en3-harsh-environment-panel-mount-8-contact-male/en3p8mx/) y declara IP68 para la [tapa EN3IPCAPX](https://www.switchcraft.com/en3-series-ip68-rated-panel-mount-or-cable-to-cable-connector-cap-with-lock-ring/en3ipcapx/).

La ficha declara 6,5 A para esta configuración de ocho contactos. Comprobar corriente admisible con cableado, temperatura y carga reales. EN3C8FX admite cable OD 4,06–6,73 mm; usar material disponible que satisfaga la ficha. Dimensiones de fijación, espesor admisible de panel, junta y acceso a tuerca pendientes de cotejar antes de perforar. No reutilizar taladros/cotas del Bulgin por analogía.

El conjunto seleccionado lleva **macho en el instrumento y hembra en el cable**, a diferencia de la anterior. Resolver en el esquema la desconexión de funciones de potencia para evitar contactos expuestos energizados; no conectar el pack sin esa revisión. El conector mantiene ocho contactos, pero no hereda asignaciones físicas de la familia anterior.

Conectar/desconectar en seco. El sellado se exige con contraparte o tapón montados; verificar con el montaje real a la profundidad de servicio inicial de 1 m y durante la misión prevista. IP68 no acredita por sí solo la profundidad ni la duración del instrumento completo. La selección no registra un pedido ni un ensayo realizado.

## Funciones reservadas; sin números de pin asignados

| Función | Contactos | Motivo |
|---|---:|---|
| Carga del pack, positivo y retorno | 2 | Mantener conexión al cargador compatible y al puerto correcto del BMS |
| Alimentación externa regulada, positivo y retorno | 2 | Prever suministro desde boya y gestión de alimentación; separar función de carga y alimentación |
| RS-485, A/B y referencia de señal | 3 | Datos/configuración para ordenador o registrador compatible |
| PILOT, propuesta D52 | 1 | Detección del cable de servicio mediante lazo limitado y optoacoplador; referencia EXT−, sin unión a CHARGE− ni BUS_REF |
| **Total** | **8** | La asignación a cavidades, retornos y aislamiento se fija en el esquemático |

No unir retornos de carga, alimentación y señal por intuición. Dependen del BMS y del aislamiento de la interfaz. Revisar polaridad, realimentación entre fuentes, desconexión, protección del cableado y estados de Pi apagada. El contacto de reserva no acepta una tensión externa sin especificar su interfaz.

## Datos: RS-485; Modbus RTU propuesto

Implementación propuesta D52: DFRobot DFR0845, con aislamiento de alimentación y señal, y Waveshare USB TO RS485 (B), CH343G, modelo 22456 en el ordenador. Mantener referencia de bus aislada y cable de par trenzado; terminación/polarización definidas por la topología real. Modbus RTU para medidas, estados y configuración; protocolo basado en la [especificación oficial de Modbus sobre línea serie](https://modbus.org/docs/Modbus_over_serial_line_V1_02.pdf). La compatibilidad depende de que el registrador admita este protocolo y el mapa que definamos.

Hoy: ordenador → adaptador USB–RS-485 → cable de servicio → equipo. El adaptador y el ramal del cargador están fuera de la envolvente; permanece un único puerto en el instrumento. No conectar señales USB ni tensión de cargador a los mismos contactos.

En boya: registrador consulta al equipo por RS-485 y transmite mediante su propio enlace. Diseñar el supervisor para responder a estados básicos o programar el despertar cuando la Pi esté apagada; no prometer acceso permanente a archivos de una Pi sin alimentación. La implementación y consumo de reposo se medirán después.

Mantener obligatoriamente espectros crudos y 18 canales en almacenamiento local. Definir exportación de archivos por bloques sobre el mismo enlace, con identificación, comprobación de integridad y reanudación; Modbus no aporta automáticamente un gestor de archivos. Medir el volumen real de espectros/imágenes y tiempo de descarga antes de fijar baud rate. No atribuir a este conector genérico prestaciones USB o Ethernet de alta velocidad. La futura telemetría podrá enviar resúmenes y seleccionar datos crudos sin borrar los originales.

## Alimentación desde boya

`Panel solar → controlador/gestión de energía de la boya → cable → puerto del equipo`.

El panel no se conecta directamente al pack. Una fuente regulada para alimentar la instrumentación y un cargador compatible con la química, número de celdas y BMS del pack son funciones distintas. El rótulo «24 V» no define tensión de carga. Puede resolverlas un sistema integrado compatible, pero no se presupone esa compatibilidad.

Reservar ahora contactos y espacio para entrada externa/gestión de fuentes. Las tensiones admisibles y umbrales se cerrarán con las etiquetas y ficha reales del pack/cargador. D52 propone desconectar ambos hilos de carga con relé normalmente abierto; el relé no sustituye al cargador. La gestión de prioridad de fuentes de boya permanece futura. En el primer prototipo, contactos de funciones aún no implementadas quedarán sin energizar. Esta revisión no recalcula autonomía ni incorpora panel, registrador o radio a la compra actual.
