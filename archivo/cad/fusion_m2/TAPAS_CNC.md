# Tapas de acrílico para CNC — revisión 2026-11-03

Revisión vigente: `CROSS_TAPAS_10MM_RANURA_3MM_2026-11-03.f3d`. Sustituye las propuestas de tapas de 15, 16 y 18 mm.

## Geometría acordada

| Característica | Dimensión nominal |
|---|---:|
| Material y espesor total de cada tapa | PMMA, 10 mm |
| Diámetro de tapa | 230 mm |
| Ranura anular en la cara interior de ambas tapas | 3 mm de profundidad |
| Diámetros interior / exterior de ranura | 168,8 / 181,2 mm |
| Ancho radial de ranura | 6,2 mm |
| Espesor residual bajo la ranura | 7 mm |
| Junta plana de silicona: ID / OD / espesor libre | 170 / 180 / 3 mm |
| Espesor de junta en el montaje nominal | 2,55 mm |
| Compresión nominal de junta | 15 % |
| Entrada del extremo del tubo en la ranura | 0,45 mm |
| Cuatro varillas M8: longitud de corte provisional | 420 mm |
| Cuatro separadores de compresión: OD / ID / largo | 14 / 9 / 376,1 mm |

El tubo conserva sus extremos planos y su geometría 180/170 × 380 mm. La junta no queda completamente escondida sin comprimir: el tubo entra 0,45 mm en la ranura de 3 mm y deja 2,55 mm entre su extremo y el fondo de la ranura. La holgura radial nominal entre tubo y ranura es 0,6 mm a cada lado.

Las arandelas interiores apoyan en la cara interior de las tapas; los separadores se han acortado. No hay rebajes de arandela que comuniquen con la ranura de sellado. Arandelas exteriores, tuercas y conectores se han recolocado. Los extremos del chasis dejan 0,5 mm frente a las tapas y la bandeja tiene alivios para los racores.

## Preparación en Fusion

- Componentes: `E02 FRONT PMMA cap 10mm; gasket groove 3mm` y `E03 REAR PMMA cap 10mm; gasket groove 3mm`.
- Cada ranura tiene croquis acotado y operación de corte editable. Parámetros: `M2_Cap_thickness`, `M2_Groove_depth`, `M2_Groove_ID`, `M2_Groove_OD`.
- Los cambios de parámetros no regeneran automáticamente todos los cuerpos ni el cierre. Recalcular la geometría de componentes afectados y comprobar interferencias.
- Fuentes de esta corrección: `ranuras_tapas.py` y `holguras_tapas_10mm.py`. El primer script parte de la copia intermedia de 16 mm y solo se ejecuta una vez; no ejecutarlo sobre el montaje ya corregido.
- El taladrado y los alojamientos de conectores ya están representados. La reserva EN3 conserva 4 mm de pared local, distintos de los 7 mm bajo la junta. Los detalles de los pasamuros siguen pendientes de cotejar con las piezas comerciales.

La preparación CAM queda para la fase de mecanizado: medir espesor real y planitud de la placa disponible, verificar referencias comerciales y tolerancias, definir máquina, herramienta, sujeción y ceros, y simular las trayectorias antes de generar el programa CNC. No se ha generado código de máquina.

## Comprobación y límites

`COMPROBACION_TAPAS_10MM_2026-11-03.json`: 185 cuerpos, cero interferencias volumétricas no previstas y ocho intersecciones nominales de roscas simplificadas. El tubo no cambió. Este resultado comprueba el encaje de las geometrías modeladas; no valida resistencia a presión, tolerancias reales ni estanqueidad. Las tapas de 10 mm necesitan ensayo con lastre y sin electrónica antes de una inmersión operativa.

El documento activo de Fusion tiene cambios sin guardar; el F3D indicado al principio es la copia exportada de esta revisión.
