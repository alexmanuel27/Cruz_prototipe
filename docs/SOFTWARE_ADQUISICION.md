# Adquisición y control de Cruz: revisión y primera iteración

## Pruebas de banco · 21 de noviembre de 2026

- **Pi 5 y cámara:** Alex corrigió la orientación de la cinta; la OV9281 Arducam se detecta en CAM/DISP 1 con `camera_auto_detect=0` y `dtoverlay=ov9281,arducam`. `rpicam-still` guardó JPEG y DNG de 1280 × 800 con sensor RAW10; el JPEG muestra señal, con zonas blancas saturadas visualmente. DNG, linealidad, saturación real y calibración aún sin evaluar. Los archivos de prueba se guardaron temporalmente en la Pi.
- **AS7265x:** Alex conectó el módulo a la Pi 5; bus I²C 1 y respuesta en `0x49`. El tipo leído fue `0x40` y el registro de selección `0x30` indicó presencia de los dos sensores asociados. Se obtuvieron crudos y valores calibrados de fabricante en 18 canales. La prueba inicial consultaba dos veces DATA_RDY: corregida en la copia temporal para tomar la primera señal de listo. Biblioteca SparkFun Python 2.0.0 con `smbus2`; prueba con 64× y registro de integración 49, ajustes predeterminados de la biblioteca, sin calibrar para Cruz. El LED azul externo no se activó; la biblioteca enciende brevemente y luego apaga su indicador interno.
- **Respuesta a iluminación:** una lectura con el sensor tapado y otra con la luz del móvil; sin distancias ni espectro controlados. Todos los canales respondieron. Cuentas crudas, en orden 410, 435, 460, 485, 510, 535, 560, 585, 610, 645, 680, 705, 730, 760, 810, 860, 900 y 940 nm:
  - Tapado: `0, 1, 0, 1, 0, 2, 1, 1, 6, 0, 1, 1, 0, 0, 0, 0, 0, 0`.
  - Móvil: `38, 348, 331, 1008, 1406, 1135, 2617, 5012, 33624, 5595, 6514, 1525, 5284, 2776, 2654, 447, 127, 120`.
- **Originales:** Alex indicó que los CSV con crudos y valores calibrados quedaron en `/home/alex/cruz-sensor-DR8T91/` de la Pi. `luz-ambiental.csv` corresponde a luz del móvil. No se han copiado ni verificado los archivos en el repo; la prueba Python y la biblioteca están en `/tmp/cruz-as7265x` de la Pi y son temporales. No hay medición de intensidad de fuente, réplicas, blanco, saturación, repetibilidad ni validación de fluorescencia. La respuesta óptica no demuestra concentraciones ni calibración del conjunto.
- **Siguiente paso:** comprobar la lectura de temperatura DS18B20 o la conductividad Atlas según el material disponible, verificando módulo, terminales, alimentación y bus antes de cablear. Tras las pruebas se entregarán al chat de PCB únicamente interfaces y resultados comprobados.

**20 de noviembre de 2026 · Revisión y plan de pruebas, sin control de hardware habilitado.**

La Raspberry Pi gobierna el instrumento. **Prioridad posterior fijada por Alex:** seleccionar y probar los componentes reales, sus conexiones y funciones básicas; integrar después y trasladar al chat del PCB los resultados verificados. El ciclo simulado de §3 se conserva como propuesta posterior para probar integración y fallos, sin preceder a esas pruebas básicas. No se modifica mecánica, esquema, PCB ni software de los instrumentos anteriores.

Alex dispone de una Raspberry Pi 5 y de la Pi 4 de MonoSpectro. Recomendación pendiente de ensayo: evaluar la Pi 5 con una tarjeta de sistema independiente y conservar la Pi 4 como referencia. Empezar por Pi 5 + OV9281, alimentación de banco conocida y V8 desconectada; comprobar detección, RAW, ajustes manuales y guardado. Después, verificar cada sensor y actuador por separado, revisando antes su interfaz eléctrica. No hay cambio definitivo de controlador ni incorporación del ESP32 aprobados todavía.

La selección energética comparará energía por ciclo completo y espera, incluyendo convertidores y periféricos. Para la Pi 5 se evaluará el despertar por su RTC y el estado de bajo consumo documentados en la [guía oficial](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#real-time-clock-rtc). El ESP32 queda como candidato a supervisor si aporta una mejora medida; leer el AS7265x desde la Pi no requiere conservar el firmware ESP32. No se exportan todavía propuestas al chat del PCB.

## 1. Qué existe y qué reutilizar

La búsqueda del árbol de Cruz, incluidos archivos ocultos salvo Git, no encontró adquisición, servicio de arranque ni firmware unificado. Los programas Python existentes pertenecen al CAD, simulación o generación/comprobación histórica de KiCad. No son controladores del instrumento. Entrada de requisitos: [especificación, §§2–8](../ESPECIFICACION.md), [calibración](VALIDACION_Y_CALIBRACION.md) y [decisión D53](../DECISIONES.md#d53--raspberry-pi-como-controlador-principal-2026-11-02).

| Origen revisado | Reutilización concreta | Adaptación necesaria para Cruz |
| --- | --- | --- |
| `MonoSpectro/app.py`: `manual`, `unpack_raw10`, `start_camera`, `collect`, `same_settings` | Captura PiCam mediante Picamera2; RAW10; ROI; exposición y ganancia manuales; promediado y detección de saturación; compatibilidad de referencias | Extraer únicamente captura y validación, sin importar la app: inicializa cámara e hilos al importar. Guardar cada réplica, metadatos efectivos y original sin pérdida. Plazo total finito aun si llegan cuadros a destiempo. Exigir RAW para fotometría validada; el fallback ISP de 8 bits queda solo diagnóstico identificado. |
| `MonoSpectro/app.py`: `wavelength_axis`, carga de JSON y exportación CSV | Polinomio píxel–λ y formato legible con ajustes de adquisición | El ROI es semiabierto: usar índices reales `x1 … x2−1`, no el `linspace(x1,x2,n)` actual. No asignar una escala espectral ficticia sin calibración. Referencias persistentes: `refs` vive en RAM y el CSV se descarga por HTTP. |
| `MonoSpectro/spectro_math.py`: `absorbance`, `apply_response`, `savgol` | Ecuaciones y corrección opcional separadas de la interfaz | No copiar `absorbance` tal cual: impone un suelo de una cuenta y usa un solo oscuro. Cruz necesita D de muestra y D₀ del blanco; señales no positivas quedan inválidas. `apply_response` recorta a cero: conservar absorbancia aparente negativa y guardar aparte cualquier corrección declarada y validada. No transferir coeficientes del otro montaje. |
| `Fluorometer/Spectro18_V_Flu/Spectro18_V_Flu.ino` | Mapa explícito de los 18 canales; adquisición de réplicas; separación de muestra, oscuro y blanco | El firmware ESP32 no se ejecuta en la Pi. Lee `getCalibrated*`, no cuentas crudas; las muestras guardan medias/SD de 18 canales y réplicas individuales solo de 435/645 nm. Cruz guardará todas las réplicas crudas y calibradas, configuración y tiempos. |
| `Fluorometer/Spectro18_V_Flu/WhiteReference.h`, `SpectrumStats.h` | Referencia de 10×18 y estadística de Welford, con comprobación de guardado fallido | Reutilizar comportamiento y casos de prueba en Python; no portar NVS ni exigir señal en 435/645 para validar cualquier blanco. Ceros de oscuro son legítimos. No heredar tiempos térmicos ni número de réplicas como calibrados. |

Rutas de origen: `/Users/alex/Nube /repos/MonoSpectro` y `/Users/alex/Nube /repos/Fluorometer`. No se importarán por rutas absolutas ni se dependerá en producción de repos vecinos. Al incorporar fragmentos, conservar atribución y licencia aplicable; MonoSpectro incluye MIT, y debe revisarse la autorización de los archivos concretos de Fluorometer antes de distribuirlos.

La ecuación de firmware `−2,7924·ln(I645)+20,1264` no usa el blanco ni el oscuro en su resultado. Las calibraciones de extractos del repo Fluorometer tampoco validan agua natural ni la geometría de Cruz. En esta primera entrega, clorofila y salinidad derivada permanecerán sin valor si no existe un modelo válido para ese dominio; se conservan las señales y conductividad originales.

Para el controlador Python del AS7265x existe una opción del propio fabricante de la placa: [SparkFun Qwiic AS7265x](https://github.com/sparkfun/qwiic_as7265x_py/blob/master/qwiic_as7265x.py), con lecturas crudas y calibradas separadas. Es candidata, no dependencia instalada o validada aquí. Su `take_measurements()` puede volver por timeout sin excepción: no interpretar retorno como lectura nueva. Comprobar disponibilidad/frescura, errores de bus y plazo total. Usar adquisición sin los emisores integrados; la excitación externa es 430 nm. La [documentación oficial de Raspberry Pi](https://www.raspberrypi.com/documentation/accessories/camera-software.html) mantiene la pila moderna de cámara; el sensor OV9281 concreto y su soporte RAW se verificarán en la Pi real.

## 2. Interfaces observadas en V8

Se exportó una netlist XML del **esquema guardado vigente**, no del archivo histórico: 75 componentes y 77 redes. Los siguientes números son **pines del símbolo J1 de 40 contactos**, no números BCM ni autorización de cableado. No se genera una configuración GPIO a partir de esta tabla. Ver [estado eléctrico V8](../electronica/cross_v8_raspberry/LEEME_PRIMERO.md).

| Función | Conexión observada | Pendiente que bloquea su uso real |
| --- | --- | --- |
| PiCam espectral / cámara auxiliar | CSI / USB previstos por especificación; no representados en J1 | Modelo de Pi/OS, enumeración y soporte OV9281, formato/stride RAW, metadatos; modos reales de la USB. Cámara auxiliar aplazada hasta definir función/cadencia. |
| Bus I²C sensores | J1.3=`SDA`, J1.5=`SCL`; J8 AS7265x, J9 Atlas, J6 ADS1115 y adaptación hacia RTC | Direcciones reales, modo I²C de Atlas, pull-ups conjuntos, niveles, cableado y ausencia de alimentación parásita con Pi apagada. No hacer barridos sobre V8 sin revisión. |
| AS7265x | J8: 1=`3V3_PI`, 2=GND, 3=SDA, 4=SCL | Orden del módulo/cable, alimentación y emisores desactivados; ajustes y saturación. La alimentación dedicada de 3,3 V acordada aún no aparece. |
| Atlas EC | J9: 1=`3V3_PI`, 2=sin conectar, 3=GND, 4=SDA, 5=SCL | Orientación y función real del zócalo Gen 2, alimentación dedicada, modo/dirección, respuesta/status, unidades, K, calibración y compensación térmica. No interpretar el quinto contacto por analogía con otro módulo. |
| DS18B20 | J10: 1=`3V3_PI`, 2=GND, 3=`TEMP_1WIRE`; J1.7; R10=4,7 kΩ | Alimentación dedicada, orden real de hilos, identidad 1-Wire, CRC y conversión completada dentro del plazo. Conservar lectura/status original; fallos no son 0 °C. |
| Bomba A4988 | `M_STEP`=J1.11→U1.7; `M_DIR`=J1.12→U1.8; `M_ENABLE_N`=J1.13→U1.1; J2 bobinas | Correspondencia del carrier WJMY, corriente por fase, microstepping, reset/sleep, dirección, arranque deshabilitado y forma de generar pulsos con tiempo definido. Caudal/volumen efectivo y purga requieren ensayo; no inferirlos de 24 V/20 W. |
| Fuente blanca | `WHITE_EN`=J1.15→R5/Q1; J3 LED, U2 LM317 | Polaridad efectiva, estado al arrancar y al caer la Pi, corriente/driver, estabilización, fuente real disponible y disipación. |
| Excitación azul | `BLUE_EN`=J1.16→D8; `BLUE_GATE`→Q7; `BLUE_CTRL`=J5.1, J4 alimentación de driver | Hay inversión por D8/Q7: no asumir que HIGH equivale a luz. Verificar CTRL del driver y ausencia de encendido durante arranque, reset y Pi apagada. |
| Batería/ADC | J6 interfaz ADS1115; J7.1=`BAT_SENSE` desde divisor R8=100 kΩ/R9=10 kΩ de `VBAT_SW` | Módulo, dirección, rango, ganancia y referencia ADC; tensión máxima real y divisor/calibración; umbrales para terminar escritura. Mide rama conmutada, no batería permanentemente. |
| RS-485 | J1.8=`UART_TX`→J19.2; J1.10=`UART_RX`→J19.1; J19.3=GND, .4=`3V3_PI`; J20.3=A, .4=B, .2=REF | Módulo/transceptor real, dirección de transmisión, compatibilidad lógica, aislamiento, terminación, UART/console Linux y formato serie. No aparece DE/RE dedicado en J1. |
| Puerto exterior EN3 | J18.1/.2 carga, .3 sin conectar, .4 GND, .5=A, .6=B, .7=REF, .8=PILOT en este borrador | El símbolo dice `ASSIGNMENT_VERIFY`: no es un pinout físico aprobado. La reserva de alimentación externa de la especificación no está resuelta; no asignar sus cavidades ni unir retornos. |
| Despertador RTC | J24: 1=`3V3_AON`, 2=GND, 3=`RTC_SDA`, 4=`RTC_SCL`, 5=`WAKE_N`; Q3/Q4 hacia I²C de Pi | Modelo, dirección, batería/reserva, interrupción, alarma y aislamiento entre dominios. No hay prueba de despertar autónomo ni de reloj UTC confiable. |
| Corte de Pi | `HOLD_PI`=J1.37→U8.4 **R**; U8.1 Q→`POWER_ON`→J26.1 | El nombre HOLD no determina la acción: la red llega al reset del biestable. Verificar circuito, estado inicial, señales durante shutdown y corte solo después de escritura y apagado completos; no implementarlo como simple “mantener HIGH”. |
| Imán / cable / carga | `SW_SENSE`=J1.29; `PILOT_SENSE`=J1.22; `CHARGE_CTRL`=J1.18→R11/Q2/K1, inhibición Q6 | Polaridades, interbloqueos, debounce, latencia y comportamiento con Pi sin alimentación; contactos energizados y cargador. No controlar carga en la primera iteración. |
| Fuga, humedad y temperatura interior | No se identifica sensor/interfaz dedicado entre los componentes y redes exportados | Definir sensor, señal, alimentación, umbral y reacción de potencia independiente del programa. Tampoco hay realimentación de caudal/presión identificada. El software no puede certificar ausencia de fuga/obstrucción sin esas señales. |

Conexiones reservadas no equivalen a interfaces validadas. El documento V8 registra 199 conexiones sin trazar, tres errores ERC de alimentación y revisión eléctrica pendiente. Esos resultados se citan, no se han repetido ERC/DRC ni paridad en esta tarea. No fabricar ni energizar V8 a partir de este informe.

El [puerto de servicio](../electronica/PUERTO_SERVICIO_Y_BOYA.md) fija RS-485 como enlace y propone Modbus RTU, pero no hay mapa de registros, baud rate, dirección de equipo ni protocolo de archivos aprobado. RS-485 no proporciona por sí solo descarga de espectros/imágenes. Esa implementación queda después de medir el volumen de datos y cerrar electrónica. La extracción final será por el conector físico, con integridad y reanudación; no se sustituye por Wi-Fi.

## 3. Integración propuesta después de las pruebas básicas: ciclo simulado

**Resultado de la entrega:** ejecutar un ciclo y una serie de ciclos sin red ni navegador, inspeccionar todos sus archivos y repetir el procesamiento a partir de originales. El modo simulado no importa bibliotecas GPIO/I²C/PiCam ni abre dispositivos. Todos sus datos y resultados se etiquetan `simulated`; nunca se mezclan con un despliegue real. No se ofrece todavía un modo hardware habilitable con un interruptor de configuración.

### Alcance mínimo en el repo de ingeniería

- `software/cruz.py`: entrada de terminal, secuencia y almacenamiento. Funciones simples de adquisición simulada; ningún framework, servidor ni panel web.
- `software/processing.py`: eje píxel–λ, transmitancia/absorbancia, resta de oscuro y blanco multicanal, validaciones de calidad. NumPy para espectros cuando se incorpore el código de cámara; JSON, CSV, tiempos, IDs y archivos con biblioteca estándar.
- `software/config/`: ejemplo de operación y calibración **sintética**; blanco/oscuro de referencia sintéticos separados. Sin coeficientes de instrumentos anteriores ni números GPIO reales.
- `software/tests/`: pruebas pequeñas de ecuaciones, secuencia, referencias incompatibles, fallos y recuperación. Fixtures de 18 canales y espectro de cámara conocidos.
- `software/README.md`: instalación, comandos, formato y límites. Si se incorporan dependencias, declaración mínima de versiones verificadas; Picamera2 solo en fase Pi, desde el sistema compatible.

Esos archivos son el alcance de la implementación siguiente; no existen todavía. Al incorporarlos, enlazar desde el índice del proyecto y registrar las pruebas en el registro. No requiere cambiar callers de Cruz porque aún no hay aplicación. Los dos precursores quedan como referencia de solo lectura.

### Secuencia que debe ejecutar

1. Validar configuración, destino, espacio disponible y reloj; crear y persistir ID único del ciclo antes de cualquier actuación simulada. Registrar inicio, versión de formato/software y hashes de configuración, calibración y referencias.
2. Simular toma→celda→bomba aguas abajo→descarga. Simular renovación de varios volúmenes efectivos, parada y espera de burbujas. Tiempos/volumen del ejemplo son sintéticos; no parámetros para la bomba real. Sin inversión ni repurga automática en esta entrega.
3. Ambas fuentes apagadas: adquirir oscuros de cámara y AS7265x con los ajustes de cada detector.
4. Solo visible encendido: estabilización, réplicas PiCam y apagado. Solo después, azul 430 nm encendido: estabilización, réplicas de los 18 canales y apagado. Conservar tiempos individuales para evaluar separación entre modalidades en el mismo llenado.
5. Adquirir temperatura y conductividad originales y sus estados; registrar compensación aplicada y tiempo. Recoger estado instrumental disponible. En simulación indicar su origen sintético; para señales no implementadas usar ausencia explícita, nunca valores normales inventados.
6. Procesar y guardar calidad por dato/modalidad y estado global. Un detector fallido no borra lo adquirido por el otro. Tiempo máximo por operación y por ciclo con reloj monótono; UTC para trazabilidad. Concluir siempre con intención de fuentes/bomba apagadas. Si una llamada bloquea, el controlador deberá tener un mecanismo externo que haga cumplir el plazo en fase hardware: un `finally` o un hilo con timeout no cubren un proceso colgado.
7. Cerrar durablemente el ciclo; esperar hasta el próximo vencimiento (15 min inicial configurable). Una sola ejecución a la vez. Si el ciclo excede la cadencia, registrar vencimiento perdido sin superponer ni acumular ciclos de recuperación. No hay corte de alimentación ni programación RTC en esta entrega.

Cada estado y fallo queda en un registro por ciclo. Si en el futuro es necesario repurgar, cerrar el intento fallido e iniciar otro ID, enlazado al anterior. No reutilizar el ID con otra muestra.

### Configuración y procesamiento

Separar `operation.json` (adquisición, cadencia, réplicas, tiempos, límites), `calibration.json` (coeficientes, unidades, método, dominio e identidad del montaje) y `references/` (blanco y oscuro de cada blanco con sus metadatos y datos originales). Guardar una copia inmutable de los archivos activos dentro del despliegue. Un cambio de configuración se aplica entre ciclos, con nueva identificación; nunca a mitad de una medida.

Validar esquema/versión, números finitos, dimensiones, identidades, ROI, formato y profundidad de bits, exposición/ganancia/integración efectivas, mapa de canales, fuente/celda y rango calibrado. El objetivo es 420–780 nm; informar cobertura útil real y enmascarar fuera del dominio comprobado. Sin coeficientes reales se guardan intensidad frente a píxel y estado sin calibrar; no inventar longitudes de onda. Blanco ausente/incompatible impide derivados afectados, sin impedir conservar originales en una adquisición diagnóstica explícita. Una configuración estructuralmente inválida bloquea el ciclo antes de actuar.

Para transmisión calcular, por píxel válido:

`T = (I − D) / (I₀ − D₀)`; `A_aparente = −log10(T)`.

Conservar I, D, I₀ y D₀ separados. Denominador o numerador no positivo, no finito, o saturación: resultado ausente y motivo; no suelo de una cuenta. T>1/A<0 se conserva con su diagnóstico de ruido/deriva, sin recorte. Una corrección fotométrica opcional no sustituye T/A originales. El blanco predespliegue no se mide automáticamente dentro del equipo; conservar edad y verificar deriva al recuperar.

Para fluorescencia, conservar por réplica los 18 enteros crudos y los 18 flotantes calibrados del fabricante, antes de corrección. Guardar `F_neta = (F_on − F_dark) − (B_on − B_dark)` cuando las referencias/configuraciones sean compatibles, en la misma escala y con unidad declarada. Conservar negativos; medias y SD son derivados adicionales. No normalizar por ganancia/integración ni convertir a concentración sin un método validado.

Mapa heredado que debe comprobar el adaptador real, en nm y letra de canal: `410:A, 435:B, 460:C, 485:D, 510:E, 535:F, 560:G, 585:H, 610:R, 645:I, 680:S, 705:J, 730:T, 760:U, 810:V, 860:W, 900:K, 940:L`. Los 18 se almacenan aunque el análisis use solo parte; no confundir el rango del AS7265x con el objetivo de transmisión.

### Archivos de salida y reinicios

Un directorio por despliegue, con manifiesto, metadatos del montaje y copias de configuración/referencias. Un subdirectorio por ID de ciclo con:

| Archivo propuesto | Contenido |
| --- | --- |
| `cycle.json` | Estado iniciado/completo/fallido/interrumpido; UTC y reloj confiable o no; IDs de equipo/celda/muestra/despliegue; versión de software/calibración; ajustes efectivos, fuentes, purga, sensores, alarmas, referencias, unidades y motivos de invalidez. |
| `events.jsonl` | Transiciones, intentos, fallos y tiempos. No reemplaza el manifiesto de integridad. |
| `camera.csv` | Réplica/tipo (oscuro/muestra), UTC, índice de píxel e intensidad antes de corrección. Guardar originales RAW sin pérdida y metadatos por captura para auditar ROI/saturación; calcular su tamaño real antes de dimensionar despliegues. |
| `as7265x.csv` | Réplica/tipo, UTC, canal/letra/λ nominal, cuenta cruda, valor calibrado del fabricante y ajustes. |
| `environment.csv` | Respuesta original y status/CRC disponibles, temperatura, conductividad con unidad y compensación, batería/otros sensores disponibles. Valor ausente y causa si faltan. |
| `processed.csv` | T/A aparente, fluorescencia neta, medias/SD, máscaras de calidad y versiones/métodos. Concentraciones ausentes salvo calibración validada. |

Archivos nuevos sin sobrescribir ciclos previos. Crear marca de inicio durable; escribir cada archivo temporal en el mismo sistema de archivos, vaciar buffers y sincronizar, renombrar y sincronizar directorio; publicar `complete` solo tras cerrar y verificar todos los archivos esperados y hashes. Esto reduce escrituras incompletas; no garantiza contra fallo físico de tarjeta/controlador. Al arrancar, conservar cualquier original parcial y registrar como interrumpidos los inicios sin cierre válido; empezar con ID nuevo, sin completar artificialmente datos ausentes. Bloqueo de ejecución única para evitar dos procesos sobre el mismo destino. Con disco lleno, conservar lo existente y detener nuevos ciclos; registrar causa si queda espacio.

No se borran datos tras exportar. El manifiesto permitirá comprobar una futura copia íntegra por el conector. El presupuesto de espacio se calcula con el formato medido, incluido RAW, para ≥7 días con margen ×2.

### Pruebas de aceptación de esa entrega

1. Caso numérico conocido: I=60, D=10, I₀=120, D₀=20 → T=0,5 y A≈0,30103. Detecta usar por error D en ambos términos. Casos no positivos, saturación y T>1; cero oscuro permitido.
2. Blanco incompatible por ROI, exposición, ganancia, integración, fuente o celda: originales conservados, derivados bloqueados y motivo explícito. Configuración corrupta/no finita: ciclo rechazado antes de actuaciones.
3. Réplicas de cámara y **18 crudos + 18 calibrados por réplica** recuperables, mapa correcto (incluidos R/I/S), sin clorofila inventada. Verificar resta separada de oscuro/blanco con un caso conocido.
4. Traza de acciones: bomba detenida antes de óptica; visible antes de azul; nunca ambas fuentes encendidas; apagado tras fallo. Fallos inyectados de cámara/sensor y plazo vencido no dejan un ciclo completo falso.
5. Interrupción durante cada fase de escritura y reinicio: datos previos intactos, ciclo interrumpido identificable y siguiente ID distinto. Simular disco lleno y segunda instancia, con rechazo seguro. Una prueba de proceso no demuestra resistencia a corte físico de energía.
6. Serie acelerada de 24 ciclos simulados sin superposición y con un fallo inyectado; exportación CSV/JSON recargable y recomputación de resultados desde originales y referencias. Registrar tamaño por ciclo, disponibilidad y todos los fallos. No contar esta serie como validación del instrumento o de su autonomía.

Comandos objetivo de la entrega, **aún no disponibles**:

```sh
python3 -m unittest discover -s software/tests
python3 software/cruz.py --simulate --cycles 1 --config software/config/operation.example.json --output /tmp/cruz-sim
```

## 4. Siguiente conexión al hardware: puertas de entrada

| Paso | Prueba concreta | Condición previa |
| --- | --- | --- |
| A. Pi + cámara aisladas | Enumerar OV9281, confirmar RAW lineal y captura/ROI/metadatos; oscuro/blanco/muestra en banco con iluminación controlada externamente | Alimentación y cámara por conexiones conocidas; V8 desconectada. No habilita GPIO de potencia. |
| B. Sensores uno a uno | AS7265x: crudos/calibrados y plazos; DS18B20: CRC; Atlas: respuesta/unidad/compensación | Cableado, niveles, alimentación y bus revisados para cada módulo. No energizar una interfaz desconocida para identificarla. |
| C. Control con cargas de prueba | Confirmar niveles lógicos, arranque/reset, fallo de programa, exclusión de fuentes y pulsos del motor | Revisión eléctrica cerrada para esas señales, estados de fallo medidos y límite independiente para actuadores. Después, calibrar bomba y tiempos reales. |
| D. Servicio físico y autonomía | Transferir archivos completos con hash y reanudar descarga interrumpida; medir tiempo real por ciclo/descarga; apagado y siguiente despertar | Transceptor y EN3 verificados; definir protocolo tras medir volumen. Validar RTC/corte/guardado y fuga/batería antes de pruebas autónomas. |

Para D, propuesta a cerrar: Modbus RTU para consulta/estado/configuración y una operación de lectura por bloques de archivos con identificador, tamaño, offset e integridad, compatible con reanudación. No fijar registros, velocidad, direcciones, tamaño de bloque ni pines sin comprobar la electrónica real. La Pi apagada no sirve archivos: la sesión de servicio requiere un despertar y alimentación mantenida verificados.

El núcleo simulado permite avanzar ahora, pero no cumple por sí solo el despliegue autónomo: faltan drivers reales, supervisión independiente, fuga/batería, servicio físico, calibración y ensayo integrado. Se omiten en esta iteración web, Wi-Fi, OTA, radio, modelos nuevos de clorofila, cámara auxiliar y rediseño mecánico.

## 5. Evidencia de esta revisión

- Netlist XML exportada con KiCad CLI desde V8 a un archivo temporal; se inspeccionaron componentes, referencias y redes. No se alteró el diseño. Para repetir: `kicad-cli sch export netlist --format kicadxml --output /tmp/cruz-v8.xml electronica/cross_v8_raspberry/cross_v8_draft.kicad_sch`.
- Comprobaciones existentes ejecutadas: `MonoSpectro/spectro_math.py`, `Fluorometer/tests/check_white.py` y `Fluorometer/tests/check_firmware.py`: todas pasan. La primera comprueba las ecuaciones actuales, incluidos sus recortes; la segunda ejecuta C++ con dispositivos simulados; la tercera comprueba principalmente estructura/texto y fórmula del firmware. No demuestran validez óptica ni compatibilidad con Pi.
- No se ejecutó una adquisición ni se instaló software en la Pi. Sin hardware activado, sin descarga física, sin pruebas de corte eléctrico. No se modificó ni recompiló firmware ESP32. Sin commit ni push.

Identificación de las fuentes locales leídas (SHA-256; HEAD orientativo, el hash de archivo identifica el contenido revisado):

| Fuente | SHA-256 |
| --- | --- |
| V8 esquema | `d2a346aeb1e3ee872ee54396d219a7cd4b42f6284495c0c0832b75d14ea90863` |
| V8 PCB | `1c81c5b83dc3ce8274b2ce2147d3c1f0fb1775d53a8852257a7018e004bbaf1a` |
| MonoSpectro `app.py` (HEAD `65af45a`) | `80f98575bbc6f7c085074f58ec61191ebfe79ea363b290f1b14f0b5611206d1d` |
| MonoSpectro `spectro_math.py` | `a18d3aad9b54bf1f4f68edbbe4af82ec35d9c20fde597ddb87479d9c150f844c` |
| Fluorometer `Spectro18_V_Flu.ino` (HEAD `f2cdedf`) | `d92809bafaec65f469ed563e159c1b481de33873a30606bbee781af6ff1a0934` |
