# Vista explosionada para inspección

`CROSS_M2_EXPLOSIONADO_ESTUDIO.f3d` contiene una vista editable con los conjuntos separados para facilitar la inspección. Las tapas y juntas se desplazan a lo largo del tubo; el propio tubo, la placa, los sensores ópticos, la hidráulica, las referencias electrónicas y los cierres se separan como grupos. Las mangueras no parecen conectadas en esta vista porque se han movido sus conjuntos: para ver el recorrido previsto abrir `CROSS_M2_ANTES_EXPLOSIONADO.f3d`.

`Cruz_explosionado_general.png` es la vista general y `Cruz_explosionado_optica_hidraulica.png` muestra solo óptica e hidráulica. Conductividad y temperatura siguen representadas como envolventes provisionales.

La vista abierta se ha separado mediante posiciones de los componentes; **no es una animación de montaje ni comprueba ajustes**. La revisión anterior detectó interferencias de las mangueras con PCB y bandeja, pendientes de resolver. Este modelo no está listo para fabricar.

El archivo `restaurar_posiciones_explosionado.json` conserva las matrices anteriores; `restaurar_montaje_explosionado.py` puede ejecutarse con la API de Fusion en el documento original si se quiere restaurarlas. Hay que conservar previamente los cambios posteriores a la explosión; el script puede sobrescribir cambios de posición. La copia anterior al explosionado es la opción más simple para volver al montaje inicial. El documento original quedó con cambios sin guardar.
