# Especificación funcional de la Cruz

**Versión 0.1 · 26 de septiembre de 2026 · Propuesta para revisión técnica.**

La Cruz integra el MonoSpectro y el fluorómetro en un aparato autónomo para agua natural, con la muestra en el centro. Este repositorio contiene ingeniería, fabricación, firmware y validación. El entregable del **1 de diciembre de 2026** es un prototipo operativo en banco y ensayado varias horas en un lago.

Esta especificación precede al diseño. Los requisitos expresos de Alex se distinguen de las cifras propuestas para hacerlos verificables. No constituye una aprobación de la óptica, una certificación de estanqueidad ni resultados experimentales.

## 1. Requisitos fijados por Alex

- Conservar los dos detectores y las fuentes de los instrumentos existentes: cámara monocroma para espectrofotometría y AS7265x para fluorescencia; excitación a 430 nm según la descripción de Alex.
- Compartir la cámara de muestra y conservar el concepto físico de cruz. La geometría de rayos de cuatro brazos ya está fijada.
- Operación in situ durante días, renovación de agua y almacenamiento autónomo para análisis posterior.
- Diseñar juntas, ventanas, pasamuros y protección contra agua en octubre.
- **30 de octubre: ensayo de estanqueidad con lastre y sin electrónica. Fecha dura.**
- Validación contra espectrofotómetro y fluorómetro comerciales, vinculada a las alícuotas reservadas de la campaña del 5–9 de octubre. La Cruz no participa en esa campaña.
- Coeficientes de calibración en fichero editable, procedimiento reproducible por otra persona y fotografías de cada etapa real del montaje.
- Óptica fijada (LED 430 nm, celda de cuarzo, lente gran angular).

## 2. Qué mide

| Salida | Definición y unidad | Condición de validez |
|---|---|---|
| Intensidad espectral | Señal de cámara frente a píxel y longitud de onda; cuentas | Guardar señal original, oscuro, exposición, ganancia y ROI |
| Transmitancia | T(λ) = [I(λ) − D(λ)] / [I₀(λ) − D₀(λ)] | Blanco y muestra con configuración y geometría compatibles |
| Absorbancia aparente | A(λ) = −log₁₀ T(λ), AU | En agua sin filtrar incluye pérdidas por dispersión; no es absorción pura |
| Fluorescencia multicanal | Señales de excitación a 430 nm encendido menos oscuro, con corrección por blanco de matriz; RFU definidas por la configuración | Guardar los 18 canales, incluidos los no utilizados por el modelo |
| Clorofila estimada en agua sin extraer | µg/L de agua original | Solo con calibración de agua natural y validación independiente en el dominio declarado (calibración en curso) |
| Clorofila estimada en extracto | Unidad definida por el método de calibración del extracto | Calibración independiente del extracto (calibración en curso). Exigir guardar unidad, volúmenes y dilución; no convertir a agua sin método |
| Estado instrumental | Fecha UTC, temperatura del agua y del interior, batería, humedad/fuga, ciclo hidráulico y alarmas | Sensores auxiliares y límites por concretar en X1.4 |

El alcance espectral definitivo para Cruz vuelve a **420–780 nm**.

Color a 440 nm, formas espectrales y fluorescencia azul pueden guardarse como indicadores. CDOM disuelto exige una muestra filtrada y un método de referencia adecuado; fDOM, CDOM y A254 no son magnitudes intercambiables. La Cruz visible no mide A254. Turbidez y nutrientes de la campaña son variables de referencia e interferencia: este prototipo sin reactivos no les asignará unidades de NTU/FNU ni concentraciones de nutrientes por simple correlación.

## 3. Condiciones de operación propuestas

Estas cifras son **objetivos de ingeniería**, fijados.

| Parámetro | Propuesta inicial | Verificación |
|---|---|---|
| Medio | Agua dulce de los lagos de campaña, sin reactivos durante despliegue | Ensayo con matriz natural y retorno de agua separado de la toma |
| Autonomía | 72 h sin intervención; 7 días como ampliación posterior | Ensayo completo de 72 h, incluido consumo hidráulico de muestra y energía |
| Cadencia | Un ciclo cada 15 min; configurable, sujeto al tiempo mínimo validado | 288 ciclos previstos en 72 h |
| Duración del ciclo | Objetivo ≤120 s desde renovación hasta guardado | Medir purga, estabilización de fuentes, lecturas y escritura |
| Profundidad de servicio | Hasta 1 m de inmersión del conjunto | Ensayo hidráulico y de envolvente; registrar cota del punto más profundo |
| Protección objetivo | IP68 como objetivo de diseño; condiciones propias: 1 m y 72 h | No declarar certificación IP68 por un ensayo interno de inmersión |
| Temperatura de agua | 4–25 °C como envolvente inicial | Ensayos en los extremos; excluir congelación del circuito |
| Campo del 24 de noviembre | Objetivo 6 h, 24 ciclos programados | Mismo lago y, si es accesible, estación y profundidad de octubre |
| Disponibilidad | ≥95 % de ciclos completos y válidos, sin intervención | Conservar también cada fallo y cada intento de recuperación |
| Almacenamiento | Espacio para ≥7 días del formato realmente medido, con margen ×2 | Dimensionar tras medir tamaño de ciclo; nunca sobrescribir datos pendientes |

Registrar el rango natural de concentraciones, turbidez y temperatura de la campaña. Antes del 12 de octubre fijar el intervalo útil de fluorescencia y el nivel mínimo que debe distinguirse. No hay base para prometer todavía un límite de detección en µg/L.

## 4. Secuencia de una medición

1. Despertar o iniciar ciclo. Comprobar configuración, reloj, espacio, batería, sensores y ausencia de fuga. Registrar ID de ciclo antes de activar actuadores.
2. Seleccionar agua del lago. Renovar el volumen completo entre la toma y la zona óptica. Detener bomba y esperar desaparición de burbujas y pulsaciones.
3. Con ambas fuentes apagadas, medir oscuros de los dos detectores con sus ajustes de adquisición correspondientes.
4. Medir **transmisión primero**: encender exclusivamente la fuente visible original, esperar su estabilización, capturar réplicas y apagar.
5. Medir **fluorescencia después**: encender exclusivamente el LED azul de 430 nm, aplicar la estabilización caracterizada y leer los 18 canales con ajustes conocidos. Apagar excitación y comprobar oscuro posterior si el ensayo óptico lo exige.
6. Validar saturación, señal útil, estabilidad, blanco compatible, tiempos y temperatura. Conservar valores originales; los fallos producen datos marcados, nunca concentraciones inventadas ni ceros de sustitución.
7. Guardar ambos resultados bajo el mismo ID, con hora individual de cada lectura. Finalizar el registro de forma resistente a un corte de alimentación.
8. Renovar o enjuagar según el protocolo validado. (La celda y conductos permanecen llenos entre ciclos, con entrada por una cara y salida por otra. Antes de medir se bombeará varias veces el volumen efectivo para renovar muestra). Entrar en espera con fuentes y bomba apagadas.

Las dos medidas deben corresponder al mismo llenado. Un fallo que obligue a repurgar inicia un nuevo ID. La frecuencia propuesta no obliga a medir si todavía no se cumplen las condiciones de estabilidad.

## 5. Renovación de agua y blancos

Base propuesta: una bomba peristáltica (sumergida/debajo del agua) instalada después de la celda (orden hidráulico: toma del lago -> celda de cuarzo/zona óptica -> bomba peristáltica sumergida -> descarga). Toma y descarga separadas. Esto significa que el agua se aspira a través de un puerto de entrada exclusivo, atraviesa la celda de medida, y posteriormente se expulsa al exterior a través de un tubo o puerto distinto, evitando que la muestra analizada se mezcle con el agua nueva o vuelva a ser medida. Una bomba aspira y expulsa a la vez; no hace falta una segunda bomba para vaciar. Se mantendrá la celda llena entre lecturas con entrada por una cara y salida por otra. Antes de medir, bombear varias veces el volumen efectivo para renovar muestra, validando el múltiplo con ensayo de arrastre.

Usar una rejilla gruesa solo para proteger la entrada. Definir su abertura después de conocer los organismos/partículas que deben pasar;  Minimizar longitud de tubo, rincones y superficies adsorbentes. Verificar retención y daño celular frente a muestra tomada directamente.

No habrá muestra de blanco dentro del equipo ni bolsa o selector de blanco automático. El blanco de transmisión se mide antes del despliegue y se guarda en memoria con metadatos y configuración. Se advierte de la deriva: la validez temporal del blanco predespliegue se comprobará en ensayo y al recuperar el equipo. Distinguir el blanco de la lectura oscura: los oscuros (con fuentes apagadas) pueden mantenerse en el ciclo si la especificación lo necesita.

La necesidad de otra válvula de aislamiento depende de la deriva de flujo con la bomba detenida. La oclusión peristáltica no se tratará como cierre de seguridad garantizado. La inversión para limpieza se habilitará solo tras validar que no devuelve agua sucia a la toma de muestra.

## 6. Estanqueidad y estados seguros

Separar físicamente el circuito mojado de la electrónica y de las superficies ópticas que deban permanecer secas. Considerar dos caminos de fuga: agua exterior a la envolvente y agua de muestra hacia el interior. Una fuga de tubo o celda no debe alcanzar directamente la alimentación.

En X1.3 se fijarán material y sección de cada junta, ranura, tolerancias, acabado, compresión, lubricante compatible, apriete, ventanas y pasamuros con sus límites de presión. El objetivo mecánico es imprimir en 3D todo o casi todo el cuerpo. Las piezas impresas se conciben como la barrera hidráulica prevista, que debe diseñarse y validarse como tal (incluyendo juntas, ventanas, pasamuros, tratamiento y ensayos de estanqueidad), no como simples soportes.

El 30 de octubre se ensaya la envolvente **final con todas sus interfaces**, lastre y testigos absorbentes, sin electrónica instalada. Un resultado negativo impide instalar electrónica. Los detalles y criterios figuran en [el protocolo de ensayos](docs/VALIDACION_Y_CALIBRACION.md).

| Incidencia | Respuesta requerida |
|---|---|
| Fuga/humedad crítica | Apagar fuentes y bomba, aislar alimentación de potencia y registrar causa si aún es posible |
| Obstrucción, sobrepresión o falta de renovación | Parar bomba por tiempo/presión límite; un único intento de recuperación validado; invalidar ciclo |
| Fuente inestable o lectura saturada | Conservar lectura y marcarla; ajustar solo mediante una política calibrada |
| Fallo de detector/comunicación | Tiempo de espera finito, actuadores apagados, evento persistente |
| Batería baja | Terminar escritura y apagado ordenado antes de tensión insegura |
| Reinicio | Actuadores apagados al arrancar; reconocer ciclo incompleto y retomar programación sin duplicar resultados |
| Memoria llena o configuración inválida | Detener adquisición con error visible; conservar datos previos |

## 7. Control e interfaz

Reutilizar Raspberry Pi para cámara y almacenamiento y ESP32 para AS7265x, actuadores y supervisión. Propuesta: enlace serie interno y una sola máquina de estados de adquisición. La viabilidad eléctrica y el reparto final se deciden el 20–23 de octubre.

La adquisición funcionará sin navegador, Wi-Fi ni internet. La interfaz local permitirá programar, iniciar/detener, consultar último ciclo y alarmas, revisar calibración, ejecutar mantenimiento y descargar datos/configuración. Bajo el agua el registro es local; el acceso por Wi-Fi se prevé al recuperar el equipo o desde una interfaz sobre la superficie expresamente diseñada.

Todo cambio de exposición, ganancia, integración, ROI, fuente o celda invalida los blancos incompatibles. El panel debe indicar con claridad medición válida, resultado fuera de calibración y señal sin calibrar. Una actualización de software no se ejecuta durante un ciclo de medida.

Desactivar indicadores y emisores de la placa que contaminen la cámara óptica. Las lecturas de sensores deben tener tiempo máximo y recuperación; una llamada bloqueante de biblioteca no puede dejar indefinidamente una fuente encendida. La supervisión y el estado eléctrico de arranque deben cubrir también un programa detenido.

## 8. Datos y calibración

Un directorio por despliegue con configuración de calibración versionada, metadatos de instrumentos y registros por ciclo. Guardar como mínimo:

- Guardar obligatoriamente el espectro crudo de cámara como intensidad por píxel antes de calibración/correcciones, además de los datos derivados; captura original sin pérdida cuando sea necesaria para auditar ROI/saturación.
- Los 18 canales AS7265x crudos y los valores calibrados del fabricante, oscuros y blancos.
- Tiempos UTC, ID de celda, detector, muestra/despliegue, versión de software y calibración.
- Exposición, ganancia, integración, corriente/estado de fuente, temperaturas, batería, purga y motivos de invalidez.
- Resultados derivados con unidad, dominio y método; exportación CSV y configuración JSON.

El fichero de configuración contendrá el mapa píxel–λ, respuesta por canal, calibración fotométrica, modelo de clorofila si pasa validación, calibración volumétrica de bomba, tiempos de purga/estabilización y límites operativos. Separar coeficientes experimentales de lecturas de blanco. No trasladar coeficientes del instrumento anterior sin comprobarlos en el montaje final.

El procedimiento completo y el criterio de revisión por otro operador están en [Validación y calibración](docs/VALIDACION_Y_CALIBRACION.md).

## 9. Entregables y puertas de paso

| Fecha | Entregable verificable |
|---|---|
| 5–6 oct | Especificación cerrada y requisitos medibles |
| 7–12 oct | Óptica fijada, integración y verificación en celda de cuarzo |
| 13–19 oct | Fuentes CAD editables, planos y diseño completo de sellado |
| 20–23 oct | Esquemáticos, presupuesto energético y BOM con referencias, precios fechados, IVA/portes y disponibilidad |
| 26–29 oct | Piezas fabricadas e inspeccionadas |
| **30 oct** | **Resultado de estanqueidad sin electrónica, con fotografías** |
| 2–4 nov | Montaje electrónico después de superar estanqueidad |
| 5–11 nov | Firmware integrado y adquisición autónoma |
| 12–16 nov | Interfaz y ensayo continuo de autonomía iniciado |
| 17–19 nov | Comparación de banco contra referencias independientes |
| 24 nov | Ensayo de campo de varias horas |
| 25–27 nov | Ajustes, documentación, fotografías y registro de desviaciones |
| 1 dic | Entrega del prototipo y evidencia verificable |

El detalle de dependencias y márgenes está en [Plan de trabajo](docs/PLAN_TRABAJO.md). La aprobación de una fase exige su evidencia; llegar a una fecha no equivale a superar el ensayo.
