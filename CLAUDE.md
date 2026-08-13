# CLAUDE.md — Manual operativo del canal de YouTube

Este repositorio produce episodios de misterios históricos en inglés (~18 min) usando IA.
**Lee este fichero completo antes de hacer cualquier cosa.**

Setup inicial: ver `docs/setup.md`

---

## PIPELINE COMPLETO — orden obligatorio

```
FASE 0  → Analizar vídeo referencia  (skill analizar-video-referencia)
FASE 1  → Guion                      (skill mystery-storytelling + blueprint de FASE 0)
FASE 2  → Audio TTS                  (core/generar_audio_kokoro.py)
FASE 3  → Whisper timestamps         (comando whisper)
FASE 4  → Plan visual                (lista de imágenes con keywords del transcript)
FASE 5  → Generar imágenes           (core/generar_imagen.py via Playwright — SIEMPRE Unlimited)
FASE 6  → Auditoría imágenes         (revisar y regenerar malas)
FASE 7  → Timing maps                (asignar imagen → rango de tiempo)
FASE 8  → Sync Vexlo                 (core/sincronizar_vexlo.py)
FASE 9  → Montaje Ken Burns          (core/montar_episodio.py)
FASE 10 → Diseño de sonido           (core/mezclar_sfx.py)
FASE 11 → Thumbnail                  (core/generar_imagen.py con prompt de documento/evidencia)
```

**FASE 0 es obligatoria la primera vez.** El blueprint que genera alimenta FASE 1.
Si ya tienes un blueprint guardado en `docs/`, puedes saltar directamente a FASE 1.

---

## FASE 0 — ANALIZAR VÍDEO DE REFERENCIA

**Cuándo ejecutar:** Antes del primer episodio, o cuando quieras cambiar de estilo.

```
Skill: analizar-video-referencia
```

El usuario proporciona:
- Un archivo MP4 local, o
- Una URL de YouTube (requiere plugin `claude-video-vision`)

**Lo que extrae la skill:**
1. Estructura de bloques con timestamps
2. Técnica de gancho (in medias res, pregunta imposible, dato que rompe)
3. Ritmo visual (segundos por imagen en tensión vs contexto)
4. Mecanismos de retención usados
5. Tono y vocabulario del narrador
6. Formato del thumbnail

**Output:** `docs/referencia_[canal].md` — el blueprint que guía FASE 1.

**Para aplicar a un nicho diferente:**
El análisis detecta la FÓRMULA (estructura, ritmo, mecanismos) y la separa del CONTENIDO.
Puedes aplicar la fórmula de un canal de misterios históricos a true crime, ciencia, historia bélica, etc.

**Requiere plugin:**
```bash
claude mcp add claude-video-vision
```
Ver `docs/setup.md` para instalación completa.

---

## FASE 1 — GUION

**Invocar SIEMPRE la skill antes de escribir:**
```
Skill: mystery-storytelling
```

**Si hay blueprint de FASE 0:**
```
Skill: mystery-storytelling
[Pegar o referenciar el blueprint de docs/referencia_[canal].md]
Escribe el guion sobre [TEMA] siguiendo la estructura del blueprint.
```

**Estructura de 9 bloques:**
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
- Guardar en: `ep0X_titulo/scripts/narration.txt` (solo texto limpio, sin markdown)

**Auditar el cold open (GANCHO):**
```
Skill: viral-hooks-mystery
```
Pegar el bloque 1 del guion. La skill detecta los 4 patrones que matan el gancho y genera 3 variantes mejoradas.

---

## FASE 2 — AUDIO TTS

**Ver guía completa:** `docs/voces.md`

**Paso 0 — elegir voz (solo la primera vez):**
```bash
python core/probar_voces.py --motor kokoro    # escucha todas las voces Kokoro
python core/probar_voces.py --motor orpheus   # escucha todas las voces Orpheus
# Resultados en: audio/prueba_voces/
```

**Motores disponibles:**

| Motor | Calidad | Coste | VRAM | Cuándo usar |
|-------|---------|-------|------|-------------|
| Kokoro am_puck | Buena | Gratis | ~0 extra | Default — narración directa y clara |
| Miso One INT4 | Superior | Gratis | ~4.5 GB | Pausas dramáticas naturales, más expresivo |
| Orpheus leo | Buena | Gratis | ~8 GB | Alternativa masculina profunda |
| ElevenLabs | Máxima | ~$5/mes | 0 (API) | Producción final de calidad máxima |

**Generar audio (Kokoro — recomendado para empezar):**
```bash
python core/generar_audio_kokoro.py \
  --guion ep0X_titulo/scripts/narration.txt \
  --salida ep0X_titulo/audio/ep0X_full.wav \
  --voice am_puck \
  --speed 1.05
```

**Generar audio (Miso One — mayor calidad, mejor para misterios):**
```bash
python core/generar_audio_miso.py \
  --guion ep0X_titulo/scripts/narration.txt \
  --salida ep0X_titulo/audio/ep0X_full.wav \
  --speaker 0
```

- Ambos scripts generan chunk por chunk y son reanudables si se interrumpen
- Guardar la voz elegida en `ep0X_titulo/scripts/voz.txt` para reproducibilidad

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

**Ritmo visual:** usar el blueprint de FASE 0 como guía.
- Tensión alta: X seg/imagen (del análisis)
- Contexto/datos: Y seg/imagen (del análisis)

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

**Reglas técnicas Playwright (NO cambiar):**
- `channel="chrome"` — Playwright Chromium crashea en Windows
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

**Adaptar el style string al blueprint:**
Si el vídeo de referencia usa un estilo diferente (watercolor, realistic, noir sketch...),
ajustar el style string en base al análisis de FASE 0. El estilo visual es parte de la fórmula.

**Narrador (Reference Element):**
```python
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
Ver `ejemplos/ep03_cash_landrum/` para prompts reales de un episodio completo.
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

ALL_BLOCKS = [("B1", B1_MAP), ("B2", B2_MAP), ...]  # requerido por montar_episodio.py
```

**Proceso:**
1. Leer `ep0X_full.json` (Whisper) → extraer timestamps de frases clave
2. Asignar imagen a cada rango
3. Verificar: sin gaps >0.5s, sin duplicados, max 5s por imagen

Ver `ejemplos/ep03_cash_landrum/timing_maps.py` como referencia completa de los 11 bloques.

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
  --ep-dir ep0X_titulo \
  --timing ep0X_titulo/timing_maps.py \
  --audio  ep0X_titulo/audio/ep0X_full.wav \
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
# Genérico (dark pad + un hit orquestal):
python core/mezclar_sfx.py \
  --narration ep0X_titulo/audio/ep0X_full.wav \
  --output    ep0X_titulo/audio/ep0X_sfx_mix.wav

# Específico del episodio (importar core y definir build_sfx_map):
# Ver ejemplos/ep03_cash_landrum/mezclar_sfx.py
```

**Volúmenes:**
- Narración: 0dB (intocable)
- Dark ambient pad (todo el vídeo): -26dB
- SFX puntuales: -8 a -16dB
- Música (Kevin MacLeod u otro): -22dB

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

**Estilo validado: documento filtrado / evidencia real** (NO ilustración genérica).

```python
THUMB_PROMPT = (
    "blurry photocopy of an official document, typed text with redacted black bars, "
    "rubber stamp EVIDENCE or CLASSIFIED, 1980s paper texture, polaroid-style photograph "
    "embedded in document, authentic worn paper look, "
    "text reading 'BURNED ALIVE' in large typewriter font, "
    "dark vignette edges, high contrast, noir atmosphere"
)
```

**Adaptar el estilo del thumbnail al blueprint de FASE 0.**
Si el canal de referencia usa otro estilo (foto real, texto grande, sin texto...), replicarlo.

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
│   ├── narrator_element_id.txt   # ID del Reference Element del narrador
│   └── voz.txt                   # motor:voz:speed elegidos
├── audio/
│   ├── ep0X_full.wav             # narración TTS
│   ├── ep0X_full.json            # Whisper word-level timestamps
│   └── ep0X_sfx_mix.wav          # narración + SFX + música
├── images/video/
│   ├── b1/  b2/  ... b9/         # imágenes por bloque
├── thumbnails/
├── videos/
│   ├── ep0X_draft.mp4            # draft con Ken Burns
│   └── ep0X_final.mp4            # con SFX mezclados
├── timing_maps.py
└── timing_maps_v2.py
```

---

## SKILLS DISPONIBLES

| Skill | Invocar con | Cuándo |
|-------|-------------|--------|
| `analizar-video-referencia` | `Skill: analizar-video-referencia` | FASE 0 — analiza el vídeo y crea el blueprint |
| `mystery-storytelling` | `Skill: mystery-storytelling` | FASE 1 — escribe el guion |
| `viral-hooks-mystery` | `Skill: viral-hooks-mystery` | FASE 1 — audita y mejora el cold open |

Las skills están en `.claude/skills/` — Claude Code las detecta automáticamente.

---

## CHECKLIST YOUTUBE

- [ ] Vídeo montado — 0 pantallas negras
- [ ] Sync imagen-audio revisado en VLC
- [ ] Audio SFX mezclado (-22dB música, -16dB SFX)
- [ ] Outro 10-15s (suscribirse + pregunta)
- [ ] Thumbnail generada (estilo blueprint)
- [ ] Título: "Can Anyone Explain What Happened at [CASO]?"
- [ ] Audiencia: "No, no está dirigido a niños"
- [ ] Toggle "Contenido alterado o sintético": ON
- [ ] Descripción con timestamps + fuentes + atribución música
- [ ] Kevin MacLeod (si se usa): atribución CC BY 4.0 OBLIGATORIA

---

## ADAPTAR A OTRO NICHO

El pipeline completo funciona para cualquier nicho de YouTube largo, no solo misterios históricos.

**Para cambiar de nicho:**

1. **FASE 0**: Analizar 2-3 vídeos del nicho objetivo → blueprint con su fórmula
2. **FASE 1**: Reemplazar `mystery-storytelling` por la estructura del blueprint
3. **FASE 5**: Ajustar el style string según el estilo visual del nicho
4. **FASE 10**: Ajustar el diseño de sonido al tono del nicho
5. **FASE 11**: Ajustar el thumbnail al estilo del nicho

El resto del pipeline (TTS, Whisper, imágenes, Ken Burns, montaje) es 100% agnóstico al nicho.

---

## REGLAS ABSOLUTAS

1. **Imágenes:** SIEMPRE Playwright Unlimited. NUNCA MCP generate_image.
2. **Playwright:** `channel="chrome"`, `headless=False`, `keyboard.type` en chunks de 40 chars.
3. **Guion:** invocar skill `mystery-storytelling` ANTES de escribir.
4. **Naming imágenes:** keywords del transcript real, no descripción visual.
5. **S_ENV:** nunca incluir "oval face" para escenas sin personaje.
6. **Kevin MacLeod:** atribución CC BY 4.0 obligatoria en descripción YouTube.
7. **Idioma del vídeo:** inglés siempre (RPM $8-15 vs $1-3 en español).
8. **FASE 0 primero:** nunca escribir el primer guion sin haber analizado un vídeo de referencia.
