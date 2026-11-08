# V7: estudio eléctrico y ubicación provisional — NO FABRICAR

Esta versión no es una placa terminada ni apta para energizar o importar como montaje definitivo a Fusion. El esquema generado presenta conexiones eléctricas no deseadas; **no debe actualizarse la placa a partir del esquema actual**. La placa conserva la red prevista por el generador, pero no está ruteada ni verificada. Hay 93 incidencias ERC, 57 incidencias DRC, 199 conexiones sin trazar y 114 discrepancias entre esquema y placa. Consultar los informes adjuntos. El generador es solo una ayuda de exploración, no un diseño validado.

## Qué se ha explorado

- Tres módulos DFR1015 separados: 5 V siempre disponible, 5 V para la Raspberry y 9 V para óptica. La entrada del fabricante es de 7,5–30 V; también recomienda funcionar por debajo de 24 V. Con el cargador indicado de 25,6 V falta medir el pack, transitorios y temperatura de los módulos en la carcasa cerrada. La huella y los soportes son aproximados, pendientes de medición física; las envolventes 3D no son el modelo certificado del fabricante.
- Contacto magnético normalmente abierto a través de la carcasa, reloj de alarma y biestable CD4013 para mantener el encendido durante el arranque. Es una propuesta sin verificar: el estado al conectar la batería, el reset al apagar y el caso de alarma y reset simultáneos deben resolverse y probarse. El reloj y parte del circuito permanecen alimentados en espera; el contacto magnético no es una desconexión total de seguridad. La Raspberry requiere software de apagado ordenado, control de alarma y una señal final de apagado: no está implementado.
- Interruptor de potencia externo previsto mediante J14/J11/J26, sin módulo instalado ni huella física confirmada. No hay continuidad de alimentación entre J14 y J11 sin el circuito externo correcto. No alimentar la placa.
- Detección del cable de servicio y propuesta de bloqueo por hardware del relé de carga sin presencia del cable. No se ha validado el circuito ni la polaridad de los 8 contactos, el cargador, los fusibles ni el comportamiento con la batería descargada; no conectar el cargador.
- Interfaces propuestas para RS-485, conductividad, temperatura, fluorómetro y control del LED azul. El controlador LED, el módulo RS-485 y el reloj no están integrados como modelos y huellas definitivas; las salidas deben comprobarse. El detector de fuga aún no está implementado. El contacto de señal y el aislamiento físico de la cámara y de sus cables también requieren revisión.
- La alimentación de la Raspberry por USB-C se representa como conector genérico: cable, negociación y caída de tensión están pendientes. El motor A4988 requiere comprobar corriente por fase, resistencia de sensado, ajuste, refrigeración y orden de pines del módulo real.

## Próximos pasos

1. Corregir el esquema y comparar cada conexión exportada con la red prevista, sin cortocircuitos accidentales; eliminar errores ERC reales.
2. Completar y verificar el circuito de arranque/apagado, el interruptor de potencia, la carga y la detección de fuga. Definir los estados seguros y el firmware de control.
3. Confirmar dimensiones, orientación, conexiones y corriente admisible de cada módulo, portafusibles, conectores y modelos 3D. Confirmar el cable USB-C y las fuentes de 5/9 V bajo carga.
4. Colocar, rutear, revisar anchuras de pista, separaciones, DRC y paridad con el esquema. Después generar el modelo 3D para que Alex compruebe el encaje en Fusion.
5. Solo tras la revisión eléctrica y las pruebas de banco, preparar fabricación y montaje. No se han realizado ensayos físicos ni de estanqueidad.

Referencias: [DFRobot DFR1015](https://www.dfrobot.com/product-2599.html), [Pololu 2814](https://www.pololu.com/product/2814), [DS3231](https://www.analog.com/media/en/technical-documentation/data-sheets/DS3231.pdf).
