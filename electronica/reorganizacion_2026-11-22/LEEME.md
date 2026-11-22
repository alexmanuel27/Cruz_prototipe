# Comprobación tras retirar el trazado · 22/11/2026

- `cross_v8_draft.svg`: esquema de ocho bloques, con EC-OEM y sonda junto a los sensores, y pulsador y RTC en el bloque de encendido.
- `erc.json`: sin incidencias eléctricas.
- `drc.json`: sin infracciones geométricas ni diferencias esquema–PCB; **209 conexiones pendientes**, esperadas porque se pidió eliminar todo el trazado.
- Ajuste visual: símbolos GND y alimentación; los rótulos de tensión muestran `5V`, `3V3` y `12V`. La rama permanente es de 5 V. Sensores desde 3V3 de Pi, U10 retirado; C8/C9 se conservan como desacoplos. Resumen en `conexiones_por_bloques.json`.
- Comprobación del contrato: gestión externa por J13, GPIO directos para iluminación, pin 40 libre, sensores y EC desde 3V3_PI con I²C común y DS3231 por J24 y pulsador de 5 s en J25; sin W1–W57 ni redes `__WIRE_`.

La placa conserva 91 posiciones y el contorno de 132 × 102 mm. Cero segmentos, vías y zonas. Esta revisión no incluye archivos para fabricar. Estado vigente en `../cross_v8_raspberry/LEEME_PRIMERO.md`.
