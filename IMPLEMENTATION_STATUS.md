# Module 7 Implementation Status

This file is the durable handoff record for future work. Update it after every approved phase
and before ending each work session. Do not infer completion from the existence of a file.

## Project Identification

- **Course:** Georgia State University CSc 8830 — Computer Vision
- **Assignment:** Module 7 — Calibrated Stereo, Uncalibrated Stereo, and Video-Based Room Dimension Estimation
- **Module directory:** `Assignments/Module_7/`
- **Primary documentation:** `MODULE_7_ASSIGNMENT_QUESTIONS.md`, `MODULE_7_ASSIGNMENT_INSTRUCTIONS.md`
- **Working plan:** `IMPLEMENTATION_PLAN.md`
- **Relevant repository:** Module 7 repository has not been initialized or identified yet; repository topology is pending user approval.
- **Current implementation phase:** Phase 3D — Standalone UI alignment and proposed evidence preparation

## Latest Local UI Polish Review — 2026-10-26

- **Status:** `IMPLEMENTED LOCALLY — PUBLIC REVIEW PENDING`
- Replaced infrastructure-facing wording in rendered pages with concise academic explanations.
- Added readable metric cards and diagnostic tables for calibration, baseline, depth, parallax,
  reprojection, and shape-specific quality results. Full technical records remain available in
  collapsed detail sections.
- Preserved machine-readable experiment statuses and all scientific findings; no calibration,
  reconstruction, measurement, threshold, or evidence file was changed.
- The dashboard checkout was synchronized for local smoke testing only. No dashboard commit,
  push, or deployment was performed.
- Live rectangle-page verification remains a user approval check because the deployed application
  was not changed during this review.

## Current Status

- **Overall project status:** Phase 2A software foundation, Phase 2B real calibration/stereo validation, and Phase 3 object-dimension software implementation are complete for their stated evidence. Phase 3A now has three real rectangle experiments; the third has verified FREE ADMISSION ruler measurements, but stereo accuracy remains outside the physical intervals and pose/model consistency remains unresolved.
- **Last completed phase:** Phase 3 deterministic rectangle, circle, and polygon dimension-estimation implementation and tests.
- **Active phase:** Phase 3D standalone UI alignment and proposed evidence preparation complete;
  Git initialization, public evidence approval, dashboard wiring, deployment, final reports, and
  Phase 4 remain separately gated.
- **Next action:** user review of the proposed evidence images and future publication decision.
- **Phase 3C diagnostic decision:** the focused ruler/geometry audit is complete. The three ruler
  photographs support the documented edge identities and approximate readings, and no independent
  edge-mapping, vertex-identity, coordinate-frame, or software defect was demonstrated. The saved
  pose and triangle reconstruction reproduce exactly under reprocessing. The experiment remains
  `EXPERIMENT COMPLETE — PHYSICAL MEASUREMENTS DOCUMENTED; STEREO TRIANGLE ACCURACY NOT VALIDATED`.
- **Pending user decisions:**
  - measured checkerboard/reference-target availability;
  - ruler/tape measure and camera-support availability;
  - measured sequential baseline procedure;
  - room-video reference visibility and coverage;
  - independent physical room measurements for validation;
  - whether any real sample, calibration capture, or evidence image may be committed publicly;
  - eventual Module 7 GitHub repository/topology.
- **Confirmed hardware:** one smartphone camera.
- **Selected Question 1 approach:** sequential calibrated stereo using two positions of the same phone, calibrated essential-matrix pose, and metric scale from a measured camera-center displacement; checkerboard-PnP is a fallback/verification method when visible.
- **Selected Question 3 direction:** calibrated moving-camera smartphone video with a measured reference; the minimum viable workflow is reference-assisted sparse multiview measurement, not unrestricted monocular room scanning.
- **Final report formats:** editable DOCX primary source and faithful PDF export.
- **Known blockers:** the ±1 mm remains physical-measurement uncertainty and is not a propagated stereo uncertainty. The equivalent-edge validation assumes a planar rectangular front face; exact right angles and equality were not independently metrologically measured. No camera-center baseline has been measured for an essential-matrix cross-check. Shape-specific object captures and independent object measurements, room videos, a metric room reference, independent room measurements, and the scanned handwritten Q2 derivation remain pending. Phase 4 remains blocked until separately authorized.

## Phase Checklist

- [x] Phase 0: Repository discovery and requirements
  - [x] Read root governance and deployment documents.
  - [x] Read existing module governance, assignment, planning, packaging, source, web, test, and ignore conventions where available.
  - [x] Preserve Module 7 question requirements and submission instructions.
  - [x] Create a proposed architecture and phased plan.
  - [x] Initialize this handoff tracker.
- [x] Phase 1: Architecture and technical design
  - [x] Record one-smartphone hardware constraint and sequential-stereo Q1 approach.
  - [x] Define Q1 pose alternatives, metric scale, coordinate frames, and failure checks.
  - [x] Define Q3 moving-video MVP with a measured metric reference.
  - [x] Define data schemas, units, error fields, and provenance requirements.
  - [x] Define handwritten-only Q2 outline and scan checklist.
  - [x] Define DOCX/PDF report architecture and validation workflow.
  - [x] Create the Phase 1 technical-design documents.
- [x] Phase 2: Calibration and stereo depth software foundation
  - [x] Implement checkerboard calibration, validation, serialization, and reprojection errors.
  - [x] Implement calibrated essential-matrix pose with explicit metric-scale provenance.
  - [x] Implement checkerboard `solvePnP` fallback, rectification, triangulation, and depth.
  - [x] Add deterministic synthetic/unit tests and CLI processing scripts.
- [x] Phase 2B: Real smartphone calibration and stereo validation — Stages A–C complete under the documented equivalent-edge assumption
  - [x] Stage A — Camera calibration: `CALIBRATION VALIDATED` by recomputation from original Module 2 photographs.
  - [x] Stage B — Stereo geometry: `STEREO GEOMETRY VALIDATED` on the real pair using automatic 54-corner checkerboard correspondences, metric checkerboard-PnP poses, triangulation, cheirality, parallax, and reprojection checks. The checkerboard-distance comparison is an in-sample geometry check, not independent physical validation.
  - [x] Stage C — Physical validation: `PHYSICAL VALIDATION COMPLETE UNDER EQUIVALENT-RECTANGULAR-EDGE ASSUMPTION`; 96.70 ± 1.00 mm gives interval 95.70–97.70 mm, containing the unchanged 95.905679 mm reconstruction.
- [x] Phase 3: Object shape and dimension measurement — software implemented and deterministically tested; real validation pending user data
  - [x] Phase 3A rectangle physical validation: `EXPERIMENT COMPLETE — PHYSICAL MEASUREMENT VERIFIED; STEREO ACCURACY NOT VALIDATED`
  - [x] Phase 3B yellow-lid circle experiment: `EXPERIMENT DOCUMENTED — PHYSICAL REFERENCE ESTABLISHED; STEREO CIRCLE GEOMETRY REJECTED`
  - [x] Phase 3C triangle experiment: `EXPERIMENT COMPLETE — PHYSICAL MEASUREMENTS DOCUMENTED; STEREO TRIANGLE ACCURACY NOT VALIDATED`
  - [x] Phase 3D Question 1 assignment surface: standalone calibrated-stereo webpage, page-provider
  contract, web smoke tests, and pending/rejected-result presentation.
- [ ] Phase 4: Room measurement from video
- [ ] Phase 5: Dashboard integration and public deployment
- [ ] Phase 6: Testing and experimental validation
- [ ] Phase 7: Handwritten derivation, report, citations, and demonstration
- [ ] Phase 8: Final submission readiness

## Completed Work

### Phase 0 — Discovery and planning

- **Description:** Inspected the root workspace contract, Git/deployment protocols, current
  module repositories, source-layout packaging, Streamlit page-provider contract, dashboard
  adapter, data/result conventions, ignore rules, and existing Module 2/5–6 geometry patterns.
- **Files created:**
  - `AGENTS.md`
  - `CLAUDE.md`
  - `GIT_WORKFLOW.md`
  - `README.md`
  - `MODULE_7_ASSIGNMENT_QUESTIONS.md`
  - `MODULE_7_ASSIGNMENT_INSTRUCTIONS.md`
  - `IMPLEMENTATION_PLAN.md`
  - `IMPLEMENTATION_STATUS.md`
- **Files modified outside Module 7:** none.
- **Validation performed:** read-only file inspection; directory/repository boundary inspection;
  current-module Git status inspection; Markdown consistency review; authoritative OpenCV and
  Hartley–Zisserman reference verification.
- **Test results:** no Python tests were run because no Module 7 implementation exists.
- **Relevant decisions:** Q1 uses sequential calibrated stereo from one smartphone; Q3 uses
  calibrated moving-camera video with a measured reference and a reference-assisted sparse
  multiview MVP; Q2 remains handwritten-only; dashboard edits are deferred.
- **Date:** 2026-10-23.
- **Claim classification:** documentation/planning implemented; architecture conclusions
  theoretically derived or observed from existing code; all empirical work pending user data.

### Phase 1 — Architecture and technical design

- **Description:** Converted the confirmed one-smartphone constraint into a sequential-stereo
  Q1 design; selected a reference-assisted calibrated moving-video MVP for Q3; defined pose,
  scale, coordinate-frame, data-schema, provenance, failure-state, and report-generation rules.
- **Files created:**
  - `docs/architecture.md`
  - `docs/calibration_protocol.md`
  - `docs/experimental_protocol.md`
  - `docs/uncalibrated_stereo_derivation.md`
  - `docs/references.md`
- **Files modified:** `AGENTS.md`, `README.md`, `IMPLEMENTATION_PLAN.md`, and this status file.
- **Validation performed:** documentation consistency review; checked that Q1 does not assume a
  rigid synchronized dual-camera rig; checked that Q3 does not claim monocular metric scale;
  checked that Q2 remains handwritten-only; checked that DOCX/PDF production is deferred to
  Phase 7.
- **Test results:** no Python or computer-vision tests were run; no algorithm implementation
  exists.
- **Technical decisions:** essential-matrix pose plus measured camera-center displacement is the
  primary Q1 method; checkerboard `solvePnP` is a fallback/verification method when visible;
  reference-assisted sparse multiview video is the Q3 MVP.
- **Confirmed equipment:** one smartphone camera only. Tripod/mount, slider, checkerboard,
  ruler/tape, validation objects, and room reference remain pending.
- **Date:** 2026-10-23.
- **Claim classification:** design documentation implemented; geometry rationale theoretically
  derived; all empirical values and capture-dependent acceptance criteria pending user data.

### Phase 2 — Calibration and stereo depth foundation

- **Description:** Implemented the reusable Python/OpenCV core for one-phone checkerboard
  calibration and sequential calibrated stereo. The implementation keeps intrinsic calibration,
  pose, metric scale, rectification, triangulation, depth, and diagnostics separate from any UI.
- **Files created:**
  - `pyproject.toml`, `.gitignore`
  - `src/module7/__init__.py`, `calibration.py`, `stereo_geometry.py`, `depth_estimation.py`,
    `io_utils.py`, and `visualization.py`
  - `scripts/run_calibration.py`, `scripts/process_stereo_pair.py`, `scripts/run_diagnostics.py`,
    `scripts/run_geometry_tests.py`
  - `tests/test_calibration.py`, `test_stereo_geometry.py`, `test_depth_estimation.py`,
    `test_io_utils.py`, and `test_visualization.py`
- **Validation performed:** synthetic checkerboard calibration, JSON round-trip, intrinsic and
  correspondence validation, essential-matrix pose recovery, explicit baseline scaling,
  checkerboard `solvePnP`, projection/rectification, metric triangulation, depth formula,
  invalid-depth handling, parallax rejection, image handling, and non-mutating diagnostics.
- **Test results:** `pytest -q` passed **24 tests**; `python3 -m compileall -q src scripts tests`
  passed. These are software/synthetic checks, not physical camera validation.
- **Real-data status:** no calibration images, stereo pair, measured camera-center displacement,
  or physical depth measurements were available. Calibration and depth values are therefore
  **pending user data collection**.
- **Claim classification:** implementation and deterministic tests are complete; formulas and
  coordinate transforms are theoretically derived; experimental validation is pending.
- **Date:** 2026-10-23.

### Phase 2B — Real smartphone calibration and stereo validation

- **Description:** Reused the original real Module 2 calibration photographs through the existing
  Module 7 calibration pipeline. Module 2 was accessed read-only; no files were copied into or
  modified in Module 2.
- **Current status:** `COMPLETE FOR DOCUMENTED EVIDENCE`; Stage A, Stage B, and Stage C are complete, with Stage C explicitly bounded by the equivalent-planar-rectangular-edge assumption.
- **Stage A — Camera calibration:** `CALIBRATION VALIDATED`; 16/16 original images were accepted,
  and Module 7 recomputation agrees closely with the original Module 2 record.
- **Stage B — Stereo geometry:** `STEREO GEOMETRY VALIDATED` for the real checkerboard-visible
  pair. The files supplied were `data/stereo_pairs/IMG_7485.JPG` and
  `data/stereo_pairs/IMG_7486.JPG` (not the previously anticipated `view1.JPG`/`view2.JPG`
  names). EXIF identifies both as Apple iPhone 15 Pro Max images at 5712×4284 file resolution;
  OpenCV decoded them as landscape `(5712, 4284)`, whereas the reused Module 2 calibration record
  is portrait `(4284, 5712)`. The original files were preserved unchanged. New derived portrait
  copies were created at `results/stereo_diagnostics/IMG_7485_portrait_calibration_frame.png`
  and `IMG_7486_portrait_calibration_frame.png` by a 90° clockwise rotation so their coordinate
  convention matches the calibration record.
- **Stage B workflow and evidence:** `scripts/process_stereo_pair.py --pose-method
  checkerboard_pnp` detected and automatically indexed 54/54 corresponding inner corners in both
  derived views; no hand-guessed pixel coordinates were used. The resulting record is
  `results/object_measurements/IMG_7485_IMG_7486_checkerboard_stereo.json`, the generated
  correspondence CSV is
  `results/stereo_diagnostics/IMG_7485_IMG_7486_checkerboard_correspondences.csv`, and the
  visual correspondence diagnostic is
  `results/stereo_diagnostics/IMG_7485_IMG_7486_correspondences.jpg`.
- **Stage B measured reconstruction results:** checkerboard-PnP relative translation was
  `[-12.179468, -81.974711, -13.615880] mm`, with derived baseline `83.985623 mm`; this is
  metric scale from the known 25.0 mm checkerboard, not an independently tape-measured
  camera-center displacement. Median triangulation parallax was `9.369687°`. All 54/54 points
  had positive depth in both views. Maximum triangulation reprojection error was `0.929288 px`
  in view 1 and `0.956960 px` in view 2; the maximum across both views was `0.956960 px`.
  Per-view checkerboard-PnP RMS errors were `0.911854 px` and `1.024915 px`.
- **Stage B reconstructed-board geometry check:** horizontal neighboring-corner distances had
  mean `25.042202 mm`, median `25.039218 mm`, range `24.940150–25.168421 mm`, and MAE from
  25.0 mm of `0.0604125 mm`. Vertical distances had mean `24.966211 mm`, median `24.960948 mm`,
  range `24.890339–25.058097 mm`, and MAE `0.0477962 mm`. The reconstructed board plane fit had
  RMS residual `0.479362 mm` and maximum absolute residual `0.985222 mm`; 200.126 mm and
  125.055 mm were recovered for the 8-square and 5-square corner spans, respectively, against
  expected 200 mm and 125 mm. These checks reuse the same detected board corners used for PnP and
  triangulation, so they are in-sample geometry consistency evidence rather than independent
  physical validation.
- **Stage B software improvement:** extended `scripts/process_stereo_pair.py` with
  `--pose-method checkerboard_pnp` and optional `--auto-correspondences-output`; added measured
  triangulation parallax to the persisted result. The real workflow has now been executed and
  reviewed; `run_diagnostics.py` wrote
  `results/stereo_diagnostics/IMG_7485_IMG_7486_diagnostics.json`.
- **Stage C — Physical validation:** `PHYSICAL VALIDATION COMPLETE UNDER EQUIVALENT-RECTANGULAR-EDGE ASSUMPTION`. The
  latest user-confirmed independent flashcard front-face width measurement is 96.70 mm with the
  previously stated provisional uncertainty ±1 mm and reference interval 95.70–97.70 mm. The saved checkerboard-PnP pose
  reconstructed the selected endpoints as
  `[-14.330552, 217.472802, 485.149307] mm` and
  `[-16.983828, 312.154228, 470.106470] mm`, giving a Euclidean length of `95.905679 mm`.
  Relative to 96.70 mm, signed error is `-0.794321 mm`, absolute error `0.794321 mm`, and
  percentage error `0.821428%`; the result is within 95.70–97.70 mm with a `0.205679 mm`
  margin above the lower bound.
- **Stage C geometry diagnostics:** both endpoints had positive depth in both views and valid
  triangulation masks. View-1 depths were `485.149307 mm` and `470.106470 mm`; view-2 depths
  were `476.189833 mm` and `463.196790 mm`. Endpoint parallax was `8.308236°` and `7.050348°`.
  Reprojection errors were `[1.350889, 0.595503] px` in view 1 and `[1.377990, 0.605518] px`
  in view 2, below the implementation's 5 px invalidation threshold. These geometry checks pass
  and are consistent with the accepted independent width comparison.
- **Stage C discrepancy review:** the fixed endpoint CSV and annotated endpoint overlays were
  reviewed without changing coordinates. A diagnostic perturbation of each endpoint by ±2 px in
  both images, with the saved pose and calibration held fixed, produced valid reconstructed
  lengths from `94.108265 mm` to `98.220563 mm` (base `95.905679 mm`). This local sensitivity
  range remains relevant as a diagnostic only; it does not constitute a formal uncertainty interval
  or replace the independent physical measurement.
- **Stage C evidence review:** the saved endpoint overlays show both points on the apparent
  intersections of the printed front-face upper edge with its left and right front-face side edges.
  The raw-to-portrait mapping, unchanged intrinsic matrix, saved checkerboard-PnP pose, and
  projection matrices are internally consistent with the recorded coordinate frame; no definite
  stereo coordinate or projection mismatch was demonstrated. `flashcard_ruler_clear2.JPG` shows
  the metric 0 cm reference, millimetre subdivisions, and both corners of the lower parallel edge
  of the printed front face. Its reading is consistent with approximately 96.70 mm. The photographs
  show a rigid box face with four straight boundary seams and physical corners. Under the explicit
  planar-rectangular-face assumption, the lower measured edge is physically equivalent in length to
  the upper stereo edge. The product illustration remains separate nominal 100 × 80 × 60 mm
  information, not physical ground truth.
- **Stage C latest evidence:** the endpoint CSV is
  `data/stereo_pairs/flashcard_top_edge_correspondences.csv`; the validation record is
  `results/object_measurements/IMG_7485_IMG_7486_flashcard_validation.json`; and annotated
  endpoint/correspondence diagnostics are under `results/stereo_diagnostics/`. The saved
-  checkerboard-PnP pose was reused without rescaling from either physical measurement. The ±1 mm
  uncertainty remains the previously stated ±1 mm ruler uncertainty only; the current pipeline has
  no formal propagated reconstruction uncertainty. The physical evidence is under
  `data/physical_validation/`; clear2 is the primary measurement image. It supports the
  corresponding front-face width and makes the 96.70 mm reading and ±1 mm physical uncertainty
  plausible. The lower/upper edge equivalence is an explicit planar-rectangular-face assumption,
  not an inference from projected parallelism alone. Earlier superseded incorrect measurements and
  their failed comparisons remain only in the audit history.
- **Stage C decision:** `PHYSICAL VALIDATION COMPLETE UNDER EQUIVALENT-RECTANGULAR-EDGE ASSUMPTION`.
  This validates the front-face width dimension, not literal identity of the upper-edge pixel
  endpoints. A direct upper-edge ruler photograph is optional if future work requires literal
  same-endpoint evidence. Do not alter calibration, pixel coordinates, or metric scale.
- **Calibration reuse evidence:** `results/calibration/module2_reuse_provenance.md`.
- **Integrity statement:** intrinsic calibration is supported by real Module 2 evidence and
  marked validated for the recorded phone/lens/resolution. Stage B is supported by one real,
  checkerboard-visible pair and is marked validated only for the implemented checkerboard-PnP
  geometry checks. Stage C is physically validated for the front-face width under the explicit
  planar-rectangular equivalent-edge assumption; literal identity of the upper-edge pixel endpoints
  is not claimed. The
  83.985623 mm baseline is board-derived, not an independently measured
  optical-center displacement.
- **Date:** 2026-10-23.
- **Claim classification:** Stage B procedure and real stereo run experimentally validated for
  the stated checkerboard-PnP/in-sample geometry checks; Stage C physical width validation is
  experimentally supported under an explicit planar-rectangular equivalent-edge assumption.

### Phase 3 — Object shape and dimension measurement

- **Description:** Implemented the calibrated-stereo object-measurement layer on top of the
  validated Phase 2 triangulation API. Shape calculations receive only metric, finite,
  positive-depth 3D landmarks that pass parallax and reprojection checks.
- **Files added/modified:**
  - `src/module7/object_measurement.py`
  - `scripts/measure_object.py`
  - `src/module7/io_utils.py` and `scripts/process_stereo_pair.py` now share the validated
    `point_id,u1,v1,u2,v2` correspondence reader.
  - `src/module7/__init__.py`, `tests/test_object_measurement.py`, and
    `tests/test_io_utils.py`.
- **Rectangle implementation:** reconstructs four ordered corners, reports width and height as
  means of opposite Euclidean 3D edges, and checks opposite-edge agreement, planarity, and
  right-angle deviation.
- **Circle implementation:** reconstructs visible boundary landmarks, fits a least-squares
  circle in the recovered 3D plane, reports center/radius/diameter, and checks coplanarity and
  radial residuals. The planar circular-boundary assumption is recorded in every result.
- **Polygon implementation:** reconstructs ordered visible vertices and reports every adjacent
  Euclidean 3D edge length; it does not substitute a 2D bounding box. Planarity is reported and
  can be made a hard gate.
- **Invalid-geometry handling:** missing/duplicate IDs, non-metric poses, non-positive depth,
  insufficient parallax, reprojection failures, collinear circle landmarks, degenerate edges,
  and shape-quality threshold failures are rejected without writing a dimension result.
- **Claim classification:** Phase 3 software is `implemented` and `tested`. The rectangle workflow
  is experimentally complete with verified physical measurements but is not a successful stereo
  accuracy validation. Circle and polygon dimensions remain pending user data collection.
- **Date:** 2026-10-23.

#### Phase 3A — Rectangle physical validation

- **Status:** `CAPTURED — RECONSTRUCTED; PROVISIONAL PHYSICAL INTERVALS FAIL; VALIDATION NOT COMPLETE`.
- **Authorized scope:** rectangle only. Circle and polygon experiments have not started.
- **Prepared protocol:** `docs/rectangle_validation_protocol.md`.
- **Validated inputs to reuse:** calibration ID `module2-originals-module7-recompute`, portrait
  calibration frame `(4284, 5712)`, 9×6 internal corners, 25.0 mm square size, and the existing
  checkerboard-PnP pose workflow.
- **Supplied originals:** `data/physical_validation/IMG_7514.JPG` and `IMG_7515.JPG`. Both carry
  Apple iPhone 15 Pro Max metadata. `IMG_7514.JPG` was rotated 90 degrees clockwise into a
  derived portrait calibration frame; `IMG_7515.JPG` was already decoded in that frame. Originals
  were not modified.
- **Capture review:** the 9×6 checkerboard was detected in both views; all four card outer
  boundary corners were visible and reviewed. The same scene arrangement is present in both
  views, but still-image evidence cannot prove zero object motion independently.
- **Reconstruction:** `checkerboard_pnp` recovered a 44.6969976 mm metric baseline; all 4/4
  rectangle landmarks had positive depth and passed the 5 px point reprojection gate. Median
  object parallax was 1.8394634 degrees. The reconstructed image-order top edge is 51.4434472
  mm and the image-order side edge is 85.8989759 mm. Rectangle planarity RMS/max were 2.75263 /
  2.84431 mm; maximum right-angle deviation was 6.91857 degrees.
- **Evidence:** correspondences are in
  `data/physical_validation/IMG_7514_IMG_7515_free_admission_rectangle_correspondences.csv`;
  annotated images, stereo JSON, measurement JSON, and the evidence manifest are under
  `results/stereo_diagnostics/` and `results/object_measurements/`. The initial contour-extreme
  selection that failed the reprojection gate is preserved as an audit artifact.
- **Physical comparison:** user-reported long/short means are 87.40 mm and 49.40 mm. A
  provisional ±1.0 mm bound gives width interval 86.40–88.40 mm and height interval 48.40–50.40
  mm. The reconstructed image-order side compares to 87.40 mm with signed error −1.5010241 mm
  (1.7174189%) and falls 0.5010241 mm below its interval. The image-order top edge compares to
  49.40 mm with signed error +2.0434472 mm (4.1365329%) and falls 1.0434472 mm above its interval.
  The bound is provisional: 1 mm subdivisions and repeated-reading spread support it as a
  conservative physical-measurement bound, but rectangle endpoint alignment/setup photographs are
  unavailable. It is not stereo-system uncertainty.
- **Claim classification:** capture and reconstruction are `experimentally processed`; geometric
  validity gates passed, but physical accuracy validation is `not validated` because both
  provisional intervals fail and endpoint-measurement evidence is incomplete.
- **Second experiment:** `IMG_7516.JPG` and `IMG_7517.JPG` were both present, normalized by a
  90-degree clockwise derived copy, and processed with the same calibration and thresholds. The
  checkerboard was detected at 54/54 corners in both views; PnP RMS errors were 1.44438 px and
  1.55534 px. Card homography residuals were 1.81–3.49 px, so no definite relative motion was
  demonstrated. However, checkerboard-PnP recovered only a 6.0410615 mm baseline and the card
  median parallax was 0.669038 degrees. All 4/4 points had positive depth and point reprojection
  errors below 1.10 px, but rectangle quality rejected the result: opposite width/height edge
  disagreement was 24.1595% / 17.8049%, planarity RMS/max was 5.08290 / 5.95519 mm, and the
  maximum right-angle deviation was 21.9274 degrees. No accepted rectangle dimensions were
  produced. The raw diagnostic edge means (59.89516 mm and 95.43512 mm) are not measurements for
  validation. A later evidence review confirms that `IMG_7501.JPG`/`IMG_7502.JPG` show the FREE
  ADMISSION card and support the separately recorded ruler readings; this does not change the
  second experiment's failed geometry decision.
- **Second-experiment decision:** `NOT VALIDATED — RECTANGLE QUALITY GATE FAILED`. The evidence
  points primarily to insufficient camera displacement/parallax. The later ruler review supports
  the physical reference readings, but does not change the failed geometry decision; calibration,
  scale, pose, thresholds, and historical records were preserved.
- **Third experiment:** `EXPERIMENT COMPLETE — PHYSICAL MEASUREMENT VERIFIED; STEREO ACCURACY NOT
  VALIDATED`. The supplied `IMG_7519.JPG` and `IMG_7520.JPG` originals were preserved and
  processed at 4284×5712 decoded resolution. Both identify as Apple iPhone 15 Pro Max files with
  EXIF orientation 6; OpenCV decoded them directly into the portrait calibration frame, so no
  content rotation was applied. The calibrated 9×6 checkerboard was detected at 54/54 corners in
  both views. Checkerboard-PnP RMS errors were 1.10839 px and 2.21646 px, with a recovered metric
  baseline of 166.387025 mm and median card parallax of 17.073946 degrees.

  The four card correspondences were recorded in the required order and all four reconstructed
  points passed positive-depth, point-reprojection, planarity, right-angle, and opposite-edge
  geometry gates. The reconstructed short and long sides were 52.336899 mm and 92.973060 mm,
  respectively. These compare with the independent means 49.40 mm and 87.40 mm at +2.936899 mm
  (5.945140%) and +5.573060 mm (6.376499%); both are outside the provisional 1 mm intervals
  [48.40, 50.40] mm and [86.40, 88.40] mm.

  The scene-consistency review did not establish a stationary common scene. The checkerboard
  homography residual median/max were 3.891/8.593 px, while the four card-corner residuals were
  14.937–46.805 px; this screen is decisive only if the card and checkerboard are coplanar. A
  calibrated card-homography decomposition was also reviewed. The previously reported 12.345324°
  discrepancy used raw distorted pixels; after distortion-aware point normalization, the closest
  decomposition discrepancy was 12.959758°. With only four card corners and no independently known
  card-plane geometry, this is a pose/model warning, not an independent pose estimate or proof of
  card movement. A 1 px perturbation sensitivity simulation gave 10.55°/13.11°/15.68° 5th/median/
  95th-percentile discrepancies; this is diagnostic only and is not an endpoint uncertainty claim.

  Visual review confirms that the saved points refer to the same apparent outer card corners in both
  views: `top_left`, `top_right`, `bottom_right`, `bottom_left`. The image-order top/bottom horizontal
  edge is the shorter physical edge (52.336899 mm reconstructed), while the vertical side is the
  longer physical edge (92.973060 mm reconstructed). The 3D rectangle is internally coherent, but
  the stereo accuracy limitation remains.

  Ruler evidence is now verified: `IMG_7501.JPG` shows the FREE ADMISSION card's long horizontal
  edge with the zero reference, millimetre subdivisions, and both endpoints; `IMG_7502.JPG` shows
  the same card's short edge with the corresponding ruler scale and endpoints. These photographs
  support the repeated readings 87.0/88.0/87.2 mm and 49.0/49.8/49.4 mm, with means 87.40 mm and
  49.40 mm. The 1 mm subdivisions, endpoint alignment, perspective, and reading spread support
  retaining ±1.00 mm as a conservative physical uncertainty; this is not stereo-system
  uncertainty. Both stereo estimates remain outside the verified intervals, so this is a legitimate
  experimental accuracy limitation rather than changed ground truth. The earlier
  blocked-missing-originals record remains preserved as an audit file, and the first and second
  experiment records remain unchanged. No reprocessing defect was demonstrated and no recapture is
  requested.
  The validation record and evidence manifest are under
  `results/object_measurements/rectangle_third/` and `results/stereo_diagnostics/rectangle_third/`.

### Phase 3B — Marked yellow-lid circular-object validation

- **Authorization:** circle validation authorized by the user; polygon validation and Phase 4 remain
  out of scope.
- **Status:** `CAPTURED — CHECKERBOARD AND POINT-LEVEL STEREO GATES PASS; CIRCLE PLANARITY GATE REJECTED`.
- **Supplied originals:** `data/physical_validation/IMG_7543.JPG` and `IMG_7544.JPG` are preserved.
  Both identify as Apple iPhone 15 Pro Max at native 5712×4284 storage resolution; derived
  90-degree-clockwise copies were used to match the calibrated 4284×5712 portrait frame. Their
  full-frame Laplacian-variance diagnostics were 14.205890 and 13.962256. LensModel and FocalLength
  are absent from both EXIF records.
- **Checkerboard result:** 54/54 internal corners were detected in both views. Checkerboard-PnP RMS
  errors were 1.937996 px and 2.537212 px. The metric baseline was 29.038850 mm and checkerboard
  median parallax was 4.465225 degrees.
- **Marker correspondence result:** 14 black markers were visible in both views and matched in
  consistent clockwise order. Marker centers were not used as circle points. The actual outer-rim
  points were selected on marker-defined rays at the visible outermost rim. The first-pass rejected
  CSV and corrected CSV are both preserved; annotated diagnostics are under
  `results/stereo_diagnostics/circle_yellow_marked/`.
- **Rim reconstruction:** all 14 corrected points passed positive-depth and reprojection gates.
  Maximum reprojection errors were 1.940798 px and 1.933694 px; median rim parallax was 4.168084°;
  reconstructed depths ranged from 322.448297 to 334.273879 mm. However, 3D planarity RMS/max were
  2.641814/3.817464 mm, exceeding the existing max-planarity limit of 2.635175 mm. The existing
  `measure_circle` workflow therefore produced no accepted diameter.
- **Physical evidence:** the four supplied lid ruler originals are present and preserved under
  `data/physical_validation/` with native 4032×3024 storage pixels. `IMG_7531.JPG` supports a rounded
  horizontal outer-rim reading of approximately 100 mm and `IMG_7532.JPG` supports a rounded vertical
  outer-rim reading of approximately 100 mm. `IMG_7533.JPG` is diagonal qualitative corroboration only
  because angle and occlusion make its endpoints insufficiently unambiguous; the lower-quality
  `IMG_7539.JPG` is indeterminate and is not used quantitatively. The accepted physical reference is
  therefore `100.0 ± 2.0 mm` with interval `98.0–102.0 mm`, a conservative photographic measurement
  uncertainty rather than stereo-system uncertainty. The accepted spans refer to the outermost rim, not
  the inner recessed ring. The ruler zero mark is not visible in the accepted spans, so the result is
  documented as approximate rather than as sub-millimetre metrology. The earlier approximate 100 mm
  user report is preserved separately and was not used for scaling or optimization.
- **Physical-evidence record:**
  `results/object_measurements/circle_yellow_marked/IMG_7531_IMG_7532_IMG_7533_IMG_7539_lid_physical_measurement_evidence.json`.
- **Decision:** `MARKED STEREO PAIR PROCESSED; CIRCLE VALIDATION NOT ACCEPTED — PLANARITY QUALITY
  GATE`. The evidence manifest is
  `results/stereo_diagnostics/circle_yellow_marked/IMG_7543_IMG_7544_circle_validation_manifest.json`.
  No accepted stereo diameter exists, so no physical accuracy comparison or circle-validation pass is
  claimed. The physical diameter reference is documented provisionally, while the stereo result remains
  rejected independently of that reference.

#### Phase 3B planarity-gate audit

- **Implementation review:** `measure_circle` in `src/module7/object_measurement.py` fits a least-squares
  plane, computes `planarity_rms` and `planarity_max`, then fits the circle in that plane. With the
  pre-existing default `max_planarity_fraction=0.05`, it rejects when
  `planarity_max > 0.05 * fitted_radius`. The code reports RMS and maximum, but only maximum is a
  planarity rejection criterion. The separate circle-fit maximum residual is checked afterward.
- **Threshold calculation:** the corrected 14-point diagnostic fit has radius 52.703507 mm, so the
  documented gate is `0.05 × 52.703507 = 2.635175 mm`. The observed planarity RMS/max are
  2.641814/3.817464 mm. The rejection was caused by `planarity_max`, not by RMS. The circle-fit
  maximum residual was below the same reference scale in the diagnostic calculation, but it was not
  reached by the CLI because the planarity gate failed first.
- **Threshold provenance:** the 5% default is part of the Phase 3 implementation and deterministic
  tests/protocol established before this real marked-lid experiment. Module 7 has no initialized Git
  history, so an exact commit timestamp cannot be independently verified; no threshold was introduced
  or changed during this experiment. Implementation and diagnostic reporting are consistent.
- **3D residual review:** signed plane residuals show a structured pattern around the rim rather than
  one isolated bad point: `lid_rim_07` is +3.817464 mm, `lid_rim_13` is −3.786036 mm, and several
  neighboring points are also grouped on positive or negative sides. Leave-one-out analysis did not
  make the plane pass; removing any single point left the maximum above 3.56 mm. This does not prove
  movement or a wrong correspondence. It is consistent with low-parallax triangulation error, pose
  error, marker-to-outer-edge inference, or a raised/beveled rim whose selected visible boundary is not
  one planar circle.
- **Geometry sensitivity:** the 29.038850 mm baseline at roughly 330 mm depth produces only 4.168084°
  median rim parallax. A deterministic diagnostic simulation with independent Gaussian pixel noise on
  the saved rim coordinates gave median maximum planarity deviations of approximately 3.98, 4.23, 4.95,
  and 6.53 mm for 0.25, 0.5, 1.0, and 2.0 px noise, respectively. A separate 1–2 px checkerboard-
  corner perturbation simulation left the median maximum deviation near 3.82–3.84 mm. These are
  sensitivity analyses, not measured uncertainties, but they show that the low-parallax geometry can
  reasonably sustain the observed failure.
- **Physical evidence at time of the planarity audit:** the lid ruler photographs had not yet been
  supplied, so the audit correctly treated the approximate 100 mm report as provisional. The later
  evidence review is recorded above and does not alter the audit, reconstruction, or rejection.
- **Diagnostic decision:** no confirmed implementation defect or demonstrated correspondence identity
  defect was found. The current classification is `UNRESOLVED EXPERIMENTAL GEOMETRY — LOW PARALLAX,
  POSE/EDGE-LOCATION SENSITIVITY, AND POSSIBLE RAISED-RIM MODEL AMBIGUITY`. No threshold relaxation,
  coordinate tuning, or recapture request was made in this audit.
- **Supplied originals:** `data/physical_validation/IMG_7540.JPG` and `IMG_7541.JPG` are preserved.
  Both identify as Apple iPhone 15 Pro Max, EXIF orientation 1, with native PIL size 5712×4284 and
  OpenCV decoded size 5712×4284. The calibrated Module 2/Module 7 record uses the portrait frame
  4284×5712, so derived 90-degree-clockwise processing copies were created; the originals were not
  changed. LensModel and FocalLength are absent from both EXIF records, so active-lens identity is
  supported by phone/model and calibrated frame compatibility, not a newly recorded lens tag.
- **Image quality:** the checkerboard is visually detectable and both runs have similar full-frame
  Laplacian-variance sharpness scores (18.751858 and 20.747802). These scores are only image-quality
  diagnostics, not an accuracy claim.
- **Checkerboard result:** the existing `scripts/process_stereo_pair.py --pose-method
  checkerboard_pnp` workflow detected 54/54 internal corners in both views. Per-view PnP RMS errors
  were 1.609630 px and 2.552749 px. The recovered metric baseline was 109.650619 mm; checkerboard
  triangulation recovered 54/54 valid positive-depth points with median parallax 15.108784 degrees.
  The saved record, auto-generated checkerboard CSV, and diagnostic image are under
  `results/object_measurements/circle_yellow/` and `results/stereo_diagnostics/circle_yellow/`.
- **Lid review:** the outermost lid rim and a concentric inner rim are visible in both views, and
  both objects appear visually stationary on the support. The yellow perimeter is smooth and lacks
  8–16 uniquely identifiable physical landmarks. Therefore no lid correspondence CSV was created,
  no lid parallax was reported, and no circle triangulation or diameter fit was run. Assigning equal
  angular positions on the two projected ellipses would not establish physical correspondence.
- **Physical measurement:** the approximately 100 mm user report remains secondary/pending because
  the uncertainty is not finalized and no lid-specific ruler photographs were located in the Module 7
  workspace. Existing `flashcard_ruler*.JPG` files are evidence for the earlier flashcard, not this lid.
- **Decision:** `VALID STEREO PAIR FOR CHECKERBOARD POSE ONLY; CIRCLE VALIDATION BLOCKED`. The full
  evidence manifest is `results/stereo_diagnostics/circle_yellow/IMG_7540_IMG_7541_circle_evidence_manifest.json`.
  The minimum justified improvement is a controlled repeat with 8–16 small removable markers just
  inside the perimeter (or a circular object with natural landmarks), plus at least three measured
  outer-diameter readings and ruler photographs showing zero, units, and endpoints.
- **Existing implementation:** `measure_circle` in `src/module7/object_measurement.py` fits a
  least-squares circle in the recovered 3D boundary plane and reports metric radius/diameter. It
  requires metric triangulation first and rejects invalid depth, insufficient parallax,
  non-coplanar boundary points, rank-deficient fits, and excessive radial residuals. The existing
  CLI is `scripts/measure_object.py --shape circle`; stereo processing remains
  `scripts/process_stereo_pair.py --pose-method checkerboard_pnp`.
- **Required user capture:** one rigid, flat circular object with a clearly visible perimeter;
  the stationary 9×6 checkerboard; two full-resolution views from laterally separated phone
  positions; repeated independent diameter readings and uncertainty; and ruler evidence showing
  the measured endpoints and zero reference.
- **Correspondence plan:** identify 8–16 perimeter points distributed around the visible boundary,
  in clockwise order, using natural edge features or small removable marks just inside the edge to
  make the same physical boundary locations identifiable. Do not guess coordinates and do not use
  only an image bounding box or one apparent diameter.
- **Processing gate:** wait for the user's originals and measurement record. Then verify metadata,
  checkerboard detection, camera pose, baseline/parallax, correspondence identity, positive depth,
  reprojection, planarity, and circle-fit residuals before reporting a diameter.

### Phase 3C — Polygon edge-length validation

- **Authorization:** polygon validation authorized by the user; Phase 4 remains out of scope.
- **Status:** `EXPERIMENT COMPLETE — PHYSICAL MEASUREMENTS DOCUMENTED; STEREO TRIANGLE ACCURACY NOT VALIDATED`.
- **Implementation reviewed:** `src/module7/object_measurement.py::measure_polygon_from_stereo`
  reconstructs metric landmarks first through the existing triangulation checks, then
  `measure_polygon` reports the Euclidean distances between adjacent vertices in the supplied boundary
  order. `scripts/measure_object.py --shape polygon` loads the saved metric stereo pose and polygon
  correspondence CSV. The optional `--require-planar` flag makes the polygon planarity limit a hard
  gate; planarity is otherwise reported as a diagnostic.
- **Selected experiment:** a rigid, flat cardboard triangle with three visible vertices was supplied
  and processed. The earlier missing-originals audit is retained as historical provenance.
- **Physical evidence required:** measure every visible edge at least three times independently, record
  every reading in millimetres, ruler resolution, uncertainty rationale, and measurement photographs
  showing the zero/reference mark and both exact endpoints. Physical measurements are comparison data
  only and must not rescale or optimize the stereo result.
- **Capture requirements:** keep the triangle/pentagon and the 9×6, 25 mm checkerboard rigid and
  stationary. Use the calibrated iPhone 15 Pro Max with fixed settings, full resolution, locked focus
  where available, and no zoom change. Capture two overlapping views after an approximately 80–120 mm
  lateral phone displacement while retaining the board and all polygon vertices. Checkerboard-PnP, not
  an assumed phone-body displacement, supplies the metric relative pose.
- **Correspondence requirements:** after image inspection, record the same physical vertices in both
  portrait-coordinate images in clockwise order (`v0,v1,v2` for a triangle or `v0`–`v4` for a
  pentagon). Use the actual corner positions, not nearby marker centers, bounding-box extrema, or
  guessed coordinates.
- **Planned quality review:** verify 54 checkerboard corners in both views, baseline, object parallax,
  positive depth, reprojection errors, vertex identity, planarity, and edge validity before measuring.
  Reconstruct all vertices first, then report every adjacent 3D edge. Compare each result with the
  independently measured edge mean and interval; geometry-gate success is not physical validation.
- **Protocol:** `docs/polygon_validation_protocol.md`.
- **Capture and metadata:** `IMG_7548.JPG` and `IMG_7549.JPG` are preserved at native 5712×4284
  storage resolution. Both identify as iPhone 15 Pro Max with EXIF orientation 6. The untouched
  OpenCV raw frames match the calibrated 4284×5712 `(width,height)` frame; derived rotated copies were
  used only for visual inspection. Full-frame Laplacian variances were 15.797173 and 14.545116.
- **Checkerboard-PnP:** 54/54 internal corners were detected in both views. PnP RMS errors were
  1.603085 px and 2.428876 px. The recovered metric baseline was 37.879812 mm; checkerboard median
  parallax was 5.321177° and all 54 checkerboard points passed positive-depth/reprojection checks.
- **Triangle vertices:** `v0` is the left/top corner, `v1` the right/top corner, and `v2` the lower
  corner in the normalized inspection frame, giving a consistent clockwise order. Correspondences were
  selected from the visible outer contour and saved in
  `data/physical_validation/IMG_7548_IMG_7549_triangle_vertex_correspondences.csv`.
- **Triangle reconstruction:** the three vertices reconstructed to metric 3D with positive depth.
  Median triangle parallax was 4.423674°. Maximum vertex reprojection errors were 4.986292 px and
  4.973531 px, both below the existing 5 px gate. Reconstructed edge lengths were 150.497091 mm
  (`v0-v1`), 144.814945 mm (`v1-v2`), and 152.796371 mm (`v2-v0`). The three-point planarity residual
  is effectively zero by construction and is not an independent flatness test; right-angle and
  opposite-edge checks do not apply to a triangle.
- **Physical edge mapping:** ruler evidence maps `v0-v1` to side 1 (110.00 mm, `IMG_7545.JPG`),
  `v1-v2` to the base (140.00 mm, `IMG_7546.JPG`), and `v2-v0` to side 2 (136.00 mm,
  `IMG_7547.JPG`). The three repeated readings and provisional ±1.00 mm intervals are preserved;
  they were not used to scale or optimize the reconstruction.
- **Physical comparison:** signed errors were +40.497091 mm (+36.815538%) for side 1,
  +4.814945 mm (+3.439246%) for the base, and +16.796371 mm (+12.350272%) for side 2. None of the
  reconstructed edges falls inside its provisional ±1 mm interval. Geometry gates passed, but physical
  accuracy is not validated.
- **Evidence records:**
  `results/object_measurements/polygon_phase3c/IMG_7548_IMG_7549_triangle_validation.json`,
  `results/object_measurements/polygon_phase3c/IMG_7548_IMG_7549_triangle_measurement.json`, and
  `results/stereo_diagnostics/polygon_phase3c/IMG_7548_IMG_7549_triangle_vertex_correspondences.png`.
  The earlier blocked-input audit remains at
  `results/object_measurements/polygon_phase3c/IMG_7548_IMG_7549_blocked_missing_originals_audit.json`.

### Phase 3C diagnostic investigation — completed

- **Scope:** read-only review of `IMG_7545.JPG`–`IMG_7547.JPG`, `IMG_7548.JPG`–`IMG_7549.JPG`,
  the saved vertex correspondence, calibration, checkerboard-PnP pose, triangulation, and
  validation records. No input, calibration, pose, scale, threshold, or selected coordinate was
  changed.
- **Ruler evidence:** `IMG_7545.JPG` supports the side-1/`v0-v1` mapping and approximate 110 mm
  reading; `IMG_7546.JPG` supports the base/`v1-v2` mapping and approximate 140 mm reading; and
  `IMG_7547.JPG` supports the side-2/`v2-v0` mapping and approximate 136 mm reading. The repeated
  109/110/111, 140/141/139, and 135/136/137 mm values remain user-reported repeated readings.
  The conservative ±1.00 mm value remains provisional physical-measurement uncertainty, not stereo
  uncertainty.
- **Coordinate and pose audit:** checkerboard re-detection returned 54/54 corners and agreed with
  the saved correspondence to less than 0.000001 px. Re-estimated PnP changed the baseline by
  0.000003 mm and the relative rotation difference was 0.0 degrees. Re-triangulation reproduced
  the saved triangle vertices within floating-point tolerance. This confirms implementation
  consistency, not physical accuracy.
- **Geometry audit:** all three vertices have positive depth and pass the existing 5 px point-level
  reprojection gate. `v1` is close to that gate at 4.986292 px and 4.973531 px. Closest calibrated
  ray separations are 0.371973 mm (`v0`), 1.136110 mm (`v1`), and 0.186204 mm (`v2`). Three-point
  planarity is mathematically automatic and was not treated as an independent accuracy test.
- **Sensitivity audit:** deterministic ±0.5/±1.0 px one-coordinate perturbations show the largest
  edge response at `v1`; several perturbations also cross the existing quality mask because the
  point is near the reprojection limit. Seeded checkerboard-coordinate simulations are recorded as
  diagnostic sensitivity only, not as measured uncertainty.
- **Evidence records:**
  `results/object_measurements/polygon_phase3c/IMG_7548_IMG_7549_triangle_diagnostic_investigation.json`
  and
  `results/stereo_diagnostics/polygon_phase3c/IMG_7548_IMG_7549_triangle_evidence_manifest.json`.
- **Final diagnostic classification:** no correction is justified by current evidence. The
  experiment remains physically unvalidated; a future controlled recapture may be considered only
  after separate authorization, but no recapture is requested in this investigation.

### Phase 3 completion audit — Question 1 readiness

- **Audit result:** the local standalone Question 1 webpage requirement is fulfilled by Phase 3D.
  The calibrated-stereo object-measurement core is implemented and tested, the real calibration/
  stereo evidence is preserved, and `app.py` plus `src/module7/webapp/` expose the required
  demonstrations through the established provider contract. Public dashboard integration remains
  separately authorized.
- **Depth-before-dimension requirement:** satisfied in the core path. `reconstruct_landmarks`
  performs calibrated triangulation, metric/positive-depth, parallax, and reprojection checks before
  `measure_rectangle`, `measure_circle`, or `measure_polygon` calculates dimensions.
- **Shape implementation status:** rectangle width/height, planar 3D circle diameter, and ordered
  polygon edge lengths are implemented and covered by the 42 passing automated tests. This is
  an `implemented`/`tested` claim, not a claim that every real shape experiment passed.
- **Real evidence status:** Phase 2B flashcard width is physically validated only under the explicit
  equivalent-rectangular-edge assumption. Phase 3 rectangle experiments are not physically
  validated; the marked circle experiment is rejected by the existing planarity gate; and the
  triangle is geometrically processed but physically unvalidated. Rejected or ungated values are not
  accepted measurements.
- **Calibration/methodology:** Module 2 original photographs were recomputed through the Module 7
  calibration workflow. The 9×6, 25 mm checkerboard, intrinsics, distortion, pose provenance,
  metric triangulation, diagnostic images, correspondence CSVs, and measurement records are
  preserved. Exact active-lens EXIF fields are absent.
- **Confirmed limitations:** physical ruler uncertainty is not stereo uncertainty; manual endpoint
  and perimeter localization are not formally propagated; nonzero calibration/PnP residuals remain;
  and passing geometry gates does not imply physical accuracy.
- **Resolved local blocker:** the Question 1 webpage now uses the existing core/evidence paths,
  exposes rectangle/circle/polygon paths and depth/3D diagnostics, shows pending/rejected statuses
  honestly, and has page-provider/smoke coverage. No algorithm, threshold, calibration, ground
  truth, or historical evidence was changed.
- **Audit record:** `results/object_measurements/phase3_completion_audit.json`.

### Phase 3D — Standalone Question 1 webpage

- **Status:** `IMPLEMENTED AND TESTED — USER REVIEW PENDING`.
- **Entry point:** `app.py`; launch with `streamlit run app.py` from `Module_7/`.
- **Provider contract:** `src/module7/webapp/_page.py`, `registry.py`, `pages.py`, and `shell.py`
  implement the established `module_label`, `page_label`, `order`, `render`, and `get_pages()`
  interface.
- **Demonstrations:** rectangle, circle, and polygon pages load genuine saved Module 7 artifacts,
  original stereo images, and diagnostic images. Rejected circle geometry and failed rectangle/
  triangle physical comparisons remain explicitly labeled; missing or malformed evidence renders
  a pending/error state rather than fabricated output.
- **Tests:** 42 automated tests pass, including the original 33 core tests plus provider,
  artifact-integrity, malformed-evidence, application-import, and Streamlit AppTest smoke checks.
  `python3 -m compileall -q src scripts tests` also passes.
- **Scope boundary:** no calibration, pose, reconstruction, threshold, correspondence, physical
  measurement, dashboard, report, commit, push, or Phase 4 work was performed.

### Phase 3D audit — repository, webpage alignment, Git, and deployment readiness

- **Status:** `AUDIT COMPLETE — ALIGNMENT IMPLEMENTED; PUBLICATION REVIEW PENDING`.
- The discrepancy bullets below preserve the pre-alignment baseline for traceability; the
  implementation update below records the authorized corrections.
- **Previous-module conventions confirmed:** Modules 2, 3, 4, and 5-6 use independent source-
  layout repositories, thin standalone `app.py` entry points, module-local page providers, the
  structural page contract, vendored `csc8830-ui` 0.6.0 design files, generated Streamlit theme
  configuration, public-copy/design tests, optional summary providers, and AppTest smoke coverage.
  The root/deployment dashboards adapt page objects structurally.
- **Historical Module 7 discrepancies:** before this task there was no Module 7 Git repository,
  vendored design package, generated theme, or design/public-copy coverage, and the shell used
  bespoke CSS. The provider contract was structurally compatible; the update below addresses the
  authorized UI gaps without creating Git state.
- **Historical public-copy findings:** the pre-alignment webapp exposed repository paths and
  internal phase wording and used em/en dash punctuation. Current rendering removes these while
  retaining academic validation failures, uncertainty, rejected geometry, and pending states.
- **Historical dependency gap:** the pre-alignment dependency used `streamlit>=1.36`; it is now
  aligned to `streamlit>=1.49,<2` with the generated theme configuration.
- **Evidence/deployment findings:** the page directly references approximately 61 MB of raw
  `data/physical_validation/` captures and approximately 758 MB of generated diagnostics. The
  current ignore rules do not define a small, user-approved public evidence bundle, and no path
  can be considered deployable until its exact file is tracked and verified with `git ls-files` in
  the future Module 7 repository.
- **Documentation correction:** `docs/architecture.md` and README now describe the implemented
  core/web boundary, standalone launch, proposed evidence bundle, and optional dashboard workflow.
- **Privacy/integrity:** no secret-like text or credential filenames were found by the workspace
  scan. Original smartphone and ruler photographs still require explicit user review before any
  public tracking or deployment decision.
- **Proposed tracking categories:** track approved source/configuration, academic documentation,
  tests, and a small real Q1 evidence bundle; keep full raw captures, working crops, large derived
  diagnostics, room videos, and unapproved private material local unless explicitly approved.
  Never blindly add all of `data/` or `results/`.
- **Required approvals before implementation:** public/private evidence selection, future GitHub
  repository location, design-system alignment, and the later root/deployment dashboard changes.
  This audit did not initialize Git, create a branch, modify any earlier module or dashboard,
  commit, push, deploy, generate reports, or begin Phase 4.

### Phase 3D UI alignment and evidence preparation update

- **Status:** `IMPLEMENTED AND TESTED — PROPOSED PUBLIC BUNDLE; PUBLICATION APPROVAL PENDING`.
- **Design integration:** vendored `csc8830-ui` version 0.6.0 under
  `src/module7/webapp/design/`; generated `.streamlit/config.toml`; replaced the bespoke shell
  with the shared standalone shell while preserving `module7.webapp.pages.get_pages()`.
- **Public copy:** removed displayed evidence paths, development phase wording, and prohibited
  dash punctuation. Academic calibration, depth, triangulation, uncertainty, rejected geometry,
  and physical-accuracy limitations remain visible. Saved records are not modified.
- **Proposed evidence bundle:** `data/proposed_public_demo/manifest.json` records 29 files
  totaling 2,347,343 bytes (approximately 2.35 MB): seven compact path-free evidence records, fourteen
  resized stereo-view images, and seven selected diagnostic display images. The manifest is
  explicitly `publication_approved: false`; original captures and full result records remain
  separate.
- **Documentation:** README and architecture documentation now describe the implemented core/web
  boundary, standalone launch, design-kit alignment, proposed bundle, and optional future
  dashboard mounting. No dashboard or deployment change was made.
- **Tests:** the original 42 tests remain passing; the expanded suite passes 60 tests, including
  design/config parity, public-copy restrictions, standalone shell checks, manifest completeness,
  and missing/malformed evidence behavior. No Git operation was performed.

### Final standalone UI and public evidence review

- **Status:** `LOCAL REVIEW COMPLETE - PUBLICATION APPROVAL PENDING`.
- **Rendered pages:** AppTest exercised Overview, Rectangle measurements, Circle measurements,
  and Polygon measurements without exceptions. Navigation, units, shared shell components,
  image-comparison sections, metrics, result sections, and honest rejected/pending status banners
  were present. The resized evidence contact sheets showed the intended checkerboard and object
  for all seven experiments. A browser connector was unavailable in this environment, so no
  browser screenshot or viewport-overflow assertion was made.
- **Evidence inventory:** every one of the 29 proposed files is listed with type, byte size,
  page association, source experiment, privacy review, essentiality, and publication recommendation
  in `docs/public_evidence_review.md` and the manifest metadata. No reviewed derivative showed a
  face or explicit personal identifier; workspace/background objects remain visible and require
  owner review. Resizing is not treated as anonymization.
- **Clean-clone result:** source plus only `data/proposed_public_demo/` renders Overview and all
  three shape pages without exceptions. Every curated experiment selection was exercised. The
  runtime no longer references the 36 full local files under `data/` and `results/`; the original
  evidence remains preserved outside the runtime bundle.
- **Publication blocker:** image-by-image owner review is still required. The bundle remains
  local-only with `publication_approved: false`; no publication or Git action was performed.
- **Visual review materials:** local-only gallery at `local_review/proposed_public_evidence_gallery.html`
  and contact sheet at `local_review/proposed_public_evidence_contact_sheet.jpg`. These are excluded
  from the public navigation and `.gitignore`.
- **Metadata review:** compact records contain no absolute paths, credentials, location fields,
  or unique device identifiers. Original capture filename mentions were removed from derived JSON;
  the iPhone model remains only as calibration-compatibility provenance.
- **Ignore-policy finding:** `.gitignore` now explicitly excludes `data/physical_validation/`,
  `results/stereo_diagnostics/`, and `local_review/`. Those approximately 61 MB and 758 MB trees
  remain local-only by decision, and the review outputs cannot be staged accidentally by default.

## Testing Status

- **Tests executed:**
  - repository file discovery with `rg --files`;
  - read-only inspection of root/module governance and architecture files;
  - read-only Git repository boundary, branch, status, and remote inspection for existing repos;
  - documentation/reference inspection;
  - `pytest -q` in `Module_7/`;
  - `python3 -m compileall -q src scripts tests`;
  - Module 7 calibration CLI run on the original Module 2 calibration images;
  - Module 7 calibration diagnostics CLI run on the recomputed record;
  - read-only Module 2 JSON/report/image metadata comparison.
  - Real `IMG_7485.JPG`/`IMG_7486.JPG` capture-quality review, automatic checkerboard detection,
    portrait-frame compatibility conversion, `checkerboard_pnp` processing, and stereo diagnostics.
  - Independent flashcard endpoint correspondence recording, saved-pose triangulation, annotated
    endpoint review, and updated comparison against a user-confirmed 96.70 mm measurement with
    the previously stated ±1 mm ruler uncertainty.
  - Phase 3C triangle original inspection, ruler-evidence review, checkerboard-PnP processing,
    three-corner correspondence verification, metric triangulation, polygon edge measurement, and
    independent physical comparison.
- **Tests passed:** 54 automated tests (the original 42 plus design/config, public-copy, shell,
  and evidence-bundle checks); Python compilation;
  Module 7 accepted 16/16 original Module 2 images and produced a valid native calibration
  record; Module 2 and Module 7 calibration records agree closely; Phase 0/Phase 1
  documentation consistency checks; real pair processing recovered 54/54 valid checkerboard
  points with positive depth and sub-pixel reprojection diagnostics.
  Phase 3 rectangle, circle, polygon, correspondence-I/O, serialization, invalid-geometry, and
  standalone webpage tests also pass. Streamlit AppTest smoke checks pass for all three shape
  pages; rejected and pending states render without application exceptions.
- **Tests failed:** the first direct run on the unmodified landscape files was correctly rejected
  because their `(5712, 4284)` decoded size did not match the portrait `(4284, 5712)` calibration
  record. The documented derived portrait-frame run succeeded.
- **Tests blocked/pending:** controlled rectangle recapture or improved endpoint/measurement
  evidence after both provisional physical intervals failed, independently measured camera-center baseline for the essential-matrix
  cross-check, clean-install verification, room validation, and deployment smoke tests. Dashboard
  and deployment are intentionally deferred to separately authorized work.

## Git Status

The workspace root is not a Git repository. Existing independent repositories were inspected:

| Repository | Verified branch/status at discovery | Remote | Module 7 relevance |
| --- | --- | --- | --- |
| `Module_2/` | `main`, clean, tracking `origin/main` | `https://github.com/minnocent12/csc8830-module-2.git` | Architecture/reference only |
| `Module_3/` | `main`, clean, tracking `origin/main` | `https://github.com/minnocent12/csc8830-module-3.git` | Architecture/reference only |
| `Module_4/` | `main`, clean, tracking `origin/main` | `https://github.com/minnocent12/csc8830-module-4.git` | Architecture/reference only |
| `Module_5-6/` | `main`, clean, tracking `origin/main` | `https://github.com/minnocent12/csc8830-module-5-6.git` | Closest multi-view/video reference |
| `csc8830-dashboard/` | `main`, one pre-existing untracked `AGENTS.md` and one pre-existing untracked `CLAUDE.md` | `https://github.com/minnocent12/csc8830-dashboard.git` | Deployment reference; not modified |
| `csc8830-ui/` | `main`, clean, tracking `origin/main` | `https://github.com/minnocent12/csc8830-ui.git` | UI reference only |

For Module 7 itself:

- **Repository location:** `UNVERIFIED — USER MUST CHECK`; no `.git` directory exists yet.
- **Branch:** `UNVERIFIED — USER MUST CHECK`; no Module 7 repository exists yet.
- **Commit SHA:** `UNVERIFIED — USER MUST CHECK`.
- **Working tree state:** the directory is a Phase 2 workspace, not a verified Git worktree.
- **Pushed:** no Module 7 commit or push was performed.
- **Governance status:** Phase 0/Phase 1 governance and design files are present locally; whether they are tracked
  or excluded in a future Module 7 repository is not yet decided.

The two pre-existing untracked governance files in `csc8830-dashboard/` were not touched.

### Local Git initialization and staging review

- **Status:** `LOCAL REPOSITORY INITIALIZED; STAGING VALIDATED; COMMIT PENDING USER APPROVAL`.
- **Repository:** independent Git repository at `Module_7/`; active branch is
  `task/module-7-initial-repository`. The Assignments root and previous module repositories were
  not modified. No remote, commit, push, or deployment exists.
- **Evidence approval:** the user approved exactly the 21 reviewed display images and seven compact
  records for repository inclusion. The manifest records `publication_approved: true`; this does
  not authorize publication or deployment.
- **Integrity:** all 29 bundle files are present, referenced assets match their recorded hashes,
  and the manifest total is 2,347,455 bytes. No raw captures, uncurated diagnostics, local review
  outputs, secrets, or generated caches are in the staging allowlist.
- **Staged result:** 107 files totaling 2,859,227 bytes are staged. This includes exactly 21
  approved images, 7 compact records, and 1 manifest. No full-resolution originals, uncurated
  diagnostics, local review outputs, secrets, or private paths are staged.
- **Validation:** `git diff --cached --check` passes; all manifest hashes match; `pytest -q`
  passes 60 tests; Python compilation passes; and the headless Streamlit smoke check returns HTTP
  200. The staged contents are ready for user review before the first commit.

## Next Agent Handoff

**If another agent takes over:**

1. Read the root governance files: `../AGENTS.md`, `../GIT_WORKFLOW.md`, and `../DEPLOYMENT.md`.
2. Read the Module 7 governance files: `AGENTS.md`, `CLAUDE.md`, and `GIT_WORKFLOW.md`.
3. Read `MODULE_7_ASSIGNMENT_QUESTIONS.md` and `MODULE_7_ASSIGNMENT_INSTRUCTIONS.md`.
4. Read `IMPLEMENTATION_PLAN.md`.
5. Read this `IMPLEMENTATION_STATUS.md`.
6. Inspect the files listed as completed before repeating any work.
7. Confirm user approval and the current phase before implementing anything.
8. Continue from the next incomplete task; do not begin Phase 4 room measurement without
   explicit approval and the required real object/room evidence.

### Exact next step for Phase 3D

Review the proposed evidence images and decide which, if any, may eventually be made public. The
bundle is local-only and marked `publication_approved: false`; no Git repository, dashboard
integration, deployment, report generation, or Phase 4 work is authorized by this task.
