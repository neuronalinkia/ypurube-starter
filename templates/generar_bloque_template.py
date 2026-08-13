"""
TEMPLATE — Generar imágenes para un bloque de episodio.
Copiar este archivo, renombrar a generar_b1.py, generar_b2.py, etc.
Rellenar JOBS con los prompts y filenames del bloque.

Naming del filename — CRÍTICO para sync Vexlo:
  El filename debe contener palabras REALES del transcript, no descripción visual.
  MALO:  b1_001_lighthouse_dramatic_storm.png
  BUENO: b1_001_storm_rag_three_day.png
"""

import sys
from pathlib import Path

# Añadir core/ al path
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))
from generar_imagen import run

# ─── Configuración — CAMBIAR ──────────────────────────────────────────────────

EP_DIR   = Path("../ep01_titulo")           # carpeta del episodio
BLOQUE   = "b1"                             # nombre del bloque
OUT_DIR  = EP_DIR / "images" / "video" / BLOQUE

# ID del Reference Element del narrador (guardar en ep_dir/scripts/narrator_element_id.txt)
ELEMENT_ID_FILE = EP_DIR / "scripts" / "narrator_element_id.txt"
ELEMENT_ID  = ELEMENT_ID_FILE.read_text().strip() if ELEMENT_ID_FILE.exists() else None
ELEMENT_REF = f"<<<{ELEMENT_ID}>>> " if ELEMENT_ID else ""

# Style string — MANTENER IGUAL en todo el episodio
S = (
    "Bold flat illustration style, 2D cartoon, thick black outlines, "
    "dark navy blue background, orange accent colors, cinematic widescreen 16:9, "
    "no text, no words, no letters. "
)

# Para escenas SIN personaje (paisajes, objetos, ambiente)
# NO incluir "oval face" — si lo incluyes meterá caras en escenas vacías
S_ENV = S  # mismo estilo, sin descripción facial

# Imagen de referencia del personaje (opcional)
REF_IMAGE = EP_DIR / "scripts" / "character_ref.png"
REF       = REF_IMAGE if REF_IMAGE.exists() else None

# ─── Jobs — RELLENAR ──────────────────────────────────────────────────────────
# Formato: (prompt, "bX_NNN_keywords_del_transcript.png")
# El prompt describe visualmente la imagen.
# El filename contiene palabras reales del transcript en ese momento.

JOBS = [
    (
        S_ENV +
        "Wide aerial view of an empty road at night, "
        "pine trees on both sides, no streetlights, cold winter stars. "
        "Total isolation. Flat illustration.",
        "b1_001_empty_road_cold_night.png"
    ),
    (
        S + ELEMENT_REF +
        "The narrator character stands facing the viewer, "
        "one hand gesturing toward the empty road ahead. "
        "Confident, knowing stance. Dark background. Flat illustration.",
        "b1_002_narrator_point_ahead.png"
    ),
    # Añadir más imágenes aquí...
]

# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    pending  = [(p, f) for p, f in JOBS if not (OUT_DIR / f).exists()]
    existing = len(JOBS) - len(pending)

    print(f"Bloque {BLOQUE} — {len(pending)} pendientes, {existing} ya existen")
    if ELEMENT_ID:
        print(f"Reference Element: {ELEMENT_ID[:12]}...")
    if not pending:
        print("Todo generado.")
    else:
        run(pending, OUT_DIR, ref_path=REF)
        print(f"\nCompletado. Imágenes en: {OUT_DIR}")
