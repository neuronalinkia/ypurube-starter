"""
Genera narración con Kokoro TTS (am_puck, speed=1.05).
Local, gratis, sin GPU extra.

Uso:
  python core/generar_audio_kokoro.py \
    --guion ep01_titulo/scripts/narration.txt \
    --salida ep01_titulo/audio/ep01_full.wav

  python core/generar_audio_kokoro.py \
    --texto "texto directo" \
    --salida audio/prueba.wav

Características:
  - Genera chunk por chunk (párrafo a párrafo)
  - Salta chunks que ya existen — reanudable si se interrumpe
  - Silencio de 0.6s entre párrafos
  - Output: WAV 24000Hz mono

Siguiente paso tras generar audio:
  python -m whisper ep01_full.wav --model large --word_timestamps True --output_format json --language en
"""

import soundfile as sf
import numpy as np
import argparse
import re
from pathlib import Path
from kokoro import KPipeline

VOICE       = "am_puck"
SPEED       = 1.05
SILENCE_DUR = 0.6
SR          = 24000


def cargar_parrafos(path):
    texto = Path(path).read_text(encoding="utf-8")
    # Limpiar marcas de markdown
    texto = re.sub(r'^#+.*$', '', texto, flags=re.MULTILINE)
    texto = re.sub(r'\*\*.*?\*\*', '', texto)
    texto = re.sub(r'^\s*---\s*$', '', texto, flags=re.MULTILINE)
    texto = re.sub(r'\[PAUSA\]', '', texto)
    parrafos = re.split(r'\n{2,}', texto)
    return [p.strip() for p in parrafos if p.strip() and len(p.strip()) > 10]


def main():
    parser = argparse.ArgumentParser()
    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--guion", help="Fichero .txt o .md del guion")
    grupo.add_argument("--texto", help="Texto directo")
    parser.add_argument("--salida", required=True, help="Fichero .wav de salida")
    parser.add_argument("--voice", default=VOICE)
    parser.add_argument("--speed", type=float, default=SPEED)
    args = parser.parse_args()

    salida = Path(args.salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    chunks_dir = salida.parent / (salida.stem + "_chunks")
    chunks_dir.mkdir(exist_ok=True)

    if args.guion:
        parrafos = cargar_parrafos(args.guion)
    else:
        parrafos = [p.strip() for p in args.texto.split("\n\n") if p.strip()]

    print(f"Cargando Kokoro TTS (voz: {args.voice}, speed: {args.speed})...")
    pipe = KPipeline(lang_code='a')
    print(f"Guion cargado: {len(parrafos)} párrafos\n")

    chunk_files = []
    silence     = np.zeros(int(SR * SILENCE_DUR), dtype=np.float32)

    for i, parrafo in enumerate(parrafos):
        chunk_path = chunks_dir / f"chunk_{i:03d}.wav"
        if chunk_path.exists():
            chunk_files.append(str(chunk_path))
            print(f"  Skip {i:03d} (ya existe)")
            continue

        print(f"  [{i+1}/{len(parrafos)}] {parrafo[:70]}...")
        generator    = pipe(parrafo, voice=args.voice, speed=args.speed, split_pattern=None)
        audio_chunks = []
        for _, _, audio in generator:
            audio_chunks.append(audio)

        if audio_chunks:
            audio_data = np.concatenate(audio_chunks)
            sf.write(str(chunk_path), audio_data, SR)
            dur = len(audio_data) / SR
            chunk_files.append(str(chunk_path))
            print(f"    -> {dur:.1f}s")

    print(f"\nUniendo {len(chunk_files)} chunks...")
    all_audio = []
    for i, cf in enumerate(chunk_files):
        data, _ = sf.read(cf)
        all_audio.append(data.astype(np.float32))
        if i < len(chunk_files) - 1:
            all_audio.append(silence)

    final_audio = np.concatenate(all_audio)
    sf.write(str(salida), final_audio, SR)

    total = len(final_audio) / SR
    print(f"\nAudio guardado: {salida}")
    print(f"Duración: {int(total//60)}:{int(total%60):02d}")
    print(f"\n--- SIGUIENTE PASO ---")
    print(f"python -m whisper {salida} --model large --word_timestamps True --output_format json --language en")


if __name__ == "__main__":
    main()
