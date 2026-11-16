# Índice del proyecto

Punto de entrada para localizar la documentación de ingeniería y preparar una revisión del proyecto. Las fechas indican la revisión de los archivos, no la realización de ensayos físicos. Las decisiones y los resultados deben comprobarse en sus fuentes.

## Alcance y decisiones

- [Especificación funcional](../ESPECIFICACION.md): requisitos y funcionamiento previstos.
- [Registro de decisiones](../DECISIONES.md): acuerdos, alternativas y cuestiones abiertas.
- [Análisis de arquitectura](ANALISIS_ARQUITECTURA.md) y [diseño óptico](DISENO_OPTICO.md): fundamentos de la integración óptica y la celda.
- [Plan de trabajo](PLAN_TRABAJO.md): calendario previsto; no evidencia de cumplimiento.

## Diseño mecánico y montaje

- [Implantación horizontal en acrílico](IMPLANTACION_ACRILICO_HORIZONTAL.md): concepto del cuerpo, cámara y lastre.
- [Modelo Fusion de montaje accesible, 3 noviembre](../cad/fusion_m2/CROSS_MONTAJE_ACCESIBLE_2026-11-03.f3d): copia de revisión local. Comprobarla frente al documento guardado en Fusion antes de utilizarla para fabricar.
- [Secuencia de montaje](../cad/fusion_m2/animacion/MONTAJE_PASO_A_PASO.md) y [vídeo de montaje](../cad/fusion_m2/animacion/CROSS_MONTAJE_ORDEN_REAL_2026-11-03.mp4): orden propuesto y acceso a piezas.
- [Piezas impresas de la revisión](../cad/fusion_m2/PIEZAS_IMPRESAS_MONTAJE_2026-11-03.json): inventario de diseño, no orden de impresión.
- [Tapas de 10 mm y preparación CNC](../cad/fusion_m2/TAPAS_CNC.md); [revisión de modelos comerciales](../cad/fusion_m2/REVISION_STEP_2026-11-03.md); [revisión de estanqueidad](REVISION_ESTANQUEIDAD_TUBO.md).
- [CAD M1](../cad/README.md), [implantación anterior](IMPLANTACION_INTERIOR_V1.md) y [concepto de PVC](IMPLANTACION_PVC_HORIZONTAL.md): antecedentes, no el montaje actual.

## Electrónica y energía

- [PCB V8: leer primero](../electronica/cross_v8_raspberry/LEEME_PRIMERO.md): estado y limitaciones del diseño más reciente disponible. **La V8 no está lista para fabricar ni energizar.**
- [Propuesta eléctrica V1](../electronica/DISENO_ELECTRICO_V1.md), [puerto de servicio](../electronica/PUERTO_SERVICIO_Y_BOYA.md) y [presupuesto energético](PRESUPUESTO_ENERGETICO.md): antecedentes de diseño; contrastar con las revisiones posteriores.
- Las versiones anteriores de los proyectos KiCad se retiraron del árbol de trabajo; se pueden consultar en el historial de Git.

## Ensayos, calibración y evidencia

- [Registro de ensayos y fotografías](REGISTRO_ENSAYOS.md): plantillas y estado documentado; no confundir pruebas previstas con resultados.
- [Validación y calibración](VALIDACION_Y_CALIBRACION.md): procedimientos y criterios propuestos.
- Las comprobaciones JSON y las imágenes en `cad/fusion_m2/` documentan estudios digitales; no sustituyen el montaje físico ni el ensayo de estanqueidad.

## Materiales y compras

- [Lista de compra](../LISTA_COMPRA.md) y [hoja de cálculo para el técnico](../Cruz_Shopping_List_EN_2026-10-30.xlsx): versiones disponibles del 30 de octubre; verificar precios, disponibilidad y decisiones posteriores.
- [Lista amplia de materiales](../LISTA_MATERIALES.md) y [antecedentes de compras](ANTECEDENTES_LISTA_COMPRA.md): históricos de consulta.

## Imágenes y fuentes

- [Dibujos y bocetos](drawings/) y [renders](renders/): ilustraciones de distintas etapas; comprobar su fecha y la arquitectura representada.
- [Modelos de componentes](../cad/componentes/MODELOS_3D.md): procedencia y limitaciones de modelos 3D.
- Los archivos conservados en `cad/fusion_m2/` incluyen copias anteriores y comprobaciones intermedias. Sus nombres describen la etapa; no asumir que una copia es una versión aprobada.

No se identificó una carpeta `firmware/` en la raíz al preparar este índice. La ausencia de un archivo o de una prueba en este índice no demuestra que no exista fuera del repositorio.
