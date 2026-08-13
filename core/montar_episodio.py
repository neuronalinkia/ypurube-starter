"""
Montaje de episodio con Ken Burns vía ffmpeg.
Lee un timing_maps.py, aplica Ken Burns a cada imagen estática,
soporta clips de vídeo reales (objetos Path), concatena y mezcla audio.

Uso:
  python core/montar_episodio.py \
    --ep-dir ep01_titulo \
    --timing ep01_titulo/timing_maps.py \
    --audio  ep01_titulo/audio/ep01_sfx_mix.wav \
    --output ep01_titulo/videos/ep01_draft.mp4

El fichero timing_maps.py debe exportar una lista ALL_BLOCKS:
  ALL_BLOCKS = [
      ("B1", B1_MAP),
      ("B2", B2_MAP),
      ...
  ]
  Donde cada MAP es lista de (start_s, end_s, "b1/filename.png") o (start_s, end_s, Path("clip.mp4"))

Si --audio no existe, usa ep_dir/audio/*_full.wav automáticamente.
"""

import subprocess
import sys
import argparse
from pathlib import Path

FFMPEG        = "ffmpeg"
W, H          = 1376, 768
RES           = f"{W}:{H}"
FPS           = "24"
CRF           = "22"
FADE_BETWEEN  = True
FADE_DURATION = 0.5


def run_ffmpeg(cmd, label=""):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  [ERROR] {label}: {result.stderr[-400:]}")
        return False
    return True


def ken_burns_filter(duration, index):
    """4 modos alternos de Ken Burns. Comas en min() escapadas para Windows."""
    frames = max(int(float(FPS) * duration), 2)
    spd    = 0.001
    mode   = index % 4

    if mode == 0:
        z = f"min(zoom+{spd}\\,1.3)"
        x = "iw/2-(iw/zoom/2)"
        y = "ih/2-(ih/zoom/2)"
    elif mode == 1:
        z = "1.12"
        x = f"(iw-iw/zoom)*on/{frames}"
        y = "ih/2-(ih/zoom/2)"
    elif mode == 2:
        z = f"min(zoom+{spd}\\,1.25)"
        x = "0"
        y = "0"
    else:
        z = "1.12"
        x = f"(iw-iw/zoom)*(1-on/{frames})"
        y = "ih/2-(ih/zoom/2)"

    return f"scale={W*2}:{H*2},zoompan=z={z}:x={x}:y={y}:d={frames}:s={W}x{H},setsar=1"


def fade_in_out(vf, duration, is_first, is_last):
    parts = [vf]
    if FADE_BETWEEN:
        if is_first and duration > FADE_DURATION * 2:
            parts.append(f"fade=t=in:st=0:d={FADE_DURATION}:color=black")
        if is_last and duration > FADE_DURATION * 2:
            parts.append(f"fade=t=out:st={max(0, duration - FADE_DURATION):.3f}:d={FADE_DURATION}:color=black")
    return ",".join(parts)


def img_to_clip(img_path, duration, out_path, idx, is_first, is_last):
    vf  = ken_burns_filter(duration, idx)
    vf  = fade_in_out(vf, duration, is_first, is_last)
    cmd = [
        FFMPEG, "-y", "-loop", "1", "-i", str(img_path),
        "-t", str(duration), "-vf", vf,
        "-r", FPS, "-c:v", "libx264", "-preset", "fast", "-crf", CRF,
        "-pix_fmt", "yuv420p", str(out_path),
    ]
    return run_ffmpeg(cmd, img_path.name)


def real_to_clip(in_path, duration, out_path, is_first, is_last):
    base_vf = f"scale={RES}:force_original_aspect_ratio=increase,crop={RES},setsar=1"
    vf = fade_in_out(base_vf, duration, is_first, is_last)
    cmd = [
        FFMPEG, "-y", "-i", str(in_path), "-t", str(duration),
        "-vf", vf, "-r", FPS, "-c:v", "libx264", "-preset", "fast", "-crf", CRF,
        "-an", "-pix_fmt", "yuv420p", str(out_path),
    ]
    return run_ffmpeg(cmd, in_path.name)


def black_clip(duration, out_path):
    cmd = [
        FFMPEG, "-y", "-f", "lavfi",
        "-i", f"color=c=black:size={W}x{H}:rate={FPS}:duration={duration}",
        "-c:v", "libx264", "-preset", "fast", "-crf", CRF,
        "-pix_fmt", "yuv420p", str(out_path),
    ]
    return run_ffmpeg(cmd, "black_clip")


def build_block(block_name, entries, imgdir, tmp_dir):
    clips  = []
    prefix = block_name.lower()
    n      = len(entries)

    for i, entry in enumerate(entries):
        start, end, source = entry
        duration = round(end - start, 3)
        if duration < 0.1:
            continue

        out = tmp_dir / f"{prefix}_{i+1:03d}.mp4"
        is_first = (i == 0)
        is_last  = (i == n - 1)

        if out.exists():
            print(f"  [{block_name}-{i+1:02d}] skip (ya existe)")
            clips.append(out)
            continue

        if isinstance(source, Path):
            if source.exists():
                print(f"  [{block_name}-{i+1:02d}] REAL {source.name} ({duration:.1f}s)", end="", flush=True)
                ok = real_to_clip(source, duration, out, is_first, is_last)
            else:
                print(f"  [{block_name}-{i+1:02d}] REAL faltante {source.name} -> negro")
                ok = black_clip(duration, out)
        else:
            img = imgdir / source
            if img.exists():
                print(f"  [{block_name}-{i+1:02d}] {img.name} ({duration:.1f}s)", end="", flush=True)
                ok = img_to_clip(img, duration, out, i, is_first, is_last)
            else:
                print(f"  [{block_name}-{i+1:02d}] FALTA {img.name} -> negro")
                ok = black_clip(duration, out)

        if ok:
            print(" OK")
        clips.append(out)

    return clips


def concat_and_mix(all_clips, audio, output):
    list_file  = output.parent / "_concat_list.txt"
    tmp_video  = output.parent / "_video_only.mp4"

    list_file.write_text("\n".join(f"file '{p}'" for p in all_clips), encoding="utf-8")

    print(f"\nConcatenando {len(all_clips)} clips...")
    if not run_ffmpeg([
        FFMPEG, "-y", "-f", "concat", "-safe", "0",
        "-i", str(list_file), "-c", "copy", str(tmp_video)
    ], "concat"):
        print("Error en concatenación.")
        return

    print("Mezclando audio...")
    if not run_ffmpeg([
        FFMPEG, "-y",
        "-i", str(tmp_video), "-i", str(audio),
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-map", "0:v", "-map", "1:a", "-shortest",
        "-movflags", "+faststart", str(output)
    ], "audio mix"):
        print("Error en mezcla de audio.")
        return

    tmp_video.unlink(missing_ok=True)
    list_file.unlink(missing_ok=True)
    print(f"\nListo: {output}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ep-dir",  required=True, help="Carpeta raíz del episodio")
    parser.add_argument("--timing",  required=True, help="Fichero timing_maps.py")
    parser.add_argument("--audio",   required=True, help="WAV de audio (narración + SFX)")
    parser.add_argument("--output",  required=True, help="MP4 de salida")
    parser.add_argument("--force",   action="store_true", help="Regenerar aunque ya exista")
    args = parser.parse_args()

    ep_dir = Path(args.ep_dir)
    imgdir = ep_dir / "images" / "video"
    output = Path(args.output)
    audio  = Path(args.audio)

    if output.exists() and not args.force:
        print(f"Ya existe: {output}  (usa --force para regenerar)")
        sys.exit(0)

    if not audio.exists():
        # Buscar automáticamente en ep_dir/audio/
        wavs = list((ep_dir / "audio").glob("*_full.wav"))
        if wavs:
            audio = sorted(wavs)[-1]
            print(f"[INFO] Audio: {audio}")
        else:
            print(f"[ERROR] Audio no encontrado: {args.audio}")
            sys.exit(1)

    # Cargar timing maps
    import importlib.util
    spec = importlib.util.spec_from_file_location("timing", args.timing)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    # Resolver paths relativos de clips reales
    all_blocks = []
    for block_name, entries in mod.ALL_BLOCKS:
        resolved = []
        for start, end, source in entries:
            if isinstance(source, Path) and not source.is_absolute():
                source = ep_dir / source
            resolved.append((start, end, source))
        all_blocks.append((block_name, resolved))

    output.parent.mkdir(parents=True, exist_ok=True)
    tmp_dir = output.parent / "tmp_render"
    tmp_dir.mkdir(exist_ok=True)

    all_clips = []
    for block_name, entries in all_blocks:
        print(f"\n=== {block_name} ({len(entries)} entradas) ===")
        all_clips.extend(build_block(block_name, entries, imgdir, tmp_dir))

    if not all_clips:
        print("Sin clips. Abortando.")
        sys.exit(1)

    concat_and_mix(all_clips, audio, output)


if __name__ == "__main__":
    main()
