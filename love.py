from __future__ import annotations
import math
import random
import streamlit as st

# =========================================================================
# 1. KONFIGURASI HALAMAN (Disesuaikan agar pas dengan layar browser HP)
# =========================================================================
st.set_page_config(page_title="I love you <3", page_icon="❤️", layout="centered")

class Config:
    width: int = 700      # Lebar kanvas web
    height: int = 500     # Tinggi kanvas web
    bg_color: str = "#0f0000"  # Warna background asli Anda (15, 0, 0)
    
    scale: int = 12       # Skala diperkecil sedikit agar presisi di layar HP
    y_offset: int = -20
    
    n_outline: int = 120  # Jumlah partikel garis luar
    n_fill: int = 90      # Jumlah partikel isi dalam
    
    outline_gap: int = 15
    fill_gap: int = 18
    
    heart_words: tuple[str, ...] = ("i love you", "I LOVE YOU", "love you")
    center_text: str = "I Love you"
    
    # Warna merah estetik asli dari kode Anda
    colors: tuple[str, ...] = (
        "#ff1414", "#dc143c", "#ff0000", "#b22222", "#ff3c3c"
    )

    @property
    def center(self) -> float:
        return self.width / 2

CFG = Config()

# =========================================================================
# 2. RUMUS MATEMATIKA BENTUK HATI (Sama persis dengan logika asli Anda)
# =========================================================================
def heart_parametric(t: float) -> tuple[float, float]:
    x = 16.0 * math.sin(t) ** 3
    y = 13.0 * math.cos(t) - 5.0 * math.cos(2 * t) - 2.0 * math.cos(3 * t) - math.cos(4 * t)
    return x, -y

def heart_to_screen(hx: float, hy: float) -> tuple[float, float]:
    sx = hx * CFG.scale + CFG.center
    sy = hy * CFG.scale + (CFG.height / 2) + CFG.y_offset
    return sx, sy

def _too_close(sx: float, sy: float, placed: list[tuple[float, float]], gap: float) -> bool:
    return any(math.hypot(sx - px, sy - py) < gap for px, py in placed)

# =========================================================================
# 3. GENERATE KOORDINAT PARTIKEL TEKS
# =========================================================================
placed_points = []
outline_particles = []

# Membuat Garis Luar Hati
for i in range(CFG.n_outline):
    t = (i / CFG.n_outline) * math.tau
    sx, sy = heart_to_screen(*heart_parametric(t))
    if not _too_close(sx, sy, placed_points, CFG.outline_gap):
        placed_points.append((sx, sy))
        outline_particles.append({
            "x": sx, "y": sy, "word": random.choice(CFG.heart_words), 
            "color": random.choice(CFG.colors), "size": 11
        })

# Membuat Isi Dalam Hati
fill_particles = []
for _ in range(CFG.n_fill * 50):
    if len(fill_particles) >= CFG.n_fill:
        break
    t = random.uniform(0, math.tau)
    r = random.uniform(0.0, 0.85)
    hx, hy = heart_parametric(t)
    sx, sy = heart_to_screen(hx * r, hy * r)
    if not _too_close(sx, sy, placed_points, CFG.fill_gap):
        placed_points.append((sx, sy))
        fill_particles.append({
            "x": sx, "y": sy, "word": random.choice(CFG.heart_words), 
            "color": random.choice(CFG.colors), "size": 9
        })

all_particles = outline_particles + fill_particles

# =========================================================================
# 4. MERENDER GRAFIK VECTOR (Membentuk Efek Bercahaya / Glow di Browser)
# =========================================================================
svg_elements = []

# Layer 1: Efek Bayangan Pendaran Cahaya (Glow Effect)
for p in all_particles:
    svg_elements.append(
        f'<text x="{p["x"]}" y="{p["y"]}" fill="{p["color"]}" font-family="Arial" '
        f'font-size="{p["size"]}px" font-weight="bold" text-anchor="middle" '
        f'opacity="0.35" filter="drop-shadow(0px 0px 5px {p["color"]})">{p["word"]}</text>'
    )

# Layer 2: Teks Utama yang Tajam
for p in all_particles:
    svg_elements.append(
        f'<text x="{p["x"]}" y="{p["y"]}" fill="{p["color"]}" font-family="Arial" '
        f'font-size="{p["size"]}px" font-weight="bold" text-anchor="middle">{p["word"]}</text>'
    )

# Layer 3: Teks Utama di Tengah Hati (Georgia dengan Efek Glow Kuat)
cx = CFG.center
cy = (CFG.height / 2) + CFG.y_offset + 10
svg_elements.append(
    f'<text x="{cx}" y="{cy}" fill="#ffc8c8" font-family="Georgia" '
    f'font-size="32px" font-weight="bold" text-anchor="middle" '
    f'filter="drop-shadow(0px 0px 8px #ff4b4b)">{CFG.center_text}</text>'
)

# Menggabungkan seluruh struktur menjadi komponen Web SVG
svg_content = f"""
<svg width="100%" height="{CFG.height}px" viewBox="0 0 {CFG.width} {CFG.height}" style="background-color: {CFG.bg_color}; border-radius: 15px;">
    {chr(10).join(svg_elements)}
</svg>
"""

# =========================================================================
# 5. MENAMPILKAN KE LAYAR WEB HP
# =========================================================================
st.write("")
st.markdown(svg_content, unsafe_allow_html=True)

# Tambahan Fitur Interaktif khusus Web/HP: Tombol Kejutan Balon
st.write("")
if st.button("Klik untuk Mengirim Balon Cinta ✨", use_container_width=True):
    st.balloons()
