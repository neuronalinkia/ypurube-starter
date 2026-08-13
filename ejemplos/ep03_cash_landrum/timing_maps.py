"""
EP03 Cash-Landrum — Timing maps completos (v1)

Generados con Whisper word-level timestamps del audio ep03_full.wav.
Ajustar los segundos exactos a los timestamps reales de tu audio.
Ver docs en CLAUDE.md: FASE 7 — TIMING MAPS

Reglas aplicadas:
- Ninguna entrada supera 5s (Vexlo Sync requirement)
- Cada imagen usada exactamente una vez (sin duplicados)
- Los clips reales de CH-47 son Path objects (fallan gracefully a negro si no existen)

Uso desde la raíz del repo:
  python core/montar_episodio.py \\
    --ep-dir ejemplos/ep03_cash_landrum \\
    --timing ejemplos/ep03_cash_landrum/timing_maps.py \\
    --audio  ejemplos/ep03_cash_landrum/audio/ep03_full.wav \\
    --output ejemplos/ep03_cash_landrum/videos/ep03_draft.mp4
"""

from pathlib import Path

# Ruta a los clips reales de CH-47 (opcionales — si no existen, se usa negro)
# Descarga footage de dominio público: NARA, Wikimedia Commons, etc.
EP_DIR = Path(__file__).parent
CLIPS  = EP_DIR / "footage"  # ep03_cash_landrum/footage/


# ─────────────────────────────────────────────────────────────────────────────
# B1 — HOOK / FM 1485  [0 – 89.98s]
# ─────────────────────────────────────────────────────────────────────────────
B1_MAP = [
    ( 0.00,  3.50, "b1/b1_001_december_29_1980_texas_date.png"),
    ( 3.50,  7.20, "b1/b1_002_two_lane_road_texas_night.png"),
    ( 7.20, 10.50, "b1/b1_003_cold_freezing_temperature.png"),
    (10.50, 14.80, "b1/b1_004_betty_cash_51_driving.png"),
    (14.80, 18.40, "b1/b1_005_vickie_landrum_57_back_seat.png"),
    (18.40, 22.00, "b1/b1_006_colby_seven_years_half_asleep.png"),
    (22.00, 25.90, "b1/b1_007_fm1485_highway_pine_forest.png"),
    (25.90, 29.60, "b1/b1_008_no_streetlights_headlights_only.png"),
    (29.60, 33.80, "b1/b1_009_betty_knows_this_road.png"),
    (33.80, 37.50, "b1/b1_010_nine_pm_something_above_road.png"),
    (37.50, 41.70, "b1/b1_011_not_stars_not_plane_hovering.png"),
    (41.70, 46.00, "b1/b1_012_diamond_shaped_water_tower_size.png"),
    (46.00, 50.30, "b1/b1_013_betty_slows_car.png"),
    (50.30, 54.60, "b1/b1_014_ufo_130_feet_above_road_stationary.png"),
    (54.60, 59.00, "b1/b1_015_flames_bursts_downward_base.png"),
    (59.00, 63.20, "b1/b1_016_flames_hit_road_dissipate.png"),
    (63.20, 67.80, "b1/b1_017_betty_stops_car_completely.png"),
    (67.80, 89.98, "b1/b1_018_turns_off_radio_silence.png"),
]


# ─────────────────────────────────────────────────────────────────────────────
# B2 — EL ENCUENTRO  [89.98 – 211.03s]
# ─────────────────────────────────────────────────────────────────────────────
B2_MAP = [
    ( 89.98,  94.00, "b2/b2_001_heat_immediate_furnace.png"),
    ( 94.00,  98.00, "b2/b2_001b_object_hovering_flames_car_view.png"),
    ( 98.00, 102.00, "b2/b2_002_vickie_prays_holds_colby.png"),
    (102.00, 105.50, "b2/b2_002b_colby_eyes_covered_vickie_shields.png"),
    (105.50, 109.00, "b2/b2_003_betty_opens_door_gets_out.png"),
    (109.00, 112.50, "b2/b2_003b_betty_steps_onto_road.png"),
    (112.50, 116.00, "b2/b2_004_betty_standing_road_shielding_eyes.png"),
    (116.00, 120.00, "b2/b2_005_light_intense_orange_white_shifting.png"),
    (120.00, 124.00, "b2/b2_005b_light_color_shift_blinding.png"),
    (124.00, 128.00, "b2/b2_006_surface_metallic_brushed_aluminum.png"),
    (128.00, 132.00, "b2/b2_007_flame_bursts_pine_trees_illuminated.png"),
    (132.00, 136.00, "b2/b2_007b_second_burst_pine_trees_wide.png"),
    (136.00, 139.50, "b2/b2_007c_object_still_heat_radiates_down.png"),
    (139.50, 143.00, "b2/b2_008_skin_burning_radiation_heat.png"),
    (143.00, 146.50, "b2/b2_008b_radiation_heat_through_body.png"),
    (146.50, 150.00, "b2/b2_009_heat_goes_through_radiation.png"),
    (150.00, 153.50, "b2/b2_009b_heat_invisible_body_absorbing.png"),
    (153.50, 157.00, "b2/b2_010_vickie_opens_door_calls_betty.png"),
    (157.00, 161.00, "b2/b2_010b_vickie_arm_reaching_for_betty.png"),
    (161.00, 165.00, "b2/b2_011_door_handle_burns_fingers.png"),
    (165.00, 168.50, "b2/b2_012_vickie_pulls_betty_back_inside.png"),
    (168.50, 173.00, "b2/b2_013_twenty_minutes_watching_impossible.png"),
    (173.00, 177.00, "b2/b2_014_object_rises_slowly_vertical.png"),
    (177.00, 181.00, "b2/b2_014b_object_lifts_vertically_slow.png"),
    # Real footage (CH-47) — falls back to black if files not present
    (181.00, 190.00, CLIPS / "real_01_helicopters_night.mp4"),
    (190.00, 199.00, CLIPS / "real_02_ch47_chinook.mp4"),
    (199.00, 207.00, "b2/b2_024_not_chasing_escorting.png"),
    (207.00, 211.03, "b2/b2_026_betty_vickie_no_words.png"),
]


# ─────────────────────────────────────────────────────────────────────────────
# B3 — LOS SÍNTOMAS  [211.03 – 348.81s]
# ─────────────────────────────────────────────────────────────────────────────
B3_MAP = [
    (211.03, 215.50, "b3/b3_001_betty_home_face_feels_tight.png"),
    (215.50, 220.00, "b3/b3_002_skin_bright_red_severe_sunburn.png"),
    (220.00, 225.00, "b3/b3_003_blisters_forming_face_neck_scalp.png"),
    (225.00, 230.00, "b3/b3_004_hair_clumps_hand.png"),
    (230.00, 235.50, "b3/b3_005_eyes_swell_shut_cannot_open.png"),
    (235.50, 241.00, "b3/b3_006_vomiting_night_next_day.png"),
    (241.00, 246.00, "b3/b3_007_pain_constant.png"),
    (246.00, 252.00, "b3/b3_008_three_days_hospital_parkway.png"),
    (252.00, 257.00, "b3/b3_009_vickie_same_symptoms.png"),
    (257.00, 263.00, "b3/b3_010_colby_seven_red_swollen_eyes.png"),
    (263.00, 269.00, "b3/b3_011_doctors_run_tests.png"),
    (269.00, 275.00, "b3/b3_015_white_blood_cell_count_dropped.png"),
    (275.00, 282.00, "b3/b3_012_ionizing_radiation_diagnosis.png"),
    (282.00, 288.00, "b3/b3_013_not_chemical_not_fire_radiation.png"),
    (288.00, 294.00, "b3/b3_014_nuclear_reactor_nuclear_weapon.png"),
    (294.00, 301.00, "b3/b3_016_hospitalized_multiple_times_first_year.png"),
    (301.00, 308.00, "b3/b3_017_medical_bills_hundred_thousand.png"),
    (308.00, 318.00, "b3/b3_018_colby_eye_problems_adolescence.png"),
    (318.00, 332.00, "b3/b3_019_three_people_one_night_one_road.png"),
    (332.00, 348.81, "b3/b3_020_injuries_only_one_explanation.png"),
]


# ─────────────────────────────────────────────────────────────────────────────
# B4 — INVESTIGACIÓN SCHUESSLER  [348.81 – 463.77s]
# ─────────────────────────────────────────────────────────────────────────────
B4_MAP = [
    (348.81, 354.00, "b4/b4_001_schuessler_aerospace_engineer_nasa.png"),
    (354.00, 360.00, "b4/b4_002_mufon_investigates_ufo_cases.png"),
    (360.00, 366.00, "b4/b4_003_schuessler_drives_huffman_texas.png"),
    (366.00, 373.00, "b4/b4_004_interviews_betty_vickie_colby_separately.png"),
    (373.00, 380.00, "b4/b4_005_engineer_approach_methodology.png"),
    (380.00, 388.00, "b4/b4_006_no_inconsistencies_accounts_match.png"),
    (388.00, 397.00, "b4/b4_007_collecting_medical_records_photos.png"),
    (397.00, 407.00, "b4/b4_008_other_witnesses_emerge.png"),
    (407.00, 418.00, "b4/b4_009_married_couple_nearby_road.png"),
    (418.00, 430.00, "b4/b4_013_five_independent_witnesses.png"),
    (430.00, 450.00, "b4/b4_014_seven_hundred_pages_documentation.png"),
    (450.00, 463.77, "b4/b4_018_cannot_appear_without_paper_trail.png"),
]


# ─────────────────────────────────────────────────────────────────────────────
# B5 — LAS BASES MILITARES  [463.77 – 582.59s]
# ─────────────────────────────────────────────────────────────────────────────
B5_MAP = [
    (463.77, 470.00, "b5/b5_010_23_chinooks_cannot_appear_sky.png"),
    (470.00, 477.00, "b5/b5_002_fort_hood_killeen_largest_base.png"),
    (477.00, 482.00, "b5/b5_002b_chinook_sixty_feet_long.png"),
    (482.00, 490.00, "b5/b5_001_schuessler_writes_military_installations.png"),
    (490.00, 497.00, "b5/b5_003_ellington_field_houston_air_guard.png"),
    (497.00, 504.00, "b5/b5_004_bergstrom_austin_red_river.png"),
    (504.00, 513.00, "b5/b5_006_no_record_flight_activity.png"),
    (513.00, 523.00, "b5/b5_007_not_classified_simply_no_record.png"),
    (523.00, 534.00, "b5/b5_008_department_army_defense_faa.png"),
    (534.00, 547.00, "b5/b5_010c_maintenance_crews_fuel_trucks.png"),
    (547.00, 582.59, "b5/b5_009_paper_trail_intentionally_removed.png"),
]


# ─────────────────────────────────────────────────────────────────────────────
# B6 — LA DEMANDA  [582.59 – 769.63s]
# ─────────────────────────────────────────────────────────────────────────────
B6_MAP = [
    (582.59, 592.00, "b6/b6_014b_jerry_mcdonald_dayton_texas.png"),
    (592.00, 602.00, "b6/b6_001_betty_vickie_hire_lawyer_1981.png"),
    (602.00, 613.00, "b6/b6_002_lawsuit_federal_court_houston.png"),
    (613.00, 623.00, "b6/b6_004_legal_argument_government_aircraft.png"),
    (623.00, 632.00, "b6/b6_003_twenty_million_dollars_damages.png"),
    (632.00, 645.00, "b6/b6_005_lawyer_presents_medical_evidence.png"),
    (645.00, 657.00, "b6/b6_006_dod_responds_single_argument.png"),
    (657.00, 669.00, "b6/b6_007_no_such_aircraft_no_such_helicopters.png"),
    (669.00, 680.00, "b6/b6_008_1986_federal_court_dismisses.png"),
    (680.00, 695.00, "b6/b6_009_ruling_failed_to_identify_agency.png"),
    (695.00, 720.00, "b6/b6_010_not_aircraft_didnt_exist.png"),
    (720.00, 769.63, "b6/b6_011_betty_vickie_leave_courthouse.png"),
]


# ─────────────────────────────────────────────────────────────────────────────
# B7 — LOS DOCUMENTOS  [769.63 – 868.53s]
# ─────────────────────────────────────────────────────────────────────────────
B7_MAP = [
    (769.63, 780.00, "b7/b7_001_senators_letters_department_defense.png"),
    (780.00, 793.00, "b7/b7_002_dod_responses_redacted.png"),
    (793.00, 804.00, "b7/b7_003_texas_health_radiation_investigation.png"),
    (804.00, 815.00, "b7/b7_004_elevated_readings_exact_spot.png"),
    (815.00, 828.00, "b7/b7_005_official_illustration_betty_description.png"),
    (828.00, 840.00, "b7/b7_006_matches_no_known_aircraft.png"),
    (840.00, 854.00, "b7/b7_007_nuclear_powered_test_vehicle_theory.png"),
    (854.00, 868.53, "b7/b7_008_no_program_declassified_matches.png"),
]


# ─────────────────────────────────────────────────────────────────────────────
# B8 — PROGRAMAS SECRETOS / ESCOLTA  [868.53 – 994.26s]
# ─────────────────────────────────────────────────────────────────────────────
B8_MAP = [
    ( 868.53,  882.00, "b8/b8_001_organized_equipped_escorted.png"),
    ( 882.00,  896.00, "b8/b8_002_fort_hood_200_miles_chinook.png"),
    ( 896.00,  913.00, "b8/b8_003_records_existed_were_destroyed.png"),
    ( 913.00,  929.00, "b8/b8_004_truck_driver_helicopters_south.png"),
    ( 929.00,  945.00, "b8/b8_005_direction_matched_timing_matched.png"),
    ( 945.00,  965.00, "b8/b8_006_two_explanations_neither_good.png"),
    ( 965.00,  994.26, "b8/b8_007_someone_knew_helicopters_were_there.png"),
]


# ─────────────────────────────────────────────────────────────────────────────
# B9 — BETTY EL RESTO DE SU VIDA  [994.26 – 1057.42s]
# ─────────────────────────────────────────────────────────────────────────────
B9_MAP = [
    ( 994.26, 1006.00, "b9/b9_001_betty_cancer_immune_disorders.png"),
    (1006.00, 1020.00, "b9/b9_002_cancer_treatments_years.png"),
    (1020.00, 1033.00, "b9/b9_003_vickie_interviews_never_changed_story.png"),
    (1033.00, 1043.00, "b9/b9_004_colby_adult_back_seat_never_changed.png"),
    (1043.00, 1050.00, "b9/b9_005_betty_cash_died_december_29_1998.png"),
    (1050.00, 1057.42, "b9/b9_006_never_explanation_never_compensation.png"),
]


# ─────────────────────────────────────────────────────────────────────────────
# B10 — LO QUE SABEMOS  [1057.42 – 1145.00s]
# ─────────────────────────────────────────────────────────────────────────────
B10_MAP = [
    (1057.42, 1070.00, "b10/b10_001_three_people_consistent_accounts.png"),
    (1070.00, 1082.00, "b10/b10_002_fm1485_december_29_1980_documented.png"),
    (1082.00, 1094.00, "b10/b10_003_documented_physical_damage_radiation.png"),
    (1094.00, 1106.00, "b10/b10_004_twenty_three_helicopters_multiple_witnesses.png"),
    (1106.00, 1120.00, "b10/b10_005_government_never_acknowledged.png"),
    (1120.00, 1145.00, "b10/b10_006_either_government_knows_or_doesnt.png"),
]


# ─────────────────────────────────────────────────────────────────────────────
# B11 — FM 1485 HOY  [1145.00 – 1178.00s]
# ─────────────────────────────────────────────────────────────────────────────
B11_MAP = [
    (1145.00, 1153.00, "b11/b11_001_fm1485_exists_drive_today.png"),
    (1153.00, 1162.00, "b11/b11_002_betty_drove_december_29_1980.png"),
    (1162.00, 1171.00, "b11/b11_003_never_fully_recovered_that_drive.png"),
    (1171.00, 1178.00, "b11/b11_004_cash_landrum_incident_until_now.png"),
]


# ─────────────────────────────────────────────────────────────────────────────
# EXPORT: ALL_BLOCKS — usado por core/montar_episodio.py
# ─────────────────────────────────────────────────────────────────────────────
ALL_BLOCKS = [
    ("B1",  B1_MAP),
    ("B2",  B2_MAP),
    ("B3",  B3_MAP),
    ("B4",  B4_MAP),
    ("B5",  B5_MAP),
    ("B6",  B6_MAP),
    ("B7",  B7_MAP),
    ("B8",  B8_MAP),
    ("B9",  B9_MAP),
    ("B10", B10_MAP),
    ("B11", B11_MAP),
]
