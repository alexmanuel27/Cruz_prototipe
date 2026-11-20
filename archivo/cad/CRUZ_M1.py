"""CRUZ M1 mechanical layout, dimensions in mm.

Run with Python + build123d: python cad/CRUZ_M1.py
The STEP files are editable solids; the STL files are separate print parts.
All dimensions marked PROVISIONAL in cad/README.md must be measured before printing.
"""

from pathlib import Path
import json
from zipfile import ZipFile, ZIP_DEFLATED

from build123d import Align, Box, Color, Compound, Cylinder, Polygon, Pos, Rot, extrude, export_gltf, export_step, export_stl


OUT = Path(__file__).with_name("m1_export")
OUT.mkdir(exist_ok=True)

# M1 envelope: each printed part fits a 220 x 220 mm bed in XY.
HEAD_X0, HEAD_X1, HEAD_HALF_Y, HEAD_HALF_X, HEAD_Y = -75, 132, 39, 32, 80
HEAD_H, HEAD_WALL, HEAD_FLOOR = 120, 7, 8
POWER_X, POWER_Y, POWER_H = 190, 150, 90
PUMP_X, PUMP_Y, PUMP_H = 105, 105, 100
BOX_WALL, BOX_FLOOR, LID_T = 5, 5, 5
CELL_SIDE, CELL_BODY_H, CELL_TOTAL_H = 12.5, 40, 60  # NEXACULE listing; verify on delivered part
CELL_Z = 60
PUMP_HEAD_XY, PUMP_TOTAL_H, PUMP_HOLE_PITCH = 57, 60, 47  # Denash listing; verify
GASKET_T = 2.0  # PROVISIONAL flat silicone sheet, not a printed component
FLUID_BORE = 8.0  # PROVISIONAL bulkhead drill size; select fitting before printing
CABLE_BORE = 10.0  # PROVISIONAL cable-gland drill size; select gland before printing
INSERT_BORE = 5.5  # PROVISIONAL heat-set M4 insert pilot; tune to chosen insert and material


def box(x, y, z, cx=0, cy=0, cz=0):
    return Pos(cx, cy, cz) * Box(x, y, z, align=(Align.CENTER, Align.CENTER, Align.MIN))


def cyl(d, h, cx=0, cy=0, cz=0):
    return Pos(cx, cy, cz) * Cylinder(d / 2, h, align=(Align.CENTER, Align.CENTER, Align.MIN))


def cross(d=0):
    """Inset of the twelve-corner cross outline; positive d moves into solid."""
    x0, x1 = HEAD_X0 + d, HEAD_X1 - d
    hy, hx, y = HEAD_HALF_Y - d, HEAD_HALF_X - d, HEAD_Y - d
    return Polygon(
        (x0, -hy), (-hx, -hy), (-hx, -y), (hx, -y),
        (hx, -hy), (x1, -hy), (x1, hy), (hx, hy),
        (hx, y), (-hx, y), (-hx, hy), (x0, hy),
        align=None,
    )


def head_lugs(height, z=0):
    lug_centers = [(-60, -43), (-60, 43), (70, -43), (70, 43),
                   (115, -43), (115, 43),
                   (-36, -65), (36, -65), (-36, 65), (36, 65)]
    lugs = None
    for x, y in lug_centers:
        one = cyl(16, height, x, y, z)
        lugs = one if lugs is None else lugs + one
    return lugs, lug_centers


def head_body():
    outer = extrude(cross(), amount=HEAD_H)
    cavity = Pos(0, 0, HEAD_FLOOR) * extrude(cross(HEAD_WALL), amount=HEAD_H)
    part = outer - cavity
    lugs, lug_centers = head_lugs(HEAD_H)
    part += lugs
    for x, y in lug_centers:
        part -= cyl(INSERT_BORE, 10, x, y, HEAD_H - 9)
        part -= cyl(INSERT_BORE, 10, x, y, -1)
    # Cell support pylons raise the quartz body without obstructing four optical faces.
    for x in (-12.5, 12.5):
        for y in (-12.5, 12.5):
            part += box(8, 8, 27, x, y, HEAD_FLOOR)
            part -= cyl(4.2, 7, x, y, 29)
    # Blind M3-insert holes for all adjustable optical fixtures; no wet through-holes.
    mounts = [(29, -10), (29, 10), (79, 0), (99, 0)]
    mounts += [(x, y) for y in (-49, 49) for x in (-11, 11)]
    mounts += [(x, y) for x in (-60, -36) for y in (-10, 10)]
    for x, y in mounts:
        part -= cyl(4.2, 7, x, y, 2)
    # Four internal ledges carry the Pi above the camera without a CSI feedthrough.
    for x in (42, 112):
        for y in (-28, 28):
            part += box(10, 14, 6, x, y, 79)
            part -= cyl(4.2, 7, x, y, 79)
    # Two fixed underside penetrations: intake -> cell and cell -> external pump.
    for x in (-19, 19):
        part -= cyl(FLUID_BORE, HEAD_FLOOR + 2, x, 18, -1)
    # Electrical penetrator, below the optical axis.
    part -= Pos(0, HEAD_Y - HEAD_WALL - 1, 21) * Rot(X=-90) * Cylinder(
        CABLE_BORE / 2, HEAD_WALL + 3, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    return part


def head_lid():
    lid = extrude(cross(), amount=LID_T)
    lugs, centers = head_lugs(LID_T)
    lid += lugs
    for x, y in centers:
        lid -= cyl(4.3, LID_T + 2, x, y, -1)
    # Inner locating rib: the face gasket sits on the flat rim outside this rib.
    rib = extrude(cross(HEAD_WALL + 0.6), amount=3) - extrude(cross(HEAD_WALL + 2.7), amount=3)
    lid += Pos(0, 0, -3) * rib
    return lid


def head_gasket():
    return extrude(cross(0.8), amount=GASKET_T) - extrude(cross(HEAD_WALL - 0.7), amount=GASKET_T)


def rectangular_lug_centers(x, y):
    corners = [(sx * (x / 2 + 3), sy * (y / 2 - 13)) for sx in (-1, 1) for sy in (-1, 1)]
    sides = [(0, sy * (y / 2 + 3)) for sy in (-1, 1)]
    sides += [(sx * (x / 2 + 3), 0) for sx in (-1, 1)]
    return corners + sides


def rectangular_body(x, y, h, holes=()):
    part = box(x, y, h) - box(x - 2 * BOX_WALL, y - 2 * BOX_WALL, h, cz=BOX_FLOOR)
    if x == POWER_X and y == POWER_Y:
        # Organizer only: wiring passes over the top, so this is not a fire barrier.
        part += box(x - 2 * BOX_WALL, 3, 60, cz=BOX_FLOOR)
    # Full-height exterior screw towers; fasteners never pierce the dry cavity.
    centers = rectangular_lug_centers(x, y)
    for px, py in centers:
        part += cyl(14, h, px, py)
    for px, py in centers:
        part -= cyl(INSERT_BORE, 10, px, py, h - 9)
        part -= cyl(INSERT_BORE, 10, px, py, -1)
    for axis, px, py, pz, diameter in holes:
        if axis == "x":
            cut = Pos(px, py, pz) * Rot(Y=90) * Cylinder(diameter / 2, BOX_WALL + 3, align=(Align.CENTER, Align.CENTER, Align.MIN))
        else:
            cut = Pos(px, py, pz) * Rot(X=-90) * Cylinder(diameter / 2, BOX_WALL + 3, align=(Align.CENTER, Align.CENTER, Align.MIN))
        part -= cut
    return part


def rectangular_lid(x, y):
    lid = box(x, y, LID_T)
    centers = rectangular_lug_centers(x, y)
    for px, py in centers:
        lid += cyl(14, LID_T, px, py)
    for px, py in centers:
        lid -= cyl(4.3, LID_T + 2, px, py, -1)
    rib = box(x - 2 * BOX_WALL - 1.2, y - 2 * BOX_WALL - 1.2, 3, cz=-3)
    rib -= box(x - 2 * BOX_WALL - 5.2, y - 2 * BOX_WALL - 5.2, 3, cz=-3)
    return lid + rib


def rectangular_gasket(x, y):
    return box(x - 1.4, y - 1.4, GASKET_T) - box(x - 2 * BOX_WALL + 1.4, y - 2 * BOX_WALL + 1.4, GASKET_T)


def cell_cradle():
    # Open sides preserve all four optical paths. Slots in the base take M3 adjustment screws.
    base = box(32, 32, 4) - box(10, 10, 6, cz=-1)
    for x in (-12.5, 12.5):
        for y in (-12.5, 12.5):
            base += box(6, 6, 41, x, y, 4)
            base -= cyl(3.4, 47, x, y, -1)
    for x in (-11, 11):
        base -= cyl(3.4, 6, x, 0, -1)
    return base


def cell_clamp():
    clamp = box(32, 32, 4) - box(10, 10, 6, cz=-1)
    for x in (-12.5, 12.5):
        for y in (-12.5, 12.5):
            clamp -= cyl(3.4, 6, x, y, -1)
    return clamp


def slit_holder():
    # Opening accepts the EXISTING 0.5 mm metal slit; it is not a printed slit.
    foot = box(24, 30, 4)
    upright = box(3, 28, 82, cx=0, cz=4) - box(5, 9, 18, cx=0, cz=43)
    part = foot + upright
    for y in (-10, 10):
        part -= cyl(3.4, 5, 0, y, -0.5)
    return part


def optical_slider(length=38, width=30):
    # Universal adjustable base for LED and AS7265x; final PCB adapter follows measurement.
    plate = box(length, width, 5)
    for x in (-length / 2 + 8, length / 2 - 8):
        slot = cyl(3.4, 7, x - 3, 0, -1) + cyl(3.4, 7, x + 3, 0, -1) + box(6, 3.4, 7, x, 0, -1)
        plate -= slot
    upright = box(length, 3, 82, cy=0, cz=5) - box(19, 5, 20, cy=0, cz=42)
    for x in (-length / 2 + 6, length / 2 - 6):
        for z in (46, 76):
            upright -= Pos(x, -3, z) * Rot(X=-90) * Cylinder(1.7, 6, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return plate + upright


def camera_angled_plate():
    foot = box(36, 30, 5)
    for x in (-10, 10):
        foot -= box(8, 3.4, 7, x, 0, -1)
    upright = Pos(0, 0, 5) * Rot(Z=36) * box(3, 30, 70)
    upright -= Pos(0, 0, 5) * Rot(Z=36) * box(5, 18, 20, cz=37)
    return foot + upright


def lamp_metal_bracket_base():
    # Only the printed base. The 10 W lamp needs a ceramic socket and metal bracket.
    base = box(36, 30, 7)
    for x in (-12, 12):
        for y in (-10, 10):
            base -= cyl(4.3, 9, x, y, -1)
    return base


def pi_shelf():
    shelf = box(90, 60, 4)
    for x in (-35, 35):
        for y in (-28, 28):
            shelf -= cyl(3.4, 6, x, y, -1)  # shelf-to-ledges
    for x in (-29, 29):
        for y in (-24.5, 24.5):
            shelf += cyl(6, 6, x, y, 4)
            shelf -= cyl(2.8, 11, x, y, -1)  # Pi nominal 58 x 49
    return shelf


def link_bar(pitch):
    part = box(pitch + 16, 16, 5)
    for x in (-pitch / 2, pitch / 2):
        part -= cyl(4.3, 7, x, 0, -1)
    return part


def electronics_tray():
    tray = box(162, 60, 4)
    # Strap slots leave the exact ESP32, BMS and driver variants open.
    for x in (-68, -18, 18, 68):
        for y in (-20, 20):
            tray -= box(3.5, 8, 6, x, y, -1)
    return tray


def battery_tray():
    tray = box(168, 64, 5)
    for x in (-68, 68):
        for y in (-25, 25):
            tray -= box(5, 14, 7, x, y, -1)  # hook-and-loop strap passages
    return tray


def pump_mount():
    plate = box(82, 82, 5)
    # 47 mm stated pitch, but hole count/pattern is still to be checked on the delivered pump.
    for x in (-PUMP_HOLE_PITCH / 2, PUMP_HOLE_PITCH / 2):
        for y in (-PUMP_HOLE_PITCH / 2, PUMP_HOLE_PITCH / 2):
            plate -= box(8, 4, 7, x, y, -1)
    for x in (-35, 35):
        plate -= box(4, 12, 7, x, 0, -1)
    return plate


def build():
    parts = {
        "H01_head_body": head_body(),
        "H02_head_lid": head_lid(),
        "H03_cell_cradle": cell_cradle(),
        "H04_cell_clamp": cell_clamp(),
        "H05_slit_holder": slit_holder(),
        "H06_camera_angled_plate": camera_angled_plate(),
        "H07_led_slider": optical_slider(),
        "H08_as7265x_slider": optical_slider(),
        "H10_lamp_metal_bracket_base": lamp_metal_bracket_base(),
        "H11_pi_shelf": pi_shelf(),
        "E01_power_body": rectangular_body(POWER_X, POWER_Y, POWER_H, [
            ("y", 0, -POWER_Y / 2 - 1, 27, CABLE_BORE),
            ("x", POWER_X / 2 - BOX_WALL - 1, 0, 27, CABLE_BORE),
        ]),
        "E02_power_lid": rectangular_lid(POWER_X, POWER_Y),
        "E03_battery_tray": battery_tray(),
        "E04_electronics_tray": electronics_tray(),
        "P01_pump_body": rectangular_body(PUMP_X, PUMP_Y, PUMP_H, [
            ("y", -25, -PUMP_Y / 2 - 1, 30, FLUID_BORE),
            ("y", 25, -PUMP_Y / 2 - 1, 30, FLUID_BORE),
            ("x", -PUMP_X / 2 - 1, 0, 25, CABLE_BORE),
        ]),
        "P02_pump_lid": rectangular_lid(PUMP_X, PUMP_Y),
        "P03_pump_mount": pump_mount(),
        "M01_head_power_link_x2": link_bar((62**2 + 53**2)**0.5),
        "M02_power_pump_link_x2": link_bar((26.5**2 + 22.5**2)**0.5),
    }
    gaskets = {
        "H09_head_gasket_PATTERN_ONLY": head_gasket(),
        "E05_power_gasket_PATTERN_ONLY": rectangular_gasket(POWER_X, POWER_Y),
        "P04_pump_gasket_PATTERN_ONLY": rectangular_gasket(PUMP_X, PUMP_Y),
    }
    manifest = {"units": "mm", "note": "M1 provisional geometry, NOT cleared for immersion or printing", "parts": {}}
    for name, part in {**parts, **gaskets}.items():
        if not part.is_valid or part.volume <= 0:
            raise ValueError(f"Invalid solid: {name}")
        bb = part.bounding_box()
        dims = [round(bb.size.X, 2), round(bb.size.Y, 2), round(bb.size.Z, 2)]
        if name in parts and (dims[0] > 220 or dims[1] > 220):
            raise ValueError(f"Part exceeds 220 x 220 mm bed: {name} {dims}")
        export_step(part, str(OUT / f"{name}.step"))
        export_stl(part, str(OUT / f"{name}.stl"))
        manifest["parts"][name] = {"bbox_mm": dims, "volume_mm3": round(part.volume, 1),
                                   "print": name in parts,
                                   "quantity": 2 if name.startswith("M0") else 1}
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    with ZipFile(OUT / "CRUZ_M1_print_parts.zip", "w", ZIP_DEFLATED) as bundle:
        bundle.write(OUT / "manifest.json", "manifest.json")
        for name in parts:
            bundle.write(OUT / f"{name}.stl", f"{name}.stl")
    assembly(parts, gaskets)
    print(f"Exported {len(parts)} printed parts and {len(gaskets)} gasket patterns to {OUT}")
    return parts


def assembly(parts, gaskets):
    """Export a spatial arrangement, including simplified bought-part envelopes."""
    bodies = []
    def add(name, part, where, color):
        item = Pos(*where) * part
        item.color = Color(color)
        bodies.append(item)

    add("head", parts["H01_head_body"], (0, 0, 0), "#202c39")
    add("power", parts["E01_power_body"], (0, 180, 0), "#253442")
    add("pump", parts["P01_pump_body"], (180, 180, 0), "#263745")
    add("cell_cradle", parts["H03_cell_cradle"], (0, 0, 35), "#f2ae43")
    add("cell_clamp", parts["H04_cell_clamp"], (0, 0, 80), "#f2ae43")
    add("slit_holder", parts["H05_slit_holder"], (29, 0, HEAD_FLOOR), "#de7756")
    add("camera_mount", parts["H06_camera_angled_plate"], (89, 0, HEAD_FLOOR), "#de7756")
    add("led_mount", parts["H07_led_slider"], (0, 49, HEAD_FLOOR), "#4789cf")
    add("sensor_mount", parts["H08_as7265x_slider"], (0, -49, HEAD_FLOOR), "#4789cf")
    add("lamp_base", parts["H10_lamp_metal_bracket_base"], (-48, 0, HEAD_FLOOR), "#d8905c")
    add("pi_shelf", parts["H11_pi_shelf"], (77, 0, 85), "#70b6aa")
    add("battery_tray", parts["E03_battery_tray"], (0, 144, 5), "#caa96d")
    add("electronics_tray", parts["E04_electronics_tray"], (0, 216, 5), "#70b6aa")
    add("pump_mount", parts["P03_pump_mount"], (180, 180, 5), "#70b6aa")
    # Bought parts are deliberately simplified envelopes, never exported as print parts.
    add("quartz_cell_reference", box(CELL_SIDE, CELL_SIDE, CELL_BODY_H, cz=40), (0, 0, 0), "#c2eced")
    add("pump_reference", box(PUMP_HEAD_XY, PUMP_HEAD_XY, PUMP_TOTAL_H, cz=10), (180, 180, 0), "#9aabb5")
    add("battery_envelope_reference", box(160, 60, 62, cz=10), (0, 144, 0), "#788f63")
    add("pi_board_reference", box(85, 56, 2, cz=95), (77, 0, 0), "#55a38b")
    add("lamp_ceramic_and_metal_REFERENCE", box(18, 18, 55, cz=12), (-48, 0, 0), "#b8a995")
    for sx in (-1, 1):
        x0, y0 = sx * 36, 65
        x1, y1 = sx * 98, 118
        angle = 40.53 if sx == 1 else 139.47
        add("head_power_link", Rot(Z=angle) * parts["M01_head_power_link_x2"], ((x0+x1)/2, (y0+y1)/2, -5), "#dcac60")
    for sy in (-1, 1):
        x0, y0 = 98, 180 + sy*62
        x1, y1 = 124.5, 180 + sy*39.5
        import math
        angle = math.degrees(math.atan2(y1-y0, x1-x0))
        add("power_pump_link", Rot(Z=angle) * parts["M02_power_pump_link_x2"], ((x0+x1)/2, (y0+y1)/2, -5), "#dcac60")
    export_gltf(Compound(bodies), str(OUT / "CRUZ_M1_open_assembly.glb"), binary=True, linear_deflection=0.25)
    for lid, where in [
        ("H02_head_lid", (0, 0, HEAD_H + 30)),
        ("E02_power_lid", (0, 180, POWER_H + 30)),
        ("P02_pump_lid", (180, 180, PUMP_H + 30)),
    ]:
        add(lid, parts[lid], where, "#34485c")
    export_gltf(Compound(bodies), str(OUT / "CRUZ_M1_exploded_assembly.glb"), binary=True, linear_deflection=0.25)


if __name__ == "__main__":
    build()
