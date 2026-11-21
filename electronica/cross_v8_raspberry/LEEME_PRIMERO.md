# PCB V8 · revisión vigente

La V8 tiene **colocación y trazado completos** dentro de 170 × 68 mm: 122 huellas, dos capas, planos de masa separados para conductividad y ambos DC/DC principales **externos y cableados**, según confirma Alex. Batería→5 V para Pi y batería→12 V para óptica en paralelo. No alimentar la Pi a 12 V.

**Estado: prototipo pendiente de liberación eléctrica y mecánica; no fabricar ni energizar el conjunto todavía.** Faltan cerrar protecciones/fusibles, corriente por fase, encendido/apagado autónomo, térmica y encaje con piezas reales. El trazado completo no resuelve estos puntos.

- [Abrir proyecto KiCad](cross_v8_draft.kicad_pro), [esquema](cross_v8_draft.kicad_sch), [PCB trazado](cross_v8_draft.kicad_pcb).
- [Revisión de cierre, alimentación, montaje, vistas y pendientes](CIERRE_PCB_2026-11-21.md).
- [Contrato de GPIO y resultados de banco conservados](REVISION_BANCO_2026-11-21.md#tabla-vigente-para-software).
- [Informes ERC/DRC, BOM, conexiones, posiciones y STEP](../cierre_pcb_2026-11-21/).
- [Bibliotecas locales](Cross.pretty/) y [archivo histórico](../../archivo/electronica/cross_v8_raspberry/).

| Comprobación · KiCad 9.0.7 · 21/11/2026 | Resultado |
| --- | --- |
| DRC | 0 errores y 0 avisos |
| Conexiones por rutear | 0 |
| Paridad esquema–PCB | 0 diferencias |
| ERC | 0 errores y 0 avisos |
| Comprobación del contrato de redes | Correcta |

El aislamiento antes virtual es ahora U13 **RECOM R05CT05S** + U15 **ISO1540D**; ambos deben adquirirse y cotejarse físicamente. U4 pasa a un pequeño **R-78HE5.0-0.3** permanente en placa, otra pieza adicional. U5/U6 son bornas para los dos convertidores principales fuera de placa. La BOM no acredita disponibilidad.

Pi 5, halógena 12 V/10 W, azul/naranja con LM317 y red de 10,4 Ω; IR con 220 Ω/1 W. Cuatro órdenes activas altas más OPT_ARM BCM21/pin 40. J1 es IDC40 de señales con pines 2/4 sin conectar; alimentación Pi por J23/cable USB-C. Parte de los pasivos se monta en la cara inferior: comprobar espacio en bandeja. No hay fijaciones nuevas definidas.

Alex transcribe pack 24 V/3 Ah, entrada 25,2 V y salida 22–25 V (5–8 A); cargador 25,2 V/2 A; motor Kamoer 24 V/20 W. Máximo medido, comportamiento del BMS, transitorios y corriente nominal por fase siguen pendientes. F1/F2 no tienen calibre liberado. HOLD_PI alto solicita corte; CD4013 carece de estado inicial garantizado y SET mantenido puede impedir apagar. No hay detector de fuga ni watchdog externo integrado.
