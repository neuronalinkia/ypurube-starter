"""
EP03 Cash-Landrum — Diseño de sonido completo.
Importa los generadores SFX de core/mezclar_sfx.py y aplica el mapa de EP03.

Bloques del vídeo:
  B1  (0-90s)     Noche en FM-1485: grillos, coche, OVNI aparece, llamas
  B2  (90-211s)   Calor extremo, salen del coche, helicópteros
  B3  (211-349s)  Radiación, quemaduras, hospital
  B4  (349-464s)  Investigación Schuessler, MUFON
  B5  (464-583s)  Bases militares, sin registros
  B6  (583-770s)  Demanda, audiencia, dismissal
  B7  (770-869s)  Documentos, ilustración oficial
  B8  (869-994s)  Dos explicaciones posibles, escolta organizada
  B9  (994-1057s) Betty el resto de su vida, cáncer
  B10 (1057-1145s) Lo que sabemos con certeza
  B11 (1145-1178s) FM-1485 hoy

Uso:
  python ejemplos/ep03_cash_landrum/mezclar_sfx.py
"""
import sys
from pathlib import Path

ROOT   = Path(__file__).parent.parent.parent
EP_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT / "core"))

from mezclar_sfx import (
    mezclar,
    dark_ambient_pad,
    night_crickets,
    car_engine,
    ufo_hum,
    flame_burst,
    heat_drone,
    helicopter_rotor,
    hospital_ambience,
    orchestral_hit,
    government_tone,
    tension_string,
    resolution_pad,
)


def build_sfx_map(total_ms):
    """Mapa SFX específico para EP03 Cash-Landrum."""
    M = []

    # ── CAPA BASE: dark ambient pad todo el vídeo ─────────────────────────
    M.append((0, -26, "dark_pad_full", total_ms, dark_ambient_pad))

    # ── B1: NOCHE EN FM-1485 (0 - 90s) ──────────────────────────────────
    M.append((0,       -16, "crickets_b1",    90_000, night_crickets))
    M.append((3_000,   -18, "car_engine_b1",  44_000, car_engine))

    # OVNI aparece ~37s — hum que va creciendo
    M.append((37_000,  -10, "ufo_hum_b1",     52_000, ufo_hum))

    # Llamas ~55s
    M.append((54_600,   -2, "flame_burst_b1",  2_500, flame_burst))
    M.append((55_000,  -16, "fire_crackle",   14_000, heat_drone))

    # ── B2: CALOR EXTREMO + HELICÓPTEROS (90 - 211s) ─────────────────────
    M.append((90_000,  -14, "heat_drone_b2",  83_000, heat_drone))

    # Helicópteros aparecen ~175s
    M.append((175_000, -10, "heli_b2",        36_000, helicopter_rotor))

    # ── B3: HOSPITAL / RADIACIÓN (211 - 349s) ────────────────────────────
    M.append((211_000, -20, "hospital_b3",   138_000, hospital_ambience))
    M.append((230_000,  -8, "hit_radiation",   1_200, orchestral_hit))

    # ── B4: INVESTIGACIÓN (349 - 464s) ───────────────────────────────────
    M.append((349_000, -24, "gov_tone_b4",   115_000, government_tone))

    # ── B5: BASES MILITARES (464 - 583s) ─────────────────────────────────
    M.append((464_000, -22, "gov_tone_b5",   119_000, government_tone))

    # ── B6: DEMANDA (583 - 770s) ─────────────────────────────────────────
    M.append((583_000, -20, "tension_b6",    187_000, dark_ambient_pad))

    # ── B7: DOCUMENTOS (770 - 869s) ──────────────────────────────────────
    M.append((800_000,  -6, "hit_diamond",     1_200, orchestral_hit))
    M.append((800_500, -14, "tension_b7",     68_500, tension_string))

    # ── B8: ESCOLTA / DOS EXPLICACIONES (869 - 994s) ─────────────────────
    M.append((869_000, -18, "dark_b8",       125_000, dark_ambient_pad))
    M.append((940_000,  -6, "hit_escort",      1_200, orchestral_hit))

    # ── B9: BETTY EL RESTO DE SU VIDA (994 - 1057s) ──────────────────────
    M.append((994_000, -22, "hospital_b9",    63_000, hospital_ambience))

    # ── B10: LO QUE SABEMOS (1057 - 1145s) ──────────────────────────────
    M.append((1_057_000, -18, "tension_b10",  88_000, dark_ambient_pad))
    M.append((1_057_000,  -4, "hit_conclusion", 1_200, orchestral_hit))

    # ── B11: FM-1485 HOY (1145 - fin) ────────────────────────────────────
    M.append((1_145_000, -14, "resolution_b11", 33_000, resolution_pad))
    M.append((1_148_000, -22, "crickets_end",   28_000, night_crickets))

    return M


if __name__ == "__main__":
    narration = EP_DIR / "audio" / "ep03_full.wav"
    output    = EP_DIR / "audio" / "ep03_sfx_mix.wav"

    if not narration.exists():
        print(f"[ERROR] Narración no encontrada: {narration}")
        print("Generar primero con: python core/generar_audio_kokoro.py \\")
        print("  --guion ejemplos/ep03_cash_landrum/scripts/narration.txt \\")
        print("  --salida ejemplos/ep03_cash_landrum/audio/ep03_full.wav \\")
        print("  --voice am_puck --speed 1.05")
        exit(1)

    mezclar(narration, output, sfx_map_fn=build_sfx_map)

    # Música opcional (Kevin MacLeod — requiere atribución CC BY 4.0)
    # Para añadir:
    # mezclar(narration, output, sfx_map_fn=build_sfx_map, music_tracks=[
    #     (349_000, "music/investigations.mp3", -22, 200_000),
    # ])
