# YouTube IA — Pipeline de producción de episodios

Canal de misterios históricos en inglés. Este repositorio contiene todos los scripts, herramientas y la metodología completa para producir un episodio de principio a fin.

---

## Requisitos de hardware

- **GPU:** NVIDIA RTX 4080 SUPER 16GB (o equivalente con ≥12GB VRAM)
- **OS:** Windows 10/11 (los scripts Playwright son específicos de este entorno)
- **Python:** 3.12 (no usar 3.13 ni 3.14 — incompatibilidad con dependencias de animación)
- **Chrome:** instalado en el sistema (no Playwright Chromium — crashea en este PC)

---

## Dependencias principales

```bash
# Python base
pip install playwright whisper-openai pydub kokoro torch torchvision torchaudio

# Playwright browsers (solo Chrome nativo, no Chromium)
playwright install  # no usar el Chromium descargado

# Real-ESRGAN (upscale 4K)
# Ver scripts/upscale_4k.py para instrucciones de instalación

# Miso One TTS (instalado en C:/Users/samuel/Desktop/MisoTTS/)
# Ver: https://github.com/MisoLabsAI/MisoTTS
# Instalar en INT4 — cabe en 16GB con margen
```

---

## Estructura de carpetas

```
ypurube-youtube-ia/
├── scripts/
│   ├── guiones/                    # guiones en .md por episodio
│   ├── generar_audio_ep0X.py       # TTS por episodio
│   ├── generar_ep0X_b1.py...b11.py # generación de imágenes por bloque
│   ├── generar_ep0X_all.py         # lanzar todos los bloques
│   ├── generar_ep0X_nuevas_imgs.py # imágenes adicionales para timing v2
│   ├── regenerar_ep0X_correcciones.py
│   ├── revisar_imagenes.py         # auditoría visual
│   ├── montar_ep0X_v2.py           # montaje final con Ken Burns
│   ├── mezclar_sfx_ep0X.py         # mezcla narración + SFX + música
│   └── upscale_4k.py
│
├── ep0X_titulo/
│   ├── audio/
│   │   ├── ep0X_v2_full.wav        # narración TTS
│   │   ├── ep0X_v2_full.json       # Whisper timestamps (word-level)
│   │   └── ep0X_sfx_mix.wav        # mezcla final con SFX y música
│   ├── images/video/
│   │   ├── b1/ b2/ ... b11/        # imágenes generadas por bloque
│   ├── real_assets/
│   │   ├── footage/
│   │   │   ├── original.mp4        # vídeo dominio público fuente
│   │   │   └── clips_ep0X/         # clips cortados 1376×768
│   │   └── cortar_video_real.py
│   ├── videos/
│   │   ├── ep0X_v2_draft.mp4       # draft con Ken Burns
│   │   └── tmp_v2/                 # clips temporales del montaje
│   ├── logs/
│   ├── timing_maps_b2_b11.py       # timing v1
│   └── timing_maps_b2_b11_v2.py   # timing v2 final (max 5s, sin duplicados)
│
├── audio/                          # muestras de voz y pruebas
├── images/                         # thumbnails y assets del canal
├── music/                          # música royalty-free
└── videos/                         # drafts y renders finales
```

---

## Pipeline completo — 11 fases

### FASE 1 — Guion

**Objetivo:** 18-20 minutos de narración (≈2.800-3.200 palabras)

- Idioma: **inglés** (canal en inglés — RPM $8-15)
- Tono: noir masculino, documental, sin condescendencia
- Estructura: **9 bloques narrativos** (ver abajo)
- Regla clave: **cada frase describe algo VISUAL y LITERAL** — el guion es también el plan de imágenes
- Usar la skill `mystery-storytelling` o `animal-behavior-script` en Claude Code para generar el guion
- Guardar en: `scripts/guiones/ep0X_titulo.md`

**Estructura de 9 bloques para misterios:**

| Bloque | Duración aprox. | Técnica |
|--------|-----------------|---------|
| B1 Cold open | 0:00–1:00 | In medias res — el momento más dramático primero |
| B2 Contexto | 1:00–3:00 | Quiénes eran, dónde, por qué importa. Open loop. |
| B3 La última vez | 3:00–6:00 | Últimos días documentados. Crear normalidad antes del quiebre. |
| B4 El descubrimiento | 6:00–10:00 | Detalle a detalle, en orden cronológico |
| B5 Explicación oficial | 10:00–12:00 | Presentarla con respeto, luego mostrar por qué no encaja |
| B6 Las teorías | 12:00–17:00 | Cada teoría como historia, no como lista |
| B7 El dato raro | 17:00–20:00 | El detalle que nadie menciona. Pregunta abierta. |
| B8 Zoom out | 20:00–22:00 | Por qué este caso importa más allá del misterio |
| B9 Cierre | 22:00–25:00 | Cerrar el open loop del cold open. Frase final. |

**Técnicas de storytelling:**
1. Open loop — abrir pregunta en B1-2 que no se responde hasta B7-8
2. Pero/Por tanto — en vez de "y entonces", usar tensión narrativa
3. In medias res — empezar en el pico dramático
4. Clue sequencing — revelar detalles uno a uno
5. Witness framing — narrar desde perspectiva del descubridor
6. Contraste normalidad/horror
7. Pregunta retórica sin respuesta — pausa — seguir

---

### FASE 2 — Audio (narración)

**Motor TTS recomendado:** Kokoro `am_puck`, speed=1.05 (local, gratis)
**Alternativa de mayor calidad:** Miso One INT4 (local, gratis — mejores pausas dramáticas)

```bash
# Kokoro
python scripts/generar_audio_ep0X.py

# Whisper — timestamps word-level (ESENCIAL para sync)
python -m whisper ep0X_titulo/audio/ep0X_v2_full.wav \
  --model large \
  --word_timestamps True \
  --output_format json \
  --language en
```

Output Whisper: `ep0X_titulo/audio/ep0X_v2_full.json`
Estructura: `data['segments'][i]['words']` → cada word tiene `start`, `end`, `word`

---

### FASE 3 — Generación de imágenes

#### REGLA CRÍTICA: SIEMPRE vía Playwright Unlimited

Las imágenes se generan **exclusivamente** vía Playwright controlando la web de Higgsfield con el toggle "Unlimited" activado. **Nunca** usar el MCP `generate_image` — descuenta créditos (~0,5-2 créditos/imagen). El modo Unlimited es ilimitado y gratuito.

**Reglas técnicas Playwright en este PC:**

| Parámetro | Valor correcto | Por qué |
|-----------|---------------|---------|
| `channel` | `"chrome"` | Playwright Chromium crashea (exitCode=2147483651) |
| `headless` | `False` | En headless el click al botón Generate no dispara la petición HTTP |
| Escritura del prompt | `page.keyboard.type(prompt, delay=6)` | `innerText`/`fill()` no actualiza el estado React |

**Script base:** `scripts/generar_imagen.py` — implementación validada.

**Style string (igual en todo el episodio):**
```python
S = ("Bold flat illustration style, 2D cartoon, thick black outlines, "
     "dark navy blue background, orange accent colors, cinematic widescreen 16:9, "
     "no text, no words, no letters. ")

# Para escenas SIN personaje (ambiente, objetos, paisajes)
S_ENV = ("Bold flat illustration style, 2D cartoon, thick black outlines, "
         "dark navy blue background, orange accent colors, cinematic widescreen 16:9, "
         "no text, no words, no letters. ")
# NOTA: S_ENV NO debe incluir "oval face" ni descripción facial — metería caras en paisajes
```

**Narrador (Reference Element):**
```python
ELEMENT_ID = "b9fc6c04-8156-43cd-851d-576c4ce29e59"  # ID del narrador EP03
ELEMENT_REF = f"<<<{ELEMENT_ID}>>> "
# Usar SOLO en prompts donde aparece el narrador. Para escenas de ambiente: NO usar.
```

**Naming de imágenes (CRÍTICO para sincronización Vexlo):**
- Formato: `b3_042_keywords_reales.png`
- Las keywords deben ser **palabras reales del transcript** en ese momento, no descripción visual
- MALO: `b3_042_lighthouse_dramatic_storm.png` (palabras visuales)
- BUENO: `b3_042_storm_rag_three_day.png` (palabras del transcript)

**Cantidad:** ≈1 imagen por concepto narrado → ≈130-160 imágenes iniciales para 19 min

**Reglas de prompts:**
- Literalidad absoluta: si el narrador dice "Betty gets out of the car" → Betty sale del coche
- Siempre especificar ángulo de cámara, plano y composición
- Para texto en imagen: especificar texto exacto, posición y estilo en el prompt

---

### FASE 4 — Auditoría de imágenes

Revisar ANTES de construir timing maps:

```bash
python scripts/revisar_imagenes.py
```

**Problemas comunes (10-15% de imágenes):**
- Narrador aparece donde debería ser ambiente → regenerar sin ELEMENT_REF
- Texto visible no deseado → añadir "no text, no words" más prominente
- Forma errónea → reescribir prompt con negaciones explícitas ("NOT round, NOT oval")
- Era equivocada → especificar año exacto en el prompt
- Imagen repetida del concepto anterior → reescribir desde otro ángulo

Script de correcciones: `scripts/regenerar_ep0X_correcciones.py`

---

### FASE 5 — Timing maps v1

Asignar timestamps exactos a cada imagen basándose en el JSON de Whisper.

**Estructura del timing map:**
```python
# ep0X_titulo/timing_maps_b2_b11.py
B2_MAP = [
    (45.2, 48.0, "b2/b2_001_arrive_island.png"),     # imagen estática
    (48.0, 52.5, CLIPS / "real_01_approach.mp4"),     # clip real (Path object)
]
```

**Proceso:**
1. Leer Whisper JSON → extraer timestamps de cada frase clave
2. Asignar imagen a cada rango temporal
3. Verificar cobertura completa: sin gaps >0.5s, sin solapamientos

---

### FASE 6 — Clips reales (footage documental)

**Límite:** máximo 20% de la duración total → evitar detección de copia
**Fuentes válidas:** dominio público, Creative Commons, Army.mil, archives.gov

```bash
# Analizar escenas del vídeo original
ffmpeg -vf "select='gt(scene,0.3)',showinfo" -vsync 0 original.mp4

# Cortar clip con ffmpeg
ffmpeg -i original.mp4 -ss 00:01:23 -t 8 -vf "scale=1376:768" -an -crf 18 clip_01.mp4
```

Integrar en timing maps como objetos `Path` (no strings).

---

### FASE 7 — Timing maps v2 (máximo 5s por imagen, sin duplicados)

**Problema a resolver:** timing v1 puede tener imágenes con duración >5s o imágenes duplicadas.

Analizar con un agente:
> "Lee timing_maps y Whisper JSON. Para cada segmento >5s, divide usando timestamps de Whisper. Para duplicados, crea prompts distintos. Escribe timing_maps_v2.py y generar_nuevas_imgs.py."

Resultado esperado: 0 segmentos >5s, 0 duplicados.
Nuevas imágenes necesarias: ≈1.4x respecto a las imágenes iniciales.

---

### FASE 8 — Imágenes adicionales

```bash
# Cerrar Chrome antes para evitar conflictos Playwright
taskkill //F //IM chrome.exe 2>nul
python -u scripts/generar_ep0X_nuevas_imgs.py 2>&1 | tee ep0X_titulo/logs/generar_nuevas.log
```

- El script salta automáticamente las imágenes que ya existen
- Si Higgsfield da TIMEOUT: relanzar, continúa desde donde paró
- Patrón típico: 2-3 rondas de 60-70 imágenes hasta completar

---

### FASE 9 — Montaje con Ken Burns

```bash
python scripts/montar_ep0X_v2.py
```

**Parámetros de render:**
- Resolución: 1376×768 (16:9)
- FPS: 24
- CRF: 22
- Preset: fast

**Ken Burns — filtro ffmpeg validado en Windows:**
```python
# CRÍTICO: escapar comas dentro de min() con \\,
z = f"min(zoom+{spd}\\,1.3)"
vf = f"scale={W*2}:{H*2},zoompan=z={z}:x={x}:y={y}:d={frames}:s={W}x{H},setsar=1"
# NO incluir fps= dentro del filtro zoompan — usar -r en la línea de comandos
```

4 modos alternos: zoom-in centro / pan L→R / zoom-in esquina / pan R→L
Fade to black entre bloques narrativos: 0.5s

**Tiempo estimado de render:** ~45-60 min para 19 min de vídeo (i9/RTX 4080)

---

### FASE 10 — Diseño de sonido

```bash
python scripts/mezclar_sfx_ep0X.py
```

**Volúmenes validados:**
| Pista | dB |
|-------|----|
| Narración | 0dB (no tocar) |
| Dark ambient pad (fondo) | -32dB |
| SFX puntuales | -16 a -20dB |
| Música Kevin MacLeod | -24dB |

**Reemplazar audio sin re-renderizar el vídeo:**
```bash
ffmpeg -i ep0X_v2_draft.mp4 -i ep0X_sfx_mix.wav \
  -c:v copy -c:a aac -b:a 192k \
  -map 0:v -map 1:a \
  -shortest ep0X_final.mp4
```

**Música royalty-free validada:**
- Fesliyan Studios — gratis para YouTube, sin atribución requerida
- YouTube Audio Library — filtrar Dark/Mysterious
- Kevin MacLeod (incompetech.com) — requiere atribución CC BY 4.0

---

### FASE 11 — Upscale 4K (solo versión final)

```bash
python scripts/upscale_4k.py
```

Real-ESRGAN con CUDA. ~2-4h por episodio de 19 min en RTX 4080 SUPER.
Solo para la versión final antes de publicar — no upscalear drafts.

---

## Metodología de sincronización Vexlo

La imagen cambia en el instante exacto en que la narración menciona el concepto.

**Principio:** el FILENAME de la imagen contiene palabras reales del transcript → el algoritmo busca cuándo se dicen esas palabras → coloca la imagen en ese momento.

### Stop words del algoritmo (no funcionan como keywords)
```
'the','a','an','and','or','of','in','on','at','to','for','is','it','its','as',
'from','with','by','not','no','one','two','three','did','has','had','was','were',
'all','island','lighthouse','men','man','sea','night','dark','light','day','days',
'time','back','out','into','came','went','found','know','knew','see','saw'
```
Los nombres de personajes también son stop words — usar palabras de sus acciones.

### Normalización automática de keywords
- `'raging'` → `'rag'`, `'entries'` → `'entri'`, `'disappeared'` → `'disappear'`
- Quita sufijos: ing, ers, ed, er, ly, es, s (solo si raíz ≥ 4 chars)

### Verificación pre-render
```bash
python ep0X/sincronizar_vexlo.py --dry-run
# Revisar vexlo_debug.txt — objetivo: 0 imágenes sin match
```

Si hay imágenes sin match: renombrarlas con keywords reales del transcript.

---

## Thumbnails

**Estilo validado:** documento filtrado / evidencia real — NO ilustración genérica.

Elementos del prompt:
```
"blurry photocopy", "typed text", "redacted black bars", "rubber stamp",
"polaroid-style photograph", "authentic document", "1980s paper texture"
```

- EP03 Cash-Landrum: informe médico + sello EVIDENCE/CLASSIFIED
- Adaptar al caso: telegrama, foto de época, documento naval, informe policial
- Máximo 3-4 palabras grandes + subtexto pequeño
- Generar 2-3 variantes antes de publicar

---

## Publicación en YouTube

### Checklist pre-subida

**Vídeo:**
- [ ] 0 pantallas negras (revisar en VLC)
- [ ] Sync imagen-audio revisado manualmente
- [ ] Audio SFX mezclado correctamente
- [ ] Outro 10-15s al final (suscripción + pregunta)
- [ ] Upscale 4K aplicado

**YouTube Studio:**
- [ ] Título con pregunta o misterio: `"Can Anyone Explain What Happened at..."`
- [ ] Thumbnail: estilo documento + texto impactante (máx 6 palabras)
- [ ] Audiencia: "No, no está dirigido a niños"
- [ ] Categoría: Entretenimiento o Educación
- [ ] Toggle **"Contenido alterado o sintético"**: ON (por precaución)
- [ ] Visibilidad: Privado → revisar → Público

**Descripción:**
- [ ] Timestamps de secciones (0:00 Intro, 1:00 Context...)
- [ ] Fuentes históricas al final
- [ ] Atribución Kevin MacLeod (OBLIGATORIA si se usa):
  ```
  Background music: "Ghost Story" by Kevin MacLeod
  Licensed under Creative Commons: By Attribution 4.0
  http://creativecommons.org/licenses/by/4.0/
  http://incompetech.com
  ```
- [ ] Si declaras AI: `"Some visuals in this video were created with AI image generation tools."`

**Tags:**
```
mystery, unsolved mystery, historical mystery, true crime, lighthouse,
disappearance, unexplained, history documentary, [nombre del caso], [año]
```

---

## Tiempos aproximados por episodio

| Fase | Tiempo |
|------|--------|
| Guion | 2-4h |
| TTS + Whisper | 30 min |
| Imágenes iniciales (~150) | 3-4h (Playwright) |
| Auditoría + correcciones | 1-2h |
| Timing maps v1 | 1h |
| Timing maps v2 + nuevas imgs | 2h + 3-4h (Playwright) |
| Montaje Ken Burns | 45-60 min |
| SFX + música | 30 min |
| Revisión final + ajustes | 1h |
| **TOTAL** | **~15-18h** |

---

## Checklist final

- [ ] Vídeo v2 montado — 0 pantallas negras
- [ ] Sync imagen-audio revisado en VLC
- [ ] Audio SFX mezclado (-24dB música, -16/-20dB SFX)
- [ ] Outro añadido
- [ ] Thumbnail generada (2-3 variantes, elegir la mejor)
- [ ] Upscale 4K aplicado
- [ ] Metadatos YouTube completos
- [ ] Toggle contenido sintético activado
- [ ] Atribución Kevin MacLeod en descripción
