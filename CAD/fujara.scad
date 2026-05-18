// Fujara V5 candidate OpenSCAD starter.
// Review scaffold only: verify against SolidWorks/design-table authority before shop use.

$fn = 72;

// Source refs:
// - family-spec.csv member FUJ-A2-STUDY
// - sw-reference/Fujara-SW-Design-Table.csv
// - CAD/fujara-body/G2Fujara_Assembly.SLDASM_dimensions.csv

target_note = "A2";
target_hz = 110.00;
temperature_c = 20;

// Validator-compatible first-pass open-open length at 20 C.
main_bore_length_mm = 1550.96;
main_bore_id_mm = 31.75;
wall_thickness_mm = 6.35;
outer_diameter_mm = main_bore_id_mm + 2 * wall_thickness_mm;

// Traditional fujara three-hole layout rule measured from the foot end.
hole1_from_foot_mm = main_bore_length_mm * 0.83;
hole2_from_foot_mm = main_bore_length_mm * 0.73;
hole3_from_foot_mm = main_bore_length_mm * 0.68;
hole_diameter_mm = 10;

// Measurement-required delivery/voicing placeholders.
side_tube_center_offset_mm = 58;
side_tube_od_mm = 22;
side_tube_id_mm = 14;
side_tube_length_mm = 420;
flue_width_mm = 12;
sound_hole_length_mm = 6.35;

module main_bore_shell() {
  difference() {
    cylinder(h = main_bore_length_mm, d = outer_diameter_mm);
    translate([0, 0, -1]) cylinder(h = main_bore_length_mm + 2, d = main_bore_id_mm);
  }
}

module tone_hole(z_pos) {
  translate([0, -outer_diameter_mm / 2, z_pos])
    rotate([90, 0, 0])
      cylinder(h = outer_diameter_mm, d = hole_diameter_mm);
}

module side_air_tube() {
  translate([side_tube_center_offset_mm, 0, main_bore_length_mm - side_tube_length_mm])
    difference() {
      cylinder(h = side_tube_length_mm, d = side_tube_od_mm);
      translate([0, 0, -1]) cylinder(h = side_tube_length_mm + 2, d = side_tube_id_mm);
    }
}

module labium_review_marker() {
  translate([-outer_diameter_mm / 2, -outer_diameter_mm / 2, main_bore_length_mm - 75])
    cube([outer_diameter_mm, 2, sound_hole_length_mm]);
}

difference() {
  main_bore_shell();
  tone_hole(hole1_from_foot_mm);
  tone_hole(hole2_from_foot_mm);
  tone_hole(hole3_from_foot_mm);
}

side_air_tube();
labium_review_marker();
