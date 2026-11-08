# Pasamuros profesionales y ensuciamiento — revisión para discutir

**21 de octubre de 2026.** Recomendaciones pendientes de selección y ensayo; no son decisiones de compra ni modificaciones del CAD. No cambia el presupuesto energético.

## Pasamuros candidato

[WetLink Penetrator JPT de Blue Robotics](https://bluerobotics.com/store/cables-connectors/penetrators/wetlink-penetrator-jpt/) permite pasar tubo continuo y trae los elementos de sellado de panel. Precio consultado: **13 USD/unidad**. Candidato para OD5: **BR-107163-155, M10, 5.5 HC, rango 4,7–5,3 mm**. El fabricante contempla tubos rígidos/flexibles, pero exige validar la configuración concreta. Es una familia distinta del WetLink estándar.

Para H1/H2 estudiar dos unidades, 26 USD de catálogo. Confirmar material, diámetro real, deformación, caudal bajo succión y espesor admisible de tapa antes de elegir. La coincidencia de diámetro no demuestra que una manguera peristáltica blanda funcione sin estrangularse. Puede necesitarse un tramo compatible para atravesar la tapa y conexión interior al circuito. No se prescribe material de ese tramo sin su ficha.

El tubo continuo evita una unión de espiga justo en la pared. Debe tener retención exterior e interior; la capacidad del pasamuros no acredita la resistencia del tubo de PMMA ni de la tapa. Los bocetos de puertos siguen siendo reservas de espacio; no se convierten en planos de taladro por encontrar este candidato. I01 sigue siendo el único conector eléctrico de carga/datos; estos dos pasos son hidráulicos.

## Qué aporta el cobre

YSI comercializa una [guarda de aleación de cobre](https://www.ysi.com/accessory/id-599563/exo1-anti-fouling-guard) y documenta [cinta, mallas y limpieza mecánica](https://www.ysi.com/ysi-blog/water-blogged-blog/2019/01/7-tips-to-fight-fouling-and-extend-water-quality-sonde-deployments). Son precedentes de protección exterior, no prueba de duración para nuestro circuito.

Propuesta: estudiar una pieza de cobre desmontable alrededor de la zona de visión de la cámara auxiliar, sin cubrir la vista. Separarla eléctricamente de piezas metálicas susceptibles de formar un par galvánico. La eficacia sobre la superficie transparente vecina debe ensayarse; una anilla no garantiza una ventana limpia. Evitar adhesivos sobre PMMA sin verificar compatibilidad.

## Integridad de la muestra

No recomendar cobre, latón o pintura biocida en las superficies interiores de toma, conductos o cubeta de esta primera versión. También evitar de entrada una rejilla de cobre inmediatamente delante de la aspiración: el agua que llega a la cubeta podría haber estado en contacto con ella.

La precaución es por posible alteración de la muestra: [Pérez y colaboradores (2006)](https://pubmed.ncbi.nlm.nih.gov/16494234/) observaron cambios de eficiencia fotoquímica en fitoplancton natural expuesto a cobre. [Reiriz y colaboradores (1994)](https://pubmed.ncbi.nlm.nih.gov/7873102/) observaron cambios de fluorescencia no equivalentes a cambios de contenido de clorofila bajo sus condiciones experimentales. Estos estudios no cuantifican cuánto liberaría una pieza nuestra ni el sesgo que tendría el AS7265x. La recomendación de separar cobre y circuito es una inferencia de diseño para reducir ese riesgo, pendiente de validación si se quiere usar allí.

## Tres problemas distintos

| Zona | Propuesta inicial | Límite |
|---|---|---|
| Exterior y visión de cámara | Protección de cobre desmontable por estudiar; inspección y limpieza accesible | No garantiza protección de toda la ventana ni del interior de cubeta |
| Toma y mangueras | Rejilla gruesa compatible, recorridos cortos y desmontables, sin rincones innecesarios | No usar filtro fino que cambie la fracción biológica medida |
| Cubeta y conductos internos | Renovación por varios volúmenes antes de medir y limpieza al recuperar | La renovación arrastra agua anterior y parte de sedimento suelto; no elimina biofilm adherido |

No introducir depósito de blanco, desinfectante o ciclo químico automático por esta discusión. El blanco sigue siendo previo al despliegue y se conserva en memoria.

## Ensayo mínimo a proponer

Comparar un montaje protegido exteriormente y otro testigo, con agua y exposición equivalentes. Registrar fotografías de toma, campo visual y cubeta, caudal o volumen por tiempo y cambios ópticos. Contrastar antes/después con material de referencia o una muestra común recién medida, sin asumir que el agua almacenada sigue idéntica varios días. Si se ensaya cobre en contacto con la muestra, añadir un control sin cobre y, si es posible, determinación de cobre disuelto; una lectura estable por sí sola no demuestra ausencia de alteración.

No fijar un intervalo de mantenimiento de semanas sin ese ensayo. La prioridad del prototipo sigue siendo función, cierre estanco y ensayo sin electrónica del 30 de octubre.
