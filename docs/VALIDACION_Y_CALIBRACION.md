# Validación y recalibración de la Cruz

**Protocolo propuesto v0.1 · 26 de septiembre de 2026. Todos los ensayos están pendientes.**

## 1. Reglas de evidencia

Identificar cada ensayo, operador, fecha, versiones de CAD/electrónica/firmware/calibración, instrumentos de referencia, condiciones, datos originales y fotografías. Registrar también fallos. No sustituir resultados por capturas de pantalla de una curva ajustada.

Los límites siguientes son objetivos iniciales de ingeniería. Alex los cierra el 5–6 de octubre antes de las pruebas de selección. Cualquier cambio posterior queda fechado y justificado en DECISIONES.md, con indicación de qué datos ya se habían visto. No relajar límites después de observar la validación reservada.

## 2. Pruebas para decidir la óptica del 7–12 de octubre

Realizar pruebas reversibles con material disponible, después de la revisión de esta propuesta. No requieren fabricar la envolvente. Identificar primero la rendija, lente, fuente visible, LED azul de 430 nm y ajustes reales.

| ID | Ensayo | Evidencia y criterio propuesto |
|---|---|---|
| OPT-01 | Eje espectral y resolución | ≥3 líneas conocidas distribuidas en el intervalo, una comprobación independiente del ajuste; error de centro ≤2 nm y FWHM objetivo ≤10 nm. Informar cobertura real  |
| OPT-02 | Transmisión de blanco y patrones | Intensidad sin saturación, ≥10 repeticiones por condición, respuesta lineal de adquisición; CV de intensidad ≤2 % fuera del fondo |
| OPT-03 | Naturaleza de señal del fluorómetro | Blanco, excitación a 430 nm apagado/encendido, diluciones y lectura de los 18 canales. Documentar por qué aumenta o disminuye cada señal; resolver la ecuación inversa de I645. Confirmar que 435 no satura y 645 responde con muestra fluorescente |
| OPT-04 | Sensibilidad en agua natural | Mínimo bajo, medio y alto del dominio objetivo, más blanco; ≥10 lecturas por condición. SNR ≥10 en el nivel mínimo de trabajo y CV ≤5 % por encima de cuantificación |
| OPT-05 | Validación de la geometría colineal heredada dentro de la nueva celda | Comprobar luz de excitación transmitida/dispersada, montaje sin filtro/rechazo de excitación, blanco, saturación e interferentes. Fondo del blanco ≤10 % de la señal neta del nivel bajo, sin saturación; repetir con interferentes |
| OPT-06 | Interferencia entre modalidades | Secuencia única de operación: transmisión→fluorescencia, con renovación entre secuencias. Cambio ≤5 % en fluorescencia y ≤0,02 AU en transmisión respecto al control; registrar temperatura |
| OPT-07 | Ventana, celda y materiales | Medir blanco con cada material y montaje completo (sin filtro); registrar transmisión a 430 nm/visible y autofluorescencia |

Definir SNR usando señal neta respecto al blanco y variabilidad de ciclos completos a igual configuración, no solo ruido de un píxel. El nivel mínimo procede del rango de interés de la campaña o de un patrón pertinente definido antes de evaluar el instrumento. Si queda por debajo de cuantificación, informarlo como tal. Registrar LOD/LOQ estimados por blancos y pendiente local solo cuando la respuesta permita ese cálculo; comprobarlos con muestras de baja concentración.

En OPT-02 comprobar además el contraste mínimo de absorbancia relevante para agua natural, ΔA, en bandas elegidas antes del ensayo. Objetivo de detección: desviación de ciclos completos ≤ΔA/3 y sesgo claramente menor que ΔA. Para cuantificar ese contraste se requiere margen mayor, inicialmente ruido ≤ΔA/10. Fijar ΔA con la pregunta de medida y las referencias, sin escogerlo retrospectivamente para que el prototipo apruebe. Los umbrales generales con colorantes no sustituyen esta prueba de señal débil.

Si OPT-05 falla, revisar rechazo óptico, baffles/distancias dentro de la geometría colineal antes de reabrir la arquitectura.

## 3. Estanqueidad del 30 de octubre

### Preparación obligatoria antes del 29 de octubre

Cerrar plano de sellado el 19 de octubre: juntas y ranuras, materiales, rugosidad/tolerancias, ventanas, adhesivos si los hay, apriete y cada penetración. Instalar los pasamuros definitivos y tramos de cable definitivos sellados; usar tapones de la misma especificación para puertos vacíos. Una tapa ciega de prueba no valida la tapa final perforada.

Preparar lastre equivalente al montaje, testigos absorbentes secos identificados y fotografiados, una balanza con resolución suficiente para detectar la ganancia de agua acordada, regla de profundidad, termómetro y sistema de recuperación. La carga de presión debe aplicarse en instalación adecuada, dentro del límite del componente más débil. Una cubeta común sin clasificación de presión no se somete a presión de prueba por suposición.

### Secuencia dura del 30 de octubre

1. Fotografiar estado seco, juntas, ventanas, pasamuros y colocación de testigos. Registrar masa inicial de testigos y del conjunto cuando sea útil, incertidumbre de balanza y temperatura.
2. Comprobación preliminar de fugas por vacío, si la envolvente y accesorios lo permiten. Aplicar el procedimiento del fabricante o el procedimiento propio cerrado el 19; registrar presión y temperatura. No usar un límite de caída sin considerar estabilidad térmica y resolución del manómetro.
3. Inmersión con lastre y **sin electrónica**, escalonada: 0,3 m durante 15 min; 1 m durante 30 min; **2 m durante 6 h** como margen frente al servicio propuesto de 1 m. Documentar presión equivalente si se usa cámara de ensayo.
4. Ensayar el circuito húmedo separado: llenado, descarga, depresión/presión operativa y salida obstruida con limitación de presión. Utilizar accionamiento externo de prueba para mantener la envolvente libre de electrónica. Comprobar fugas hacia la zona seca y por ventanas/racores. Si este montaje no está disponible, el ensayo queda incompleto.
5. Secar exterior, abrir evitando goteo desde la tapa, inspeccionar/fotografiar testigos y volver a pesarlos. Buscar agua libre, manchas, condensación, fisuras, deformación y movimiento de juntas/ventanas.

**Aprobación del 30:** ninguna entrada visible ni humectación de testigos, ninguna ganancia de masa distinguible de la incertidumbre de medida establecida, ninguna deformación o daño y circuito húmedo sin fuga dentro de su envolvente de presión. Cumplir el ensayo no equivale a certificación IP68; tampoco prueba aún 72 h.

**Si falla:** marcar FALLIDO, localizar fuga y revisar la interfaz. No instalar electrónica el 2–4 de noviembre hasta repetir el ensayo completo y superarlo. Conservar fotos y resultado fallido. El objetivo es detectar el defecto en octubre, no atribuir un aprobado parcial al conjunto.

### Duración extendida y montaje final

Después de inspeccionar y volver a cerrar el 30, iniciar una inmersión sin electrónica de **72 h a 1 m**, hasta el 2 de noviembre, para comprobar la duración objetivo. El 2 se pueden preparar arneses fuera; instalar electrónica el 3–4 solo tras aprobar e inspeccionar. Tras cualquier apertura/modificación de sellado, repetir comprobación de fugas y una inmersión sin alimentación adecuada a la intervención antes de poner el equipo en servicio. Evitar cambiar pasamuros después del ensayo.

La validación posterior con electrónica incluirá disipación, condensación, temperatura y funcionamiento. La prueba en seco no cubre el calentamiento real.

## 4. Hidráulica, autonomía y fallos

| ID | Prueba | Criterio propuesto |
|---|---|---|
| HID-01 | Medir caudal por masa/volumen y tiempo a varios niveles de batería y alturas | Ajuste en configuración; volumen de purga suficiente en el peor caso, sin trabajar fuera de presión permitida |
| HID-02 | Transición alto→bajo y blanco→muestra | Arrastre ≤1 % de la diferencia alto–bajo después de purga; señal de muestra tras blanco dentro de ±5 % del control |
| HID-03 | Bomba detenida y variación de cota | Flujo residual no modifica lectura/llenado; si lo hace, añadir aislamiento y repetir |
| HID-04 | Agua natural directa frente a pasada por circuito | Sesgo ≤5 % en señal neta sobre cuantificación; inspeccionar partículas/células si aparece sesgo |
| HID-05 | Obstrucción y entrada de aire | Parada por límite, fallo guardado y recuperación acotada; no aceptar giro de motor como prueba de caudal |
| AUT-01 | 72 h a 15 min, sin navegador | ≥274 de 288 ciclos de muestra válidos, ninguna fuga, datos previos íntegros, energía con reserva objetivo ≥20 % |
| AUT-02 | Cortes de alimentación y reinicios en purga, lectura y guardado | Máximo ciclo en curso incompleto, sin corrupción de ciclos previos; fuentes y bomba apagadas al arrancar |
| AUT-03 | Sensor desconectado, disco lleno, reloj/configuración inválidos | Fallo explícito y persistente, sin bucle ilimitado ni resultados aparentemente válidos |
| AUT-04 | Control estable antes/después de 72 h y después de limpieza | Deriva de transmisión ≤0,02 AU y fluorescencia ≤5 % en control estable; separar cambios del patrón y del instrumento |

Arrancar AUT-01 el 13 de noviembre permite terminar el 16 y reservar el 17–19 para comparación. Usar matriz estable para separar deriva instrumental de evolución biológica y una prueba adicional con agua natural para observar ensuciamiento. Un ensayo de seis horas de campo no demuestra autonomía de tres días en todos los lagos.

## 5. Alícuotas de octubre y comparación de noviembre

El [protocolo de campaña](../../campana-lagos-bruselas/PROTOCOLO_CONGELADO.md) prevé 15 matrices primarias y cinco duplicados de campo. Son planes, no muestras ya obtenidas. Los IDs y condiciones finales deben copiarse del registro real, sin reinterpretarlos.

**Dependencia crítica:** reservar el material durante la recogida del 5–9 de octubre. El hito C2.2 del 12–13 se usará para comprobar inventario y distribución, no para retrasar una preservación que el método exija el mismo día. Los plazos analíticos mandan sobre el calendario administrativo.

| Fracción | Uso en Cruz | Precaución que afecta la validez |
|---|---|---|
| Agua sin filtrar | Transmisión aparente e interferencias; fluorescencia in vivo si sigue siendo representativa | Refrigeración/congelación no conserva automáticamente células y rendimiento de fluorescencia durante semanas |
| Filtrado para color/CDOM | Comparación de color visible y, si existe equipo UV, referencia UV separada | Guardar filtro, fecha, recipiente y condición; comprobar estabilidad con el método correspondiente |
| Filtro/extracto para clorofila de referencia | Valor de clorofila de la muestra original y control analítico | Método, volumen filtrado, volumen de extracto, dilución, unidad e incertidumbre trazables |
| Nutrientes | Contexto e interferencias | Preservación y caducidad del método específico; no equivalen a mediciones directas de Cruz |

El [protocolo Turner](https://docs.turnerdesigns.com/t2/doc/appnotes/S-0053.pdf) recomienda mantener muestras frías y oscuras, filtrar pronto y congelar el filtro cuando se difiere la extracción. Ese tratamiento preserva material para referencia extractiva; no acredita una muestra in vivo intacta en noviembre.

Asignar antes del análisis un juego independiente para evaluación: propuesta de una matriz primaria por lago, con réplicas técnicas, y material restante/patrones para calibración. Verificar que el volumen permite la purga sin consumir toda la reserva: `V_reserva ≥ Σ(V_purga + V_lectura) + volumen de referencia + margen`. No recircular una alícuota y tratar sus lecturas como muestras independientes.

Nota: El desarrollo de protocolos para la conservación a largo plazo de muestras se pospone para una etapa posterior. Por ahora, las pruebas se realizarán con el material disponible, y los problemas derivados de la degradación o estabilidad de alícuotas se abordarán más adelante.

Para fluorescencia in vivo, usar además material vivo/fresco disponible y caracterizado ese día. La salida ya prevista del 24 de noviembre proporciona pares contemporáneos con agua del lago y extracción de referencia. Si las reservas pierden validez y no hay material vivo en banco, declarar pendiente esa parte de la validación; no sustituirla silenciosamente por extractos ni por valores históricos.

### Comparación instrumental y criterios

- **Transmisión:** mismo camino óptico, blanco y estado de filtración. Comparar con el espectrofotómetro en su resolución nativa y después ajustada a la FWHM medida de Cruz; conservar ambas comparaciones. Objetivo inicial RMSE ≤0,10 AU y sesgo absoluto ≤0,05 AU en el intervalo previamente declarado, comenzando por 0,05–1 AU. No escoger longitudes favorables después de ver los datos.
- **Transmisión en agua de lago débilmente absorbente:** satisfacer también el criterio de contraste de OPT-02. Aprobar colorantes entre 0,05 y 1 AU no demuestra capacidad para señales menores; si falla esta parte, limitar explícitamente el uso de transmisión y registrar el requisito pendiente.
- **Fluorescencia:** anotar excitación/emisión y filtros del comercial. Si permite 430 nm, comparar señal bajo condiciones equivalentes. Si usa otra excitación, comparar estimaciones de clorofila frente a extracción, sin equiparar RFU entre instrumentos.
- **Clorofila en agua sin extraer y en extracto:** no imponer el mismo criterio/unidad a ambos modos sin sus calibraciones. Mostrar error relativo absoluto, sesgo y errores por muestra publicados. Mostrar también error absoluto, incertidumbre de referencia, pendientes y residuos; R² solo no decide aprobación. Con cinco matrices reservadas la evidencia es limitada y se informa el n real.
- La conversión de extracto será explícita: `C_agua = C_extracto × V_extracto / V_agua × dilución`, con unidades compatibles y los factores adicionales del método documentados.
- No ajustar calibración con el conjunto reservado. Réplicas técnicas estiman repetibilidad; no aumentan el número de matrices independientes.

## 6. Recalibración ejecutable por otro operador

### Material necesario

Instrumento limpio, celda identificada, blanco del método, patrones de longitud de onda y absorbancia, material fluorescente de control compatible con el filtro y muestras/patrones para clorofila, referencias comerciales con calibración vigente, termómetro, material volumétrico y ordenador para configuración. Anotar lotes, caducidades, unidades y preparación; un colorante de control no sustituye automáticamente clorofila-a en agua natural.

### Procedimiento

1. Recuperar la última calibración válida y crear una copia nueva con ID, fecha y operador. Revisar limpieza, junta y alineación. Registrar qué cambió desde la anterior.
2. Cargar ajustes fijos de adquisición. Medir estabilización de cada fuente y controlar temperatura; no usar tiempos heredados sin verificación.
3. Medir al menos diez oscuros por modalidad a esos ajustes. Guardar media, desviación y señales individuales; comprobar ausencia de luz ambiente.
4. Verificar eje píxel–λ con líneas conocidas. Ajustar el polinomio de menor grado suficiente, comprobar monotonicidad y una línea independiente. Medir FWHM y limitar el intervalo útil a la zona comprobada.
5. Medir blanco de agua y patrones de absorbancia de varios niveles frente al comercial. Calcular transmitancia con sustracción de oscuro. No convertir señales ≤0 después de sustracción en absorbancias finitas. Conservar absorbancias negativas compatibles con ruido/deriva para diagnóstico, sin recortarlas para mejorar métricas.
6. Medir blanco fluorescente y una serie de concentraciones que cubra el dominio de uso, con réplicas independientes. Guardar los 18 canales. Empezar por una relación sencilla en el tramo útil, comprobar residuos, saturación y autoabsorción antes de considerar otro modelo. Validar cualquier normalización por tiempo o ganancia.
7. Ajustar coeficientes con el conjunto de calibración; evaluar una muestra/control independiente que no entró en el ajuste. Verificar transferencia a agua natural si se van a mostrar µg/L in vivo.
8. Medir calibración volumétrica de bomba, purga, arrastre y retorno de blanco a muestra. Guardar tiempos y límites resultantes.
9. Escribir la nueva configuración con unidades, dominio, identificación de hardware y enlaces a datos/ensayos. Validar estructura, números finitos, límites y compatibilidad de blancos antes de activarla.
10. Reiniciar, cargar la configuración desde disco y repetir un control independiente. Si falla, restaurar la anterior, registrar el fallo y dejar bloqueadas las concentraciones afectadas.
11. Un segundo operador repite limpieza, blanco y control siguiendo únicamente este procedimiento. Registrar sus resultados y resolver las ambigüedades detectadas en la documentación.

### Contenido previsto del fichero de calibración

| Grupo | Campos mínimos |
|---|---|
| Identidad | Versión de formato, ID y fecha de calibración, operador, instrumento/celda/filtro/fuentes, software y ensayo de origen |
| Cámara | ROI, exposición, ganancia, modo de imagen, coeficientes píxel–λ, intervalo válido y FWHM medida |
| Fotometría | Modelo y coeficientes de transferencia si son necesarios, unidades, dominio y referencias de blanco/oscuro |
| AS7265x | Mapa de canales, integración, ganancia, respuesta/offset por canal y controles de saturación |
| Clorofila | Modelo, entradas, coeficientes, unidad final, dominio, referencia y estado de validación |
| Hidráulica | Caudal calibrado con condiciones, Vef, volumen/tiempo de purga y tiempos de estabilización |
| Calidad | Límites de señal, deriva, temperatura, antigüedad de blanco y criterios de fallo |

No incluir coeficientes numéricos ficticios para que un archivo parezca completo. Hasta obtenerlos, el equipo puede guardar señales identificadas como no calibradas; no mostrar concentraciones.

Recalibrar tras cambiar celda, óptica, detector, filtro, fuente o modo de adquisición, y cuando un control falle. Repetir blanco y control tras limpieza/reapertura. La verificación se realiza antes del despliegue y tras la recuperación, y se usan controles de deriva en los ensayos de banco sin implicar una muestra de blanco a bordo.

## 8. Campo del 24 de noviembre

Elegir entre los cinco lagos efectivamente muestreados y con condiciones de instalación documentadas. La recogida manual autorizada no demuestra por sí sola que se pueda dejar equipo sumergido; registrar la condición aplicable al despliegue.

Documentar fijación, recuperación, profundidad, posición de toma y descarga, temperatura, hora y coordenadas. Objetivo: 6 h sin intervención, 24 ciclos previstos y al menos 23 válidos. Tomar pares contemporáneos al inicio, mitad y final para referencias comerciales, con tiempo de conservación del método. Repetir blanco/control e inspección al recuperar el aparato.

Comparar noviembre con octubre como observación temporal del mismo sitio. Para exactitud instrumental usar los pares contemporáneos; el valor del lago puede cambiar entre ambos meses.
