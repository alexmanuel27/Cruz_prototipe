> **Actualización D52, 30 oct 2026:** Alex sustituye la halógena por el Nichia Optisolis blanco. Las referencias y cálculos anteriores con halógena se conservan como antecedente; no describen la fuente ni el presupuesto final. Ver [diseño eléctrico vigente](../archivo/electronica/DISENO_ELECTRICO_V1.md). No se recalcula autonomía en esta revisión.

> **Actualización D55, 21 nov 2026:** la geometría vigente es iluminación común con LED seleccionables, cámara en transmisión y AS7265x a 90°. Las referencias al diseño colineal previo son antecedentes, no una configuración validada.

# Análisis de detectores, óptica y operación in situ

**26 de septiembre de 2026. Análisis previo al diseño; ningún ensayo nuevo realizado.**

## 1. Recomendación

Conservar **cámara para transmisión y AS7265x para fluorescencia**, junto con las fuentes originales. Compartir celda, tiempo de muestreo, hidráulica y registro. Realizar las modalidades sucesivamente, con la bomba detenida y una sola fuente encendida.

La complementariedad tiene fundamento, pero todavía no está demostrada la sensibilidad de la combinación en agua natural. Hay tres condiciones de cierre: integración en celda de cuarzo, verificar relación señal/saturación de los canales 435/645 y comprobar el sellado. Ninguna se resuelve mediante una curva de calibración más flexible.

## 2. Qué se encontró en los proyectos

| Evidencia | Consecuencia para la Cruz |
|---|---|
| [MonoSpectro README](../../MonoSpectro/README.md): OV9281, Pi 4, red de 1000 líneas/mm, cámara a 36°, rendija de 0,5 mm, separación rendija–lente de 60 mm, lámpara halógena de 10 W | El instrumento físico anterior funciona; rendija de 0,5 mm a 60 mm, lente gran angular y alcance definitivo 420–780 nm confirmados |
| README menciona una futura excitación azul de 430 nm | Fuente de 430 nm fijada por Alex |
| [Fluorometer](../../Fluorometer/Spectro18_V_Flu/Spectro18_V_Flu.ino): AS7265x y ESP32, diez lecturas, solo canales 435 y 645 nm guardados, ecuación fija de clorofila | Reutilizar control y lectura; cambiar la adquisición a 18 canales y calibración externa cuando llegue X3 |
| [Calibración histórica](../../publication%20plan/Chlorophyll_Fluorometer/data_results/calibration.py) etiqueta clorofila en µg/mL | Trazar unidades y factores de extracción. µg/mL de extracto no equivale a µg/L de agua |
| [MonoSpectro app.py](../../MonoSpectro/app.py): captura dentro del generador de vídeo; [script.js](../../MonoSpectro/static/script.js): blanco y absorbancia en navegador | Se necesita un servicio de adquisición autónomo y persistencia de blancos en el equipo |

La excitación de 430 nm procede de la descripción de Alex. La geometría colineal anterior se sustituyó por D55. El filtro óptico fue eliminado del diseño base anterior; comprobar el fondo en la geometría nueva.

No había mapas `graphify-out/graph.json` en los tres repositorios técnicos consultados. El análisis se basó en los archivos citados, sin crear un grafo nuevo. Los borradores de los artículos se consultaron como antecedentes técnicos; no se modificaron.

## 3. Por qué no compartir detector

| Opción | Ventaja real | Coste o límite | Dictamen para diciembre |
|---|---|---|---|
| AS7265x único | Lectura sencilla, integración y ganancia ajustables; elimina cámara y red | Solo bandas anchas y discretas; se pierde detalle espectral del MonoSpectro | Descartada por la función espectral requerida |
| OV9281 única | Un detector y espectro continuo muestreado en píxeles | La sensibilidad de fluorescencia reportada por Alex es insuficiente; rendija, red y reparto espacial consumen fotones | Descartada con los componentes actuales |
| Dos detectores, dos celdas en serie | Conserva más fácilmente la geometría anterior | Distinto volumen y tiempo de tránsito, más juntas y limpieza; pierde muestra central común | Alternativa de contingencia, no cumple plenamente la Cruz pedida |
| Dos detectores, una celda | Conserva funciones y observa el mismo llenado | Exige resolver geometría, luz parásita y sellado de ventanas | Recomendada, pendiente de prueba óptica |

El [fabricante del AS7265x](https://ams-osram.com/products/sensor-solutions/ambient-light-color-spectral-proximity-sensors/ams-as7265x-smart-spectral-sensor) especifica 18 bandas entre 410 y 940 nm, con FWHM nominal de 20 nm. Espaciado de centros y anchura de banda son cosas diferentes. Tampoco todos los centros están separados 25 nm: el [ejemplo oficial de SparkFun](https://github.com/sparkfun/SparkFun_AS7265x_Arduino_Library/blob/main/examples/Example1_BasicReadings/Example1_BasicReadings.ino) incluye 610, 645, 680, 705 y 730 nm, entre otros. Interpolar esas bandas a 1 nm no aumenta la resolución.

En la cámara, número de píxeles, paso de muestreo y resolución óptica tampoco son equivalentes. Hay que medir FWHM de líneas estrechas. A 60 mm, la rendija confirmada de 0,5 mm subtiende aproximadamente 0,48°. La estimación exacta de la resolución final depende de lente, red, enfoque e incidencia.

La fluorescencia necesita fotones útiles y rechazo de excitación. Una respuesta de fábrica del AS7265x no garantiza sensibilidad suficiente a concentraciones de lago. Del mismo modo, «obturador global» no es una especificación de límite de detección de fluorescencia. Aquí la elección de dos detectores se apoya en las funciones requeridas y en la experiencia experimental comunicada por Alex, no en una comparación de sensibilidades que aún no está medida en la Cruz.

## 4. Geometría fijada por Alex · D55

La disposición óptica en T comparte el brazo de iluminación entre ambas modalidades:

```text
LED seleccionables ─────── MUESTRA ─────────── rendija/red/cámara
                               │
                               ▼
                         AS7265x a 90°
```

El haz y la cámara están en el mismo eje; el AS7265x observa perpendicularmente. Los cuatro LED son seleccionables desde el brazo común; su colocación y el acoplamiento de cada uno quedan por diseñar. Las atribuciones previas de señal en geometría colineal no se trasladan como resultados de esta disposición.

## 5. La señal de clorofila debe verificarse de nuevo

El firmware aplicaba una ecuación (ahora usaremos calibración independiente para clorofila en agua y extracto). Su pendiente respecto a intensidad es negativa. Eso no demuestra que el aparato mida mal, pero obliga a identificar si la señal procede de emisión, atenuación, dispersión o un régimen de autoabsorción. El blanco se guarda, pero no aparece en esa expresión; tampoco hay sustracción explícita del oscuro en el cálculo de clorofila.

Para cerrar la óptica, usar la misma muestra con excitación apagada/encendida, blanco y serie de dilución bajo condiciones que eviten saturación. Comprobar las contribuciones de excitación, dispersión y emisión en los 18 canales para cada fuente. Ninguna atribución previa de 435 o 645 nm se considera validada en la nueva celda.

Mantener 430 nm es una restricción del proyecto. La referencia comercial [SeaOWL de Sea-Bird](https://www.seabird.com/news/seaowl-case-study) usa 470 nm para clorofila y 370 nm para fDOM: esto muestra que excitación y azul no son intercambiables para todas las matrices; no demuestra por sí solo que 430 nm sea inviable. La prueba decisiva es la relación señal/ruido con **agua natural no extraída**, en el rango requerido por la campaña.

La [nota de Turner sobre clorofila in vivo](https://docs.turnerdesigns.com/t2/doc/appnotes/S-0053.pdf) explica que la relación entre fluorescencia y clorofila depende de condiciones de la muestra y necesita comparación con extracción. Una curva de extractos no se traslada directamente a células intactas. Temperatura, historia de luz, turbidez y composición biológica deben formar parte del registro y de las limitaciones.

La transmisión puede aportar A430 y absorbancia en emisión para estudiar/corregir el efecto de filtro interno más adelante, pero la primera versión no aplicará corrección automática sin validación en matriz natural. No extrapolar; medir.

## 6. Celda común y separación óptica

Propuesta funcional: celda de flujo de cuatro caras ópticamente útiles, camino de transmisión inicial de 10 mm, desmontable para limpieza y reposicionable. Elegir material con transmisión conocida a 430 nm y baja autofluorescencia. Celda de flujo de cuarzo ya comprada. Registrar fabricante/modelo/datasheet y verificar integración.

**Sensibilidad con agua natural:** mantener 10 mm reduce cambios, pero puede dejar poca señal de absorción. Ejemplo puramente ilustrativo: un coeficiente de absorción de 1 m⁻¹ produce `A = a × L / ln(10) ≈ 0,0043 AU` con L=0,01 m. Un error de 0,10 AU aceptable en otra comparación sería inútil para distinguir ese nivel. La decisión óptica debe incluir ruido y contraste mínimo en las bandas de interés. Si no bastan, evaluar un camino más largo y su efecto sobre tamaño, dispersión y fluorescencia; no declarar aptitud para lago basándose solo en colorantes concentrados.

El AS7265x contiene tres chips. La recogida de luz debe iluminar sus áreas de forma reproducible; acercar la placa a una ventana no garantiza que los tres observen el mismo volumen. Examinar aperturas y campo de visión del montaje real, y probar homogeneidad con una muestra estable.

Medir el blanco con excitación encendida para incluir fluorescencia de ventana, juntas y adhesivos. Las superficies negras también pueden fluorescer: ensayarlas fuera y dentro del campo de visión. Confirmar que el canal 435 no satura, el 645 distingue fluorescencia de forma útil, y los materiales de la celda no generan fondo.

Para transmisión, fijar exposición y ganancia, verificar respuesta lineal del flujo de imagen y evaluar luz parásita/IR. El modo de imagen actual no demuestra lectura RAW de 8 bits del sensor: distingue profundidad del dato procesado y capacidad nativa. Conservar señal sin suavizar; cualquier suavizado y transferencia fotométrica deben evaluarse sin perder la resolución que justifica usar cámara.

## 7. Cómo se hace la renovación de agua

Se emplean dos familias de equipos: sensores abiertos al agua con limpieza de ventanas y equipos con celdas de flujo alimentadas por bomba. La segunda encaja mejor con conservar el camino de transmisión y el volumen central de la Cruz. Turner documenta [fluorometría con celda y bombeo](https://docs.turnerdesigns.com/t2/doc/appnotes/998-5000.pdf), incluyendo burbujas, retardo de transporte y efectos del tubo. Sus caudales de ejemplo no son especificaciones para nuestra celda.

```mermaid
flowchart LR
    L["Lago · rejilla gruesa"] --- H["Circuito: Celda y Bomba peristáltica (sumergida)"]
    H --- R["Descarga separada de la toma"]
```

La **ubicación hidráulica de la bomba** respecto a la celda está fijada aguas abajo (orden: toma del lago -> celda de cuarzo/zona óptica -> bomba peristáltica sumergida -> descarga). Una bomba aguas abajo permite que las células lleguen a la zona óptica antes de atravesar los rodillos, de modo que la muestra se mida antes de pasar por la bomba. La contrapartida es la depresión, que puede generar burbujas: mantener toma corta, baja pérdida de carga y celda próxima a la cota del agua; verificarlo experimentalmente.

La [documentación de Watson-Marlow](https://www.wmfts.com/en/resources/search-documents/manuals/en/120-manual-en/) explica que en una peristáltica el líquido contacta con el tubo. Eso facilita limpieza y sustitución, pero no elimina desgaste, pulsación, adsorción ni la necesidad de comprobar oclusión con la bomba parada. Bombas de membrana incorporan otras superficies/válvulas mojadas; una centrífuga puede servir a caudales mayores, pero complica dosificar volúmenes pequeños y detener el flujo.

Dimensionar por volumen, no por un número arbitrario de segundos:

- `Vef = volumen de toma + tubos previos + celda + zonas que puedan reintroducir muestra anterior`.
- Como punto de partida, purgar `5 × Vef`. Un volumen perfectamente mezclado dejaría `exp(−5) ≈ 0,67 %` de muestra anterior; los rincones reales pueden ser peores.
- `t_purga = volumen_purga / Q_banco`, donde `Q_banco` es el volumen por tiempo o por revolución calibrado una vez en banco y guardado en configuración (no hay caudalímetro a bordo). El ensayo de arrastre alto→bajo determina el múltiplo de purga.
- Registrar también el retardo entre toma y lectura; el instante de escritura no es necesariamente el instante en que esa agua entró desde el lago.
- Rejilla, recorrido y descarga deben evitar sedimento, recirculación y pérdida selectiva de células. Verificar renovación incluso si el motor gira: corriente de motor sola no prueba caudal.

Para 72 h a 15 min hay 288 ciclos. Con 25 mL por purga se renuevan 7,2 L en total de agua del lago. El blanco de transmisión se toma antes del despliegue y no consume fluido a bordo. Son ejemplos de cálculo, no consumos medidos.

Para días o pocas semanas no habrá limpieza automática ni tratamiento anti-biofilm; solo inspección y limpieza manual antes/después y registro de deriva/ensuciamiento. Dejar anti-biofilm como ampliación si despliegues largos lo exigen.

## 8. Estanqueidad y temperatura

La prioridad es limitar interfaces de presión y hacerlas inspeccionables. Una envolvente comercial o mecanizada para la zona seca, soportes internos impresos y celda húmeda aislada ofrecen un camino razonable. Una caja comercial pierde la garantía de su configuración ensayada al añadir taladros o ventanas propios: se ensaya el conjunto final.

El [manual de sellos de Parker](https://www.parker.com/content/dam/Parker-com/Literature/O-Ring-Division-Literature/ORD-5700.pdf) es referencia para dimensionar ranuras, acabados y compresión durante X1.3. La [guía de Blue Robotics](https://bluerobotics.com/learn/watertight-enclosure-wte-assembly-new/) sirve de precedente para inspección de juntas, pasamuros y prueba de vacío tras modificaciones. El vacío es una comprobación complementaria; no sustituye inmersión ni resistencia a presión exterior.

A 1 m, la sobrepresión de agua dulce es aproximadamente 9,8 kPa; a 2 m, 19,6 kPa. La cámara de muestra puede sufrir además depresión o presión de bomba. Hay que dimensionar esa diferencia y el caso de salida obstruida, incluso si la profundidad es pequeña.

La lámpara de 10 W introduce carga térmica. Ejemplo de límite: 30 s entregan 300 J; si solo el 10 % llega a 5 mL de agua aislada, el aumento sería aproximadamente 1,4 °C. La fracción real se medirá. Disipar hacia la carcasa y minimizar tiempo encendido conservando estabilidad; mantener transmisión primero y fluorescencia después, registrando calentamiento. No asumir que el agua exterior elimina instantáneamente el calor de una celda aislada.

## 9. Autonomía y coste de mantener las fuentes

**Actualización 21 oct:** Alex elige CITYORK 24 V / 3 Ah por precio y plazo, con BMS/cargador anunciados, y apagado ordenado de Pi con corte real entre ciclos. El ejemplo previo de bomba 3 W, lámpara 30 s y Pi 2 min queda sustituido por el [presupuesto acordado y fechado](../compras/LISTA_COMPRA.md#7-presupuesto-energético-conservado): bomba 20 W / 30 s, halógena 10 W / 5 s, cinco LED de 0,4 W / 5 s cada uno, Pi/cámara 5 W / 90 s por ciclo de 15 min.

Subtotal: **88,8 Wh para 288 ciclos en 72 h**, antes de auxiliares. Con 72 Wh declarados, 20 % de reserva y 85 % de rendimiento supuesto aplicados una sola vez, resultan **39,7 h antes de auxiliares**. No se demuestra 72 h con este pack. Los tiempos, potencia efectiva, capacidad del pack y consumo del supervisor/AS7265x/reposos requieren medición.

Usar `E = Σ(P_estado × t_estado)` y medir a la entrada de batería, incluyendo arranque y pérdidas. La Pi debe terminar escritura y apagado antes del corte de alimentación; el driver de bomba y las fuentes deben quedar apagados entre ciclos. Conservar las fuentes acordadas y medir su estabilización sin imponer el tiempo supuesto de energía a una lectura óptica inestable.

## 10. Condición de cierre óptico del 12 de octubre

El acta debe contener: identidad física de componentes, ancho/altura de rendija, lente y distancias, geometría con rayos, celda y materiales, filtro identificado, FWHM medida, rango útil, oscuros/blancos, SNR en agua natural, interferencias, efecto térmico y comparación con los dos equipos previos.

Se acepta la arquitectura cuando ambas modalidades conservan utilidad en la misma celda y se demuestra que su interferencia está dentro de los límites definidos antes del ensayo. Si la fluorescencia con las fuentes fijadas no alcanza el rango necesario, se registra el fallo y se revisa el requisito; una interfaz que muestre un número no convierte el aparato en fluorómetro validado.
