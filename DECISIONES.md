# Registro de decisiones de ingeniería

**Inicio: 26 de septiembre de 2026. Revisión: 27 de septiembre de 2026.**

Estados: **fijada por Alex**, **recomendación pendiente de ensayo**, **alternativa descartada para esta versión** y **pendiente de cierre**. Una recomendación escrita por el asistente no equivale a aprobación experimental o autorización de fabricación. La especificación funcional ha sido aprobada. Diseño óptico detallado en curso.

| ID | Estado | Decisión y motivo | Alternativa y razón para descartarla o mantenerla abierta | Evidencia / fecha de cierre |
|---|---|---|---|---|
| D01 | Fijada por Alex | Repositorio exclusivamente de ingeniería de Cruz; entrega funcional el 1 dic | Artículo de Cruz queda para otro repositorio y periodo | Instrucción del 26 sep; P3 |
| D02 | Fijada por Alex | Conservar los dos detectores y las fuentes originales | Detector único AS7265x pierde detalle espectral; cámara única no tiene sensibilidad suficiente según experiencia reportada | Análisis documental; verificar rendimiento conjunto en X1.2 |
| D03 | Fijada por Alex | Compartir celda (cuarzo comprada) y alternar fuentes | Celda de cuarzo comprada y geometría fijada en 4 brazos. | OPT-06, cierre 12 oct |
| D04 | Fijada por Alex | Mantener disposición colineal para excitación a 430 nm y detección fluorescente | La geometría en cruz de cuatro brazos acomoda esta disposición ya existente en el fluorómetro anterior | Confirmación de Alex |
| D05 | Fijada por Alex | Cambiar excitación a 430 nm | Fijada por Alex: LED azul de 430 nm | OPT-03/04 |
| D06 | Fijada por Alex | Rendija confirmada en 0,5 mm de ancho y a 60 mm de la cámara | Eliminada la incertidumbre sobre la dimensión de 5 mm | Confirmación de Alex |
| D07 | Fijada por Alex | Guardar 18 canales y señal de cámara original | Decisión: Guardar obligatoriamente el espectro crudo de cámara como intensidad por píxel antes de calibración/correcciones, además de los datos derivados. | Firmware existente; X3 y calibración |
| D08 | Fijada por Alex | Celda llena. Entrada por una cara, salida por otra. | Hidráulica fijada: celda y conductos llenos, bombear volumen efectivo varias veces. Eliminar caudalímetro. | HID-01…05 |
| D09 | Fijada por Alex | Se usará una bomba peristáltica sumergida instalada después de la celda (aguas abajo) | Orden hidráulico fijado: toma del lago -> celda de cuarzo/zona óptica -> bomba peristáltica sumergida -> descarga. La muestra se mide antes de pasar por la bomba. | Instrucción del usuario; HID-04/05 |
| D10 | Fijada por Alex | Sin bolsa ni selector de blanco automático dentro del equipo. El blanco de transmisión se mide antes del despliegue y se guarda en memoria. | Se advierte de deriva; la validez temporal del blanco predespliegue se comprobará en ensayo y al recuperar el equipo. Los oscuros se mantienen | Instrucción del 26 sep; ajustar calendario |
| D11 | Alternativa descartada para esta versión | Toma de agua natural sin filtración fina | Filtro de 0,45 µm eliminaría fracciones de interés y convertiría la muestra en otra distinta | Protocolo de campaña; definir rejilla gruesa en X1.3 |
| D12 | Fijada por Alex | Objetivo mecánico: imprimir en 3D todo o casi todo el cuerpo. | Las piezas impresas constituirán la barrera hidráulica prevista y deben diseñarse y validarse como tal (juntas, pasamuros, estanqueidad), no como simples soportes. | Instrucción del 26 sep |
| D13 | Fijada por Alex | Ensayo sin electrónica el 30 oct; reparar antes de instalarla si falla | Posponer detección de fugas hasta noviembre amenaza el plazo y el hardware | EST-01 obligatorio |
| D14 | Fijada por Alex | Objetivo 72 h a 15 min y profundidad inicial 1 m | «Días» sin cadencia/profundidad no permite dimensionar; 7 días quedan como ampliación | Cerrar objetivos 6 oct; demostrar con AUT-01 |
| D15 | Pendiente de cierre | Comparar Pi continua con batería mayor frente a apagado ordenado por supervisor | No escoger ahorro teórico sin medir arranque, estabilización y pérdidas; tampoco sustituir lámpara para ocultar consumo | Balance medido, 20–23 oct |
| D16 | Fijada por Alex | Funcionamiento autónomo sin navegador | Se requiere un servicio de adquisición autónomo; la dependencia del navegador queda descartada | Confirmación de Alex |
| D17 | Fijada por Alex | Calibración en fichero, con procedimiento para otro operador | Coeficientes incrustados impiden recalibrar sin recompilar y rompen trazabilidad | Especificación, §8 |
| D18 | Alternativa descartada para esta versión | Reportar espectro, RFU y clorofila solo cuando validada | Concentraciones directas de nutrientes, A254, NTU/FNU o CDOM a partir de esta configuración no están demostradas | Protocolo congelado de campaña |
| D19 | Recomendación pendiente de ensayo | Reservar fracciones de octubre y repetir referencia junto a Cruz en noviembre | Una concentración histórica no certifica estabilidad biológica/química semanas después | Validación, §5 |
| D20 | Fijada por Alex | Óptica fijada (celda cuarzo comprada, LED 430, lente gran angular) | Celda ya comprada, filtro óptico eliminado del diseño base. | Acta óptica requerida, 12 oct |
| D21 | Fijada por Alex | Fotografías reales durante cada fase | No se pueden reconstruir juntas/cableado ocultos al documentar meses después | Registro de ensayos y fotos |

| D22 | Fijada por Alex | Secuencia: transmisión primero y fluorescencia después | Orden fijado por Alex; OPT-06 comprobará si la transmisión previa altera la fluorescencia y fijará tiempos de espera si fueran necesarios. | Instrucción del 26 sep |
| D23 | Fijada por Alex | Magnitudes de octubre | Otras magnitudes sugeridas podrán incorporarse después, no quedan descartadas permanentemente (fuera de alcance inicial hasta que haya señal/referencia). | Instrucción del 26 sep |
| D24 | Modelo M1 provisional | Tres cavidades secas impresas: cabezal óptico en cruz con cubeta desmontable, caja de batería/electrónica y cápsula independiente para bomba | Dejar la bomba IP31 expuesta bajo el agua es incompatible con su ficha; ubicarla con la batería agravaría una fuga de tubo | [CAD M1](cad/README.md), 30 sep; comprobar medidas y EST-01 |
| D25 | Modelo M1 provisional | Junta plana de silicona cortada para cada tapa, tornillos fuera de cavidad y racores estáticos comerciales | Una simple unión de dos piezas FDM o una junta impresa no acredita estanqueidad a 1 m | [CAD M1](cad/README.md); cerrar juntas/racores en X1.3 |
| D26 | Modelo M1 provisional | Cubeta de cuatro caras NEXACULE 3,5 ml/10 mm, variante 46090230005978; bomba Denash B0FRB83924 | La ficha de venta no aporta todas las tolerancias ni demuestra caudal sumergido; medir ambas piezas antes de fabricar | [Ficha y cotas pendientes](cad/README.md); X1.3/HID-01 |

## Acta de cierre de óptica

**Estado actual: cerrado.**
Geometría: 4 brazos (transmisión en un eje, fluorescencia colineal LED 430->muestra->AS7265x en otro).
Fuente fluorescencia: LED azul de 430 nm.
Lente: Gran angular confirmada.
Alcance: 420-780 nm.
Celda: Flujo de cuarzo comprada.
Filtro óptico: Eliminado del diseño base (señal en 435 nm es excitación, resto cero, 645 nm es fluorescencia).

## Cómo registrar una revisión

Añadir fecha, decisión anterior, nueva decisión, motivo, evidencia, datos ya conocidos, archivos afectados y ensayos que deben repetirse. Mantener el historial mediante Git y el acta correspondiente; no borrar un fallo ni presentarlo como ensayo pendiente.
