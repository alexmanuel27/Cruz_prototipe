> **Actualización D52, 30 oct 2026:** Alex sustituye la halógena por el Nichia Optisolis blanco. Las referencias y cálculos anteriores con halógena se conservan como antecedente; no describen la fuente ni el presupuesto final. Ver [propuesta eléctrica del 30 de octubre](../archivo/electronica/DISENO_ELECTRICO_V1.md). No se recalcula autonomía en esta revisión.

# Presupuesto energético conservado

**Trasladado de la lista amplia el 30 de octubre de 2026; sin recalcular.** La [lista de compra vigente](../compras/LISTA_COMPRA.md) contiene únicamente los faltantes definidos por Alex.


**Conservado sin recalcular por indicación de Alex.** El presupuesto previo no incorpora todavía la cámara auxiliar USB E14; no se presenta como cálculo completo actualizado con esa cámara.

Datos del anuncio C01: Li-ion, **24 V / 3 Ah / 72 Wh declarados**, BMS contra sobretensión, descarga profunda, cortocircuito y temperatura; uso indicado **1–3 A**; dimensiones **70 × 37,5 × 56 mm**, peso neto descrito 278 g. Son datos del vendedor, pendientes de recepción y ensayo. Otra tabla indica 157 g: registrar el peso real. No hay en el texto consultado una especificación suficiente de corriente continua/pico del BMS, número de celdas, tensión máxima/mínima ni salida del cargador.

Antes de comprar los DC/DC y el driver: fotografiar etiquetas de pack/cargador, comprobar polaridad DC5521, tensión a plena carga y límites documentados. Ensayar arranque de Pi, bomba y fuentes con el pack. El conector DC5521 suministrado queda **dentro de la envolvente seca**; no sirve como conector exterior sumergible. Usar el cargador del kit por el puerto de carga previsto; no conectar una fuente genérica de 24 V como cargador. Adaptar después la conexión al único puerto exterior de carga/datos.

Presupuesto acordado para **un ciclo cada 15 min**, todavía sin mediciones eléctricas:

| Carga | Hipótesis por ciclo | Wh en 24 h / 96 ciclos | Wh en 72 h / 288 ciclos |
|---|---|---:|---:|
| Bomba | 20 W × 30 s | 16,00 | 48,00 |
| Halógena | 10 W × 5 s | 1,33 | 4,00 |
| Cinco LED en total | Cada uno 4 V × 100 mA × 5 s | 0,27 | 0,80 |
| Pi + cámara | 5 W × 90 s; alimentación cortada entre ciclos tras apagado ordenado | 12,00 | 36,00 |
| **Subtotal** | **0,3083 Wh/ciclo; media 1,233 W** | **29,60** | **88,80** |

Los cinco LED incluyen el de 430 nm; longitudes de onda y secuencia de los otros cuatro pendientes. Estos tiempos son hipótesis energéticas, no estabilizaciones ópticas demostradas.

Con los **72 Wh declarados**, el cociente ideal es **58,4 h**. Aplicando una sola vez 20 % de reserva y rendimiento supuesto de conversión de 85 %: `72 × 0,80 × 0,85 = 48,96 Wh`, equivalentes a **39,7 h** con esas cuatro cargas. **Faltan** supervisor/RTC, AS7265x, reposos de convertidores/driver, sensores y posibles diferencias de consumo: la autonomía real será menor. Si la etiqueta nominal resulta ser 22,2 V × 3 Ah = 66,6 Wh, el mismo cálculo baja a **36,7 h**. Medir capacidad útil y energía por ciclo antes de prometer duración.

La batería pequeña es la elección para el primer prototipo por precio y plazo. **No demuestra el objetivo original de 72 h**; ese requisito queda como ampliación pendiente para esta configuración. El ensayo de campo de varias horas sigue siendo el primer objetivo operativo.

