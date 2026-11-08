# Assembly animation

- **CROSS_MONTAJE_ORDEN_REAL_2026-11-03.mp4** — 31 assembly stages, 1920 × 1080, 24 fps, Spanish captions and embedded chapters.
- **MONTAJE_PASO_A_PASO.md** — sequence, timestamps, proposed mechanical access changes and validation limits.
- **PORTADA_MONTAJE.png** / **SECUENCIA_MONTAJE.png** — cover and sequence overview.
- **../CROSS_MONTAJE_ACCESIBLE_2026-11-03.f3d** — proposed revision, assembled.
- **CROSS_ANTES_ANIMACION.f3d** — original preserved before animation work.

This MP4 was generated from the Fusion model viewport. It is not an editable native Fusion storyboard. No cloud save was made.

`PLAN_MONTAJE.json`, `ESTADO_ANTES_ANIMACION.json` and the Python scripts retain the assembly sequence and source transforms. Rendering restores those transforms after each batch. `VALIDACION_MONTAJE.json` and `VALIDACION_CIERRE_FINAL.json` record sampled insertion checks; `ESTADO_FINAL_VERIFICADO.json` records final pose verification and existing timeline issues. Physical fit, tools and flexible cables still need checking.

Intermediate native frames and captioned frames are generated caches. They can be reproduced by running `renderizar_en_fusion.py` in batches inside the corresponding Fusion design, then running `componer_video.py` with Pillow and imageio-ffmpeg. Do not rerun the mechanical revision scripts on an already revised design.
