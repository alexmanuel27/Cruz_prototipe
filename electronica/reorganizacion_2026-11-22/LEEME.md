# Comprobación tras retirar el trazado · 22/11/2026

- `cross_v8_draft.svg`: esquema reorganizado por bloques siguiendo la disposición de Alex; equilibrio entre líneas locales y etiquetas de alimentación, masa, señales largas y enlaces entre bloques.
- `erc.json`: sin incidencias eléctricas.
- `drc.json`: sin infracciones geométricas ni diferencias esquema–PCB; **298 conexiones pendientes**, esperadas porque se pidió eliminar todo el trazado.
- Ajuste visual: símbolos GND y alimentación; los rótulos de tensión muestran `5V`, `3V3` y `12V`. Las ramas aislada y permanente conservan su identidad eléctrica. Sensores desde 3V3 de Pi, U10 retirado; C8/C9 se conservan como desacoplos. Resumen en `conexiones_por_bloques.json`.
- Comprobación del contrato: 404 pines verificados tras retirar U10 y alimentar sensores desde 3V3_PI; sin W1–W57 ni redes `__WIRE_`.

La placa conserva 121 posiciones y el contorno de 132 × 102 mm. Cero segmentos, vías y zonas. Esta revisión no incluye archivos para fabricar. Estado vigente en `../cross_v8_raspberry/LEEME_PRIMERO.md`.
