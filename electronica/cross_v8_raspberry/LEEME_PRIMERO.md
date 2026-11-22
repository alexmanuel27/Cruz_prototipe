# PCB V8 · esquema reorganizado y placa sin trazado

**Estado vigente: 22/11/2026.** Por indicación de Alex se ha retirado todo el trazado y descartado la revisión con puentes de cable.

- [Proyecto KiCad](cross_v8_draft.kicad_pro) · [esquema](cross_v8_draft.kicad_sch) · [PCB](cross_v8_draft.kicad_pcb).
- 121 posiciones tras retirar U10, incluidas dos DNP. Sin W1–W57 ni redes auxiliares `__WIRE_`. Sensores alimentados desde los 3V3 de Raspberry, según la prueba y decisión de Alex. C8/C9 se conservan como desacoplos.
- PCB: **0 pistas, 0 vías y 0 zonas de cobre**. Contorno de 132 × 102 mm; U10 retirado. **298 conexiones pendientes de trazar.**
- Esquema: bloques funcionales numerados con la disposición de Alex, ampliada para potencia óptica y alimentación/aislamiento de sensores. **Líneas para conexiones locales legibles y etiquetas para alimentación/masa compartida, señales largas y enlaces entre bloques.** U7 está en conversión de alimentación; EC-OEM y su conector de sonda están con el aislamiento EC.
- Comprobación: ERC sin incidencias; DRC sin infracciones geométricas y sin diferencias esquema–PCB. Verificados los 404 pines restantes: los únicos cambios eléctricos son retirar U10 y unir la antigua rama de sensores a 3V3_PI.
- Símbolos GND triangulares como el elegido por Alex; símbolos de alimentación con rótulos visibles `5V`, `3V3` y `12V`. Se conservan separadas las ramas permanente, Pi y EC aislada.
- [Informes y vista del esquema](../reorganizacion_2026-11-22/).
- [Contrato GPIO y resultados de banco](REVISION_BANCO_2026-11-21.md#tabla-vigente-para-software).

Los dos DC/DC principales siguen externos y cableados; la Pi recibe 5 V por su alimentación USB-C. J1.2/J1.4 quedan sin conectar. Se conservan U11 SN74CBTLV3125D y las huellas de componentes de la revisión anterior.

La revisión de fabricación con 87 cables y su ZIP CNC están descartados y respaldados fuera del proyecto activo. **Esta PCB está sin rutear y no está lista para fabricar.** Se mantiene como requisito futuro una sola cara de pistas para la Bantam, con fresa prevista de 0,3 mm; dimensiones útiles y sujeción reales por confirmar. Continúan pendientes las protecciones, corriente del motor, arranque/apagado y térmica.
