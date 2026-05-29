// Fujara — Monolithic Body Variant (CAD/fujara-body-monolithic/)
// Issue #2: integrate Flue_Top voicing geometry into Body_Top + Body_Bottom.
//
// This variant keeps the original fujara.scad assembly as the default.
// The monolithic version eliminates the separate Flue_Top glue joint by
// cutting the flue windway, sound window, and labium edge directly into
// Body_Top. Body_Bottom is the lower bore continuation.
//
// Fabrication authority status: PENDING_MEASUREMENT.
// Verify all dimensions against design-table/fujara-dimensions-parametric.xlsx
// and family-spec.csv before any machining.
// See CAD/mcp-session-log.md for V5 provenance.

$fn = 72;

// ── Parameters (from family-spec.csv FUJ-A2-STUDY + design-table) ────────────

target_note       = "A2";
target_hz         = 110.00;

main_bore_length_mm  = 1550.96;   // open-open effective length seed
main_bore_id_mm      = 31.75;     // bore ID from design table
wall_thickness_mm    = 6.35;
outer_dia_mm         = main_bore_id_mm + 2 * wall_thickness_mm;

// Tone holes (position from foot end — traditional 0.83/0.73/0.68 ratios).
hole1_from_foot_mm = main_bore_length_mm * 0.83;
hole2_from_foot_mm = main_bore_length_mm * 0.73;
hole3_from_foot_mm = main_bore_length_mm * 0.68;
hole_diameter_mm   = 10;

// ── Body_Top / Body_Bottom split point ───────────────────────────────────────
// The joint sits just below the voicing zone so both pieces are manageable
// on a lathe. Adjust split_z to match your blank/lathe capacity.
split_z_mm = main_bore_length_mm - 500;  // starter value; measurement-required

// ── Monolithic flue geometry (integrated into Body_Top) ──────────────────────
// In the separate-part assembly these lived in Fujara_Flue_Top.
// Here they are cut directly into the top section.
flue_width_mm           = 12.0;   // windway width — measurement-required
flue_depth_mm           = 4.0;    // windway height — measurement-required
sound_window_length_mm  = 30.0;   // labium opening along bore axis — measurement-required
sound_window_width_mm   = 16.0;   // labium opening across bore — measurement-required
labium_angle_deg        = 35;     // splitting-edge angle from horizontal — measurement-required

// Side air tube (unchanged from fujara.scad reference design).
side_tube_center_offset_mm = 58;
side_tube_od_mm            = 22;
side_tube_id_mm            = 14;
side_tube_length_mm        = 420;

// ── Modules ──────────────────────────────────────────────────────────────────

module bore_shell(len_mm) {
  difference() {
    cylinder(h = len_mm, d = outer_dia_mm);
    translate([0, 0, -1]) cylinder(h = len_mm + 2, d = main_bore_id_mm);
  }
}

module tone_hole(z_pos) {
  translate([0, -outer_dia_mm / 2, z_pos])
    rotate([90, 0, 0])
      cylinder(h = outer_dia_mm + 2, d = hole_diameter_mm);
}

// Integrated flue windway cut into the body wall at the top.
// The windway runs axially through the wall from the side-tube inlet port
// to the sound window opening.
module flue_windway() {
  translate([side_tube_center_offset_mm - flue_width_mm / 2,
             -outer_dia_mm / 2,
             main_bore_length_mm - side_tube_length_mm - flue_depth_mm])
    cube([flue_width_mm, outer_dia_mm / 2 + flue_depth_mm, side_tube_length_mm + flue_depth_mm]);
}

// Sound window opening through the bore wall.
module sound_window() {
  translate([-sound_window_width_mm / 2,
             -outer_dia_mm / 2 - 1,
             main_bore_length_mm - side_tube_length_mm - sound_window_length_mm])
    cube([sound_window_width_mm, wall_thickness_mm + 2, sound_window_length_mm]);
}

// Labium (splitting edge) — angled face at the top of the sound window.
// Modelled as a rotated wedge; refine angle after P0 voicing tests.
module labium_edge() {
  translate([0, -outer_dia_mm / 2, main_bore_length_mm - side_tube_length_mm])
    rotate([labium_angle_deg, 0, 0])
      cube([sound_window_width_mm, 2, wall_thickness_mm], center = true);
}

module side_air_tube() {
  translate([side_tube_center_offset_mm, 0,
             main_bore_length_mm - side_tube_length_mm])
    difference() {
      cylinder(h = side_tube_length_mm, d = side_tube_od_mm);
      translate([0, 0, -1]) cylinder(h = side_tube_length_mm + 2, d = side_tube_id_mm);
    }
}

// ── Body_Top: upper bore section with integrated flue/voicing geometry ────────
module body_top() {
  top_len = main_bore_length_mm - split_z_mm;
  translate([0, 0, split_z_mm])
    difference() {
      union() {
        bore_shell(top_len);
        side_air_tube();
      }
      flue_windway();
      sound_window();
    }
}

// ── Body_Bottom: lower bore continuation with tone holes ─────────────────────
module body_bottom() {
  difference() {
    bore_shell(split_z_mm);
    tone_hole(hole1_from_foot_mm);
    tone_hole(hole2_from_foot_mm);
    tone_hole(hole3_from_foot_mm);
  }
}

// ── Assembly ─────────────────────────────────────────────────────────────────
// Render Body_Top + Body_Bottom together for visual review.
// Change SHOW_TOP / SHOW_BOTTOM to isolate pieces for machining review.

SHOW_TOP    = true;
SHOW_BOTTOM = true;

if (SHOW_BOTTOM) body_bottom();
if (SHOW_TOP)    body_top();
