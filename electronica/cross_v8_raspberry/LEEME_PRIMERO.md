# PCB V8 · esquema reorganizado y placa sin trazado

**Estado vigente: 22/11/2026.** Por indicación de Alex se ha retirado todo el trazado y descartado la revisión con puentes de cable.

- [Proyecto KiCad](cross_v8_draft.kicad_pro) · [esquema](cross_v8_draft.kicad_sch) · [PCB](cross_v8_draft.kicad_pcb).
- 122 posiciones originales, incluidas dos DNP. Sin W1–W57 ni redes auxiliares `__WIRE_`.
- PCB: **0 pistas, 0 vías y 0 zonas de cobre**. Contorno de 132 × 102 mm y componentes conservados. **301 conexiones pendientes de trazar.**
- Esquema: bloques funcionales numerados con la disposición de Alex, ampliada para potencia óptica y alimentación/aislamiento de sensores. **Conexiones internas mediante líneas; una etiqueta por red y bloque únicamente para las conexiones entre bloques.** U7 está en conversión de alimentación; EC-OEM y su conector de sonda están con el aislamiento EC.
- Comprobación: ERC sin incidencias; DRC sin infracciones geométricas y sin diferencias esquema–PCB. Las 409 conexiones de pines originales se conservan.
- [Informes y vista del esquema](../reorganizacion_2026-11-22/).
- [Contrato GPIO y resultados de banco](REVISION_BANCO_2026-11-21.md#tabla-vigente-para-software).

Los dos DC/DC principales siguen externos y cableados; la Pi recibe 5 V por su alimentación USB-C. J1.2/J1.4 quedan sin conectar. Se conservan U11 SN74CBTLV3125D y las huellas de componentes de la revisión anterior.

La revisión de fabricación con 87 cables y su ZIP CNC están descartados y respaldados fuera del proyecto activo. **Esta PCB está sin rutear y no está lista para fabricar.** Se mantiene como requisito futuro una sola cara de pistas para la Bantam, con fresa prevista de 0,3 mm; dimensiones útiles y sujeción reales por confirmar. Continúan pendientes las protecciones, corriente del motor, arranque/apagado y térmica.
