"""
EP03 Cash-Landrum — Bloque 3: LOS SÍNTOMAS (20 imágenes, 3:31–5:49)
Las consecuencias físicas — radiación que destruyó tres vidas.

Uso:
  python ejemplos/ep03_cash_landrum/generar_b3.py
"""
import sys
from pathlib import Path

ROOT    = Path(__file__).parent.parent.parent
EP_DIR  = Path(__file__).parent
sys.path.insert(0, str(ROOT / "core"))
from generar_imagen import run

OUT_DIR = EP_DIR / "images/video/b3"
OUT_DIR.mkdir(parents=True, exist_ok=True)

S = (
    "Bold flat illustration style, 2D cartoon, thick black outlines, "
    "dark navy blue background, orange accent colors, cinematic widescreen 16:9, "
    "no text, no words, no letters. "
)

JOBS = [
    (S + "A woman in her 50s stands before a bathroom mirror, gripping the sink edge. "
     "Her face is visibly red and inflamed, skin tight and irritated under harsh bathroom light. "
     "Expression of alarm — something is wrong. Flat illustration.",
     "b3_001_betty_home_face_feels_tight.png"),

    (S + "Extreme close-up of human skin — forearm glowing bright crimson red, "
     "the color of a severe radiation sunburn. The redness is uniform, unnatural. "
     "No wound, no heat source visible — the damage comes from within. Flat illustration.",
     "b3_002_skin_bright_red_severe_sunburn.png"),

    (S + "Close-up medical view of facial skin and neck with multiple fluid-filled blisters "
     "forming on the surface — clusters of raised, translucent domes on red skin. "
     "Scalp visible at the top of frame with blisters at the hairline. Flat illustration.",
     "b3_003_blisters_forming_face_neck_scalp.png"),

    (S + "An open palm held horizontally — a large clump of dark hair rests in the hand. "
     "Not a few strands — a full fistful. More falling in the background. "
     "Expression of horror implied by the framing. Flat illustration, stark close-up.",
     "b3_004_hair_clumps_hand.png"),

    (S + "Extreme close-up of a face — both eyes swollen completely shut, "
     "lids puffy and purple-red, impossible to open. The swelling is severe. "
     "No visible white of eye — just inflamed sealed tissue. Flat illustration.",
     "b3_005_eyes_swell_shut_cannot_open.png"),

    (S + "A woman lying in a dark bedroom, visibly ill — pale, sweating, a metal bucket "
     "on the floor beside the bed. The clock on the nightstand shows late night. "
     "Through the window, dawn begins to break — she has been sick all night. Flat illustration.",
     "b3_006_vomiting_night_next_day.png"),

    (S + "A woman alone in bed, face contorted in pain, clutching her stomach. "
     "Darkness outside the window. Nobody else in the room. Flat illustration.",
     "b3_007_pain_constant.png"),

    (S + "Exterior: Parkway General Hospital exterior at night — a medium-sized hospital building, "
     "lights on inside, the emergency entrance visible. A car parked at the entrance. "
     "Flat illustration, establishing shot.",
     "b3_008_three_days_hospital_parkway.png"),

    (S + "An older woman with gray hair sits upright in a hospital bed, "
     "oxygen tube visible, IV drip attached to her arm. "
     "Expression of exhaustion and fear. Dark hospital room. Flat illustration.",
     "b3_009_vickie_same_symptoms.png"),

    (S + "A small boy (7 years old) with closed, swollen red eyes sits in a hospital chair. "
     "His eyes are visibly irritated and painful. A parent's hand rests on his shoulder. "
     "Flat illustration, intimate and sad.",
     "b3_010_colby_seven_red_swollen_eyes.png"),

    (S + "Two doctors in white coats examining a patient chart together, "
     "pointing at highlighted test results with expressions of concern. "
     "Hospital corridor in background. Flat illustration.",
     "b3_011_doctors_run_tests.png"),

    (S + "A medical test results page with a graph showing white blood cell count — "
     "the line drops sharply from normal to critically low. "
     "A red line marking the danger threshold is crossed dramatically. Flat illustration.",
     "b3_015_white_blood_cell_count_dropped.png"),

    (S + "A doctor's written report — close-up shows the diagnosis section. "
     "The words 'acute radiation exposure' clearly visible on the document. "
     "A rubber stamp with 'CONFIRMED' pressed on the diagnosis. Flat illustration.",
     "b3_012_ionizing_radiation_diagnosis.png"),

    (S + "Medical diagram: ionizing radiation waves penetrating through a human body outline. "
     "The waves pass through completely — not absorbed, not stopped at the skin. "
     "Orange arrows showing radiation pathway. Dark navy background. Flat illustration.",
     "b3_013_not_chemical_not_fire_radiation.png"),

    (S + "Diagram comparing radiation sources: a nuclear reactor on left, "
     "a nuclear warhead on right, both glowing. "
     "An equals sign pointing to: the type of radiation Burns were exposed to. "
     "Dark, ominous, flat illustration.",
     "b3_014_nuclear_reactor_nuclear_weapon.png"),

    (S + "A woman's name crossed out, then re-admitted on a hospital log book — "
     "multiple admission dates visible for the same patient within one year. "
     "The cycle of discharge and readmission visible as repeated entries. Flat illustration.",
     "b3_016_hospitalized_multiple_times_first_year.png"),

    (S + "A pile of medical billing envelopes on a kitchen table — many, mounting up. "
     "A calculator beside them, the total adding up to an impossible sum. "
     "Dark navy kitchen, orange lamp. Flat illustration.",
     "b3_017_medical_bills_hundred_thousand.png"),

    (S + "A teenage boy wearing sunglasses indoors, sitting at a school desk. "
     "His posture is guarded, eyes protected from normal light. "
     "Other students in background look normal. He looks different. Flat illustration.",
     "b3_018_colby_eye_problems_adolescence.png"),

    (S + "Three people — a woman in her 50s, an older woman, a small boy — "
     "each shown in their own hospital bed in a triptych frame. "
     "All connected by the same night, same road, same injuries. Flat illustration.",
     "b3_019_three_people_one_night_one_road.png"),

    (S + "A medical textbook open to a chapter on radiation injury. "
     "The symptoms listed: burns, hair loss, eye damage, immune suppression. "
     "Each symptom has a checkmark next to it. Flat illustration, close-up.",
     "b3_020_injuries_only_one_explanation.png"),
]

if __name__ == "__main__":
    existing = [j[1] for j in JOBS if (OUT_DIR / j[1]).exists()]
    pending  = [j for j in JOBS if not (OUT_DIR / j[1]).exists()]
    print(f"EP03 B3 — {len(pending)} pendientes, {len(existing)} ya existen")
    if pending:
        run(pending, OUT_DIR)
    print(f"\nB3 completo. Imágenes en: {OUT_DIR}")
