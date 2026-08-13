# CLAUDE.md — Manual operativo del canal de YouTube

Este repositorio produce episodios de misterios históricos en inglés (~18 min) usando IA.
**Lee este fichero completo antes de hacer cualquier cosa.**

---

## PIPELINE COMPLETO — orden obligatorio

```
FASE 1  → Guion              (skill mystery-storytelling)
FASE 2  → Audio TTS          (core/generar_audio_kokoro.py)
FASE 3  → Whisper timestamps  (comando whisper)
FASE 4  → Plan visual         (lista de imágenes con keywords del transcript)
FASE 5  → Generar imágenes    (core/generar_imagen.py via Playwright — SIEMPRE Unlimited)
FASE 6  → Auditoría imágenes  (revisar y regenerar malas)
FASE 7  → Timing maps         (asignar imagen → rango de tiempo)
FASE 8  → Sync Vexlo          (core/sincronizar_vexlo.py)
FASE 9  → Montaje Ken Burns   (core/montar_episodio.py)
FASE 10 → Diseño de sonido    (core/mezclar_sfx.py)
FASE 11 → Thumbnail           (core/generar_imagen.py con prompt de documento/evidencia)
```

---

## FASE 1 — GUION

**Invocar SIEMPRE la skill antes de escribir:**
```
Skill: mystery-storytelling
```

Estructura de 9 bloques:
- B1 Cold open (in medias res — momento más dramático)
- B2 Contexto (quiénes, dónde, por qué importa + open loop)
- B3 La última vez (normalidad documentada antes del quiebre)
- B4 El descubrimiento (detalle a detalle, orden cronológico)
- B5 Explicación oficial (con respeto, luego mostrar dónde falla)
- B6 Las teorías (cada una como historia, no como lista)
- B7 El dato raro (lo que nadie menciona + pregunta abierta)
- B8 Zoom out (por qué importa más allá del misterio)
- B9 Cierre (cerrar el open loop del cold open)

**Reglas del guion:**
- Inglés. Voz narradora masculina, noir, directa.
- Cada frase debe describir algo VISUAL y LITERAL — el guion es también el plan de imágenes.
- 2.800-3.200 palabras (18-20 min a 140 ppm).
- NO listas, NO datos sueltos — historia fluida.
- Guardar en: `scripts/guiones/ep0X_titulo.md`

**Analizar vídeo de referencia de estilo:**
Si el usuario envía un vídeo de referencia (Vexlo, Mack, etc.):
```
Skill: claude-video-vision:watch-video
```
Extraer: ritmo de cambio de imágenes, estilo visual, estructura narrativa, tono.

---

## FASE 2 — AUDIO TTS

**Motor:** Kokoro `am_puck`, speed=1.05 (local, gratis, sin GPU extra)

```bash
python core/generar_audio_kokoro.py \
  --guion scripts/guiones/ep0X_titulo.md \
  --salida ep0X_titulo/audio/ep0X_full.wav
```

- Genera chunk por chunk (párrafo por párrafo)
- Silencio entre párrafos: 0.6s
- Si ya existe un chunk, lo salta (reanudable)
- Output: `ep0X_titulo/audio/ep0X_full.wav` (24000Hz, mono)

**Alternativa mayor calidad:** Miso One INT4 (`core/generar_audio_miso.py`)
- Mejores pausas dramáticas, mejor para misterio
- Requiere venv específico de MisoTTS — ver config.py para rutas

---

## FASE 3 — WHISPER (timestamps word-level)

**CRÍTICO** — sin esto no hay sync Vexlo.

```bash
python -m whisper ep0X_titulo/audio/ep0X_full.wav \
  --model large \
  --word_timestamps True \
  --output_format json \
  --language en
```

Output: `ep0X_titulo/audio/ep0X_full.json`
Estructura: `data['segments'][i]['words']` → cada word: `{"word": "...", "start": 0.0, "end": 0.3}`

---

## FASE 4 — PLAN VISUAL (lista de imágenes por bloque)

Para cada bloque del guion, listar qué imágenes se necesitan.
**Regla crítica del naming de imágenes:**
- El filename debe contener palabras REALES del transcript en ese momento
- MALO: `b3_012_lighthouse_dramatic.png` (descripción visual)
- BUENO: `b3_012_storm_rag_three_day.png` (palabras que aparecen en el transcript)

**Stop words del algoritmo Vexlo** (no funcionan como keywords):
```
'the','a','an','and','or','of','in','on','at','to','for','is','it','its','as',
'from','with','by','not','no','one','two','three','did','has','had','was','were',
'all','island','lighthouse','men','man','sea','night','dark','light','day','days',
'time','back','out','into','came','went','found','know','knew','see','saw','report'
```
Los nombres de personajes también son stop words — usar palabras de sus acciones.

Cantidad objetivo: ≈1 imagen por concepto narrado → ≈130-160 para 19 min.

---

## FASE 5 — GENERACIÓN DE IMÁGENES

### REGLA ABSOLUTA: SIEMPRE vía Playwright Unlimited. NUNCA MCP generate_image.

El MCP `generate_image` descuenta créditos (~1-2/imagen). Playwright con Unlimited es gratis.

```bash
# Generar imágenes individuales o en batch
python core/generar_imagen.py "prompt|filename.png" "prompt2|filename2.png" \
  --out-dir ep0X_titulo/images/video/b1

# Con imagen de referencia de personaje
python core/generar_imagen.py "prompt|filename.png" \
  --ref ep0X_titulo/scripts/character_ref.png \
  --out-dir ep0X_titulo/images/video/b1
```

**Reglas técnicas Playwright en este PC (NO cambiar):**
- `channel="chrome"` — Playwright Chromium crashea
- `headless=False` — en headless el click Generate no dispara la petición
- `keyboard.type(prompt, delay=6)` en chunks de 40 chars — `innerText`/`fill()` no actualiza React

**Style strings:**
```python
# Para escenas CON el narrador
S = ("Bold flat illustration style, 2D cartoon, thick black outlines, "
     "dark navy blue background, orange accent colors, cinematic widescreen 16:9, "
     "no text, no words, no letters. ")

# Para escenas SIN personaje (ambiente, objetos, paisajes)
S_ENV = ("Bold flat illustration style, 2D cartoon, thick black outlines, "
         "dark navy blue background, orange accent colors, cinematic widescreen 16:9, "
         "no text, no words, no letters. ")
# S_ENV NO incluye "oval face" — si lo incluyes meterá caras en paisajes
```

**Narrador (Reference Element):**
```python
# El ID del elemento de referencia del narrador se guarda en:
# ep0X_titulo/scripts/narrator_element_id.txt
ELEMENT_ID = Path("ep0X_titulo/scripts/narrator_element_id.txt").read_text().strip()
ELEMENT_REF = f"<<<{ELEMENT_ID}>>> "
# Usar SOLO en prompts donde el narrador aparece en pantalla
```

**Para crear un nuevo Reference Element de narrador:**
```bash
python core/crear_elemento_ref.py
# Sube la imagen del personaje a Higgsfield y devuelve el element_id
# Guardarlo en ep0X_titulo/scripts/narrator_element_id.txt
```

**Crear scripts por bloque:**
Ver `templates/generar_bloque_template.py` como punto de partida.
Patrón: lista de tuplas `(prompt, filename)` → llamar a `core/generar_imagen.py`

---

## FASE 6 — AUDITORÍA DE IMÁGENES

Revisar ANTES de construir timing maps. Problemas comunes (10-15%):
- Narrador en escena de ambiente → regenerar sin ELEMENT_REF
- Texto visible no deseado → añadir "no text, no words" más prominente
- Forma errónea → reescribir con negaciones ("NOT round, NOT circular")
- Era equivocada (vestuario/tecnología) → especificar año exacto
- Imagen repetida del concepto anterior → reescribir desde otro ángulo

```bash
# UI web para revisar variantes
python core/revisar_imagenes.py --carpeta ep0X_titulo/images/video/b1
```

---

## FASE 7 — TIMING MAPS

Asignar cada imagen a su rango de tiempo (start_s, end_s).

**Formato:**
```python
# ep0X_titulo/timing_maps.py
B1_MAP = [
    (0.00,  3.50,  "b1/b1_001_december_29_1980.png"),
    (3.50,  7.20,  "b1/b1_002_empty_road_night.png"),
    # ...
]
```

**Proceso:**
1. Leer `ep0X_full.json` (Whisper) → extraer timestamps de frases clave
2. Asignar imagen a cada rango
3. Verificar: sin gaps >0.5s, sin duplicados, max 5s por imagen

**Timing maps v2 (si hay imágenes >5s o duplicados):**
Analizar con agente → subdividir segmentos largos → generar imágenes adicionales.

---

## FASE 8 — SYNC VEXLO

El algoritmo coloca cada imagen en el momento exacto donde el transcript menciona sus keywords.

```bash
python core/sincronizar_vexlo.py \
  --audio ep0X_titulo/audio/ep0X_full.json \
  --images ep0X_titulo/images/video \
  --blocks ep0X_titulo/timing_maps.py \
  --output ep0X_titulo/ep0X_vexlo.mp4 \
  --dry-run   # verificar sin renderizar
```

Verificar `vexlo_debug.txt`:
- Objetivo: 0 imágenes sin match
- Si hay sin match: renombrar con keywords reales del transcript

---

## FASE 9 — MONTAJE KEN BURNS

```bash
python core/montar_episodio.py \
  --timing ep0X_titulo/timing_maps_v2.py \
  --imgdir ep0X_titulo/images/video \
  --audio ep0X_titulo/audio/ep0X_full.wav \
  --output ep0X_titulo/videos/ep0X_draft.mp4
```

**Parámetros fijos:**
- Resolución: 1376×768 (16:9)
- FPS: 24
- CRF: 22, preset fast
- Ken Burns: zoom-in / pan L→R / zoom-in esquina / pan R→L (alternando)
- Fade to black entre bloques: 0.5s

**Ken Burns — filtro ffmpeg validado en Windows:**
```python
z = f"min(zoom+{spd}\\,1.3)"  # CRÍTICO: escapar comas con \\,
vf = f"scale={W*2}:{H*2},zoompan=z={z}:x={x}:y={y}:d={frames}:s={W}x{H},setsar=1"
# NO poner fps= dentro de zoompan — usar -r en línea de comando
```

---

## FASE 10 — DISEÑO DE SONIDO

```bash
python core/mezclar_sfx.py \
  --narration ep0X_titulo/audio/ep0X_full.wav \
  --output ep0X_titulo/audio/ep0X_sfx_mix.wav
```

**Volúmenes:**
- Narración: 0dB (intocable)
- Dark ambient pad (todo el vídeo): -32dB
- SFX puntuales: -16 a -20dB
- Música (Kevin MacLeod u otro): -24dB

**Reemplazar audio sin re-renderizar:**
```bash
ffmpeg -i ep0X_draft.mp4 -i ep0X_sfx_mix.wav \
  -c:v copy -c:a aac -b:a 192k \
  -map 0:v -map 1:a -shortest ep0X_final.mp4
```

**Música royalty-free:**
- Fesliyan Studios — gratis, sin atribución requerida
- YouTube Audio Library — filtrar Dark/Mysterious
- Kevin MacLeod — gratis pero requiere atribución CC BY 4.0

---

## FASE 11 — THUMBNAIL

**Estilo validado: documento filtrado / evidencia real** (NO ilustración genérica de OVNI).

```python
THUMB_PROMPT = (
    "blurry photocopy of an official document, typed text with redacted black bars, "
    "rubber stamp EVIDENCE or CLASSIFIED, 1980s paper texture, polaroid-style photograph "
    "embedded in document, authentic worn paper look, "
    "text reading 'BURNED ALIVE' in large typewriter font, "
    "dark vignette edges, high contrast, noir atmosphere"
)
```

```bash
python core/generar_imagen.py "prompt|thumbnail_v1.png" --out-dir ep0X_titulo/thumbnails
```

Generar 2-3 variantes antes de elegir.

---

## ESTRUCTURA DE CARPETAS (por episodio)

```
ep0X_titulo/
├── scripts/
│   ├── narration.txt              # guion limpio (solo texto, sin markdown)
│   └── narrator_element_id.txt   # ID del Reference Element del narrador
├── audio/
│   ├── ep0X_full.wav             # narración TTS
│   ├── ep0X_full.json            # Whisper word-level timestamps
│   └── ep0X_sfx_mix.wav          # narración + SFX + música
├── images/video/
│   ├── b1/  b2/  ... b9/         # imágenes por bloque
├── thumbnails/                    # variantes de thumbnail
├── videos/
│   ├── ep0X_draft.mp4            # draft con Ken Burns
│   └── ep0X_final.mp4            # con SFX mezclados
├── timing_maps.py                 # v1
└── timing_maps_v2.py              # v2 final (max 5s, sin duplicados)
```

---

## CHECKLIST YOUTUBE

- [ ] Vídeo montado — 0 pantallas negras
- [ ] Sync imagen-audio revisado en VLC
- [ ] Audio SFX mezclado (-24dB música, -16/-20dB SFX)
- [ ] Outro 10-15s (suscribirse + pregunta)
- [ ] Thumbnail generada (estilo documento)
- [ ] Título: "Can Anyone Explain What Happened at [CASO]?"
- [ ] Audiencia: "No, no está dirigido a niños"
- [ ] Toggle "Contenido alterado o sintético": ON
- [ ] Descripción con timestamps + fuentes + atribución música
- [ ] Kevin MacLeod (si se usa): atribución CC BY 4.0 OBLIGATORIA

---

## ANALIZAR VÍDEOS DE REFERENCIA

Cuando el usuario envíe un vídeo de referencia o quiera analizar el estilo de otro canal:

```
Skill: claude-video-vision:watch-video
```

Extraer y documentar:
- Ritmo de cambio de imágenes (segundos por imagen)
- Estilo visual (colores, paleta, ilustración vs real)
- Estructura narrativa (bloques, open loops, ganchos)
- Tono de voz y cadencia del narrador
- Uso de texto en pantalla
- Transiciones

Guardar análisis en `docs/referencia_[canal].md`.

---

## REGLAS ABSOLUTAS

1. **Imágenes:** SIEMPRE Playwright Unlimited. NUNCA MCP generate_image.
2. **Playwright:** `channel="chrome"`, `headless=False`, `keyboard.type` en chunks de 40 chars.
3. **Guion:** invocar skill `mystery-storytelling` ANTES de escribir.
4. **Naming imágenes:** keywords del transcript real, no descripción visual.
5. **S_ENV:** nunca incluir "oval face" para escenas sin personaje.
6. **Kevin MacLeod:** atribución CC BY 4.0 obligatoria en descripción YouTube.
7. **Idioma del vídeo:** inglés siempre (RPM $8-15 vs $1-3 en español).
