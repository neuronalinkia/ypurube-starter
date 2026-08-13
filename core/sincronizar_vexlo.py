"""
Sincronización Vexlo — coloca cada imagen en el momento exacto donde el transcript
menciona las keywords de su filename.

Principio: el FILENAME contiene palabras reales del transcript.
El algoritmo busca cuándo se dicen → pone la imagen ahí.

Uso:
  # Solo verificar (sin renderizar)
  python core/sincronizar_vexlo.py \
    --audio ep01/audio/ep01_full.json \
    --images ep01/images/video \
    --output ep01/ep01_vexlo.mp4 \
    --dry-run

  # Render completo
  python core/sincronizar_vexlo.py \
    --audio ep01/audio/ep01_full.json \
    --images ep01/images/video \
    --output ep01/ep01_vexlo.mp4 \
    --audio-wav ep01/audio/ep01_full.wav

Naming de imágenes — CRÍTICO:
  MALO:  b3_012_lighthouse_dramatic.png  (descripción visual)
  BUENO: b3_012_storm_rag_three_day.png  (palabras reales del transcript)
"""

import json
import re
import subprocess
import argparse
from pathlib import Path
from collections import defaultdict

STOP_WORDS = {
    'the','a','an','and','or','of','in','on','at','to','for','is','it','its','as',
    'from','with','by','not','no','one','two','three','did','has','had','was','were',
    'all','island','lighthouse','men','man','sea','night','dark','light','day','days',
    'time','back','out','into','came','went','found','know','knew','see','saw','report',
    'inside','outside','portrait','intro','establishing','test','wide','close','last',
    'final','again',
}

SUFFIXES     = ['ing', 'ers', 'ed', 'er', 'ly', 'es', 's']
MIN_DURATION = 2.0
WINDOW       = 3.0


def normalize(word):
    w = word.lower().strip(".,;:!?'\"")
    for suf in SUFFIXES:
        if w.endswith(suf) and len(w) - len(suf) >= 4:
            return w[:-len(suf)]
    return w


def keywords_from_filename(filename):
    stem  = Path(filename).stem
    parts = stem.split('_')
    start_idx = 0
    if parts and parts[0].startswith('b') and parts[0][1:].isdigit():
        start_idx = 1
    if start_idx < len(parts) and parts[start_idx].isdigit():
        start_idx += 1
    result = []
    for p in parts[start_idx:]:
        n = normalize(p)
        if n not in STOP_WORDS and len(n) >= 4:
            result.append(n)
    return result


def load_whisper(json_path):
    data  = json.loads(Path(json_path).read_text(encoding='utf-8'))
    words = []
    for seg in data.get('segments', []):
        for w in seg.get('words', []):
            word = w.get('word', '').strip()
            if word:
                words.append({'w': normalize(word), 's': w.get('start', 0), 'e': w.get('end', 0)})
    return words


def build_index(words, block_start, block_end):
    index = defaultdict(list)
    for w in words:
        if block_start <= w['s'] < block_end:
            index[w['w']].append(w['s'])
    return index


def score_timestamp(t, keywords, index):
    return sum(1 for kw in set(keywords) if any(abs(ts - t) <= WINDOW for ts in index.get(kw, [])))


def assign_timestamps(images_dir, whisper_words, block_ranges):
    results  = []
    no_match = []

    for block_name, (b_start, b_end) in block_ranges.items():
        block_dir = Path(images_dir) / block_name
        if not block_dir.exists():
            continue

        images = sorted(block_dir.glob("*.png"))
        if not images:
            continue

        index = build_index(whisper_words, b_start, b_end)

        for img in images:
            keywords = keywords_from_filename(img.name)
            if not keywords:
                results.append((b_start, img))
                no_match.append(img.name)
                continue

            # Candidatos: timestamps donde aparecen las keywords
            candidates = sorted({t for kw in keywords for t in index.get(kw, [])})
            best_t, best_score = b_start, 0

            for t in candidates:
                s = score_timestamp(t, keywords, index)
                if s > best_score:
                    best_score, best_t = s, t

            if best_score == 0:
                for kw in keywords:
                    times = index.get(kw, [])
                    if times:
                        best_t = times[0]
                        break
                else:
                    no_match.append(img.name)

            results.append((best_t, img))

    results.sort(key=lambda x: x[0])
    return results, no_match


def build_timeline(assigned, total_duration):
    timeline = []
    for i, (t, img) in enumerate(assigned):
        start = t
        if i + 1 < len(assigned):
            end = max(start + MIN_DURATION, assigned[i+1][0])
        else:
            end = max(start + MIN_DURATION, total_duration)
        timeline.append((start, end, img))
    return timeline


def render(timeline, audio_wav, output, W=1376, H=768, FPS=24, CRF=22):
    tmp_dir = Path(output).parent / "tmp_vexlo"
    tmp_dir.mkdir(exist_ok=True)
    clip_list = []

    for i, (start, end, img) in enumerate(timeline):
        dur    = max(end - start, 0.1)
        frames = max(int(dur * FPS), 1)
        mode   = i % 4
        spd    = 0.0015

        if mode == 0:
            x, y = "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
        elif mode == 1:
            x, y = "0", "ih/2-(ih/zoom/2)"
        elif mode == 2:
            x, y = "iw/2-(iw/zoom/2)", "0"
        else:
            x, y = "iw-(iw/zoom)", "ih/2-(ih/zoom/2)"

        z        = f"min(zoom+{spd}\\,1.3)"
        vf       = f"scale={W*2}:{H*2},zoompan=z={z}:x={x}:y={y}:d={frames}:s={W}x{H},setsar=1"
        out_clip = tmp_dir / f"clip_{i:04d}.mp4"

        subprocess.run([
            "ffmpeg", "-y", "-loop", "1", "-i", str(img),
            "-vf", vf, "-t", str(dur),
            "-r", str(FPS), "-c:v", "libx264",
            "-crf", str(CRF), "-preset", "fast",
            "-pix_fmt", "yuv420p", str(out_clip)
        ], check=True, capture_output=True)
        clip_list.append(str(out_clip))
        print(f"  Clip {i+1}/{len(timeline)}: {img.name} ({dur:.1f}s)", end="\r")

    print()
    list_file  = tmp_dir / "clips.txt"
    list_file.write_text("\n".join(f"file '{c}'" for c in clip_list))
    concat_out = Path(output).parent / "tmp_concat.mp4"

    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(list_file), "-c", "copy", str(concat_out)
    ], check=True, capture_output=True)

    subprocess.run([
        "ffmpeg", "-y", "-i", str(concat_out), "-i", str(audio_wav),
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-map", "0:v", "-map", "1:a", "-shortest",
        "-movflags", "+faststart", str(output)
    ], check=True, capture_output=True)

    print(f"Render completo: {output}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio",     required=True, help="Whisper JSON")
    parser.add_argument("--images",    required=True, help="Carpeta con b1/, b2/...")
    parser.add_argument("--output",    required=True, help="Fichero .mp4 de salida")
    parser.add_argument("--audio-wav", help="WAV de narración para el render")
    parser.add_argument("--blocks",    help="Python con BLOCK_RANGES dict (opcional)")
    parser.add_argument("--dry-run",   action="store_true")
    args = parser.parse_args()

    whisper_words = load_whisper(args.audio)
    total_dur     = max(w['e'] for w in whisper_words) if whisper_words else 0
    print(f"Whisper: {len(whisper_words)} palabras, {total_dur:.1f}s total")

    images_dir = Path(args.images)
    block_dirs = sorted([d for d in images_dir.iterdir() if d.is_dir()])

    if args.blocks:
        import importlib.util
        spec = importlib.util.spec_from_file_location("timing", args.blocks)
        mod  = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        block_ranges = mod.BLOCK_RANGES
    else:
        n = len(block_dirs)
        dur_per = total_dur / n if n else total_dur
        block_ranges = {d.name: (i * dur_per, (i+1) * dur_per) for i, d in enumerate(block_dirs)}

    print(f"Bloques: {list(block_ranges.keys())}")

    assigned, no_match = assign_timestamps(images_dir, whisper_words, block_ranges)
    print(f"Imágenes asignadas: {len(assigned)} | Sin match: {len(no_match)}")

    debug_path = Path(args.output).parent / "vexlo_debug.txt"
    with open(debug_path, "w") as f:
        f.write(f"Total: {len(assigned)} | Sin match: {len(no_match)}\n\n")
        if no_match:
            f.write("SIN MATCH (renombrar con keywords del transcript):\n")
            for nm in no_match:
                f.write(f"  {nm}\n")
        f.write("\nTIMELINE:\n")
        for t, img in assigned:
            f.write(f"  {t:7.2f}s  {img.name}\n")

    print(f"Debug guardado: {debug_path}")
    if no_match:
        print("[!] Imágenes sin match — renombrar con keywords reales del transcript.")

    if args.dry_run or not args.audio_wav:
        print("Dry-run. Usar sin --dry-run + --audio-wav para renderizar.")
        return

    timeline = build_timeline(assigned, total_dur)
    durs = [e - s for s, e, _ in timeline]
    print(f"Duración media: {sum(durs)/len(durs):.2f}s | >6s: {sum(1 for d in durs if d > 6)}/{len(durs)}")
    print("Renderizando...")
    render(timeline, args.audio_wav, args.output)


if __name__ == "__main__":
    main()
