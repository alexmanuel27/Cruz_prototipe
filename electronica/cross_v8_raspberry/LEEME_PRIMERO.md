# PCB V8 · esquema reorganizado y placa sin trazado

**Estado vigente: 22/11/2026.** Por indicación de Alex se ha retirado todo el trazado y descartado la revisión con puentes de cable.

- [Proyecto KiCad](cross_v8_draft.kicad_pro) · [esquema](cross_v8_draft.kicad_sch) · [PCB](cross_v8_draft.kicad_pcb).
- 95 posiciones, incluidas dos DNP. Sin W1–W57 ni redes auxiliares `__WIRE_`. Sensores alimentados desde los 3V3 de Raspberry, según la prueba y decisión de Alex. C8/C9 se conservan como desacoplos.
- PCB: **0 pistas, 0 vías y 0 zonas de cobre**. Contorno de 132 × 102 mm; **219 conexiones pendientes de trazar.**
- Esquema: bloques funcionales numerados con la disposición de Alex, ampliada para potencia óptica e I²C de sensores. **Líneas para conexiones locales legibles y etiquetas para alimentación/masa compartida, señales largas y enlaces entre bloques.** El EC-OEM y su conector de sonda están en el bloque de conductividad.
- Comprobación: ERC sin incidencias; DRC sin infracciones geométricas y sin diferencias esquema–PCB. Verificado el contrato de conexiones del mando óptico directo, EC en I²C común y alarma del DS3231 en J24.5.
- Símbolos GND triangulares como el elegido por Alex; símbolos de alimentación con rótulos visibles `5V`, `3V3` y `12V`. La rama permanente de 5 V alimenta el RTC y el encendido. Los sensores usan 3,3 V de Pi.
- [Informes y vista del esquema](../reorganizacion_2026-11-22/).
- [Contrato GPIO y resultados de banco](REVISION_BANCO_2026-11-21.md#tabla-vigente-para-software).

J13 recibe **SYS+/SYS− del gestor externo de carga y alimentación**, que tiene conexiones propias para la fuente DC y el pack. Se retiraron el relé K1 y su circuito de carga de la PCB. F1 protege la entrada del instrumento según su calibre pendiente. El gestor debe alimentar el equipo y gestionar la corriente de carga de forma independiente. El MPPT futuro se integra fuera de esta placa con una interfaz compatible con el gestor. La tensión, potencia y continuidad de SYS quedan por validar con el gestor elegido. El divisor de J7 mide SYS conmutado.

U7 queda retirado. En el lado común, los 3V3 vienen de la Raspberry. El RTC en J24 y el biestable U8 se alimentan con los 5 V permanentes de U4. El módulo DS3231 de Alex expone INT/SQW, que corresponde a J24.5 (WAKE_N); verificar el orden real de sus contactos. U16 adapta la orden de corte de J1.37 de 3,3 V a 5 V. El EC-OEM recibe 3V3 de la Pi y comparte SDA, SCL y GND. La sonda queda conectada a PRB/PRBG. R26/R27 siguen como pull-ups opcionales DNP. J1.18 queda libre y J1.22 conserva la lectura del piloto, sin despertar el equipo al detectar el cargador.

Los pines físicos 15, 16, 36 y 38 mandan las puertas de los IRLZ44N a 3,3 V a través de 470 Ω y cada puerta tiene su pull-down. El pin 40 queda libre. Queda por ensayar el arranque en frío y la temperatura de la halógena con mando directo, y comprobar en agua las lecturas EC con el montaje completo.

Los dos DC/DC principales siguen externos y cableados; la Pi recibe 5 V por su alimentación USB-C. J1.2/J1.4 quedan sin conectar. El I²C y el 1-Wire llegan directamente a los sensores.

La revisión de fabricación con 87 cables y su ZIP CNC están descartados y respaldados fuera del proyecto activo. **Esta PCB está sin rutear y no está lista para fabricar.** Se mantiene como requisito futuro una sola cara de pistas para la Bantam, con fresa prevista de 0,3 mm; dimensiones útiles y sujeción reales por confirmar. Continúan pendientes las protecciones, corriente del motor, arranque/apagado y térmica.
