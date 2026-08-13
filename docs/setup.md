# Setup desde cero — Requisitos y configuración

Todo lo que necesitas para producir el primer episodio completo.

---

## Requisitos del sistema

- **OS**: Windows 10/11 (el repo usa rutas Windows; Linux/Mac requiere ajustes menores en paths)
- **Python**: 3.10+ (`python --version`)
- **ffmpeg**: instalado y en PATH ([descargar](https://ffmpeg.org/download.html))
- **Google Chrome**: instalado (Playwright usa Chrome, no Chromium)
- **GPU (opcional)**: CUDA para Miso One TTS. Sin GPU, usar Kokoro (no necesita GPU).

---

## 1. Clonar el repo

```bash
git clone https://github.com/neuronalinkia/ypurube-starter.git
cd ypurube-starter
```

---

## 2. Instalar dependencias Python

```bash
pip install kokoro soundfile numpy pydub playwright whisper openai-whisper
python -m playwright install chromium  # para el fallback
```

Para Miso One TTS (calidad superior, requiere GPU ≥6GB VRAM):
```bash
# Clonar MisoTTS en tu escritorio
git clone https://github.com/MisoLabsAI/MisoTTS ~/Desktop/MisoTTS
cd ~/Desktop/MisoTTS && pip install -e .
# Descargar modelo INT4 (~4.5GB) desde HuggingFace:
# https://huggingface.co/droyster/MisoTTS-8B-torchao-int4
```

Para Orpheus TTS (voz profunda alternativa):
```bash
pip install orpheus-tts
```

Para diseño de sonido (mezclar_sfx.py):
```bash
pip install pydub numpy
# En Windows también: pip install pyaudio (para pydub con audio output)
```

---

## 3. Configurar Higgsfield Unlimited (imágenes gratis)

El script `core/generar_imagen.py` usa Playwright con tu sesión de Chrome para generar imágenes en Higgsfield Unlimited sin gastar créditos.

**Primera vez (una sola vez):**

```bash
# Abrir Chrome con el perfil dedicado
python -c "
from pathlib import Path
import subprocess
PROFILE = str(Path.home() / '.higgsfield-session')
subprocess.Popen(['chrome', f'--user-data-dir={PROFILE}', 'https://higgsfield.ai'])
"
```

1. En el navegador que se abre: crear cuenta en Higgsfield o hacer login
2. Activar plan Unlimited (verificar que tienes acceso a generación ilimitada)
3. Cerrar el navegador

A partir de ahí, `core/generar_imagen.py` reutiliza esa sesión automáticamente.

**Verificar que funciona:**
```bash
python core/generar_imagen.py "A dark road at night, flat illustration|test.png" --out-dir /tmp/test
```

---

## 4. Instalar el plugin claude-video-vision

Este plugin permite que Claude vea vídeos de YouTube directamente para analizar el estilo.

**Instalación en Claude Code:**
```bash
claude mcp add claude-video-vision
```

O añadir manualmente en `.mcp.json`:
```json
{
  "mcpServers": {
    "claude-video-vision": {
      "command": "npx",
      "args": ["-y", "@anthropic/claude-video-vision"]
    }
  }
}
```

**Verificar:**
- Abre Claude Code en este directorio
- Escribe: `Skill: analizar-video-referencia`
- Pega una URL de YouTube o sube un archivo MP4

---

## 5. Las skills del canal

Las skills están en `.claude/skills/` dentro del repo — Claude Code las detecta automáticamente al abrir el proyecto.

| Skill | Cuándo usarla |
|-------|--------------|
| `analizar-video-referencia` | Antes de escribir el primer guion — analiza el vídeo de referencia |
| `mystery-storytelling` | Para escribir cada guion nuevo |
| `viral-hooks-mystery` | Para auditar y mejorar el cold open |

**Invocar una skill:**
```
Skill: mystery-storytelling
```
O simplemente dile a Claude: "escribe el guion sobre [tema]" — detectará la skill automáticamente.

---

## 6. Instalar Whisper (para timestamps)

```bash
pip install openai-whisper
# Para el modelo large (mejor calidad):
whisper --model large audio.wav --word_timestamps True --output_format json --language en
```

El modelo `large` descarga ~2.9GB la primera vez. Después está cacheado.

---

## 7. Crear el narrador (Reference Element)

El narrador consistente en todas las imágenes usa un Reference Element de Higgsfield.

```bash
# 1. Genera o consigue una imagen de tu narrador (cualquier PNG)
# 2. Ejecuta:
python core/crear_elemento_ref.py
# Te pedirá la imagen y devolverá un element_id
# 3. Guarda el ID en cada episodio:
echo "element_id_aqui" > ep01_titulo/scripts/narrator_element_id.txt
```

---

## 8. Estructura de carpetas por episodio

Cada episodio vive en su propia carpeta:

```
ep01_titulo/
├── scripts/
│   ├── narration.txt              # guion limpio (solo texto, sin markdown)
│   ├── narrator_element_id.txt   # ID del Reference Element del narrador
│   └── voz.txt                   # motor:voz:speed elegidos
├── audio/
│   ├── ep01_full.wav             # narración TTS
│   ├── ep01_full.json            # Whisper word-level timestamps
│   └── ep01_sfx_mix.wav          # narración + SFX + música
├── images/video/
│   ├── b1/  b2/  ... b9/         # imágenes por bloque
├── thumbnails/
├── videos/
│   ├── ep01_draft.mp4
│   └── ep01_final.mp4
├── timing_maps.py
└── timing_maps_v2.py
```

Crear la estructura:
```bash
mkdir -p ep01_titulo/scripts ep01_titulo/audio ep01_titulo/images/video ep01_titulo/thumbnails ep01_titulo/videos
```

---

## 9. Checklist antes del primer episodio

- [ ] Python 3.10+ instalado (`python --version`)
- [ ] ffmpeg en PATH (`ffmpeg -version`)
- [ ] Google Chrome instalado
- [ ] Higgsfield: sesión creada y Unlimited activado
- [ ] `python core/generar_imagen.py "test|test.png" --out-dir /tmp` → genera imagen OK
- [ ] `python core/probar_voces.py --motor kokoro` → genera audio OK
- [ ] Plugin claude-video-vision instalado (para FASE 0)
- [ ] Whisper instalado (`whisper --help`)

---

## Problemas frecuentes

**"Playwright no dispara el click Generate"**
→ Verificar que `headless=False` en `generar_imagen.py`. En headless el DOM de React no responde.

**"Las imágenes salen con texto aunque puse no text"**
→ Mover "no text, no words, no letters" al INICIO del prompt, antes de la descripción visual.

**"Kokoro no genera audio"**
→ `pip install kokoro soundfile` y verificar que la voz existe: `am_puck`, `am_echo`, etc.

**"El montaje sale desincronizado"**
→ Los timestamps del timing_maps.py deben coincidir con el audio real. Extraer con Whisper, no estimar a mano.

**"ffmpeg: zoompan falla en Windows"**
→ Verificar que las comas en `min()` están escapadas con `\\,` y que no hay `fps=` dentro del filtro zoompan.
