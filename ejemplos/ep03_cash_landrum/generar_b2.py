"""
EP03 Cash-Landrum — Bloque 2: EL ENCUENTRO (27 imágenes, 1:30–3:38)
Betty sale del coche, calor extremo, helicópteros aparecen.

Nota: los clips reales de CH-47 son opcionales.
Si no existen, el montaje usa negro automáticamente.

Uso:
  python ejemplos/ep03_cash_landrum/generar_b2.py
"""
import sys
from pathlib import Path

ROOT    = Path(__file__).parent.parent.parent
EP_DIR  = Path(__file__).parent
sys.path.insert(0, str(ROOT / "core"))
from generar_imagen import run

OUT_DIR = EP_DIR / "images/video/b2"
OUT_DIR.mkdir(parents=True, exist_ok=True)

ELEMENT_ID_FILE = EP_DIR / "scripts/narrator_element_id.txt"
ELEMENT_ID  = ELEMENT_ID_FILE.read_text().strip() if ELEMENT_ID_FILE.exists() else None
ELEMENT_REF = f"<<<{ELEMENT_ID}>>> " if ELEMENT_ID else ""

S = (
    "Bold flat illustration style, 2D cartoon, thick black outlines, "
    "dark navy blue background, orange accent colors, cinematic widescreen 16:9, "
    "no text, no words, no letters. "
)

JOBS = [
    (S + "Scene: intense heat waves rising from a dark road at night, "
     "orange glow from above illuminating everything, pine trees in background. "
     "An industrial furnace glow fills the frame — oppressive, suffocating heat. "
     "Flat illustration, wide shot.",
     "b2_001_heat_immediate_furnace.png"),

    (S + "Wide shot: the diamond-shaped UFO hovers above the road, massive orange flames "
     "shooting downward. Seen from the car windshield — two terrified faces reflected. "
     "Night sky, pine trees lit orange on both sides. Flat illustration.",
     "b2_001b_object_hovering_flames_car_view.png"),

    (S + "Interior back seat of a 1980s car at night. An older woman with gray hair "
     "holds a young boy of 7 tightly, eyes closed, lips moving in prayer. "
     "Both pressed against the seat, orange light flooding through windshield. "
     "Intimate, scared, flat illustration.",
     "b2_002_vickie_prays_holds_colby.png"),

    (S + "Interior car backseat: the boy's eyes are covered by an older woman's hand, "
     "shielding him from the light. Her other arm wraps around him protectively. "
     "Orange light floods in from outside. Flat illustration.",
     "b2_002b_colby_eyes_covered_vickie_shields.png"),

    (S + "A car door opening from inside — a woman's hand pushing it open, "
     "foot stepping onto dark road asphalt. Orange glow from above floods in. "
     "Low angle shot, dramatic lighting, flat illustration.",
     "b2_003_betty_opens_door_gets_out.png"),

    (S + "A woman in her 50s stands on the dark road, just stepped out. "
     "Her silhouette against the massive glowing UFO above. "
     "The car door still open behind her. Pine trees on both sides. Flat illustration.",
     "b2_003b_betty_steps_onto_road.png"),

    (S + "A woman in her 50s stands on a dark road looking up, one hand raised "
     "flat above her eyes to shield from intense light. "
     "Silhouetted against the massive glowing diamond-shaped object above. "
     "Wide shot, dramatic scale, flat illustration.",
     "b2_004_betty_standing_road_shielding_eyes.png"),

    (S + "Point of view looking up at the UFO — intense orange and white light "
     "shifts and pulses from the diamond-shaped object. "
     "The light is overwhelming, shifting, like looking at a welder's torch. "
     "Close-up of the light source, flat illustration.",
     "b2_005_light_intense_orange_white_shifting.png"),

    (S + "The blinding light shifts — orange to white to orange. "
     "The woman shields her eyes but cannot look away. "
     "The light pulsing, color shifting, hypnotic. Flat illustration.",
     "b2_005b_light_color_shift_blinding.png"),

    (S + "Extreme close-up of the UFO's metallic surface — brushed aluminum texture, "
     "reflecting orange and white light, perfectly smooth panels visible. "
     "Seams and rivets faintly visible. Alien but industrial. Flat illustration.",
     "b2_006_surface_metallic_brushed_aluminum.png"),

    (S + "Wide shot of a dark Texas road flanked by tall pine trees. "
     "The UFO fires a massive burst of flame downward — the pine trees on both sides "
     "are illuminated bright orange for hundreds of feet. Dramatic, cinematic. "
     "Flat illustration.",
     "b2_007_flame_bursts_pine_trees_illuminated.png"),

    (S + "Second flame burst — pine trees lit for hundreds of feet, massive scale. "
     "The entire road section glowing orange beneath the hovering object. "
     "Wide shot, dramatic. Flat illustration.",
     "b2_007b_second_burst_pine_trees_wide.png"),

    (S + "The UFO hangs still in the night sky — no movement. "
     "Heat radiates downward visibly as shimmer lines. "
     "Oppressive stillness. Flat illustration.",
     "b2_007c_object_still_heat_radiates_down.png"),

    (S + "Close-up of a woman's bare arm — the skin visibly red and burning, "
     "heat shimmer rising from the surface. She is not touching a fire. "
     "The damage comes from invisible radiation. Flat illustration, close-up.",
     "b2_008_skin_burning_radiation_heat.png"),

    (S + "Diagram: invisible radiation waves passing through a human body outline. "
     "Orange wave lines going through the silhouette — not stopping at the skin. "
     "Dark navy background, clinical and ominous. Flat illustration.",
     "b2_008b_radiation_heat_through_body.png"),

    (S + (ELEMENT_REF or "") +
     "The narrator character stands in the foreground, pointing at a diagram "
     "showing radiation waves passing through a human body. "
     "Dark navy background, orange wave lines. Explanatory pose. Flat illustration.",
     "b2_009_heat_goes_through_radiation.png"),

    (S + "Body absorbing invisible radiation — heat shimmer all around, "
     "the skin glowing faintly. The woman stands still, transfixed. "
     "Close-up on torso and arms. Flat illustration.",
     "b2_009b_heat_invisible_body_absorbing.png"),

    (S + "The rear door of a 1980s car opening from inside, a woman's arm reaching out "
     "calling toward someone outside. Orange light from above illuminates everything. "
     "Flat illustration, medium shot.",
     "b2_010_vickie_opens_door_calls_betty.png"),

    (S + "An older woman's arm reaching out from the car door, "
     "stretching toward the woman standing on the road. Desperate reach. "
     "Orange light everywhere. Flat illustration.",
     "b2_010b_vickie_arm_reaching_for_betty.png"),

    (S + "Extreme close-up of a woman's fingers touching a car door handle. "
     "The metal glowing hot orange — contact burns visible on the skin immediately. "
     "Pain in the recoil of the hand. Flat illustration.",
     "b2_011_door_handle_burns_fingers.png"),

    (S + "An older woman pulling another woman back into a car — "
     "both struggling, one being guided back through the car door. "
     "Urgency and fear in the motion. Orange light outside. Flat illustration.",
     "b2_012_vickie_pulls_betty_back_inside.png"),

    (S + "Interior of a 1980s car — two women sitting in the front seats, "
     "both staring through the windshield at the glowing UFO outside. "
     "Neither speaks. Twenty minutes of watching. Flat illustration.",
     "b2_013_twenty_minutes_watching_impossible.png"),

    (S + "The diamond-shaped UFO begins to move upward very slowly. "
     "The light changing as it rises. Pine trees below. "
     "The object ascending southeast, night sky around it. Flat illustration.",
     "b2_014_object_rises_slowly_vertical.png"),

    (S + "The UFO lifting vertically — the flame bursts below it stopping. "
     "The object ascending, lighter now, moving away. "
     "The road dark again below. Flat illustration.",
     "b2_014b_object_lifts_vertically_slow.png"),

    (S + "The UFO flame bursts have stopped. The object rises silently. "
     "The road below begins to go dark again as the glow fades. "
     "Trees returning to shadow. Flat illustration.",
     "b2_015_flame_bursts_stop.png"),

    (S + "Wide shot: the UFO now far southeast, fading. "
     "But in the dark sky: silhouettes of helicopters — many of them — "
     "surrounding the retreating object. Military formations visible. "
     "Flat illustration, wide dramatic shot.",
     "b2_024_not_chasing_escorting.png"),

    (S + "Interior of a 1980s car: two women in the front seats, "
     "both watching the sky through the windshield. "
     "Neither says a word. Stunned silence. "
     "The sky outside now dark except for fading helicopter shapes. Flat illustration.",
     "b2_026_betty_vickie_no_words.png"),
]

if __name__ == "__main__":
    existing = [j[1] for j in JOBS if (OUT_DIR / j[1]).exists()]
    pending  = [j for j in JOBS if not (OUT_DIR / j[1]).exists()]
    print(f"EP03 B2 — {len(pending)} pendientes, {len(existing)} ya existen")
    if pending:
        run(pending, OUT_DIR)
    print(f"\nB2 completo. Imágenes en: {OUT_DIR}")
