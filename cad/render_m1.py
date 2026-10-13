"""Make an inspectable M1 assembly view from the actual exported STL parts.

Optional visualization dependencies: trimesh, plotly, kaleido, Chrome.
Run CRUZ_M1.py first, then this file. All geometry remains in CRUZ_M1.py.
"""

from pathlib import Path
import math

import numpy as np
import plotly.graph_objects as go
import trimesh
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "m1_export"
RENDERS = ROOT.parent / "docs" / "renders"
RENDERS.mkdir(exist_ok=True)


def placed_mesh(name, location, angle=0):
    mesh = trimesh.load_mesh(OUT / f"{name}.stl")
    if angle:
        mesh.apply_transform(trimesh.transformations.rotation_matrix(math.radians(angle), [0, 0, 1]))
    mesh.apply_translation(location)
    return mesh


def add_mesh(fig, mesh, color, label, opacity=1):
    v, f = mesh.vertices, mesh.faces
    fig.add_trace(go.Mesh3d(
        x=v[:, 0], y=v[:, 1], z=v[:, 2],
        i=f[:, 0], j=f[:, 1], k=f[:, 2],
        color=color, opacity=opacity, flatshading=True,
        lighting=dict(ambient=0.58, diffuse=0.72, specular=0.14, roughness=0.82),
        lightposition=dict(x=-300, y=-250, z=500),
        name=label, showlegend=False, hoverinfo="name",
    ))


def box_ref(size, at):
    mesh = trimesh.creation.box(extents=size)
    mesh.apply_translation(np.array(at) + np.array(size) * np.array([0, 0, .5]))
    return mesh


fig = go.Figure()
items = [
    ("H01_head_body", (0, 0, 0), 0, "#456b8c", "Cabezal óptico", 0.19),
    ("E01_power_body", (0, 180, 0), 0, "#52718a", "Batería y electrónica", 0.18),
    ("P01_pump_body", (180, 180, 0), 0, "#52718a", "Cámara sellada de bomba", 0.18),
    ("H03_cell_cradle", (0, 0, 35), 0, "#f5ab3c", "Soporte de cubeta", 1),
    ("H04_cell_clamp", (0, 0, 80), 0, "#f5ab3c", "Abrazadera de cubeta", 1),
    ("H05_slit_holder", (29, 0, 8), 0, "#db7458", "Soporte de rendija", 1),
    ("H06_camera_angled_plate", (89, 0, 8), 0, "#db7458", "Cámara a 36°", 1),
    ("H07_led_slider", (0, 49, 8), 0, "#4f9acc", "LED 430 nm", 1),
    ("H08_as7265x_slider", (0, -49, 8), 0, "#4f9acc", "AS7265x", 1),
    ("H10_lamp_metal_bracket_base", (-48, 0, 8), 0, "#db7458", "Base de lámpara", 1),
    ("H11_pi_shelf", (77, 0, 85), 0, "#4ba59d", "Bandeja Raspberry Pi", 1),
    ("E03_battery_tray", (0, 144, 5), 0, "#b4a06c", "Bandeja de batería", 1),
    ("E04_electronics_tray", (0, 216, 5), 0, "#4ba59d", "Bandeja electrónica", 1),
    ("P03_pump_mount", (180, 180, 5), 0, "#4ba59d", "Base de bomba", 1),
    ("H02_head_lid", (0, 0, 150), 0, "#607a90", "Tapa óptica", 0.29),
    ("E02_power_lid", (0, 180, 120), 0, "#607a90", "Tapa de batería", 0.29),
    ("P02_pump_lid", (180, 180, 130), 0, "#607a90", "Tapa de bomba", 0.29),
]
for name, location, angle, color, label, opacity in items:
    add_mesh(fig, placed_mesh(name, location, angle), color, label, opacity)

for sx in (-1, 1):
    x0, y0 = sx * 36, 65
    x1, y1 = sx * 98, 118
    angle = math.degrees(math.atan2(y1-y0, x1-x0))
    add_mesh(fig, placed_mesh("M01_head_power_link_x2", ((x0+x1)/2, (y0+y1)/2, -5), angle), "#c9a36b", "Unión cabezal–energía")
for sy in (-1, 1):
    x0, y0 = 98, 180 + sy*62
    x1, y1 = 124.5, 180 + sy*39.5
    angle = math.degrees(math.atan2(y1-y0, x1-x0))
    add_mesh(fig, placed_mesh("M02_power_pump_link_x2", ((x0+x1)/2, (y0+y1)/2, -5), angle), "#c9a36b", "Unión energía–bomba")

add_mesh(fig, box_ref((12.5, 12.5, 40), (0, 0, 40)), "#e0f8f7", "Cubeta de cuarzo (envolvente)", .92)
add_mesh(fig, box_ref((160, 60, 62), (0, 144, 10)), "#a8bf74", "Reserva de batería", .72)
add_mesh(fig, box_ref((85, 56, 2), (77, 0, 95)), "#5fb08d", "Raspberry Pi 4", 1)
add_mesh(fig, box_ref((57, 57, 60), (180, 180, 10)), "#bcc9cf", "Bomba Denash (envolvente)", .9)

fig.update_layout(
    title=dict(text="CRUZ  /  M1  —  disposición CAD preliminar", x=.05, font=dict(size=27, color="#20354a")),
    paper_bgcolor="#f5f7fa", margin=dict(l=0, r=0, b=0, t=70),
    scene=dict(
        bgcolor="#f5f7fa", aspectmode="data",
        xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
        camera=dict(eye=dict(x=1.45, y=-1.65, z=1.15), projection=dict(type="orthographic")),
    ),
    annotations=[dict(text="VISTA ABIERTA · STL/STEP generados del mismo modelo · cotas provisionales",
                      x=.05, y=.035, xref="paper", yref="paper", showarrow=False,
                      font=dict(size=14, color="#587087"), align="left")],
)
fig.write_html(RENDERS / "CRUZ-M1-CAD-interactive.html", include_plotlyjs=True)
raw = RENDERS / "CRUZ-M1-CAD-iso-raw.png"
fig.write_image(raw, width=1600, height=1050, scale=1.3)
fig.update_layout(scene_camera=dict(eye=dict(x=.03, y=-.001, z=2.4), projection=dict(type="orthographic")))
fig.write_image(RENDERS / "CRUZ-M1-CAD-top.png", width=1300, height=1300, scale=1.2)

# A legible board image: crop only the rendered geometry, then label it without
# modifying or reinterpreting the CAD meshes.
src = Image.open(raw).convert("RGB")
pixels = np.asarray(src)
bg = np.array([245, 247, 250])
mask = (np.abs(pixels.astype(int) - bg).max(axis=2) > 38)
mask[:160, :] = False
mask[-150:, :] = False
ys, xs = np.where(mask)
crop = src.crop((max(0, xs.min()-50), max(0, ys.min()-60), min(src.width, xs.max()+50), min(src.height, ys.max()+60)))
board = Image.new("RGB", (1800, 1120), "#f5f7fa")
art_w = 1000
art_h = round(crop.height * art_w / crop.width)
art = crop.resize((art_w, art_h), Image.Resampling.LANCZOS)
board.paste(art, (700, 145))
d = ImageDraw.Draw(board)
font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
bold_path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
ft = lambda n, bold=False: ImageFont.truetype(bold_path if bold else font_path, n)
d.text((62, 58), "CRUZ  /  M1", fill="#1e354b", font=ft(62, True))
d.text((63, 132), "Diseño CAD imprimible", fill="#597087", font=ft(26))
d.line((62, 190, 450, 190), fill="#c8d3dd", width=3)
sections = [
    (245, "01  CABEZAL ÓPTICO", ["Cubeta de cuarzo · 4 caras", "OV9281 + rendija a 60 mm", "LED 430 nm · AS7265x"]),
    (440, "02  ENERGÍA", ["Batería y BMS", "ESP32 · drivers · fusible", "Pi 4 en el cabezal"]),
    (635, "03  BOMBA SELLADA", ["Denash IP31 en cápsula", "Después de la cubeta", "Toma y descarga al lago"]),
]
for y, heading, lines in sections:
    d.rounded_rectangle((62, y, 445, y+155), radius=15, outline="#d7e1e9", width=2, fill="white")
    d.text((82, y+21), heading, fill="#244862", font=ft(22, True))
    for j, line in enumerate(lines):
        d.text((82, y+58+j*27), line, fill="#526b7e", font=ft(19))
d.line((62, 852, 1735, 852), fill="#c8d3dd", width=3)
d.text((62, 878), "AGUA:  LAGO  →  CUBETA  →  BOMBA  →  DESCARGA", fill="#1d627d", font=ft(28, True))
d.text((62, 948), "STEP + STL individuales · junta plana cortada · cotas de ajuste pendientes", fill="#5f7281", font=ft(21))
d.text((62, 990), "Vista abierta del modelo real. No representa un equipo ensayado.", fill="#81929f", font=ft(19))
board.save(RENDERS / "CRUZ-M1-CAD-iso.png")
raw.unlink()
print("Rendered CAD preview and interactive view")
