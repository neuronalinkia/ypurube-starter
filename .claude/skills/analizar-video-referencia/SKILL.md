---
name: analizar-video-referencia
description: Analiza un vídeo de YouTube de referencia y extrae su DNA narrativo completo — estructura, ritmo, ganchos, estilo visual, tono — para replicar la fórmula en un nuevo tema o nicho. Usa claude-video-vision para ver el vídeo frame a frame.
version: 1.0.0
---

# Analizar Vídeo de Referencia — Extracción de DNA Narrativo

Tu objetivo es diseccionar un vídeo de referencia hasta entender EXACTAMENTE por qué funciona, y producir un blueprint que permita replicar esa fórmula en un tema o nicho diferente.

No estás copiando el contenido. Estás copiando la ESTRUCTURA, el RITMO y los MECANISMOS de retención.

---

## PASO 1 — Ver el vídeo completo

```
Skill: claude-video-vision:watch-video
```

Si el usuario proporciona un archivo de vídeo local o URL, usa este plugin para procesarlo.
Si no tienes acceso al plugin, pide al usuario que pegue la transcripción o describe los primeros 5 minutos.

---

## PASO 2 — Extraer el DNA narrativo

Analiza y documenta EXACTAMENTE:

### 2A. GANCHO (primeros 60 segundos)

- **Técnica de apertura**: ¿In medias res? ¿Pregunta imposible? ¿Dato que rompe expectativas?
- **Primera frase**: Cópiala textualmente. ¿Qué tiene de especial?
- **Open loop plantado**: ¿Cuál es la pregunta que no se responde hasta el final?
- **Velocidad de información**: ¿Cuántos datos por minuto en el hook?
- **Segundos hasta primer gancho visual**: ¿Cuándo cambia la imagen por primera vez?

### 2B. ESTRUCTURA DE BLOQUES

Para cada bloque del vídeo (con timestamps):
```
[00:00-01:30] BLOQUE 1 — NOMBRE
  Función: qué hace narrativamente
  Técnica: qué mecanismo de retención usa
  Transición al siguiente: cómo conecta con el bloque 2
  Duración: Xs (~N% del vídeo total)
```

### 2C. RITMO VISUAL

- **Promedio de segundos por imagen/corte**: (total imágenes / duración)
- **En momentos de tensión alta**: X seg/imagen
- **En momentos de contexto/datos**: X seg/imagen
- **Transiciones**: fade / corte directo / zoom / ninguna
- **Estilo visual**: ilustración / imágenes reales / documentos / mixto
- **Paleta de colores dominante**: describir

### 2D. FÓRMULA DE RETENCIÓN

Detectar los mecanismos usados:
- [ ] Open loop (pregunta sin responder que obliga a seguir)
- [ ] Pattern interrupt (algo inesperado que resetea la atención)
- [ ] Progresión de información (cada dato lleva al siguiente)
- [ ] Contraste emocional (calma → tensión → calma → tensión)
- [ ] Dato + emoción (nunca solo datos, nunca solo emoción)
- [ ] Personaje identificable (el oyente se pone en su lugar)
- [ ] Reloj / cuenta atrás (urgencia narrativa)
- [ ] "Pero espera — hay más" (escalada constante)

### 2E. TONO Y VOZ

- **Tipo de narrador**: ¿Omnisciente? ¿Testigo? ¿Investigador?
- **Relación con el oyente**: ¿Formal? ¿Colega? ¿Mentor?
- **Vocabulario**: ¿Técnico? ¿Coloquial? ¿Periodístico?
- **Velocidad de habla**: ¿Dramáticas pausas? ¿Ritmo rápido?
- **Adjetivos usados**: listar los 5 más frecuentes
- **Frase más memorable**: la que resumiría todo el vídeo

### 2F. ESTRUCTURA DEL THUMBNAIL

- **Elemento principal**: foto de persona / objeto / texto / combinación
- **Texto visible**: cuántas palabras, qué dice exactamente
- **Color dominante**: y por qué llama la atención
- **Promesa implícita**: qué espera ver el viewer al hacer click

---

## PASO 3 — Blueprint para nuevo tema

Una vez extraído el DNA, crear el BLUEPRINT DE ADAPTACIÓN:

```
BLUEPRINT: [Nuevo tema] en estilo [Canal analizado]

GANCHO (adaptar al nuevo tema):
  Técnica a usar: [técnica identificada en el original]
  Primera frase propuesta: [adaptación al nuevo tema]
  Open loop propuesto: [la pregunta que no se responderá hasta el final]

ESTRUCTURA DE BLOQUES:
  [B1] [nombre] — [X min] — [técnica de retención del original]
  [B2] [nombre] — [X min] — [técnica]
  ...

RITMO VISUAL:
  Objetivo: X seg/imagen en tensión, Y seg/imagen en contexto
  Estilo: [misma paleta y estilo visual]
  Transiciones: [mismo tipo]

THUMBNAIL:
  Formato: [copiar estructura del original]
  Texto: [adaptar al nuevo tema]

DIFERENCIADOR:
  Qué hace el original que nadie más hace en este nicho:
  [detalle específico que hay que replicar exactamente]
```

---

## PASO 4 — Guardar análisis

Guardar en: `docs/referencia_[nombre_canal].md`

Formato del archivo:
```markdown
# Análisis: [Nombre del canal] — [Título del vídeo analizado]
Fecha: [fecha]
URL: [url si disponible]

## DNA Narrativo
[contenido completo del análisis]

## Blueprint para [nuevo tema]
[blueprint adaptado]

## Lo que copiamos exactamente
1. [elemento 1]
2. [elemento 2]
3. [elemento 3]
```

---

## PASO 5 — Ejecutar el pipeline con el blueprint

Una vez guardado el análisis, el siguiente paso es FASE 1 del pipeline:

```
Skill: mystery-storytelling
```

**Instrucción especial para mystery-storytelling cuando hay blueprint:**
> "Escribe el guion sobre [nuevo tema] siguiendo EXACTAMENTE la estructura del blueprint en docs/referencia_[canal].md. La técnica de gancho es [técnica]. El open loop es [open loop]. El ritmo de información es [ritmo]."

---

## Notas importantes

- **No copias el contenido** — copias la arquitectura
- **El estilo visual sí se copia** — es parte de la identidad del nicho
- **El tono sí se adapta** — el nuevo narrador tiene que sonar auténtico
- **Los datos NUNCA se inventan** — la investigación es tuya, la estructura es prestada
- **Crédito narrativo**: si alguien pregunta "¿por qué suenas como X canal?", la respuesta correcta es "porque X canal encontró una fórmula que funciona para este tipo de historia"
