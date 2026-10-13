# Plan de ingeniería hasta el 1 de diciembre de 2026

**Propuesta del 26 de septiembre. Responsable técnico: Alex.**

Fuente del calendario: [P3 del plan doctoral](</Users/alex/Nube /nube/investigacion/doctorado/Orbital/plan-sep-dic-2026.md>). Se conservan sus hitos; las actividades adicionales de comprobación se hacen explícitas para evitar suponer que ya están incluidas.

## 1. Camino crítico

Especificación → prueba óptica → cierre de geometría  → diseño de sellado → fabricación → **estanqueidad 30 oct** → electrónica → adquisición autónoma → autonomía y banco → campo 24 nov → documentación.

En paralelo, la campaña debe entregar material reservado, trazable y con conservación válida. Esa dependencia es analítica y no se resuelve comprando componentes. El firmware de los instrumentos previos necesita cambios para poder operar sin navegador y con calibración externa; no basta con unir sus interfaces web.

## 2. Fechas, resultados y condiciones de paso

| Periodo | Trabajo y evidencia | Dependencia / condición de paso |
|---|---|---|
| 26 sep–4 oct | Revisar este análisis; inventario físico de fuentes/detectores, rendija, filtro y lente; preparar lista de reservas de campaña | Solo preparación y consulta técnica; óptica aún abierta |
| **5–6 oct · X1.1** | Cerrar ESPECIFICACION.md: magnitudes, 72 h propuestas, cadencia, profundidad, errores admisibles, interfaz y estados de fallo | Especificación funcional aprobada (27 de septiembre) |
| **5–9 oct · dependencia C2.1** | Campaña con MonoSpectro; separar y preservar reserva en cada jornada | Registro de IDs, volumen, estado, conservación y referencia; Cruz no sale |
| **7–12 oct · X1.2** | OPT-01…07, comparación de geometrías y acta de cierre óptico | En curso. No pedidos ni impresión hasta este cierre |
| 12–13 oct · dependencia C2.2 | Auditar reservas y distribución a proyectos | Preservación ya iniciada cuando lo exigía cada método |
| **13–19 oct · X1.3** | Ajustar el [CAD M1 preliminar](../cad/README.md) a piezas medidas; cerrar celda, juntas, pasamuros, presión, apriete, limpieza, disipación y protocolo de estanqueidad | Geometría y componentes ópticos cerrados; revisión completa el 19 |
| **20–23 oct · X1.4** | Esquemáticos, drivers, protecciones, enlace Pi–ESP32, memoria, consumo real y BOM | Verificar arranque de lámpara/bomba, estabilidad de alimentación y capacidad para 72 h |
| **26–29 oct · X2.1** | Impresión de soportes, mecanizado de interfaces, montaje sin electrónica e inspección dimensional | Juntas y pasamuros disponibles; fotos de cada interfaz antes de ocultarla |
| **30 oct · X2.2** | Ensayo duro de estanqueidad, lastre y sin electrónica; acta APROBADO/FALLIDO | Si falla: rediseño y repetición antes de electrónica |
| 30 oct–2 nov | Extensión sin electrónica de 72 h a profundidad de servicio | Preparación externa de arneses el 2; inspección final antes de instalar |
| **2–4 nov · X2.3** | Preparar arneses; instalación tras aprobar, prevista el 3–4; control de humedad y carga térmica | No modificar interfaces ensayadas sin repetir comprobación |
| **5–11 nov · X3.1** | Adquisición autónoma, secuencia segura, lectura 18 canales, configuración, persistencia y recuperación | Un ciclo completo sin interfaz abierta; fallos de actuador/sensor acotados |
| **12–16 nov · X3.2** | Interfaz local y descarga; iniciar AUT-01 el 13 para acabar el 16 | Congelar versión antes del ensayo de autonomía; toda modificación relevante exige reevaluar su efecto |
| **17–19 nov · X4.1** | Comparación contra comerciales, reservas reanalizadas y material vivo pertinente; criterios del protocolo | Acceso a referencias reservado, calibración congelada y muestras válidas |
| 20–23 nov | Margen para correcciones concretas, repetición afectada y preparación de campo | No introducir funciones nuevas ni contar este margen dos veces |
| **24 nov · X4.2** | Campo de varias horas en un lago de la campaña, con pares de muestra actuales | Banco aprobado, condiciones de despliegue documentadas y recuperación prevista |
| **25–27 nov · X4.3** | Ajustes finales, instrucciones de uso/recalibración, registro y fotografías completas | Toda prestación respaldada por ensayo; desviaciones visibles |
| **1 dic** | Prototipo, fuentes editables, código, BOM y datos de aceptación entregados | Reportar por separado banco, campo y autonomía multiday realmente demostrados |

## 3. Riesgos de agenda que el calendario original no resuelve solo

**Campaña y especificación/diseño coinciden.** Alex tiene trabajo de campo del 5 al 9 y Cruz del 5 al 12. Dejar esta propuesta avanzada en septiembre reduce carga, pero no elimina las sesiones de revisión y óptica. Reservar bloques explícitos y apoyo de Daniela para preparación/lecturas cuando su agenda lo permita; no dar esa disponibilidad por confirmada. Un cierre óptico tardío comprime la fabricación y pone en riesgo el 30.

**Los comerciales tienen agenda compartida.** El plan reserva fluorómetro para P1 del 12 al 15 de octubre. Hacer las pruebas decisivas de selección con material/patrones disponibles y aprovechar una sesión de referencia al inicio del 12 solo si está confirmada; si la decisión depende de una referencia indisponible, no afirmar que quedó validada. Reservar en la planificación también el 17–19 de noviembre y el procesado de pares del 24.

**Los equipos originales siguen trabajando.** MonoSpectro participa en mediciones hasta el 27 de octubre y el fluorómetro tiene sus propios hitos. «Mismos detectores y fuentes» se interpreta como conservar tecnología/modelos; no supone permiso para desmantelar los ejemplares activos. Primero inventariar repuestos. Si hay que duplicar componentes, incluirlos en BOM después del cierre óptico, o acordar una fecha real de transferencia.

## 4. Pedidos después del cierre óptico

El plazo de una semana es una hipótesis comunicada por Alex, no una promesa de proveedor. Antes de comprar, confirmar stock, entrega, impuestos y compatibilidad exacta. Este análisis no realiza pedidos.

| Lote | Momento más temprano propuesto | Necesidad |
|---|---|---|
| Duplicados de componentes (Lente confirmada; celda de cuarzo ya comprada; lote de repuestos/duplicados si es necesario) | Después del acta óptica del 12 oct | Verificar datasheet y dimensiones de la celda de cuarzo para cerrar mecánica |
| Envolvente, juntas, pasamuros, tubos y bomba | Tras fijar interfaces, como máximo 19 oct | Recibir alrededor del 26; esta holgura es pequeña, comprobar stock antes de cerrar diseño |
| Alimentación, drivers, almacenamiento y auxiliares | Tras verificación eléctrica, preferiblemente 20–21 oct | Recibir antes del montaje del 2–4 nov; el 23 es un límite ajustado |

Si un componente define una ventana o sellado y su entrega es incierta, elegir una alternativa disponible antes de cerrar X1.3. No mecanizar agujeros contra una ficha incompleta ni posponer el ensayo duro por comodidad de proveedor.

El plan doctoral menciona aproximadamente **5.000 € para el conjunto de proyectos**. No se asigna esa suma completa a Cruz. La BOM futura distinguirá reutilización, duplicado, fabricación, fungible y repuesto, con referencia del fabricante, proveedor, cantidad, precio unitario real, moneda, IVA, portes, fecha y plazo confirmado.

Antecedentes localizados: [compras mensuales](</Users/alex/Nube /nube/investigacion/doctorado/compras/mensuales>) incluye Amazon Bélgica, RS y Tinytronics; [MonoSpectro](../../MonoSpectro/README.md) enlaza RobotShop y Edmund Optics. Las listas históricas orientan dónde consultar, pero no prueban inventario, compra ejecutada ni precios actuales. No se ha creado una BOM definitiva mientras la óptica sigue abierta.

## 5. Archivos a producir en cada fase

| Destino | Contenido requerido |
|---|---|
| `ESPECIFICACION.md` | Requisitos medibles y revisiones aprobadas |
| `DECISIONES.md` | Alternativas, razones, estado y evidencia |
| `cad/` — M1 iniciado el 30 sep, cierre en X1.3 | Modelo paramétrico nativo editable, STEP, planos con tolerancias/ensambles y STL derivados; medir interfaces antes de fabricar |
| `electronica/` desde X1.4 | Fuentes de esquemas, conexiones, protecciones, presupuesto energético y BOM fechada |
| `firmware/` desde X3 | Software Pi y ESP32 integrado, versiones de dependencias, configuración y comprobación mínima de ciclo/fallos |
| `docs/ensayos/` | Un acta por ensayo con datos originales, configuración, criterios y resultado |
| `docs/fotos/` | Fotografías reales de fabricación, juntas, montaje, cableado, ensayo y campo, vinculadas a actas |

Crear fuentes y documentación con cada trabajo real. El CAD M1 es una propuesta paramétrica temprana y no equivale al cierre de fabricación de X1.3; esquemáticos y firmware se cerrarán en sus fases. En fablab existen precedentes editables de Inventor y KiCad; verificar equipo, material y capacidad actuales antes de adoptar sus parámetros de fabricación.

## 6. Resultado esperado de esta fase

La especificación funcional y la geometría óptica se han fijado. El siguiente paso técnico es identificar físicamente los componentes, ejecutar OPT-01…07 y ajustar las interfaces del CAD M1. La compra y la fabricación esperan la selección dimensional de juntas, racores, batería y disipación, además de las pruebas ópticas y térmicas necesarias.
