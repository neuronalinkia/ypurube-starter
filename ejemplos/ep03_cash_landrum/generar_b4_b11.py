"""
EP03 Cash-Landrum — Bloques 4-11: Investigación, Bases militares, Demanda, Documentos,
Helicópteros, Betty el resto de su vida, Lo que sabemos, FM 1485 hoy.

Este script genera todas las imágenes de B4 a B11 en secuencia.
B1, B2, B3 están en scripts separados por volumen.

Uso:
  python ejemplos/ep03_cash_landrum/generar_b4_b11.py
  python ejemplos/ep03_cash_landrum/generar_b4_b11.py --block b5   # solo un bloque
"""
import sys
import argparse
from pathlib import Path

ROOT    = Path(__file__).parent.parent.parent
EP_DIR  = Path(__file__).parent
sys.path.insert(0, str(ROOT / "core"))
from generar_imagen import run

ELEMENT_ID_FILE = EP_DIR / "scripts/narrator_element_id.txt"
ELEMENT_ID  = ELEMENT_ID_FILE.read_text().strip() if ELEMENT_ID_FILE.exists() else None
ELEMENT_REF = f"<<<{ELEMENT_ID}>>> " if ELEMENT_ID else ""

S = (
    "Bold flat illustration style, 2D cartoon, thick black outlines, "
    "dark navy blue background, orange accent colors, cinematic widescreen 16:9, "
    "no text, no words, no letters. "
)


# ─────────────────────────────────────────────────────────────────────────────
# B4 — INVESTIGACIÓN SCHUESSLER  (~5:49–7:43)
# ─────────────────────────────────────────────────────────────────────────────
B4 = [
    (S + "A serious man in his 40s sits at a large engineering desk covered in technical blueprints. "
     "Behind him on the wall: rocket schematics, trajectory diagrams. "
     "He wears a white button shirt — an engineer, not a bureaucrat. Flat illustration.",
     "b4_001_schuessler_aerospace_engineer_nasa.png"),

    (S + "A man's hands open a thick manila folder on a desk — inside, case files with photographs, "
     "handwritten notes, a MUFON emblem visible on the cover sheet. "
     "The files look well-worn, carefully organized. Dark navy desk, orange lamp light. Flat illustration.",
     "b4_002_mufon_investigates_ufo_cases.png"),

    (S + "A sedan driving down a long flat Texas highway toward a small town on the horizon. "
     "The road is straight and empty, flanked by pine trees. "
     "Daytime, the town sign ahead indistinct. Flat illustration, wide shot from behind the car.",
     "b4_003_schuessler_drives_huffman_texas.png"),

    (S + "Split panel: three separate interview scenes side by side — "
     "left: a man with a notepad interviewing a woman in her 50s; "
     "center: same man with an older woman; right: same man with a young boy. "
     "All three scenes focused and methodical. Flat illustration.",
     "b4_004_interviews_betty_vickie_colby_separately.png"),

    (S + (ELEMENT_REF or "") + "The narrator character holds a clipboard with a long checklist, "
     "posture straight and precise — like an engineer running a systematic test. "
     "Dark background, flat illustration.",
     "b4_005_engineer_approach_methodology.png"),

    (S + "Three documents laid side by side on a dark surface — each representing one witness account. "
     "Each document has a large orange checkmark at the bottom. "
     "All three checkmarks visible at once — perfect corroboration. Flat illustration, top-down.",
     "b4_006_no_inconsistencies_accounts_match.png"),

    (S + "A man carefully placing photographs, medical records, and hospital bills "
     "into a thick case file. His hands are precise and methodical. "
     "The file is growing very thick. Flat illustration.",
     "b4_007_collecting_medical_records_photos.png"),

    (S + "Multiple witness statements arriving in the mail — envelopes opened, "
     "letters laid out on a table. More corroborating accounts. "
     "An expanding case. Flat illustration.",
     "b4_008_other_witnesses_emerge.png"),

    (S + "An elderly married couple being interviewed together at their kitchen table. "
     "The man and woman are describing something serious to a man taking notes. "
     "Their expressions are earnest and consistent. Flat illustration.",
     "b4_009_married_couple_nearby_road.png"),

    (S + "A highway map of Texas with five red pins placed at different locations "
     "around the Houston area — each pin representing an independent witness. "
     "The pins form a rough pattern around FM 1485. Flat illustration.",
     "b4_013_five_independent_witnesses.png"),

    (S + "A very thick case file — the spine reads '700 PAGES'. "
     "Stacked beside it: photograph prints, hospital bills, correspondence. "
     "The sheer volume is overwhelming. Flat illustration.",
     "b4_014_seven_hundred_pages_documentation.png"),

    (S + "A map of Texas with question marks over three major military installations: "
     "Fort Hood (Killeen), Ellington Field (Houston), Bergstrom AFB (Austin). "
     "The question is: which base launched 23 helicopters? Flat illustration.",
     "b4_018_cannot_appear_without_paper_trail.png"),
]


# ─────────────────────────────────────────────────────────────────────────────
# B5 — LAS BASES MILITARES  (~7:43–9:42)
# ─────────────────────────────────────────────────────────────────────────────
B5 = [
    (S + "23 dark helicopter silhouettes arranged in a formation in the night sky. "
     "Each is a CH-47 Chinook shape — massive, twin-rotor. "
     "The question hangs in the air: where did they come from? Flat illustration.",
     "b5_010_23_chinooks_cannot_appear_sky.png"),

    (S + "Aerial view of Fort Hood — a massive military installation spread across Texas flatlands. "
     "'FORT HOOD — LARGEST ACTIVE DUTY POST IN THE US' label. "
     "Enormous scale, dozens of buildings, hangars, airfields. Flat illustration.",
     "b5_002_fort_hood_killeen_largest_base.png"),

    (S + "Close-up of a CH-47 Chinook helicopter — massive scale shown by a human figure beside it. "
     "The helicopter is 60 feet long, two stories tall. Flat illustration.",
     "b5_002b_chinook_sixty_feet_long.png"),

    (S + "A formal letter being written — addressed to 'Commander, Fort Hood, Killeen TX'. "
     "The subject line: 'Flight Activity December 29, 1980'. "
     "The letter is professional, methodical, urgent. Flat illustration.",
     "b5_001_schuessler_writes_military_installations.png"),

    (S + "Ellington Field, Houston — a military airfield near NASA's Johnson Space Center. "
     "F-4 jets and transport helicopters visible on the tarmac. "
     "The installation looks official and well-staffed. Flat illustration.",
     "b5_003_ellington_field_houston_air_guard.png"),

    (S + "Bergstrom Air Force Base, Austin — another military installation on a Texas map. "
     "Chinook helicopters visible in hangars. Flat illustration.",
     "b5_004_bergstrom_austin_red_river.png"),

    (S + "A stack of response letters from military installations — each showing NO RECORD. "
     "Each letter has an official letterhead and the same devastating response: "
     "'No flight activity recorded for the date in question.' Flat illustration.",
     "b5_006_no_record_flight_activity.png"),

    (S + "An empty military flight log for December 29, 1980 — all fields blank. "
     "The date is circled in orange. No entries. Nothing. Flat illustration.",
     "b5_007_not_classified_simply_no_record.png"),

    (S + "A series of official letters from Army, Defense, and FAA — "
     "each stamped with the same response: NO RECORD. "
     "An escalating wall of denial from all agencies. Flat illustration.",
     "b5_008_department_army_defense_faa.png"),

    (S + "A logistics diagram for a military helicopter operation: "
     "fuel trucks, maintenance crews, ground personnel, air traffic coordination. "
     "All the support required for 23 helicopters to fly — "
     "people who would know. Flat illustration.",
     "b5_010c_maintenance_crews_fuel_trucks.png"),

    (S + "A paper trail — official documents connected by lines — suddenly ending. "
     "The last document in the chain is redacted entirely. "
     "Beyond it: just darkness. A trail that was deliberately cut. Flat illustration.",
     "b5_009_paper_trail_intentionally_removed.png"),
]


# ─────────────────────────────────────────────────────────────────────────────
# B6 — LA DEMANDA  (~9:42–12:49)
# ─────────────────────────────────────────────────────────────────────────────
B6 = [
    (S + "A Texas map with five scattered witness location markers — "
     "all surrounding FM 1485 on the night of December 29, 1980. "
     "Five independent dots. Same event. Flat illustration.",
     "b6_014b_jerry_mcdonald_dayton_texas.png"),

    (S + "Betty Cash and Vickie Landrum sitting across from a lawyer at a desk in 1981. "
     "Legal documents on the table between them. Serious expressions. "
     "The lawyer holds a pen ready. Flat illustration.",
     "b6_001_betty_vickie_hire_lawyer_1981.png"),

    (S + "Exterior of a federal courthouse in Houston — stone steps, classical columns. "
     "Two women climbing the steps with their lawyer. "
     "The American flag above the entrance. Flat illustration.",
     "b6_002_lawsuit_federal_court_houston.png"),

    (S + "A legal brief cover page: 'CASH et al. v. UNITED STATES' "
     "Filed in United States District Court, Southern District of Texas. "
     "Official document on dark surface. Flat illustration.",
     "b6_004_legal_argument_government_aircraft.png"),

    (S + "A dollar figure — $20,000,000 — displayed prominently against dark background. "
     "Beneath it: the simple legal argument — government aircraft caused documented harm. "
     "Flat illustration.",
     "b6_003_twenty_million_dollars_damages.png"),

    (S + "A lawyer presenting thick medical files to a federal judge. "
     "Evidence boxes visible: medical records, photographs, witness statements. "
     "700 pages of documentation in the courtroom. Flat illustration.",
     "b6_005_lawyer_presents_medical_evidence.png"),

    (S + "Department of Defense official response letter — "
     "a single paragraph stating no matching aircraft exists in US military. "
     "The text is formal, impersonal, final. Dark background. Flat illustration.",
     "b6_006_dod_responds_single_argument.png"),

    (S + "A military aircraft inventory display — rows of aircraft types. "
     "None of them matches the diamond shape from the incident. "
     "'NO MATCH' highlighted in orange. Flat illustration.",
     "b6_007_no_such_aircraft_no_such_helicopters.png"),

    (S + "A federal judge's gavel slamming down — 1986. "
     "The courtroom reacts. 'CASE DISMISSED' stamped in orange "
     "on the case file in the foreground. Flat illustration.",
     "b6_008_1986_federal_court_dismisses.png"),

    (S + "The court ruling text — close-up of the key sentence: "
     "'Plaintiffs have failed to identify the specific agency or aircraft responsible.' "
     "The sentence is underlined. Flat illustration.",
     "b6_009_ruling_failed_to_identify_agency.png"),

    (S + (ELEMENT_REF or "") + "The narrator character stands pointing at a legal document, "
     "his expression serious. He points to what the ruling actually says — "
     "and what it doesn't. Not 'it didn't happen'. Just: you can't name who. Flat illustration.",
     "b6_010_not_aircraft_didnt_exist.png"),

    (S + "Betty and Vickie leaving the courthouse — no compensation, no acknowledgment. "
     "Their backs to the camera, walking down the stone steps. "
     "The courthouse door closed behind them. Flat illustration.",
     "b6_011_betty_vickie_leave_courthouse.png"),
]


# ─────────────────────────────────────────────────────────────────────────────
# B7 — LOS DOCUMENTOS / DESCRIPCIÓN OVNI  (~12:49–14:28)
# ─────────────────────────────────────────────────────────────────────────────
B7 = [
    (S + "A U.S. Senator's letterhead — a formal letter sent to the Department of Defense "
     "demanding a full explanation of the Cash-Landrum incident. "
     "Official, serious, urgent. Flat illustration.",
     "b7_001_senators_letters_department_defense.png"),

    (S + "Department of Defense response letter — large sections blacked out with redaction bars. "
     "Only fragments visible: dates, locations obscured. "
     "Official stamp below. Flat illustration, disturbing.",
     "b7_002_dod_responses_redacted.png"),

    (S + "Texas Department of Health investigators in radiation suits measuring readings "
     "at an empty section of Texas road at night. "
     "Their instruments indicate elevated radiation. Flat illustration.",
     "b7_003_texas_health_radiation_investigation.png"),

    (S + "A radiation meter reading elevated levels — the needle pushed into the orange zone. "
     "GPS coordinates of FM 1485 shown. "
     "Elevated radiation. The exact spot Betty identified. Flat illustration.",
     "b7_004_elevated_readings_exact_spot.png"),

    (S + "The official witness drawing of the UFO — a diamond/pyramid shape, "
     "metallic surface, flame jets from the base. "
     "This is the only official documented illustration. Drawn from Betty's description. "
     "Flat illustration.",
     "b7_005_official_illustration_betty_description.png"),

    (S + "An aircraft identification chart — all known US military aircraft types shown. "
     "The diamond shape from the incident is placed beside them. "
     "No match found. Flat illustration.",
     "b7_006_matches_no_known_aircraft.png"),

    (S + "A diagram of a nuclear-powered experimental aircraft concept: "
     "diamond shape, nuclear reactor providing lift, intense heat radiation as byproduct. "
     "Theoretical but matching. Dark navy background. Flat illustration.",
     "b7_007_nuclear_powered_test_vehicle_theory.png"),

    (S + "A classified government program file — most details redacted. "
     "'PROJECT [REDACTED]' visible on cover. "
     "'STATUS: DECLASSIFIED (PARTIAL)' stamp. Flat illustration.",
     "b7_008_no_program_declassified_matches.png"),
]


# ─────────────────────────────────────────────────────────────────────────────
# B8 — PROGRAMAS SECRETOS / ESCOLTA  (~14:28–16:34)
# ─────────────────────────────────────────────────────────────────────────────
B8 = [
    (S + "23 CH-47 Chinook helicopters in tight formation surrounding a glowing object. "
     "Not chasing — surrounding, escorting. Moving together southeast. "
     "This is organized, coordinated, deliberate. Flat illustration.",
     "b8_001_organized_equipped_escorted.png"),

    (S + "A map of Texas: Fort Hood, Ellington Field, Bergstrom. "
     "Lines showing the 200-mile radius around Huffman, Texas. "
     "All three major Chinook bases within range. Flat illustration.",
     "b8_002_fort_hood_200_miles_chinook.png"),

    (S + "Two parallel documents side by side: "
     "left: empty flight log for December 29, 1980. "
     "right: a massive Chinook operation that would require extensive documentation. "
     "The contrast is stark. Flat illustration.",
     "b8_003_records_existed_were_destroyed.png"),

    (S + "A truck driver on Highway I-45, stopped at a rest area, looking up at the sky. "
     "In the distance: a large formation of helicopters heading south. "
     "He has no reason to make this up. Flat illustration.",
     "b8_004_truck_driver_helicopters_south.png"),

    (S + "A timeline — the truck driver's sighting: same night, same helicopters, heading south. "
     "Direction matched Betty's account. Timing matched. "
     "Independent confirmation from a stranger on a road. Flat illustration.",
     "b8_005_direction_matched_timing_matched.png"),

    (S + (ELEMENT_REF or "") + "The narrator character stands before two open options on a chalkboard: "
     "'OPTION A: Flew without filing records — illegal.' "
     "'OPTION B: Records existed and were destroyed.' "
     "Both options are circled. Neither is good. Flat illustration.",
     "b8_006_two_explanations_neither_good.png"),

    (S + "Someone was watching those helicopters. Multiple people saw them. "
     "A web diagram connecting witnesses, installations, the object. "
     "At the center: the question that was never answered. Flat illustration.",
     "b8_007_someone_knew_helicopters_were_there.png"),
]


# ─────────────────────────────────────────────────────────────────────────────
# B9 — BETTY EL RESTO DE SU VIDA  (~16:34–17:37)
# ─────────────────────────────────────────────────────────────────────────────
B9 = [
    (S + "Betty Cash in a hospital chemotherapy ward — older now, mid-60s. "
     "She sits in a treatment chair, IV in her arm. "
     "She has been fighting cancer for years. Flat illustration.",
     "b9_001_betty_cancer_immune_disorders.png"),

    (S + "A calendar showing years passing — 1981, 1985, 1990, 1995. "
     "Each year marked with a hospital cross symbol. "
     "The health problems never stop. Flat illustration.",
     "b9_002_cancer_treatments_years.png"),

    (S + "Vickie Landrum in an interview setting — older, frail, determined. "
     "She is speaking clearly. Her story has never changed. "
     "This is her testimonial, not her confession. Flat illustration.",
     "b9_003_vickie_interviews_never_changed_story.png"),

    (S + "Colby — now an adult man in his 30s — speaking to someone off-camera. "
     "His expression is serious, certain. He has never changed his story either. "
     "From back seat at age 7 to adult testimony. Flat illustration.",
     "b9_004_colby_adult_back_seat_never_changed.png"),

    (S + "A tombstone: Betty Cash, born 1931, died December 29, 1998. "
     "The death date — exactly 18 years after the incident. "
     "Dark sky, sparse cemetery. Flat illustration.",
     "b9_005_betty_cash_died_december_29_1998.png"),

    (S + "Betty Cash in a final photograph — older, unwell, but still looking forward. "
     "She never received an explanation. She never received compensation. "
     "She never stopped trying. Flat illustration.",
     "b9_006_never_explanation_never_compensation.png"),
]


# ─────────────────────────────────────────────────────────────────────────────
# B10 — LO QUE SABEMOS CON CERTEZA  (~17:37–19:05)
# ─────────────────────────────────────────────────────────────────────────────
B10 = [
    (S + "Three people — Betty, Vickie, Colby — shown in portrait panels side by side. "
     "Their names and ages labeled: Betty Cash 51, Vickie Landrum 57, Colby Landrum 7. "
     "Three consistent accounts. Spanning decades. Flat illustration.",
     "b10_001_three_people_consistent_accounts.png"),

    (S + "FM 1485 road at night — the spot where it happened. "
     "A glowing outline marking the exact location. "
     "This is a documented place. This happened. Flat illustration.",
     "b10_002_fm1485_december_29_1980_documented.png"),

    (S + "Medical evidence panel: burn patterns, radiation test results, "
     "white blood cell count chart. "
     "All labeled as consistent with ionizing radiation exposure. "
     "These are not disputed. Flat illustration.",
     "b10_003_documented_physical_damage_radiation.png"),

    (S + "23 helicopter silhouettes in formation — photographed against night sky. "
     "Multiple independent witnesses pointing up at the same formation. "
     "The helicopters were real. The witnesses are real. Flat illustration.",
     "b10_004_twenty_three_helicopters_multiple_witnesses.png"),

    (S + "The United States government seal — behind it, a blank space "
     "where the explanation should be. "
     "'NO ACKNOWLEDGMENT' stamped. Flat illustration.",
     "b10_005_government_never_acknowledged.png"),

    (S + (ELEMENT_REF or "") + "The narrator character stands in front of two columns on a board: "
     "'WHAT WE KNOW' and 'WHAT WE DON'T KNOW'. "
     "The first column is full. The second column has one enormous question. Flat illustration.",
     "b10_006_either_government_knows_or_doesnt.png"),
]


# ─────────────────────────────────────────────────────────────────────────────
# B11 — FM 1485 HOY  (~19:05–19:38)
# ─────────────────────────────────────────────────────────────────────────────
B11 = [
    (S + "FM 1485 today — modern daylight shot. The same two-lane road, same pine trees. "
     "Normal traffic visible. A completely ordinary Texas road. "
     "The contrast with what happened here is stark. Flat illustration.",
     "b11_001_fm1485_exists_drive_today.png"),

    (S + "An empty two-lane Texas road at dusk — the same road. "
     "Looking down the road into the distance where the object hovered. "
     "Nothing there now. Just asphalt and trees. Flat illustration.",
     "b11_002_betty_drove_december_29_1980.png"),

    (S + "A lone car driving down FM 1485 at night — headlights cutting through darkness. "
     "Pine trees on both sides. The same isolation. "
     "Anyone could drive this road tonight. Flat illustration.",
     "b11_003_never_fully_recovered_that_drive.png"),

    (S + "Title card in the style of a classified document stamp: "
     "'THE CASH-LANDRUM INCIDENT' in large typewriter font. "
     "Below: DOCUMENTED — INVESTIGATED — DISMISSED — FORGOTTEN "
     "Each word stamped in orange, getting smaller. Flat illustration.",
     "b11_004_cash_landrum_incident_until_now.png"),
]


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

BLOCKS = {
    "b4":  (B4,  EP_DIR / "images/video/b4"),
    "b5":  (B5,  EP_DIR / "images/video/b5"),
    "b6":  (B6,  EP_DIR / "images/video/b6"),
    "b7":  (B7,  EP_DIR / "images/video/b7"),
    "b8":  (B8,  EP_DIR / "images/video/b8"),
    "b9":  (B9,  EP_DIR / "images/video/b9"),
    "b10": (B10, EP_DIR / "images/video/b10"),
    "b11": (B11, EP_DIR / "images/video/b11"),
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--block", default=None,
                        help="Ejecutar solo un bloque (ej: b4, b5, b6)")
    args = parser.parse_args()

    target_blocks = [args.block] if args.block else list(BLOCKS.keys())

    for block_name in target_blocks:
        if block_name not in BLOCKS:
            print(f"Bloque desconocido: {block_name}")
            continue
        jobs, out_dir = BLOCKS[block_name]
        out_dir.mkdir(parents=True, exist_ok=True)
        existing = [j[1] for j in jobs if (out_dir / j[1]).exists()]
        pending  = [j for j in jobs if not (out_dir / j[1]).exists()]
        print(f"\nEP03 {block_name.upper()} — {len(pending)} pendientes, {len(existing)} ya existen")
        if pending:
            run(pending, out_dir)
        print(f"{block_name.upper()} completo. Imágenes en: {out_dir}")
