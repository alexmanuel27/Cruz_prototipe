> **Actualización D56, 21 nov 2026:** Alex selecciona una [lámpara halógena](../DECISIONES.md#d56--halógena-para-transmisión-2026-11-21) para transmisión. Alex confirmó 12 V y 10 W y comprobó el encendido con una fuente de banco. Quedan por medir la estabilización óptica y la temperatura en el montaje.

> **Actualización D55, 21 nov 2026:** geometría óptica en T: un brazo común con fuentes seleccionables, cámara en transmisión y AS7265x a 90°. Sustituye la geometría colineal anterior. Geometría detallada, integración y validación pendientes; no se han modificado CAD ni PCB.

# Diseño Óptico Detallado: Cruz

Este documento técnico define la geometría y los componentes ópticos del prototipo Cruz. El diseño está en curso y sirve como especificación base para el diseño mecánico y electrónico.

## 1. Parámetros Confirmados
*   **Rendija de Transmisión:** 0,5 mm de ancho, después de la celda en el camino óptico. Alex confirmó una separación nominal de 60 mm respecto a la cámara; la figura del MonoSpectro acota 60 mm hasta la red/lente unida a ella. Medir las superficies de referencia antes de trasladar esa cota al CAD.
*   **Rango Espectral de Transmisión:** 420–780 nm.
*   **Lente:** Gran angular (la utilizada y validada físicamente en el montaje de MonoSpectro).
*   **Celda de Muestra:** Celda de flujo de cuarzo, comprada y compartida entre ambos caminos ópticos.
*   **Fluorescencia (Excitación):** LED azul de 430 nm.
*   **Fluorescencia (Detección):** Sensor AS7265x de 18 canales; se registrarán todos. Los canales útiles para cada excitación requieren validación en esta geometría.
*   **Filtros Ópticos:** El diseño anterior eliminó el filtro de emisión; verificar luz de excitación y señal de fondo a 90° antes de considerar cerrado el diseño óptico. No atribuir pureza de fluorescencia por canal sin ensayo.
*   **Geometría:** Un brazo común con halógena y LED azul, rojo e infrarrojo seleccionables ilumina la celda. La cámara observa transmisión en el eje del haz; el AS7265x observa a 90°.
*   **Secuencia Óptica:** Primero medición de transmisión, luego fluorescencia.
*   **Hidráulica:** Toma -> Celda de cuarzo (entrada por una cara, salida por otra) -> Bomba peristáltica sumergida -> Descarga.

## 2. Geometría Propuesta

```mermaid
flowchart TD
    subgraph Eje Transmisión
    A[Brazo común: halógena y LED seleccionables] -->|Luz incidente| C{Celda de Cuarzo}
    C -->|Luz transmitida, sin colimador| B[Rendija 0,5 mm]
    B --> G[Red + lente gran angular]
    G --> D[Cámara monocroma]
    end

    subgraph Eje Fluorescencia
    C -->|Observación a 90°| F[Sensor AS7265x]
    end
```

La distancia nominal de 60 mm pertenece al conjunto rendija–cámara heredado; el punto exacto desde el cual medirla sigue pendiente de verificación física.

## 3. Interfaces y Dimensiones Pendientes (TBD)
*   **Distancias Exactas AS7265x:** Distancia desde la ventana de cuarzo hasta la superficie del sensor AS7265x (TBD).
*   **Distancias Exactas LED:** Distancia desde el LED de 430 nm hasta la ventana (TBD).
*   **Acoplamiento Hidráulico:** Dimensiones precisas de los racores de entrada y salida de la celda de cuarzo (TBD).
*   **Posicionamiento de la Rendija:** Tolerancias de paralelismo de la rendija respecto al sensor de imagen de la cámara.

## 4. Tolerancias Ajustables Necesarias
*   **Enfoque de la Cámara:** Mecanismo de ajuste para afinar la distancia de la lente a la celda (TBD).
*   **Alineación del Eje Principal:** Capacidad de alinear perpendicularmente el haz de transmisión a las caras de la celda.
*   **Ajuste de Altura AS7265x/LED:** Calzas o correderas para garantizar la altura central de la fuente de excitación y detección frente al volumen útil de la celda de cuarzo.

## 5. Protocolo de Pruebas (OPT-01 a OPT-07)
| ID Ensayo | Descripción | Criterio de Aceptación (Numérico o TBD) |
|---|---|---|
| OPT-01 | Eje espectral y resolución | ≥3 líneas conocidas; error de centro ≤2 nm, FWHM objetivo ≤10 nm |
| OPT-02 | Transmisión de blanco y patrones | CV de intensidad ≤2 % fuera del fondo |
| OPT-03 | Naturaleza de señal del fluorómetro | 435 no satura, 645 responde con muestra fluorescente |
| OPT-04 | Sensibilidad en agua natural | SNR ≥10 en el nivel mínimo, CV ≤5 % sobre cuantificación |
| OPT-05 | Validación de la geometría a 90° en la nueva celda | Fondo del blanco ≤10 % de la señal neta del nivel bajo |
| OPT-06 | Interferencia entre modalidades | Cambio ≤5 % en fluorescencia y ≤0,02 AU en transmisión |
| OPT-07 | Ventana, celda y materiales | Registrar transmisión a 430 nm/visible y autofluorescencia |

## 6. Condiciones de Aprobación
El diseño óptico se dará por cerrado y autorizará la fase de CAD final, compras e impresión únicamente si:
1.  Los valores TBD se completan basados en ensayos físicos documentados (con fotografía y hoja de cálculo) o en especificaciones técnicas concretas del fabricante.
2.  Las pruebas OPT-01 a OPT-07 se completan con resultados positivos.

## 7. Trazabilidad a Archivos Fuente

| Dato / Decisión | Archivo Fuente / Ruta Local |
|---|---|
| Geometría, Rendija y Filtros | `/Users/alex/Nube /repos/Cruz_prototipe/ESPECIFICACION.md` |
| Geometría en T y brazo común | `/Users/alex/Nube /repos/Cruz_prototipe/DECISIONES.md` (D55) |
| AS7265x y cálculo de clorofila | `/Users/alex/Nube /repos/Fluorometer/README.md` |
| Firmware Fluorescencia (menciona LED 435 nm como antecedente; no cambia especificación Cruz de LED 430 nm) | `/Users/alex/Nube /repos/Fluorometer/Spectro18_V_Flu/Spectro18_V_Flu.ino` |
| Fotos y Ensamblaje Original | `/Users/alex/Nube /repos/MonoSpectro/docs/images/cad_assembly.png` |
| Paper/Detalles del sistema | `/Users/alex/Nube /nube/investigacion/doctorado/espectroscopia/j.sna.2021.112698.pdf` |
