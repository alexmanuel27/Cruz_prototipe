# Comprobación tras retirar el trazado · 22/11/2026

- `cross_v8_draft.svg`: esquema reorganizado por bloques siguiendo la disposición de Alex; conexiones internas mediante líneas y etiquetas solo entre bloques.
- `erc.json`: sin incidencias eléctricas.
- `drc.json`: sin infracciones geométricas ni diferencias esquema–PCB; **301 conexiones pendientes**, esperadas porque se pidió eliminar todo el trazado.
- Etiquetas: 377 → 105. Las redes internas sin etiqueta reciben nombres automáticos de KiCad; se comparan los conjuntos completos de pines, no esos nombres. Resumen en `conexiones_por_bloques.json`.
- Comprobación del contrato: 409 conexiones originales conservadas; sin W1–W57 ni redes `__WIRE_`.

La placa conserva 122 posiciones y el contorno de 132 × 102 mm. Cero segmentos, vías y zonas. Esta revisión no incluye archivos para fabricar. Estado vigente en `../cross_v8_raspberry/LEEME_PRIMERO.md`.
