"""
Diseño de sonido — mezcla narración + SFX sintéticos + música de fondo.
Incluye generadores SFX para episodios de misterio histórico.

Uso básico (SFX mínimo — solo dark pad):
  python core/mezclar_sfx.py \
    --narration ep01/audio/ep01_full.wav \
    --output    ep01/audio/ep01_sfx_mix.wav

Con música (Kevin MacLeod u otro mp3 royalty-free):
  python core/mezclar_sfx.py \
    --narration ep01/audio/ep01_full.wav \
    --output    ep01/audio/ep01_sfx_mix.wav \
    --music-dir music/

Con mapa SFX personalizado por episodio:
  Crear un script propio que importe los generadores de este fichero
  y defina su propio build_sfx_map(total_ms).
  Ver: ejemplos/ep03_cash_landrum/mezclar_sfx.py

Volúmenes validados:
  Narración:          0 dB  (no tocar nunca)
  Dark ambient pad:  -26 dB  (fondo todo el vídeo)
  SFX puntuales:  -8/-16 dB  (golpes, efectos específicos)
  Música:           -22 dB  (Kevin MacLeod, loop bajo la narración)
"""

import os
import argparse
import math
import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine, WhiteNoise
from pathlib import Path


# ─── GENERADORES SFX ─────────────────────────────────────────────────────────
# Todos devuelven AudioSegment. Parámetro: duration_ms (milisegundos).

def dark_ambient_pad(duration_ms):
    """Pad oscuro de fondo — acordes diminuidos graves. Usar en todo el episodio."""
    sr  = 44100
    n   = int(sr * duration_ms / 1000)
    t   = np.linspace(0, duration_ms / 1000, n)
    freqs = [36.7, 41.2, 48.999, 55.0]
    wave  = sum(
        np.sin(2 * np.pi * f * t) * (0.15 + 0.05 * np.sin(2 * np.pi * 0.05 * t + i))
        for i, f in enumerate(freqs)
    ) / len(freqs) * 0.3
    samples = (wave * 32767).astype(np.int16)
    return AudioSegment(samples.tobytes(), frame_rate=sr, sample_width=2, channels=1) \
        .apply_gain(-10).fade_in(5000).fade_out(5000)


def orchestral_hit(duration_ms=1200):
    """Golpe orquestal grave — para momentos de impacto narrativo."""
    hit    = Sine(50).to_audio_segment(duration=300).apply_gain(2)
    hit   += Sine(100).to_audio_segment(duration=300).apply_gain(-4)
    result = AudioSegment.silent(duration=duration_ms)
    return result.overlay(hit.fade_out(900))


def tension_string(duration_ms):
    """Cuerdas de tensión — glissando ascendente. Para revelaciones."""
    sr  = 44100
    n   = int(sr * duration_ms / 1000)
    t   = np.linspace(0, duration_ms / 1000, n)
    f   = 120 + 200 * (t / (duration_ms / 1000))
    wave = np.sin(2 * np.pi * np.cumsum(f) / sr) * np.linspace(0, 1, n) * 0.2
    samples = (wave * 32767).astype(np.int16)
    return AudioSegment(samples.tobytes(), frame_rate=sr, sample_width=2, channels=1) \
        .apply_gain(-8).fade_out(500)


def night_crickets(duration_ms):
    """Grillos nocturnos — escenas de noche y carretera."""
    sr  = 44100
    n   = int(sr * duration_ms / 1000)
    t   = np.linspace(0, duration_ms / 1000, n)
    carrier  = np.sin(2 * np.pi * 4000 * t)
    envelope = 0.5 + 0.5 * np.sin(2 * np.pi * 2.5 * t)
    wave     = carrier * envelope * 0.15
    samples  = (wave * 32767).astype(np.int16)
    return AudioSegment(samples.tobytes(), frame_rate=sr, sample_width=2, channels=1) \
        .apply_gain(-10).fade_in(2000).fade_out(2000)


def car_engine(duration_ms):
    """Motor de coche en marcha."""
    sr   = 44100
    n    = int(sr * duration_ms / 1000)
    t    = np.linspace(0, duration_ms / 1000, n)
    wave = (
        0.6 * np.sin(2 * np.pi * 80 * t) +
        0.3 * np.sin(2 * np.pi * 160 * t + 0.5 * np.sin(2 * np.pi * 0.3 * t)) +
        0.1 * np.sin(2 * np.pi * 240 * t)
    ) * 0.2
    samples = (wave * 32767).astype(np.int16)
    return AudioSegment(samples.tobytes(), frame_rate=sr, sample_width=2, channels=1) \
        .apply_gain(-6).fade_in(1500).fade_out(1500)


def ufo_hum(duration_ms):
    """Zumbido grave oscilante — para OVNIs, anomalías, presencias."""
    sr   = 44100
    n    = int(sr * duration_ms / 1000)
    t    = np.linspace(0, duration_ms / 1000, n)
    wave = (0.5 * np.sin(2 * np.pi * 55 * t) + 0.5 * np.sin(2 * np.pi * 58 * t)) * 0.3
    wave *= np.linspace(0.1, 1.0, n) ** 1.5
    samples = (wave * 32767).astype(np.int16)
    return AudioSegment(samples.tobytes(), frame_rate=sr, sample_width=2, channels=1) \
        .apply_gain(-4).fade_in(3000)


def heat_drone(duration_ms):
    """Drone de calor / tensión extrema."""
    sr   = 44100
    n    = int(sr * duration_ms / 1000)
    t    = np.linspace(0, duration_ms / 1000, n)
    wave = np.tanh(3 * np.sin(2 * np.pi * 45 * t + 0.3 * np.sin(2 * np.pi * 0.8 * t))) * 0.25
    samples = (wave * 32767).astype(np.int16)
    return AudioSegment(samples.tobytes(), frame_rate=sr, sample_width=2, channels=1) \
        .apply_gain(-8).fade_in(2000).fade_out(3000)


def flame_burst(duration_ms=2500):
    """Explosión / destello de llamas."""
    noise  = WhiteNoise().to_audio_segment(duration=duration_ms)
    burst  = noise.apply_gain(4).low_pass_filter(800).fade_in(50).fade_out(1500)
    hit    = Sine(55).to_audio_segment(duration=400).apply_gain(0).fade_out(350)
    result = AudioSegment.silent(duration=duration_ms)
    return result.overlay(burst).overlay(hit)


def helicopter_rotor(duration_ms):
    """Rotores de helicóptero CH-47 — característico doble rotor."""
    sr     = 44100
    n      = int(sr * duration_ms / 1000)
    t      = np.linspace(0, duration_ms / 1000, n)
    rotor1 = np.sin(2 * np.pi * 11.25 * t) ** 2
    rotor2 = np.sin(2 * np.pi * 11.25 * t + np.pi * 0.4) ** 2
    bg     = np.random.randn(n) * 0.05
    wave   = np.tanh((0.4 * rotor1 + 0.4 * rotor2 + bg) * 2.5) * 0.4 * 0.3
    samples = (wave * 32767).astype(np.int16)
    return AudioSegment(samples.tobytes(), frame_rate=sr, sample_width=2, channels=1) \
        .low_pass_filter(600).apply_gain(-4).fade_in(3000).fade_out(4000)


def hospital_ambience(duration_ms):
    """Ambiente de hospital — silencio con zumbido eléctrico."""
    tone  = Sine(60).to_audio_segment(duration=duration_ms).apply_gain(-32)
    noise = WhiteNoise().to_audio_segment(duration=duration_ms).high_pass_filter(6000).apply_gain(-36)
    return tone.overlay(noise).fade_in(3000).fade_out(3000)


def government_tone(duration_ms):
    """Tono burocrático / gobierno — escenas de investigación oficial."""
    sr   = 44100
    n    = int(sr * duration_ms / 1000)
    t    = np.linspace(0, duration_ms / 1000, n)
    wave = (0.5 * np.sin(2 * np.pi * 350 * t) + 0.5 * np.sin(2 * np.pi * 440 * t)) * 0.05
    samples = (wave * 32767).astype(np.int16)
    return AudioSegment(samples.tobytes(), frame_rate=sr, sample_width=2, channels=1) \
        .apply_gain(-16).fade_in(500).fade_out(500)


def resolution_pad(duration_ms):
    """Pad de cierre — más luminoso, acorde mayor. Para el bloque final."""
    sr    = 44100
    n     = int(sr * duration_ms / 1000)
    t     = np.linspace(0, duration_ms / 1000, n)
    freqs = [55.0, 69.3, 82.4, 110.0]
    wave  = sum(np.sin(2 * np.pi * f * t) * 0.15 for f in freqs) / len(freqs)
    samples = (wave * 32767).astype(np.int16)
    return AudioSegment(samples.tobytes(), frame_rate=sr, sample_width=2, channels=1) \
        .apply_gain(-12).fade_in(8000).fade_out(5000)


# ─── MAPA SFX GENÉRICO ───────────────────────────────────────────────────────

def build_sfx_map_default(total_ms):
    """
    Mapa SFX mínimo que funciona para cualquier episodio de misterio.
    Solo dark pad de fondo + orchestral hit en el minuto 1.
    Para episodios específicos, crear mezclar_sfx.py propio (ver ejemplos/ep03).
    """
    return [
        # (start_ms, vol_db, label, duration_ms, generator_fn)
        (0, -26, "dark_pad_full", total_ms, dark_ambient_pad),
        (60_000, -6, "hit_intro", 1_200, orchestral_hit),
    ]


# ─── MÚSICA ──────────────────────────────────────────────────────────────────

def load_music(path, duration_ms, gain_db=-22):
    """Carga un archivo de música, lo loopea si es necesario."""
    if not Path(path).exists():
        print(f"  [MÚSICA NO ENCONTRADA] {path} — ignorando")
        return AudioSegment.silent(duration=duration_ms)
    music = AudioSegment.from_file(str(path))
    while len(music) < duration_ms:
        music = music + music
    return music[:duration_ms].apply_gain(gain_db).fade_in(4000).fade_out(4000)


# ─── MAIN ────────────────────────────────────────────────────────────────────

def mezclar(narration_path, output_path, sfx_map_fn=None, music_tracks=None):
    """
    Función principal reutilizable desde scripts de episodio.

    sfx_map_fn: función que recibe total_ms y devuelve lista de
                (start_ms, vol_db, label, duration_ms, generator_fn)
    music_tracks: lista de (start_ms, path, gain_db, duration_ms)
    """
    print(f"Cargando narración: {narration_path}")
    narration = AudioSegment.from_wav(str(narration_path))
    total_ms  = len(narration)
    print(f"Duración: {total_ms/1000:.1f}s  ({total_ms//60000}:{(total_ms%60000)//1000:02d})")

    sfx_track = AudioSegment.silent(duration=total_ms)
    sfx_map   = (sfx_map_fn or build_sfx_map_default)(total_ms)

    print(f"\nAplicando {len(sfx_map)} capas de SFX...\n")
    for start_ms, vol_db, label, duration_ms, gen_fn in sfx_map:
        if start_ms >= total_ms:
            print(f"  [SKIP]  {label} @ {start_ms/1000:.0f}s — fuera de rango")
            continue
        actual_ms = min(duration_ms, total_ms - start_ms)
        sfx       = gen_fn(actual_ms).apply_gain(vol_db)
        sfx_track = sfx_track.overlay(sfx, position=start_ms)
        m, s = divmod(start_ms // 1000, 60)
        print(f"  {m}:{s:02d}  {label:<28}  {vol_db:+d}dB  {actual_ms/1000:.0f}s")

    print("\nMezclando narración + SFX...")
    final = narration.overlay(sfx_track)

    if music_tracks:
        for start_ms, path, gain_db, duration_ms in music_tracks:
            clip  = load_music(path, duration_ms, gain_db)
            final = final.overlay(clip, position=start_ms)
            m, s  = divmod(start_ms // 1000, 60)
            print(f"  Música: {Path(path).name} @ {m}:{s:02d}  {gain_db:+d}dB")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    print(f"\nGuardando: {output_path}")
    final.export(str(output_path), format="wav")
    print(f"Listo. {total_ms/1000:.0f}s -> {output_path}")

    print("\n--- SIGUIENTE PASO ---")
    print(f"python core/montar_episodio.py \\")
    print(f"  --ep-dir [ep_dir] \\")
    print(f"  --timing [timing_maps.py] \\")
    print(f"  --audio  {output_path} \\")
    print(f"  --output [ep_dir]/videos/ep_draft.mp4")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--narration", required=True, help="WAV de narración (sin SFX)")
    parser.add_argument("--output",    required=True, help="WAV de salida (narración + SFX)")
    parser.add_argument("--music-dir", default=None,
                        help="Carpeta con música royalty-free (mp3). Si no se especifica, sin música.")
    args = parser.parse_args()

    music_tracks = None
    # Para añadir música, descomentar y ajustar:
    # if args.music_dir:
    #     music_dir = Path(args.music_dir)
    #     music_tracks = [
    #         (0, music_dir / "dark_ambient.mp3", -22, len(AudioSegment.from_wav(args.narration))),
    #     ]

    mezclar(args.narration, args.output, music_tracks=music_tracks)


if __name__ == "__main__":
    main()
