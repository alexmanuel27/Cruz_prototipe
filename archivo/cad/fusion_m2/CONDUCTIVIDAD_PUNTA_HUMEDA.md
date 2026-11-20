# Conductividad: solo la punta dentro del agua

Revisión 2026-11-02. Montaje actualizado en `CROSS_EC_PUNTA_HUMEDA_2026-11-02.f3d`.

## Corrección

La sonda Atlas K1 mide en los electrodos de la punta. Se descarta la cámara larga que envolvía todo el cuerpo. El nuevo conjunto `06_AGUA_Y_SENSORES / 03_CONDUCTIVIDAD_SOLO_PUNTA_HUMEDA` incorpora:

- Modelo oficial Atlas de la sonda, con los orificios de sus electrodos.
- Bloque corto de flujo, de 37 mm, con la zona activa completamente mojada.
- Salida situada a la altura del techo de la cavidad para facilitar la evacuación de aire.
- Racor de compresión alrededor del vástago, con el cuerpo largo y el cable en seco.
- Apoyos separados para el bloque y el cuerpo seco: el racor no sostiene todo el peso.

Las dos mangueras se adaptaron al nuevo bloque; sus curvas modeladas tienen radio de 15 mm. El circuito mantiene temperatura → conductividad → cubeta → bomba. La cámara larga, sus juntas, sus varillas y los recorridos anteriores quedan ocultos y descartados.

## Datos y fuentes

La ficha actual Gen 3 muestra una zona sensible de 15,5 mm, vástago de 12 mm, cabeza de 16 mm y longitud de 150,3 mm. Es necesario sumergir toda la superficie conductora. En el montaje, la punta está en X=186 mm y su zona activa queda dentro de la cavidad X=178–206 mm; eje Y=0, Z=−60 mm.

- [Ficha oficial de la sonda](https://files.atlas-scientific.com/EC_K_1.0_probe.pdf).
- [STEP oficial de Atlas](https://files.atlas-scientific.com/ENV-40-EC-K-1.0.zip), guardado en `cad/componentes/atlas_conductividad/`.
- [Guía de montaje en tubería](https://files.atlas-scientific.com/connecting-probes-into-a-pipe.pdf).
- [Racor de sonda Atlas, opción 1/2 NPT](https://atlas-scientific.com/connectors/probe-pipe-fitting/).

El STEP publicado es de 2021 y corresponde a una generación anterior: cuerpo de unos 145,6 mm, vástago de 12,2 mm y cabeza de 16,3 mm. La ficha actual y este STEP no coinciden exactamente. Verificar la generación de la pieza comprada antes de cerrar el diámetro del sellado y las posiciones de sus apoyos. Se recortó únicamente la representación del cable del STEP para evitar una cola rígida de cable atravesando el montaje; el cable real debe dirigirse hacia la interfaz EZO.

## Fabricación y comprobación

El bloque de flujo es una propuesta mecanizada. El racor comercial está representado mediante una reserva de espacio; su longitud, rosca y juntas deben ajustarse a la pieza elegida. No fabricar una junta estanca a partir de esa envolvente simplificada ni usar sus cotas como plano de roscado.

Los apoyos blandos de 2 mm se cortan en espuma y las cunas están integradas en el chasis. La lista general de piezas impresas conserva sus 19 piezas. El cuerpo de agua y el racor no son piezas previstas para impresión FDM.

`COMPROBACION_EC_PUNTA_2026-11-02.json` registra la revisión de los 185 cuerpos activos del montaje, incluyendo las categorías que Alex tenía ocultas en su vista: cero cruces no previstos. Permanecen ocho intersecciones de las representaciones simplificadas de las roscas M8.

Después del montaje real: comprobar inmersión de toda la zona activa, purga de burbujas, estanqueidad del racor y calibración con la sonda instalada. El documento activo de Fusion tiene cambios sin guardar; la copia F3D sí está exportada.
