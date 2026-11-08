# Alimentación y carga — revisión de arquitectura V3

**2 de noviembre de 2026.** Alex corrigió el dato previo de 14,2 V: la salida indicada para el cargador es **25,6 V**. El pack CITYORK anunciado como 24 V usa **un solo par de conexiones para alimentación y carga**. El valor 14,2 V queda descartado; no es una segunda tensión del sistema. Esto no determina la química, número de celdas, capacidad real, tensión máxima efectiva del pack, corriente nominal del cargador o comportamiento del BMS.

## Consecuencia para los DFR1015

Alex confirmó los convertidores DFRobot DFR1015. El fabricante [declara entrada de 7,5–30 V y recomienda menos de 24 V](https://www.dfrobot.com/product-2599.html). Por tanto, **25,6 V está dentro del intervalo declarado, pero por encima de la recomendación**; no se puede concluir que el convertidor esté dañado o que sea incompatible solo por ese dato. Tampoco se ha demostrado su funcionamiento fiable en la aplicación. Reservar 4,4 V nominales hasta 30 V no constituye una medición de transitorios.

El cierre de ingeniería requiere medir la tensión real en los bornes durante carga completa y operación, polaridad, transitorios de bomba/conmutación, salida y temperatura de cada convertidor bajo carga en la caja cerrada. Seleccionar protección contra transitorios y, si las mediciones o la recomendación del fabricante no resultan aceptables, un convertidor con margen mayor; no fijar un componente de supresión cuya tensión de trabajo/corte se desconoce. Las corrientes anunciadas por el fabricante dependen de la salida y refrigeración: no usar los 5 A como garantía sin ensayo.

## Esquema de conexión propuesto: terminales comunes

```text
                            ┌── F1 ── distribución interna de carga
PACK + / terminal común ────┤             y conversores
                            └── F2 ── contacto K1A normalmente abierto ── carga + del puerto

PACK − / terminal común ────┬──────── retorno interno
                            └──────── contacto K1B normalmente abierto ── carga − del puerto

Cargador original 25,6 V ───── cable de servicio ───── contactos de carga del puerto
```

K1 es una propuesta de relé bipolar que solo conecta los dos contactos de carga cuando su bobina está activada. Los polos de carga deben corresponder a los **mismos terminales externos del pack** que alimentan el equipo, respetando la protección del BMS. Con bobina desactivada, ambos contactos externos quedan abiertos. El circuito de alimentación sigue protegido por F1. F2 protege el ramal positivo de carga según el montaje definitivo; la posición y capacidad de cada fusible deben justificarse para ambos sentidos de corriente, cableado, corriente y limitación del BMS/cargador. No puentea el BMS ni constituye un cargador.

Esta figura es **funcional, no un esquema cableable**. Se requiere comprobar qué contacto del BMS corresponde a cada cable y validar polaridad, corriente del cargador, valores reales de fusibles, poder de corte en continua y corriente admisible de K1 y del conector sumergible. La potencia y resistencia de bobina determinan el circuito de control. Hace falta concretar además:

1. Un modo de servicio que despierte el equipo o habilite la conexión de carga aun con la Raspberry apagada, y el comportamiento con batería agotada.
2. Detección de cable, estado de carga, falla de fuga y prioridad de operación de modo que la desconexión del cable abra K1. Evitar que un contacto del puerto quede alimentado con el cable retirado, sin atribuir certificación de interbloqueo a software.
3. Aislamiento y asignación inequívoca de los ocho pines: carga +/−, alimentación externa futura +/−, RS485 A/B/referencia y señal de presencia. La alimentación de boya requiere un circuito de selección y regulación distinto; no unir una fuente externa directamente en paralelo al pack.
4. Carga y prueba con el cargador compatible suministrado, siguiendo las condiciones del fabricante y verificando el calentamiento del sistema. La aceptación final depende de ensayo y de la identificación del BMS, no de la tensión anunciada por sí sola.

El diseño V3 de KiCad **todavía no incluye este circuito de carga, el temporizador de encendido ni la distribución de potencia**. No usar este documento como autorización para cablear, fabricar, soldar o energizar la placa.
