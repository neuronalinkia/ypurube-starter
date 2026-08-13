"""
Prueba todas las voces disponibles con el mismo texto de muestra.
Genera un WAV por voz en audio/prueba_voces/ para escucharlas y elegir.

Uso:
  # Probar todas las voces de Kokoro
  python core/probar_voces.py --motor kokoro

  # Probar todas las voces de Orpheus
  python core/probar_voces.py --motor orpheus

  # Probar solo una voz
  python core/probar_voces.py --motor kokoro --voz am_puck

Escucha los resultados en: audio/prueba_voces/
Elige la voz y úsala en generar_audio_kokoro.py con --voice [nombre]
"""

import argparse
import numpy as np
import soundfile as sf
from pathlib import Path

# Texto de muestra — representativo del tono del canal
TEXTO_MUESTRA = (
    "December 29th, 1980. A quiet two-lane road in southeast Texas. "
    "No streetlights. No other cars. Just Betty Cash, her friend Vickie, "
    "and a seven-year-old boy named Colby, driving home. "
    "At nine in the evening, something appeared above the road. "
    "Something that was not a plane. Not a star. Not anything "
    "that had a name yet. And in the next fifteen minutes, "
    "all three of them would be exposed to something that would follow them "
    "for the rest of their lives."
)

OUT_DIR = Path("audio/prueba_voces")


def probar_kokoro(voz_filtro=None):
    from kokoro import KPipeline

    VOCES = [
        "am_puck",    # recomendada — oscuro, masculino, directo
        "am_adam",    # grave, formal
        "am_echo",    # suave, reflexivo
        "am_eric",    # neutro americano
        "am_fenrir",  # épico, intenso
        "am_liam",    # joven, energético
        "am_michael", # clásico, documental
        "am_onyx",    # profundo, autoritario
        "am_santa",   # cálido (menos útil para misterio)
    ]

    if voz_filtro:
        VOCES = [v for v in VOCES if voz_filtro in v]

    print("Cargando Kokoro TTS...")
    pipe = KPipeline(lang_code='a')

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for voz in VOCES:
        out = OUT_DIR / f"kokoro_{voz}.wav"
        if out.exists():
            print(f"  Skip (ya existe): {out.name}")
            continue
        print(f"  Generando: {voz}...")
        generator    = pipe(TEXTO_MUESTRA, voice=voz, speed=1.05, split_pattern=None)
        audio_chunks = []
        for _, _, audio in generator:
            audio_chunks.append(audio)
        if audio_chunks:
            audio = np.concatenate(audio_chunks)
            sf.write(str(out), audio, 24000)
            print(f"    -> {out.name} ({len(audio)/24000:.1f}s)")

    print(f"\nEscucha los resultados en: {OUT_DIR}/")
    print("Usa la voz elegida con: --voice am_puck (o el nombre que corresponda)")


def probar_orpheus(voz_filtro=None):
    """
    Orpheus TTS — requiere instalación separada.
    GitHub: canopyai/orpheus-tts
    pip install orpheus-tts
    """
    try:
        from orpheus_tts import OrpheusModel
    except ImportError:
        print("Orpheus no instalado. Instalar con: pip install orpheus-tts")
        print("GitHub: https://github.com/canopyai/Orpheus-TTS")
        return

    VOCES = [
        "leo",   # masculina profunda — recomendada para misterios
        "dan",   # masculina neutra
        "tara",  # femenina clara
        "leah",  # femenina suave
        "jess",  # femenina energética
        "mia",   # femenina cálida
        "zac",   # masculina joven
    ]

    if voz_filtro:
        VOCES = [v for v in VOCES if voz_filtro in v]

    print("Cargando Orpheus TTS...")
    model = OrpheusModel(model_name="canopy-labs/orpheus-3b-0.1-ft")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for voz in VOCES:
        out = OUT_DIR / f"orpheus_{voz}.wav"
        if out.exists():
            print(f"  Skip (ya existe): {out.name}")
            continue
        print(f"  Generando: {voz}...")
        try:
            syn_tokens = model.generate_speech(
                prompt=TEXTO_MUESTRA,
                voice=voz,
                repetition_penalty=1.1,
            )
            chunks = []
            for chunk in syn_tokens:
                chunks.append(chunk)
            if chunks:
                audio = np.frombuffer(b"".join(chunks), dtype=np.int16)
                sf.write(str(out), audio, 24000, subtype='PCM_16')
                print(f"    -> {out.name}")
        except Exception as e:
            print(f"    Error: {e}")

    print(f"\nEscucha los resultados en: {OUT_DIR}/")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--motor", choices=["kokoro", "orpheus"], required=True,
                        help="Motor TTS a probar")
    parser.add_argument("--voz", default=None,
                        help="Filtrar a una voz específica (ej: am_puck, leo)")
    args = parser.parse_args()

    if args.motor == "kokoro":
        probar_kokoro(args.voz)
    elif args.motor == "orpheus":
        probar_orpheus(args.voz)


if __name__ == "__main__":
    main()
