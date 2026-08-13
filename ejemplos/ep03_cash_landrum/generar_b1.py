"""
EP03 Cash-Landrum — Bloque 1: HOOK (18 imágenes, 0:00–1:30)
Texas road, cold night, UFO appears, flames, car stops.

Uso desde la raíz del repo:
  python ejemplos/ep03_cash_landrum/generar_b1.py
"""
import sys
from pathlib import Path

ROOT    = Path(__file__).parent.parent.parent   # raíz de ypurube-starter
EP_DIR  = Path(__file__).parent
sys.path.insert(0, str(ROOT / "core"))
from generar_imagen import run

OUT_DIR = EP_DIR / "images/video/b1"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Reference Element del narrador (crear con: python core/crear_elemento_ref.py)
# Guardar el ID en scripts/narrator_element_id.txt
ELEMENT_ID_FILE = EP_DIR / "scripts/narrator_element_id.txt"
ELEMENT_ID  = ELEMENT_ID_FILE.read_text().strip() if ELEMENT_ID_FILE.exists() else None
ELEMENT_REF = f"<<<{ELEMENT_ID}>>> " if ELEMENT_ID else ""

S = (
    "Bold flat illustration style, 2D cartoon, thick black outlines, "
    "dark navy blue background, orange accent colors, cinematic widescreen 16:9, "
    "no text, no words, no letters. "
)

# S_ENV para escenas sin personaje — NO incluye menciones de cara
S_ENV = S

JOBS = [
    (
        S_ENV +
        "Wide aerial bird's eye view of FM 1485, an empty two-lane Texas highway at night. "
        "No cars, no people, no figures. "
        "Dark asphalt road with dashed center line cuts straight through dense pine forest. "
        "Cold winter stars in dark navy sky above. "
        "Pine forest silhouettes on both sides of the road. "
        "Complete emptiness, total isolation. Flat illustration.",
        "b1_001_december_29_1980_texas_date.png"
    ),
    (
        S_ENV +
        "Wide shot of FM 1485, a narrow two-lane road cutting through southeast Texas at night. "
        "Tall pine forest on both sides, no streetlights, only moonlight casting faint blue light. "
        "The road disappears into darkness ahead. Isolated and quiet. Flat illustration.",
        "b1_002_two_lane_road_texas_night.png"
    ),
    (
        S_ENV +
        "Close-up of a vintage outdoor thermometer mounted on a wooden post, "
        "showing temperature just above freezing (40F). "
        "Frost crystals visible on the glass casing. "
        "Dark navy background with faint orange moonlight. Simple and stark.",
        "b1_003_cold_freezing_temperature.png"
    ),
    (
        S_ENV +
        "NIGHT SCENE. Interior view inside a 1980s American car. "
        "No city, no daylight, no sunshine, no buildings. "
        "A woman's two hands grip the large steering wheel. "
        "The dashboard glows dim green and orange. "
        "Through the dark windshield ahead: a narrow empty road at night, headlights on asphalt, pine trees on both sides. "
        "Dark interior, quiet, isolated. Flat illustration.",
        "b1_004_betty_cash_51_driving.png"
    ),
    (
        S_ENV +
        "Interior rear seat of a 1980s car at night. "
        "An older woman in her late 50s with gray hair sits against the window, wearing a winter coat. "
        "She looks forward slightly worried. Dark outside the windows. "
        "Warm interior lighting from dashboard reflects faintly. Flat illustration.",
        "b1_005_vickie_landrum_57_back_seat.png"
    ),
    (
        S_ENV +
        "Interior back seat of a 1980s car at night, right side. "
        "A young boy about 7 years old, wearing a jacket, eyes drooping almost asleep, "
        "head tilted slightly to the side. Very drowsy, peaceful expression. Dark night outside. "
        "Flat illustration, warm and intimate.",
        "b1_006_colby_seven_years_half_asleep.png"
    ),
    (
        S_ENV +
        "Wide shot: FM 1485, a narrow two-lane highway through dense pine forest. "
        "The highway stretches straight ahead, pine silhouettes tall on both sides, "
        "no streetlights, no other vehicles, just the dark road and dark sky. "
        "Extremely isolated and atmospheric. Flat illustration.",
        "b1_007_fm1485_highway_pine_forest.png"
    ),
    (
        S_ENV +
        "Pitch black Texas night road. "
        "Only two headlight beams visible — twin cones of white-orange light cutting forward through total darkness. "
        "Road asphalt barely visible within the light cones, pine tree silhouettes at the edge of the beams. "
        "Absolute blackness everywhere else. No streetlights, no buildings, no other objects. "
        "Minimalist, tense, isolating. Flat illustration.",
        "b1_008_no_streetlights_headlights_only.png"
    ),
    (
        S + (ELEMENT_REF or "") +
        "Wide shot: the narrator character stands on the left side of a dark two-lane Texas road, "
        "facing the viewer. One hand extended pointing ahead down the empty road into the darkness. "
        "Pine tree silhouettes frame the sides. Moonlight above. "
        "Confident, knowing stance. Flat illustration.",
        "b1_009_betty_knows_this_road.png"
    ),
    (
        S_ENV +
        "Close-up of a 1980s car dashboard clock showing 9:00 PM. "
        "The analog clock face illuminated in green dashboard light. "
        "Slightly blurry background of windshield and dark road ahead. "
        "Simple and ominous. Flat illustration.",
        "b1_010_nine_pm_something_above_road.png"
    ),
    (
        S_ENV +
        "Dark Texas road at night, pine trees on both sides. "
        "In the sky above the road, a bright glowing object hovers — clearly not a star, "
        "not a plane — emitting orange-white light. No flames yet, just hovering, glowing. "
        "The scale is impressive — larger than a car. Mysterious. Flat illustration.",
        "b1_011_not_stars_not_plane_hovering.png"
    ),
    (
        S_ENV +
        "Wide shot: FM 1485 at night. Above the road, a large diamond-shaped metallic object hovers. "
        "Its size is massive — comparable to a water tower. "
        "The object glows orange and white, silhouettes of pine trees on both sides. "
        "A small car on the road below shows the enormous scale difference. "
        "Dramatic and ominous. Flat illustration.",
        "b1_012_diamond_shaped_water_tower_size.png"
    ),
    (
        S_ENV +
        "Interior of a 1980s car: a woman's foot pressing the brake pedal, "
        "the car decelerating. Dashboard shows brake light indicator. "
        "Through the windshield in the distance: the glowing UFO object hovering. "
        "Tension visible in the foot pressure. Flat illustration.",
        "b1_013_betty_slows_car.png"
    ),
    (
        S_ENV +
        "Wide shot of FM 1485 at night. The diamond-shaped UFO hovers "
        "approximately 130 feet above the road center. "
        "Visual scale reference: pine trees (50-60 ft tall) below the object show the height. "
        "The object dwarfs everything. Orange-white glow illuminates the road below. "
        "Flat illustration, dramatic composition.",
        "b1_014_ufo_130_feet_above_road_stationary.png"
    ),
    (
        S_ENV +
        "The diamond-shaped UFO base: bright orange and red flames burst downward "
        "from the bottom of the object in powerful jets. "
        "The flame bursts are intense and directional. "
        "Dark navy sky, the object itself metallic and massive above. "
        "Dramatic upward angle, flat illustration.",
        "b1_015_flames_bursts_downward_base.png"
    ),
    (
        S_ENV +
        "Close-up of Texas asphalt road surface at night. "
        "Orange flame impacts the road — heat shimmer and dissipating flame on the asphalt. "
        "The flame hits and spreads outward briefly before disappearing. "
        "UFO glow visible from above. Dramatic close-up. Flat illustration.",
        "b1_016_flames_hit_road_dissipate.png"
    ),
    (
        S_ENV +
        "Wide shot: FM 1485 at night. A 1980s American sedan completely stopped "
        "in the center of the road, headlights still on. "
        "The massive glowing diamond UFO hovers ahead, illuminating the car in orange light. "
        "No other vehicles. The car is tiny compared to the object. Flat illustration.",
        "b1_017_betty_stops_car_completely.png"
    ),
    (
        S_ENV +
        "Interior close-up: a woman's hand reaching toward the car radio dial, "
        "turning it off. The dashboard radio display goes dark. "
        "Outside the windshield: the UFO glow visible. Silence implied by the gesture. "
        "Flat illustration, intimate moment.",
        "b1_018_turns_off_radio_silence.png"
    ),
]

if __name__ == "__main__":
    existing = [j[1] for j in JOBS if (OUT_DIR / j[1]).exists()]
    pending  = [j for j in JOBS if not (OUT_DIR / j[1]).exists()]
    print(f"EP03 B1 — {len(pending)} pendientes, {len(existing)} ya existen")
    if ELEMENT_ID:
        print(f"Reference Element: {ELEMENT_ID[:12]}...")
    else:
        print("AVISO: sin narrator_element_id.txt — imágenes con narrador sin personaje consistente")
    if pending:
        run(pending, OUT_DIR)
    print(f"\nB1 completo. Imágenes en: {OUT_DIR}")
