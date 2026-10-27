# CSc 8830 Module 7 — Calibrated Stereo, Uncalibrated Stereo, and Room Measurement

Module 7 implements the reusable calibration and sequential-stereo depth foundation for one
smartphone camera, shape-specific object dimension estimators, and a standalone Question 1
Streamlit demonstration. Real experiments remain visible with their evidence-backed validation
statuses; software completeness does not upgrade a failed physical-accuracy experiment.

Read the requirements in
[`MODULE_7_ASSIGNMENT_QUESTIONS.md`](MODULE_7_ASSIGNMENT_QUESTIONS.md), the submission rules
in [`MODULE_7_ASSIGNMENT_INSTRUCTIONS.md`](MODULE_7_ASSIGNMENT_INSTRUCTIONS.md), the technical
design in [`docs/architecture.md`](docs/architecture.md), and the current handoff record in
[`IMPLEMENTATION_STATUS.md`](IMPLEMENTATION_STATUS.md).

## Phase 2 implementation

- `src/module7/calibration.py`: checkerboard detection, multi-view intrinsic calibration,
  reprojection-error reporting, and JSON serialization.
- `src/module7/stereo_geometry.py`: calibrated correspondence validation, essential-matrix
  relative pose, explicit metric-scale attachment, checkerboard `solvePnP` fallback, sequential
  rectification, projection, and sparse triangulation.
- `src/module7/depth_estimation.py`: the theoretical rectified formula `Z=fB/d`, triangulated
  camera-1 forward depth, validity masks, and summaries.
- `src/module7/object_measurement.py`: metric 3D landmark gating plus rectangle width/height,
  fitted 3D-circle diameter, and visible polygon-edge measurements.
- `src/module7/io_utils.py`: image loading, BGR/channel validation, image-size checks, and
  NumPy-safe JSON I/O, including the shared correspondence CSV reader.
- `src/module7/visualization.py`: non-mutating correspondence and reprojection diagnostics.
- `scripts/run_diagnostics.py`: validates and summarizes saved calibration/stereo records
  without inventing or re-running experimental values.
- `scripts/measure_object.py`: applies the existing saved metric stereo pose and calibration to
  a user-supplied landmark CSV, then writes an auditable shape-measurement record.

The essential matrix supplies translation direction only. Metric reconstruction requires a
positive measured displacement between camera centers, or a metric checkerboard pose. The
`scale_source` field records the source of that scale. An optional baseline uncertainty is
carried into the result as relative scale uncertainty, and triangulation refuses to report a
metric result when scale is absent.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

The runtime dependencies are Python, OpenCV, NumPy, and Streamlit. The Question 1 web page reads
the genuine saved Module 7 evidence records and uses the same calibration/stereo outputs as the
CLI; it does not maintain a second geometry pipeline.

## Standalone Question 1 webpage

Install the project and launch the local Streamlit application from the Module 7 directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
streamlit run app.py
```

The page provider is `module7.webapp.pages.get_pages()` and exposes Overview, Rectangle
measurements, Circle measurements, and Polygon measurements. The pages display the original
stereo views, saved annotated correspondences, calibration/PnP metadata, metric 3D points, depth,
shape dimensions, physical comparisons, and the original validation status.

The bundled examples are real saved experiments. The flashcard width is shown as physically
validated only under its documented equivalent-rectangular-edge assumption. The FREE ADMISSION
rectangle and cardboard triangle retain their physical-accuracy failures. The yellow-lid circle
page explicitly shows that no accepted diameter was produced because the planarity gate failed.
Missing or malformed evidence is shown as pending/error rather than replaced with invented values.

The Module 7 page provider is standalone. It is not yet wired into the shared course dashboard;
dashboard integration is a later authorized phase. The vendored `csc8830-ui` 0.6.0 package and
generated `.streamlit/config.toml` provide the same shell and theme conventions used by the
earlier modules.

## Proposed public evidence bundle

`data/proposed_public_demo/manifest.json` describes the compact runtime bundle containing
resized stereo views, selected diagnostic images, and compact path-free JSON records for the real
rectangle, circle, and triangle experiments. The user approved the reviewed bundle for repository
inclusion; no deployment has been performed. The original captures and full result records remain
separate and unchanged.
The detailed local inventory and clean-clone audit is recorded in
[`docs/public_evidence_review.md`](docs/public_evidence_review.md).

The standalone pages require only this curated bundle at runtime. They do not require the original
full-resolution captures or local result directories. The bundle is approved for the authorized
local repository staging review; no remote repository or deployment has been created.

## Optional shared-dashboard integration

The standalone app is the grading entry point for this module. After separate approval, a parent
directory can mount the provider in the existing dashboard pattern:

```bash
cd /path/to/Assignments
python -m pip install -e Module_7
streamlit run csc8830-dashboard/app.py
```

The dashboard registry would import `module7.webapp.pages.get_pages()` as a structural provider.
The deployment mirror would additionally need the documented Module 7 source-sync case and the
approved evidence bundle. This task does not edit the dashboard or deploy.

## Deterministic tests

Run the software-only checks with:

```bash
pytest -q
python scripts/run_geometry_tests.py
python3 -m compileall -q src scripts tests
```

The tests use deterministic synthetic observations only to verify equations, validation,
serialization, calibration behavior, pose recovery, scale handling, rectification, and
triangulation. They are not physical camera validation.

## Real checkerboard calibration

The existing Module 2 real checkerboard images were processed directly by the Module 7 script;
see [`results/calibration/module2_reuse_provenance.md`](results/calibration/module2_reuse_provenance.md).
For a future camera/lens/resolution condition, place real checkerboard images in
`data/calibration/` and record the measured square size. The script detects usable views and
fails if no valid observations are available; it never creates placeholder camera parameters.

```bash
python scripts/run_calibration.py \
  --input-dir data/calibration \
  --pattern-cols 9 --pattern-rows 6 \
  --square-size 25 --square-unit mm \
  --output results/calibration/phone_calibration.json
```

The JSON record contains the image size, target geometry, intrinsic matrix, distortion
coefficients, accepted source-image identifiers, calibration flags, and overall/per-view
reprojection errors. The values become experimental only after the user reviews the real run.

## Real sequential stereo processing

For the first Stage B validation, keep the 9×6 calibration checkerboard visible in both views.
The preferred path is now `checkerboard_pnp`: it automatically detects and indexes the same 54
corners in both images, derives metric relative pose from the known 25 mm board, and does not
require manually guessed pixel coordinates. It can also save the generated correspondence CSV.

```bash
python scripts/process_stereo_pair.py \
  --pose-method checkerboard_pnp \
  --calibration results/calibration/module2_originals_module7_recomputed.json \
  --view1 data/stereo_pairs/view1.jpg \
  --view2 data/stereo_pairs/view2.jpg \
  --auto-correspondences-output data/stereo_pairs/checkerboard_correspondences.csv \
  --output results/object_measurements/checkerboard_stereo_pair.json \
  --diagnostic-image results/object_measurements/checkerboard_correspondences.jpg
```

The existing essential-matrix path remains available for arbitrary verified landmarks. It
requires a correspondence CSV with columns `point_id,u1,v1,u2,v2` and a measured baseline between
optical camera centers, not phone-body edges:

```bash
python scripts/process_stereo_pair.py \
  --calibration results/calibration/phone_calibration.json \
  --view1 data/stereo_pairs/view1.jpg \
  --view2 data/stereo_pairs/view2.jpg \
  --correspondences data/stereo_pairs/correspondences.csv \
  --baseline 0.12 --baseline-unit m \
  --baseline-uncertainty 0.002 \
  --output results/object_measurements/stereo_pair.json \
  --diagnostic-image results/object_measurements/correspondences.jpg
```

The processing path validates calibration and image dimensions, estimates pose from calibrated
correspondences or checkerboard PnP, attaches metric scale, checks parallax and depth signs,
computes reprojection errors, rectifies the pair, triangulates points in camera 1's coordinate
frame, and writes a provenance-bearing JSON record. Invalid geometry causes a failure or
explicit `valid_mask=False` entries rather than silently producing dimensions.

After a run, summarize its stored evidence with:

```bash
python scripts/run_diagnostics.py \
  --calibration results/calibration/phone_calibration.json \
  --stereo-result results/object_measurements/stereo_pair.json \
  --output results/object_measurements/diagnostics.json
```

## Current boundaries

Implemented and tested: Phase 2A calibration/geometry/depth software, Phase 2B real calibration
and stereo validation, Phase 3 rectangle/circle/polygon dimension estimation, and the standalone
Question 1 Streamlit presentation. Phase 3 real experiments remain mixed: only the documented
flashcard width validation is accepted; the rectangle, circle, and triangle limitations remain
visible in the web page and evidence records.
Pending work: clean-install verification, public deployment, Phase 4 room-video measurement, and
the final DOCX/PDF report. Phase 4 remains explicitly out of scope until separately authorized.

## Phase 3 object dimension estimation

The measurement workflow first calls the existing calibrated-stereo triangulation API. It
requires a metric `StereoPose`, rejects non-finite or non-positive depth, insufficient parallax,
and reprojection failures, and only then computes dimensions in the pose's `m` or `mm` unit.

The correspondence file uses the shared Phase 2 format:

```text
point_id,u1,v1,u2,v2
```

For a rectangle, pass four IDs in `top-left, top-right, bottom-right, bottom-left` order. For a
circle, pass at least three corresponding visible boundary landmarks; more boundary samples are
preferred for a residual check. For a polygon, pass visible vertices in boundary order. The
circle path assumes a rigid planar circular boundary and fits a circle in its recovered 3D plane.
The polygon path reports every adjacent 3D edge and never substitutes a bounding-box dimension.

Example using a saved Phase 2 pose record and a new user-captured object correspondence file:

```bash
python scripts/measure_object.py \
  --calibration results/calibration/module2_originals_module7_recomputed.json \
  --stereo-record results/object_measurements/checkerboard_stereo_pair.json \
  --correspondences data/objects/rectangle_correspondences.csv \
  --shape rectangle \
  --landmark-ids top_left top_right bottom_right bottom_left \
  --output results/object_measurements/rectangle_measurement.json
```

The generated record is marked `computed_not_experimentally_validated` until the user supplies
an independent ruler/tape measurement. A successful command is therefore a software result,
not a physical accuracy claim.

The final report is planned in both editable Word and PDF formats:
`Module_7_Assignment_Report.docx` and `Module_7_Assignment_Report.pdf`.
