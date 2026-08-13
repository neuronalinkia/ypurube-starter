"""
Genera narración con Miso One TTS (INT4 cuantizado).
Calidad superior a Kokoro — pausas dramáticas naturales, énfasis real.
Recomendado para narración de misterios donde el silencio importa.

Instalación:
  git clone https://github.com/MisoLabsAI/MisoTTS  (en Desktop/MisoTTS)
  cd MisoTTS && pip install -e .
  # Descargar modelo INT4: droyster/MisoTTS-8B-torchao-int4 en HuggingFace
  # VRAM necesaria: ~4.5GB (INT4) — cabe en cualquier GPU ≥6GB

Uso:
  python core/generar_audio_miso.py \
    --guion ep01_titulo/scripts/narration.txt \
    --salida ep01_titulo/audio/ep01_full.wav

  python core/generar_audio_miso.py \
    --texto "texto directo" \
    --salida audio/prueba.wav \
    --speaker 0

Voces disponibles:
  --speaker 0   voz masculina (narrador por defecto)
  --speaker 1   voz masculina alternativa

Rutas a configurar según tu instalación:
  MISO_INT4_DIR  → donde descargaste el modelo INT4
  MISO_DIR       → donde clonaste MisoTTS
"""

import os
import sys
import re
import argparse
from pathlib import Path

# ─── Rutas — AJUSTAR a tu instalación ────────────────────────────────────────
MISO_DIR      = Path.home() / "Desktop" / "MisoTTS"
MISO_INT4_DIR = Path.home() / ".cache" / "huggingface" / "hub" / \
    "models--droyster--MisoTTS-8B-torchao-int4" / "snapshots"
# ─────────────────────────────────────────────────────────────────────────────

os.environ["NO_TORCH_COMPILE"]      = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"


def find_miso_int4():
    """Busca el snapshot más reciente del modelo INT4."""
    if MISO_INT4_DIR.exists():
        snapshots = sorted(MISO_INT4_DIR.iterdir())
        if snapshots:
            return snapshots[-1]
    raise FileNotFoundError(
        f"Modelo Miso INT4 no encontrado en {MISO_INT4_DIR}\n"
        "Descargar desde: https://huggingface.co/droyster/MisoTTS-8B-torchao-int4"
    )


def cargar_modelo(speaker_id):
    import torch

    model_path = find_miso_int4()
    sys.path.insert(0, str(model_path))
    sys.path.insert(1, str(MISO_DIR))

    os.environ["MISO_TTS_TOKENIZER"] = str(MISO_DIR / "llama_tokenizer")

    from load_quantized import load_miso_8b_torchao_int4

    print(f"VRAM libre: {torch.cuda.mem_get_info()[0]/1024**3:.1f} GB")
    print("Cargando Miso One INT4...")

    generator = load_miso_8b_torchao_int4(
        repo_id=str(model_path),
        device="cuda" if torch.cuda.is_available() else "cpu",
        disable_watermark=False,
    )
    vram = (torch.cuda.mem_get_info()[1] - torch.cuda.mem_get_info()[0]) / 1024**3
    print(f"Modelo cargado. VRAM usada: {vram:.1f} GB\n")
    return generator


def limpiar_texto(texto):
    texto = re.sub(r'\[PAUSA\]', '', texto)
    texto = re.sub(r'\*\*.*?\*\*', '', texto)
    texto = re.sub(r'^#+.*$', '', texto, flags=re.MULTILINE)
    texto = re.sub(r'^\s*---\s*$', '', texto, flags=re.MULTILINE)
    texto = re.sub(r'\n{2,}', '\n', texto)
    return texto.strip()


def split_en_frases(texto, max_palabras=35):
    frases = re.split(r'(?<=[.!?…])\s+', texto)
    chunks, actual, palabras = [], [], 0
    for f in frases:
        n = len(f.split())
        if palabras + n > max_palabras and actual:
            chunks.append(' '.join(actual))
            actual, palabras = [f], n
        else:
            actual.append(f)
            palabras += n
    if actual:
        chunks.append(' '.join(actual))
    return [c for c in chunks if c.strip()]


def generar(generator, texto, speaker_id, salida):
    import torch
    import torchaudio
    from generator import Segment

    salida      = Path(salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    chunks_dir  = salida.parent / (salida.stem + "_chunks")
    chunks_dir.mkdir(exist_ok=True)

    chunks = split_en_frases(limpiar_texto(texto))
    print(f"{len(chunks)} chunks a generar\n")

    segmentos, audios = [], []
    for i, chunk in enumerate(chunks):
        chunk_path = chunks_dir / f"chunk_{i:03d}.wav"
        if chunk_path.exists():
            import torchaudio as ta
            wav, sr = ta.load(str(chunk_path))
            audio = wav.squeeze()
            print(f"  Skip {i:03d} (ya existe)")
        else:
            print(f"  [{i+1}/{len(chunks)}] {chunk[:70]}{'...' if len(chunk)>70 else ''}")
            audio = generator.generate(
                text=chunk,
                speaker=speaker_id,
                context=segmentos[-3:],
                max_audio_length_ms=15000,
                temperature=0.8,
                topk=50,
            )
            torchaudio.save(str(chunk_path), audio.unsqueeze(0).cpu(), generator.sample_rate)

        seg = Segment(text=chunk, speaker=speaker_id, audio=audio)
        segmentos.append(seg)
        audios.append(audio)

    audio_final = torch.cat(audios, dim=0)
    torchaudio.save(str(salida), audio_final.unsqueeze(0).cpu(), generator.sample_rate)
    dur = audio_final.shape[0] / generator.sample_rate
    print(f"\nGuardado: {salida}")
    print(f"Duración: {int(dur//60)}:{int(dur%60):02d}")
    print(f"\n--- SIGUIENTE PASO ---")
    print(f"python -m whisper {salida} --model large --word_timestamps True --output_format json --language en")


def main():
    parser = argparse.ArgumentParser()
    grupo  = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--guion", help="Fichero .txt o .md del guion")
    grupo.add_argument("--texto", help="Texto directo")
    parser.add_argument("--salida",  required=True, help="Fichero .wav de salida")
    parser.add_argument("--speaker", type=int, default=0, choices=[0, 1],
                        help="0=masculina principal, 1=masculina alternativa")
    args = parser.parse_args()

    generator = cargar_modelo(args.speaker)

    if args.guion:
        texto = Path(args.guion).read_text(encoding="utf-8")
    else:
        texto = args.texto

    generar(generator, texto, args.speaker, args.salida)


if __name__ == "__main__":
    main()
