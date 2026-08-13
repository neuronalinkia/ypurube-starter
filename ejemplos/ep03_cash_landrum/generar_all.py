"""
EP03 Cash-Landrum — Genera TODAS las imágenes del episodio.

Llama a los scripts de bloque en orden. Cada script es reanudable
(salta las imágenes que ya existen). Puedes interrumpir y reiniciar.

Uso:
  # Todas los bloques en secuencia
  python ejemplos/ep03_cash_landrum/generar_all.py

  # Solo un bloque específico
  python ejemplos/ep03_cash_landrum/generar_b1.py
  python ejemplos/ep03_cash_landrum/generar_b2.py
  python ejemplos/ep03_cash_landrum/generar_b3.py
  python ejemplos/ep03_cash_landrum/generar_b4_b11.py --block b4

NOTA: Genera en modo Unlimited de Higgsfield (gratis, no gasta créditos).
  Requiere que generar_imagen.py esté configurado con el perfil Chrome.
  Primera vez: abre el navegador y haz login en Higgsfield manualmente.

Pipeline completo:
  1. Generar audio:
     python core/generar_audio_kokoro.py \\
       --guion ejemplos/ep03_cash_landrum/scripts/narration.txt \\
       --salida ejemplos/ep03_cash_landrum/audio/ep03_full.wav \\
       --voice am_puck --speed 1.05

  2. Whisper timestamps:
     python -m whisper ejemplos/ep03_cash_landrum/audio/ep03_full.wav \\
       --model large --word_timestamps True --output_format json --language en

  3. Generar imágenes (este script):
     python ejemplos/ep03_cash_landrum/generar_all.py

  4. Montar vídeo:
     python core/montar_episodio.py \\
       --ep-dir ejemplos/ep03_cash_landrum \\
       --timing ejemplos/ep03_cash_landrum/timing_maps.py \\
       --audio  ejemplos/ep03_cash_landrum/audio/ep03_full.wav \\
       --output ejemplos/ep03_cash_landrum/videos/ep03_draft.mp4

  5. Mezclar SFX:
     python ejemplos/ep03_cash_landrum/mezclar_sfx.py

  6. Vídeo final con SFX:
     ffmpeg -i ep03_draft.mp4 -i ep03_sfx_mix.wav \\
       -c:v copy -c:a aac -b:a 192k \\
       -map 0:v -map 1:a -shortest ep03_final.mp4
"""
import subprocess
import sys
from pathlib import Path

EP_DIR = Path(__file__).parent

STEPS = [
    (EP_DIR / "generar_b1.py",     "B1 — HOOK (Texas road, UFO appears)"),
    (EP_DIR / "generar_b2.py",     "B2 — EL ENCUENTRO (heat, helicopters)"),
    (EP_DIR / "generar_b3.py",     "B3 — LOS SÍNTOMAS (radiation injuries)"),
    (EP_DIR / "generar_b4_b11.py", "B4-B11 — Investigation through FM-1485 today"),
]

if __name__ == "__main__":
    total = len(STEPS)
    for i, (script, label) in enumerate(STEPS, 1):
        print(f"\n{'='*60}")
        print(f"  PASO {i}/{total}: {label}")
        print(f"{'='*60}")
        result = subprocess.run([sys.executable, str(script)])
        if result.returncode != 0:
            print(f"\n[ERROR] Falló: {script.name}")
            print("Corregir y reiniciar — el progreso se conserva.")
            sys.exit(1)

    print("\n" + "="*60)
    print("  TODAS LAS IMÁGENES GENERADAS")
    print("="*60)
    print("\nSiguiente paso:")
    print("  Revisar imágenes: python core/revisar_imagenes.py --carpeta ejemplos/ep03_cash_landrum/images/video/b1")
    print("\nLuego montar:")
    print("  python core/montar_episodio.py \\")
    print(f"    --ep-dir {EP_DIR} \\")
    print(f"    --timing {EP_DIR / 'timing_maps.py'} \\")
    print(f"    --audio  {EP_DIR / 'audio/ep03_full.wav'} \\")
    print(f"    --output {EP_DIR / 'videos/ep03_draft.mp4'}")
