# Registro de ensayos y fotografías

**26 de septiembre de 2026. Estado inicial: ningún ensayo físico de Cruz ejecutado en esta tarea. No hay fotografías de montaje ni resultados experimentales nuevos.**

## Ensayos programados

| ID | Fecha prevista | Objeto | Estado | Datos / foto / resultado |
|---|---|---|---|---|
| OPT-01…07 | 7–12 oct | Espectro, emisión, geometría e interferencia | Planificado | Pendientes |
| EST-01 | **30 oct** | Inmersión con lastre, sin electrónica, todas las interfaces | **Planificado; fecha dura** | Pendientes |
| EST-02 | 30 oct–2 nov | Inmersión prolongada de 72 h sin electrónica | Planificado | Pendientes |
| HID-01…05 | Durante integración; cierre antes del 17 nov | Renovación, arrastre, burbujas y fallos de bombeo | Planificado | Pendientes |
| AUT-01…04 | 13–16 nov y pruebas de fallos durante X3 | Autonomía, deriva y recuperación | Planificado | Pendientes |
| BAN-01 | 17–19 nov | Comparación contra espectrofotómetro | Planificado | Pendientes |
| BAN-02 | 17–19 nov | Fluorescencia y clorofila frente a referencias | Planificado | Pendientes |
| CAM-01 | 24 nov | Campo varias horas y pares contemporáneos | Planificado | Pendientes |

Los criterios se encuentran en [Validación y calibración](VALIDACION_Y_CALIBRACION.md). Una fecha prevista no es un resultado aprobado.

## Plantilla del acta de cada ensayo

Copiar esta estructura en `docs/ensayos/AAAA-MM-DD_ID.md` al ejecutar el trabajo:

- **ID, fecha y operador:**
- **Objetivo y requisito comprobado:**
- **Estado:** iniciado / completado / interrumpido.
- **Versiones:** CAD, electrónica, software, calibración y configuración real.
- **Instrumentos y patrones:** referencia, número de serie, lote, calibración, unidades.
- **Muestras:** ID, preparación, conservación, edad y volumen.
- **Condiciones:** temperatura, profundidad/presión, alimentación y ajustes.
- **Criterio de aceptación fijado antes del ensayo:**
- **Procedimiento realmente seguido y desviaciones:**
- **Datos originales y archivos de configuración:** enlaces relativos.
- **Fotografías:** antes, durante y después; cada una con pie, fecha y componente visible.
- **Resultados:** valores, dispersión, incertidumbre pertinente y observaciones.
- **Dictamen:** APROBADO / FALLIDO / INCONCLUSO, con razón.
- **Acciones:** reparación, repetición requerida y vínculo a la decisión.
- **Revisión:** responsable y fecha.

## Fotografías que deben tomarse mientras aún son posibles

| Etapa | Fotografías mínimas |
|---|---|
| Inventario | Etiquetas de cámara, lente, LED/lámpara, placa AS7265x y filtro; regla junto a rendija |
| Fabricación | Pieza y versión, acabado de ranuras, medidas críticas y defectos |
| Sellado | Junta en su ranura antes de cerrar; ventana, cada pasamuros y racor; vista de conjunto |
| EST-01 | Interior seco y lastre; testigos identificados; profundidad/montaje; apertura e inspección final |
| Electrónica | Conexiones de potencia, fusible/protecciones, polaridad, rutas de cables y fijación antes de ocultarlas |
| Óptica | Muestra central, fuentes, detectores, filtro, baffles y ajustes de alineación |
| Hidráulica | Toma, orientación de celda, bomba y descarga; posición de burbujas/fugas si aparecen |
| Campo | Lugar, fijación, profundidad, toma/descarga y estado al recuperar |

Guardar originales en `docs/fotos/AAAA-MM-DD/` con nombres como `EST-01_junta_tapa_antes_01.jpg`. Conservar metadatos y relacionarlos con el acta. Un render CAD o una imagen ilustrativa no sustituye una fotografía de montaje. Los fallos también se fotografían.
