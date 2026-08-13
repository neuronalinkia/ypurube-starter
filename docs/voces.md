# Guía de voces — qué usar y cuándo

## Flujo para elegir voz

```
1. Escucha las muestras → audio/kokoro_am_*.wav y audio/orpheus_*.wav
2. Elige la voz que encaje con el tono del episodio
3. Configura el script de audio correspondiente
4. Genera el episodio completo con esa voz
```

Para generar muestras de todas las voces de un motor:
```bash
python core/probar_voces.py --motor kokoro
python core/probar_voces.py --motor orpheus
```

---

## Opciones disponibles

### Kokoro TTS — Local, gratis, rápido

Instalación:
```bash
pip install kokoro soundfile numpy
```

| Voz | Carácter | Para qué sirve |
|-----|----------|---------------|
| **am_puck** | Oscuro, masculino, directo | **Default del canal. Misterios históricos.** |
| am_fenrir | Épico, intenso | Casos bélicos, conspiraciones |
| am_michael | Clásico documental | Estilo BBC/History Channel |
| am_onyx | Profundo, autoritario | Casos judiciales, crímenes |
| am_adam | Grave, formal | Tono académico/científico |
| am_echo | Suave, reflexivo | Historias más personales |
| am_eric | Neutro americano | Narración estándar |
| am_liam | Joven, energético | Casos modernos, tecnología |

Uso:
```bash
python core/generar_audio_kokoro.py \
  --guion ep01/scripts/narration.txt \
  --salida ep01/audio/ep01_full.wav \
  --voice am_puck \
  --speed 1.05
```

Parámetros:
- `--speed 1.05` → velocidad ligeramente más rápida (mejor retención)
- `--speed 1.0` → velocidad natural
- `--speed 0.95` → más lento, más dramático

---

### Miso One INT4 — Local, gratis, mayor calidad

Cuándo usarlo: cuando Kokoro suena plano y necesitas pausas dramáticas naturales.
El modelo varía cadencia y énfasis según el contexto — Kokoro no.

Instalación:
```bash
git clone https://github.com/MisoLabsAI/MisoTTS ~/Desktop/MisoTTS
cd ~/Desktop/MisoTTS && pip install -e .
# Descargar modelo INT4 (~4.5GB):
# https://huggingface.co/droyster/MisoTTS-8B-torchao-int4
```

VRAM necesaria:
- INT4: ~4.5 GB → cabe en cualquier GPU ≥6 GB
- FP8: ~9 GB → para GPUs ≥12 GB
- FP16: ~18 GB → no recomendado en GPU <24 GB

Uso:
```bash
python core/generar_audio_miso.py \
  --guion ep01/scripts/narration.txt \
  --salida ep01/audio/ep01_full.wav \
  --speaker 0
```

Voces:
- `--speaker 0` → masculina principal (más grave, documental)
- `--speaker 1` → masculina alternativa (más expresiva)

---

### Orpheus TTS — Local, gratis, voice cloning

Instalación:
```bash
pip install orpheus-tts
```

| Voz | Carácter |
|-----|----------|
| **leo** | Masculina profunda — recomendada para misterios |
| dan | Masculina neutra |
| tara | Femenina clara |
| leah | Femenina suave |
| jess | Femenina energética |
| mia | Femenina cálida |
| zac | Masculina joven |

Orpheus soporta **voice cloning** — puedes darle una muestra de audio de 10-30s
y generará en esa voz:
```python
from orpheus_tts import OrpheusModel
model = OrpheusModel(model_name="canopy-labs/orpheus-3b-0.1-ft")
# Usar voice cloning: pasar audio_prompt al generate_speech
```

---

### ElevenLabs — API de pago, máxima calidad

Cuándo usarlo: cuando necesitas la máxima calidad posible o voice cloning avanzado.
Precio: ~$5/mes para uso moderado.

Voces masculinas probadas (EN):
| ID | Carácter |
|----|----------|
| andrew | Narrador documental claro |
| brian | Grave, dramático |
| christopher | Formal, académico |
| eric | Neutro americano |
| guy | Energético, directo |
| roger | Profundo, maduro |
| steffan | Suave, reflexivo |

Instalación:
```bash
pip install elevenlabs
```

Uso básico:
```python
from elevenlabs.client import ElevenLabs
from elevenlabs import save

client = ElevenLabs(api_key="TU_API_KEY")  # guardar en .env como ELEVENLABS_API_KEY

audio = client.text_to_speech.convert(
    voice_id="nPczCjzI2devNBz1zQrb",  # Brian
    text="Your text here",
    model_id="eleven_multilingual_v2",
    voice_settings={"stability": 0.5, "similarity_boost": 0.75}
)
save(audio, "output.mp3")
```

Voice IDs validados:
```
andrew:      nPczCjzI2devNBz1zQrb  (aproximado — buscar en ElevenLabs)
brian:       nPczCjzI2devNBz1zQrb
christopher: (buscar en dashboard)
```
Buscar IDs exactos en: https://elevenlabs.io/voice-library

---

## Tabla de decisión

| Situación | Motor recomendado |
|-----------|-------------------|
| Episodio nuevo, primera prueba | Kokoro am_puck |
| El narrador suena plano/robótico | Miso One INT4 |
| Necesito pausas dramáticas naturales | Miso One INT4 |
| Necesito la máxima calidad para publicar | ElevenLabs |
| Quiero voice cloning con mi propia voz | Orpheus o ElevenLabs |
| Tengo menos de 6 GB VRAM | Kokoro (sin GPU extra) |

---

## Añadir al CLAUDE.md el motor elegido

Cuando elijas voz para un episodio, guardar la decisión en el episodio:
```
ep01_titulo/scripts/voz.txt
```
Contenido:
```
motor: kokoro
voz: am_puck
speed: 1.05
```

Así Claude puede reproducir exactamente la misma voz en correcciones o re-generaciones.
