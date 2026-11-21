# Cruz Prototype

Cruz is an autonomous optical instrument for monitoring natural waters. It is being developed in lakes for eventual use in bays. A single quartz flow cell serves a shared illumination arm with a halogen transmission source and selectable blue, red and infrared LEDs, an inline camera for transmission, and an AS7265x at 90° for fluorescence. The transmission target is 420–780 nm; fluorescence includes nominal 430 nm excitation, with additional red and infrared sources to be tested. A downstream peristaltic pump draws water through the cell. Temperature and conductivity are part of the design.

## Project files

| To work on | Open |
| --- | --- |
| Requirements and design rationale | [Functional specification](ESPECIFICACION.md) · [Decision log](DECISIONES.md) · [Optical design](docs/DISENO_OPTICO.md) |
| Mechanical assembly | [CAD guide](cad/README.md) |
| Fabrication files | [End-cap SVG for Shaper Origin](body/TAPA_SHAPER_230_PROTOTIPO.svg) · [Machining notes](body/LEEME.md) · [R3 attachment ring STL](cad/fusion_m2/ARO_AMARRE_M8_REFORZADO_R3.stl) · [R5 internal chassis STL and assembly guide for Prusa MINI](cad/fusion_m2/chasis_r5/README.md) |
| Electronics | [KiCad V8 project](electronica/cross_v8_raspberry/cross_v8_draft.kicad_pro) · [PCB status and open items](electronica/cross_v8_raspberry/LEEME_PRIMERO.md) |
| Acquisition and control | [Reusable software, V8 interfaces and proposed first iteration](docs/SOFTWARE_ADQUISICION.md) |
| Test records and simulation data | [Test log](docs/REGISTRO_ENSAYOS.md) · [R3 load and ballast study](cad/fusion_m2/simulacion_amarre_2026-11-20/) · [Calibration procedures](docs/VALIDACION_Y_CALIBRACION.md) |
| Procurement records | [Purchase list](compras/LISTA_COMPRA.md) · [Technician's workbook](compras/Cruz_Shopping_List_EN_2026-10-30.xlsx) |
| Earlier designs and assembly video | [Archive guide](archivo/README.md) |

## Prototype status

The enclosure uses a horizontal clear acrylic tube with a 180 mm outer diameter, a 172 mm inner diameter and a length of 380 mm. Both Ø230 mm end caps use 10 mm acrylic. The auxiliary USB camera looks forward through the front cap. The rear cap service holes will be drilled to suit the actual fittings.

The removable R5 chassis uses two flat-printed end frames and a bolted centre bridge. The optical cradle, cover and PCB tray are removable. All six parts fit the Original Prusa MINI. Fusion v13 documents the R3 attachment ring and ballast simulation. Physical load and leak tests are pending. KiCad V8 is the editable electronics draft. Routing and electrical review are pending. Purchase prices and quantities in the workbook are dated 30 October 2026.

The [engineering index](docs/INDICE_PROYECTO.md) links to the detailed design, build and validation records.
