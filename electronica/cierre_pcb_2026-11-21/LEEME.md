# Entrega de revisión PCB V8 · 21/11/2026

[Estado, montaje y condiciones pendientes](../cross_v8_raspberry/CIERRE_PCB_2026-11-21.md). La fuente editable es `../cross_v8_raspberry/cross_v8_draft.kicad_pro`; estos archivos son resultados de revisión, no una liberación de fabricación.

- `erc.json`: cero errores y cero avisos.
- `drc.json`: cero errores/avisos, cero conexiones pendientes y cero diferencias esquema–PCB.
- `redes.xml`: redes exportadas del esquema final, verificadas mediante `../revision_banco_2026-11-21/comprobar_conexiones.py`.
- `bibliotecas_comparadas.json`: 27 símbolos estándar sincronizados tras comprobar identidad de pines. CD4013 conserva unidad/números/tipos/coordenadas; su unidad de alimentación pasa de dibujo normal a común a ambos estilos.
- `bom.csv`: 122 posiciones físicas; R26/R27 DNP. No acredita existencias ni compra.
- `conectores.csv`: redes por pin; usar números de pad junto con los planos y el equipo real.
- `posiciones.csv`: 120 componentes a montar, 26 inferiores; milímetros, sistema de coordenadas KiCad, DNP excluidos.
- `vistas/`: cobre y montaje de ambas caras en SVG y PNG; las vistas inferiores están espejadas. Los dos DNP aparecen tachados en montaje.
- `placa_sin_componentes.step`: sustrato y taladros para revisión mecánica. No incluye envolventes/alturas de componentes, cableado ni fijaciones nuevas.
- `verificacion.json`: resultados, límites y hashes de las fuentes y salidas.

KiCad 9.0.7. Trazado inicial local con Freerouting 2.0.1, cierre de la última pista y relleno de planos con KiCad. No se ha probado hardware, transitorios, temperatura ni encaje. Los respaldos previos están fuera del repositorio en `/Users/alex/.codex/backups/Cruz/2026-11-21_antes_colocacion_trazado`.
