# Referencias 3D del PCB V4

Actualizado el 2 de noviembre de 2026. Los modelos se asignaron a las huellas del [PCB editable](../cross_v4_draft.kicad_pcb), y se exportó un STEP para el montaje de Fusion. Los modelos apoyan el estudio de espacio; no aprueban el circuito ni constituyen dimensiones medidas de los componentes comprados.

| Elemento | Archivo | Procedencia y alcance |
|---|---|---|
| K1, relé Omron G2RL-2 | `KiCad_Omron_G2RL_DPDT.step` | Modelo de la familia DPDT G2RL incluido en KiCad (`Relay_THT.3dshapes/Relay_DPDT_Omron_G2RL.step`), de kicad StepUp, CC BY-SA 4.0 con excepción de KiCad. Se giró 90° para coincidir con la envolvente de la huella. Comprobar la variante física. |
| U1, controlador de motor | `Pololu_A4988_referencia.step` | [STEP oficial Pololu 1182](https://www.pololu.com/product/1182/resources), usado como referencia de geometría. Alex tiene una placa WJMY compatible, no se afirma que tenga componentes y posiciones idénticos. Se han añadido dos modelos de zócalo de la biblioteca KiCad; altura de separación propuesta **8,5 mm**, no medida. Verificar pines, orientación, altura real de los zócalos y disipación. |
| Disipador U1 | `Disipador_A4988_9x9x5_APROX.step` | Bloque de reserva aproximado 9 × 9 × 5 mm, según dimensiones publicadas para el conjunto WJMY; su posición se ha supuesto centrada y se debe verificar. No es el modelo del disipador exacto. |
| F1 y F2 | `Fusible_5x20_envolvente_APROX.step` | Volumen aproximado 22,6 × 7 × 8 mm para reserva, basado en cotas generales de los [clips Littelfuse 111](https://www.littelfuse.com/assetdocs/littelfuse_fuse_clip_111_datasheet?assetguid=b1ca8750-5406-48d2-b921-b86728e90adf) y un fusible 5 × 20. No representa la forma ni asegura la altura exacta de los clips. Tipo y valores aún no seleccionados. |
| Demás huellas ya presentes | Biblioteca 3D de KiCad | Componentes genéricos de las huellas provisionales. La inclusión de un modelo no confirma que sea el componente que se comprará o utilizará. |

## Aún faltan

- Los **tres convertidores DFR1015** no están implementados todavía en el PCB. No se ha encontrado un STEP oficial verificado: el fabricante indica 27 × 20 mm y existen volúmenes aproximados de 27 × 20 × 10 mm en Fusion, pero el paso y posición exacta de conexiones y altura de los zócalos siguen pendientes.
- La [placa Atlas aislada Gen 2](../../../cad/componentes/atlas_isolated_carrier/README.md) cuenta con STEP oficial; su colocación en el zócalo J9 sigue sin verificarse (orientación, altura y soporte). El sensor AS7265x tiene una envolvente de referencia separada en Fusion y se conecta mediante cuatro cables.
- No están diseñados los módulos de encendido autónomo, RS485, alimentación y driver del LED azul ni sus huellas y 3D finales. No puede afirmarse que todos los componentes del instrumento estén modelados.
- Los conectores de PCB y portafusibles son propuestas, no componentes definitivos. Faltan cableado, radios de curvatura, fijaciones de PCB y prueba completa de interferencias.

## Verificación realizada

- El exportador STEP de KiCad terminó sin errores de modelo no encontrado para las huellas colocadas en V4.
- En Fusion se cotejaron las cajas envolventes: modelo de relé y placa A4988 coinciden en planta con sus huellas. Las envolventes aproximadas de los fusibles quedan separadas entre sí por aproximadamente 1,4 mm. Esto no es una comprobación completa de interferencias ni confirma el montaje físico.
- [STEP actualizado de la placa](../../../cad/fusion_m2/PCB_V4_REFERENCIAS_3D_BORRADOR.step), importado en el documento activo `Cross_M2_horizontal_design` como `PCB_V4_REFERENCIAS_3D_BORRADOR`. Se ocultó sin borrar la referencia anterior V4; Fusion conserva cambios sin guardar.
- DRC con paridad tras modificar las referencias 3D: 25 avisos de serigrafía, 106 conexiones sin trazar, cero diferencias de paridad. Sigue siendo **un borrador no fabricable ni energizable**.
