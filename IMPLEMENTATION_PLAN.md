# CSc 8830 Module 7 — Implementation Plan

## 0. Plan status and scope

**Current phase:** Phase 3D standalone UI alignment and proposed evidence preparation complete;
Git initialization, public evidence approval, dashboard integration, and deployment remain gated.
The yellow-lid circle
and triangle experiments remain closed as documented, and Phase 4 remains out of scope.

This document remains phase-gated. Phase 2 calibration/stereo software and real Phase 2B
validation are complete. Phase 3 object-measurement software is implemented and deterministically
tested; Phase 3A is complete as documented with verified physical measurements but unsuccessful
stereo accuracy. Phase 3B marked-lid capture has been supplied and processed. Fourteen marker-defined
outer-rim correspondences pass point-level stereo checks, but the recovered rim fails the existing
  3D planarity gate. The later lid ruler review documents a provisional physical reference, but does
  not change the rejected stereo result. Phase 3C triangle processing is complete; its geometry gates
  passed but its reconstructed edges did not meet the independent physical intervals. The core
  Question 1 workflow and required standalone webpage are implemented and tested locally. Public
  dashboard integration, repository publication, and deployment remain separately authorized work.

The latest local public-UI polish review improves student-facing status labels, metric formatting,
and structured diagnostics while retaining the underlying machine-readable statuses and technical
detail records. It is local and uncommitted; live deployment verification and publication remain
outside this change.

The plan follows the authoritative requirements in
`MODULE_7_ASSIGNMENT_QUESTIONS.md` and `MODULE_7_ASSIGNMENT_INSTRUCTIONS.md`, the root
`Assignments/AGENTS.md`, the root Git protocol, and the existing Module 2–6 architecture.

Claims in this document are classified as follows:

- **implemented:** Phase 0/Phase 1 documentation, the Phase 2 calibration/geometry/depth
  foundation, the Phase 3 metric object-measurement APIs and CLI, and the Phase 3D standalone
  Question 1 webpage;
- **tested:** deterministic unit/synthetic checks, shape-fit quality gates, correspondence I/O,
  standalone provider/evidence tests, Streamlit smoke checks, and Python compilation listed in
  `IMPLEMENTATION_STATUS.md`;
- **theoretically derived:** geometry and projective-vision relationships described as design
  rationale, with references to be cited in the eventual report;
- **experimentally validated:** intrinsic calibration is validated from reused real Module 2
  photographs, and the real checkerboard-visible stereo pair passes the implemented
  checkerboard-PnP, triangulation, cheirality, parallax, reprojection, and in-sample board-geometry
  checks; the verified `IMG_7501.JPG`/`IMG_7502.JPG` photographs support the FREE ADMISSION
  card's corresponding long and short physical measurements;
- **pending user data collection:** a photograph of the exact upper stereo-selected edge if strict
  same-endpoint identity is required, an independently measured camera-center baseline for an essential-matrix
  cross-check, circle/polygon object
  stereo captures, landmark correspondences, room videos, physical measurements, and empirical accuracy
  results. One smartphone
  and the calibration target are confirmed from Module 2 evidence.

The plan does not substitute synthetic values for required measurements. The actual Phase 2B
capture results are recorded in `IMPLEMENTATION_STATUS.md`; Stage C physical width validation is
complete under the explicitly documented equivalent-edge assumption.

---

## 1. Requirements traceability

| Assignment requirement | Planned implementation/document evidence | Phase |
| --- | --- | --- |
| Q1: calibrated stereo must estimate depth before physical dimensions | `calibration.py`, `stereo_geometry.py`, `depth_estimation.py`, standalone object-measurement pages, calibration/depth evidence, report method section | 2–3, 3D, 5–7 |
| Q1: rectangles, circles, and visible polygon edges | Shape-specific landmark workflow and Euclidean 3D edge calculations; circle assumptions recorded | 3 |
| Q2: no implementation necessary | Theory page only; no uncalibrated measurement pipeline planned | 1, 5, 7 |
| Q2: handwritten derivation, intermediate calculations, assumptions | User-created scanned derivation, checklist, pending-safe web display, final PDF appendix | 1, 7 |
| Q2: uncalibrated metric-scale limitation | Handwritten outline and report review checklist explicitly require projective/scale ambiguity | 1, 7 |
| Q3: video-based room dimensions | Calibrated moving-camera video, reference-assisted metric scale, room geometry, validation protocol | 4, 6 |
| All references cited | `docs/references.md`, inline citations in report sections and captions | 1, 7 |
| Working web application | Standalone `app.py` and `module7.webapp.pages.get_pages()` implemented in Phase 3D; later dashboard integration remains separate | 3D, 5 |
| No fabricated results | Pending banners, provenance records, empty templates, and integrity checks | All |

---

## 2. Repository discovery and architecture summary

### 2.1 Repository boundaries and Git policy

The workspace has no root `.git` directory. Modules 2, 3, 4, 5–6, `csc8830-dashboard`, and
`csc8830-ui` are separate Git repositories. Modules 2, 3, 4, and 5–6 are independently
installable source-layout Python projects with their own `src/`, `tests/`, `app.py`, and
`pyproject.toml`. The public dashboard is a deployment mirror and is not the place to develop
assignment logic.

The established module repositories use local-only governance/planning exclusions in either
`.gitignore` or `.git/info/exclude`; large/private raw inputs and some generated artifacts are
also excluded. Module 7 should adopt the same policy only after its own repository topology is
approved. This Phase 1 work does not initialize a repository, create a branch, commit, push, or
change another repository.

One naming inconsistency was found: the actual directory is `Module_5-6`, while older planning
text and package/document names sometimes use `Module_5_6`. Module 7 will use the requested
directory `Module_7` and package name `module7` consistently.

### 2.2 Core/application separation

The existing modules keep deterministic OpenCV/NumPy processing in importable core modules and
keep Streamlit rendering in `src/moduleN/webapp/`. Their standalone entry points add `src/` to
the import path, call the module-local page provider, and render through a module-local shell.
The root dashboard imports providers dynamically and adapts page objects structurally rather
than requiring one shared `PageSpec` class.

Module 2 provides the most relevant prior calibration patterns: chessboard detection,
`cv2.calibrateCamera`, intrinsic/distortion persistence, reprojection-error analysis,
undistorted point back-projection, and physical dimension calculations. Module 5–6 provides
the closest multi-view geometry patterns: camera/view metadata, homography/SfM organization,
reprojection validation, image/video handling, and page-provider integration. Module 7 will
use these as design references only and will not import their runtime code.

### 2.3 Web contract

The future Module 7 provider will follow the established contract:

```text
module7.webapp.pages.get_pages()
    -> iterable of page objects with:
       module_label, page_label, order, render
```

The module-local `PageSpec`, `registry.py`, `shell.py`, and `ui.py` should remain standalone.
The root dashboard can later add `("Module 7", "module7.webapp.pages")` to its provider list;
the public dashboard will require the corresponding deployment-mirror and sync-script changes.
Those changes are intentionally deferred and are outside Phase 0.

### 2.4 Data and evidence policy

Earlier modules distinguish raw/private inputs from small committed evidence and generated
results. Module 7 should use:

- `data/` for user-supplied calibration captures, stereo pairs, object images, and room videos;
- `results/` for reproducible derived calibration, disparity/depth, reconstructed landmarks,
  room geometry, figures, and validation tables;
- `docs/` for protocols, assumptions, citations, theory, report notes, and demo guidance.

No bundled sample is available yet. Later upload-gated pages must follow the root fallback
rule: use only a real user-selected capture or a public/licensed real sample, run the exact
same processing path as an upload, and show a clear bundled-sample notice. If no permissible
real sample has been committed, show a pending state. The precise sample file must be checked
with `git ls-files` in the Module 7 repository before deployment.

---

## 3. Proposed Module 7 directory structure

This is a target for later phases, not a claim that all listed files exist now. Phase 0 created
the governance, README, assignment, plan, and status documents; Phase 1 added the five design
documents under `docs/`. Implementation, test, data, result, and report artifacts remain future
work.

```text
Module_7/
├── AGENTS.md
├── CLAUDE.md
├── GIT_WORKFLOW.md
├── MODULE_7_ASSIGNMENT_QUESTIONS.md
├── MODULE_7_ASSIGNMENT_INSTRUCTIONS.md
├── IMPLEMENTATION_PLAN.md
├── IMPLEMENTATION_STATUS.md
├── README.md
├── app.py
├── pyproject.toml
├── data/
│   ├── calibration/
│   ├── stereo_pairs/
│   ├── objects/
│   └── room_videos/
├── docs/
│   ├── architecture.md
│   ├── calibration_protocol.md
│   ├── experimental_protocol.md
│   ├── uncalibrated_stereo_derivation.md
│   ├── references.md
│   ├── DEMO_VIDEO_CHECKLIST.md
│   └── report/
├── results/
│   ├── calibration/
│   ├── object_measurements/
│   └── room_measurements/
├── scripts/
├── src/
│   └── module7/
│       ├── __init__.py
│       ├── calibration.py
│       ├── stereo_geometry.py
│       ├── depth_estimation.py
│       ├── object_measurement.py
│       ├── room_measurement.py
│       ├── validation.py
│       ├── visualization.py
│       └── webapp/
│           ├── __init__.py
│           ├── _page.py
│           ├── registry.py
│           ├── shell.py
│           ├── ui.py
│           └── pages.py
└── tests/
```

The eventual package should use Python 3, OpenCV, NumPy, Matplotlib only where visualization
requires it, Streamlit, and pytest for development tests. No additional dependency is justified
at Phase 0. A separate `scipy` dependency is not planned unless a later implementation proves
that a required fit cannot be implemented clearly and robustly with the permitted stack.

---

## 4. Technical design

### 4.1 Question 1 — calibrated stereo object measurement

#### Acquisition and calibration

1. Use the confirmed single smartphone camera with one fixed lens/mode and image resolution.
2. Capture a printed checkerboard with a measured square size in multiple poses. Keep the
   target and square-size record with the experiment metadata.
3. Calibrate the phone with `cv2.calibrateCamera` to obtain one intrinsic matrix `K`, one
   distortion vector `D`, per-view poses, and per-view/aggregate reprojection error.
4. Capture each stationary object twice from two phone positions. Measure the displacement
   between the camera centers as the sequential-stereo baseline. Estimate the relative rotation
   and translation direction for that specific pair with calibrated essential-matrix geometry,
   then scale the translation direction by the measured baseline magnitude.
5. Use `cv2.stereoRectify` only with the per-pair `R` and metric `t` when rectification is useful;
   use `initUndistortRectifyMap`/`remap` for derived images. Do not treat the phone as a
   synchronized permanent two-camera rig or blindly apply `cv2.stereoCalibrate`.

The exact target, number of captures, image resolution, calibration flags, measured baseline,
relative pose, and results will be recorded from the real experiment. They must not be filled
with guessed values. A checkerboard visible in both sequential object views may support a
`solvePnP` pose estimate as a verification/fallback method.

#### Correspondence and depth

For an ideal horizontally rectified pair, corresponding points share a row and

```text
Z = f B / d
```

where `Z` is depth in the calibrated coordinate unit, `f` is the rectified focal length in
pixels, `B` is the metric baseline, and `d = x_left - x_right` is disparity in pixels. This
relationship assumes a pinhole model, correct rectification, a known metric baseline,
corresponding points on the same physical point, and nonzero positive disparity. It is a
theoretical relationship, not an experimental result.

The actual implementation should use calibrated projection geometry for the final point
reconstruction: either `cv2.triangulatePoints(P1, P2, points1, points2)` for sparse landmarks,
or the rectification `Q` matrix with a carefully validated disparity value for dense output.
This avoids applying one approximate depth to every edge. Every endpoint or selected boundary
landmark should be reconstructed in 3D, then dimensions should be computed as Euclidean
distances:

```text
length(A, B) = ||X_A - X_B||_2
```

The report must state whether coordinates are in metres or millimetres and how OpenCV's
coordinate frame is oriented.

The first implementation should support a transparent, grader-auditable workflow:

- obtain candidate correspondences from a classical feature/correspondence method or explicit
  user landmark selection on the rectified pair;
- retain the selected left/right landmark pairs and disparity values as evidence;
- reject points with invalid disparity, failed matching, occlusion, inconsistent rectified
  rows, or negative/non-finite reconstructed depth;
- show the rectified pair, correspondence overlays, disparity/depth visualization, and 3D
  landmark table before reporting dimensions.

Dense stereo may be used for visualization and depth context, but sparse object landmarks are
preferred for dimensions because the measurement endpoints must be explainable.

#### Shape handling

- **Rectangle:** select four visible corners in boundary order. Reconstruct all corners and
  report the relevant adjacent 3D edge lengths (for example width and height or width and
  length), with the view-dependent choice documented.
- **Circle:** assume a rigid circular object whose visible boundary points lie on one physical
  plane. Select or detect enough corresponding perimeter points to reconstruct a 3D contour,
  fit a plane/circle in that recovered object plane, and report the diameter. The report must
  state the planar-object, visibility, correspondence, and circularity assumptions. A single
  image ellipse diameter or one depth value is not sufficient evidence of calibrated-stereo
  diameter estimation.
- **Other polygon:** preserve visible vertices in boundary order, reconstruct each vertex, and
  report every visible adjacent edge length. Do not collapse a polygon into a bounding-box
  measurement without labeling that as a different quantity.

#### Validation and error analysis

Use user-measured object dimensions as ground truth only after the user records them. Store
object identity, capture pair/video frame, landmark coordinates, calibration identifier, depth,
estimated dimensions, physical dimensions, absolute error, relative/percentage error, and
notes about occlusion or correspondence quality. Report error statistics only for completed
real trials. Automated geometry tests are software tests, not physical validation.

### 4.2 Question 2 — uncalibrated stereo handwritten derivation

There will be no uncalibrated stereo measurement implementation. The plan for the user's
handwritten work is an outline and review checklist only:

1. Define homogeneous image points and two projective cameras, for example
   `P1 = [I | 0]` and a projectively equivalent second camera.
2. Establish corresponding image points and derive the epipolar constraint
   `x2^T F x1 = 0`.
3. Explain estimation of `F` from point correspondences, including normalization, outlier
   handling, and the rank-2 constraint at a conceptual level.
4. Explain relative projective reconstruction and triangulation from camera matrices.
5. Relate recovered 3D point distances to object edges and dimensions.
6. Explicitly show the metric-scale ambiguity and, more generally, the projective ambiguity of
   uncalibrated reconstruction. Explain that absolute dimensions require additional metric
   information or assumptions, such as calibrated intrinsics and baseline, a known reference
   length, known camera motion, or enough constraints for a metric upgrade.
7. Work every requested numerical example and intermediate calculation by hand.

The user will scan the original handwritten pages. `docs/uncalibrated_stereo_derivation.md`
will later contain provenance, a page inventory, and a checklist—not a typed substitute. The
web page will display the scan only when the user supplies it; otherwise it will show a
pending state.

### 4.3 Question 3 — room dimensions from video

#### Approach comparison

| Approach | Metric scale | Main risk | Decision |
| --- | --- | --- | --- |
| Full calibrated monocular SfM/SLAM | Requires global scale recovery and pose refinement | Scale drift, trajectory drift, substantial implementation scope | Optional extension |
| Reference-assisted sparse calibrated multiview video | A measured target/reference anchors the metric room frame | Reference visibility and room coverage | **Minimum viable first implementation** |
| Ordinary uncalibrated monocular video | Scale ambiguous without an external reference | Cannot honestly promise absolute room dimensions | Rejected as a metric method |

The selected Q3 direction is a **single-smartphone moving-camera video workflow**. The minimum
viable implementation uses calibrated multiview geometry plus a fixed measured reference target
or known-length geometry. It is intentionally narrower than a general monocular room scanner:
each measurement segment must retain a metric connection to the reference, and unobserved room
boundaries remain pending.

#### Proposed workflow

1. Calibrate the smartphone at the exact video resolution and lens mode.
2. Fix a measured reference target in the room and record its metric coordinate frame.
3. Record a slow moving video with overlap, sufficient parallax, visible reference anchor frames,
   and visible floor/wall/ceiling boundaries where possible.
4. Extract quality-controlled keyframes; detect and match features; reject ambiguous matches and
   geometrically inconsistent tracks.
5. Estimate relative camera motion with calibrated essential-matrix geometry. Use `solvePnP`
   whenever known reference points are visible to anchor the camera pose and metric scale. Do not
   treat unit translations from `recoverPose` as metric motion.
6. Triangulate repeated room landmarks, fit supported floor/wall/ceiling planes, and estimate
   length/width/height from documented plane intersections or room-corner landmarks.
7. If multiple video segments are required, connect them through overlapping reference targets
   or a documented metric registration; never align segments by eye.
8. Validate every reported dimension against independent tape-measure measurements. Report
   coverage, plane/reprojection residuals, frame-to-frame spread, and failure cases.

#### Limitations and user-supplied materials

The method can fail or become uncertain with textureless walls, reflective surfaces, repeated
patterns, occluded corners, motion blur, rolling shutter, insufficient parallax, reference
loss, pose drift, disconnected segments, and incomplete coverage. The user must supply the
smartphone video, a measured reference target or known geometry, room access, and independent
room measurements. No room dimension will be reported before those materials exist.

---

## 5. Planned web application surface

The page names below are proposed to match the requested assignment components and existing
navigation conventions:

1. **Calibrated Stereo — Object Measurement**: upload/select a stereo pair or recorded frame,
   show calibration provenance, select/inspect shape landmarks, reconstruct points, and report
   shape-specific dimensions.
2. **Calibration and Depth Visualization**: display intrinsic/extrinsic metadata, rectification,
   correspondence overlays, disparity/depth, and 3D point evidence.
3. **Uncalibrated Stereo — Handwritten Derivation**: theory overview, metric-scale warning,
   scanned handwritten pages when supplied, or an honest pending banner.
4. **Video-Based Room Measurement**: select real room videos, inspect frame coverage, reconstruct
   room geometry, fit surfaces, and report dimensions only when valid metric data is present.
5. **Results and Validation**: display provenance, validation tables, error statistics,
   limitations, and pending sections.

The standalone app will be implemented before dashboard wiring. The root dashboard must not be
modified during Phase 1. After later approval and standalone verification, future integration will
require: adding the provider to `Assignments/app.py`, making the same provider addition in the
deployment mirror, adding the Module 7 repository URL to `sync_module_src.sh`, syncing only
committed `src/`, `data/`, `results/`, and `docs/`, running the documented local smoke test,
and verifying the public page after a real deployment reboot.

---

## 6. Phased milestones

### Phase 0 — Discovery and planning

- **Goal:** establish requirements traceability, architecture, Git/data policy, technical
  direction, and durable handoff.
- **Inputs/dependencies:** root and module governance, assignment documents, actual source code,
  dashboard contract, and verified authoritative references.
- **Files involved:** the four required Phase 0 documents plus Module 7 governance/README files;
  no existing module or dashboard code.
- **Tasks:** complete discovery; write preserved questions and submission instructions; write
  this plan; initialize status tracking.
- **Acceptance criteria:** no algorithm code or empirical result exists; user can review the
  proposed geometry and room method; architecture and conflicts are recorded.
- **Tests/validation:** file existence, Markdown inspection, repository-boundary inspection,
  and consistency review.
- **Expected artifacts:** four required documents and handoff-ready governance.
- **User involvement:** review and approve or revise the plan; identify available cameras,
  calibration target, stereo capture method, and intended room experiment.
- **Completion status:** complete; approved by the user before Phase 1.
- **Entry criteria for Phase 1:** satisfied by user approval.

### Phase 1 — Technical design and experiment protocol

- **Goal:** lock the one-smartphone sequential-stereo design, coordinate conventions, calibration
  target, object landmark workflow, moving-video room strategy, report formats, and validation
  tables.
- **Inputs/dependencies:** approved Phase 0 plan and user decisions/material availability.
- **Files involved:** `docs/architecture.md`, `docs/calibration_protocol.md`,
  `docs/experimental_protocol.md`, `docs/uncalibrated_stereo_derivation.md`,
  `docs/references.md`, and data/result schemas.
- **Tasks:** record the confirmed single phone; distinguish measured baseline from pose; compare
  essential-matrix, checkerboard-PnP, and controlled-translation alternatives; define metadata
  schemas, units, failure states, reference-assisted room scale, citation ledger, and DOCX/PDF
  report architecture.
- **Acceptance criteria:** a reproducible one-phone protocol exists; Q1 has a defensible
  per-pair metric pose design; Q3 has a feasible reference-assisted moving-video MVP; Q2 remains
  handwritten-only; report production is planned for both DOCX and PDF.
- **Tests/validation:** documentation and consistency review only; no physical validation and no
  algorithm tests.
- **Expected artifacts:** the five Phase 1 design documents and updated plan/status files.
- **User involvement:** later acquire/confirm the checkerboard, ruler, support, validation
  objects, room reference, and capture access.
- **Completion status:** complete; the user authorized Phase 2 implementation.
- **Entry criteria for Phase 2:** satisfied by the user's Phase 2 authorization. Physical
  capture materials remain required for experimental validation, not for deterministic software
  testing.

### Phase 2 — Stereo calibration and depth

- **Goal:** implement and test calibrated stereo calibration, rectification, correspondence,
  triangulation, disparity/depth, and evidence export.
- **Inputs/dependencies:** approved Phase 1 design; real calibration captures; one smartphone;
  measured checkerboard; and a future measured sequential baseline.
- **Files involved:** `src/module7/calibration.py`, `stereo_geometry.py`, `depth_estimation.py`,
  `io_utils.py`, `visualization.py`, calibration/processing/diagnostic scripts, tests, and
  `data/calibration/`.
- **Tasks:** implement validated input handling; preserve original images; calculate and save
  calibration metadata; create rectification/depth outputs; expose invalid/occluded states;
  track baseline uncertainty and reject excessive reprojection/parallax failures.
- **Acceptance criteria:** synthetic geometry tests pass; the real-run path produces
  provenance-backed calibration/depth evidence when supplied with captures; no hard-coded
  calibration or depth values.
- **Tests/validation:** unit tests, synthetic projection/triangulation tests, calibration input
  validation, and a future user-run real calibration with reprojection review.
- **Expected artifacts:** calibration record, rectification figures, depth evidence, and test
  results. Real numeric fields remain pending until the user run.
- **User involvement:** capture and select calibration images, measure target square size and
  sequential camera displacement, review reprojection quality, and confirm camera settings.
- **Completion status:** Phase 2A software foundation and Phase 2B Stages A–C are complete for
  their stated evidence. The Stage C decision is documented under the equivalent-rectangular-edge
  assumption.
- **Entry criteria for Phase 3:** calibrated geometry passes software checks and a usable,
  provenance-backed real calibration record exists; Phase 2B physical stereo validation must
  also be complete; Phase 3 requires explicit approval.

### Phase 2B — Real smartphone calibration and stereo validation

- **Goal:** run the existing calibration and sequential-stereo pipeline on real observations
  from the confirmed one-smartphone setup, then compare reconstructed depth with independent
  physical measurements.
- **Existing implementation:** `scripts/run_calibration.py` for checkerboard calibration,
  `scripts/run_diagnostics.py` for saved-record review, and `scripts/process_stereo_pair.py`
  for stereo processing. Its `checkerboard_pnp` mode reuses the existing checkerboard detector,
  metric object points, `solvePnP`, relative-pose, triangulation, and rectification functions;
  no duplicate pipeline is authorized.
- **Stage status:** Stage A `CALIBRATION VALIDATED` by recomputation from the original Module 2
  photographs; Stage B `STEREO GEOMETRY VALIDATED` on the real checkerboard-visible pair using
  automatic 54-corner correspondences and checkerboard-PnP; Stage C is physically validated for the
  front-face width under an explicit planar-rectangular equivalent-edge assumption.
- **Calibration capture target:** the documented protocol recommends approximately 15–25 usable
  checkerboard views with varied coverage. The script requires at least 3 accepted views; that
  lower bound is an input guard, not a recommended experimental sample size.
- **Evidence required:** actual source images, measured square size, fixed camera settings,
  calibration JSON, accepted/rejected view record, aggregate/per-view reprojection review, and
  a documented decision about whether the calibration is usable for the intended working range.
- **Validation rule:** do not mark `CALIBRATION VALIDATED`, `STEREO GEOMETRY VALIDATED`, or
  `PHYSICAL VALIDATION COMPLETE` without the corresponding real evidence. If captures fail or
  are incomplete, use `BLOCKED` or `PENDING USER CAPTURE`.
- **Reuse result:** Option A was selected. The original Module 2 images were processed directly
  by `scripts/run_calibration.py`, producing
  `results/calibration/module2_originals_module7_recomputed.json`. The original Module 2 JSON
  remains a documented comparison record rather than a silent parameter import.
- **Stage B pose recommendation:** keep the same checkerboard visible in both views and use
  `--pose-method checkerboard_pnp` for the first metric validation. Record the physical
  camera-center displacement as an independent cross-check. Use essential mode later for
  arbitrary object landmarks when the board is not visible.
- **Stage B software improvement:** `process_stereo_pair.py` now auto-detects and indexes the
  54 checkerboard corners in both views, optionally writes the exact generated CSV, and records
  triangulation parallax. This removes manual pixel guessing for the first checkerboard
  validation pair without creating a second geometry pipeline.
- **Stage B real-data result:** the supplied `IMG_7485.JPG`/`IMG_7486.JPG` pair was processed
  through derived 90° clockwise portrait-coordinate copies because the reused calibration record
  is `(4284, 5712)` while the originals decode as `(5712, 4284)`. The original files were not
  modified. The checkerboard-PnP baseline was `83.985623 mm`, median triangulation parallax was
  `9.369687°`, all `54/54` points had positive depth in both views, and the maximum triangulation
  reprojection error was `0.956960 px`. Neighboring reconstructed board edges were within the
  documented 25.0 mm target to sub-0.1 mm mean absolute error. This is an in-sample board
  consistency check because the board points define both the PnP pose and the triangulated
  correspondences; it does not satisfy independent physical validation.
- **Stage C latest real-data result:** the user-confirmed independent flashcard front-face top
  edge is `96.70 ± 1.00 mm`, with interval 95.70–97.70 mm. Using the saved checkerboard-PnP pose
  without rescaling, the unchanged selected endpoints reconstruct to a `95.905679 mm` Euclidean
  segment. Signed error is `-0.794321 mm`, absolute error `0.794321 mm`, and percentage error
  `0.821428%`; the estimate is within the stated interval. Both endpoints had positive depth and
  reprojection errors below the 5 px implementation guard. This is a physical validation pass for
  the front-face width under the explicit planar-rectangular equivalent-edge assumption. The
  ruler's ±1 mm is not a stereo-system accuracy claim; no formal propagated reconstruction
  uncertainty is available in the current pipeline.
- **Stage C discrepancy review:** holding the saved pose, calibration, and selected pixel
  coordinates fixed for the reported result, a diagnostic ±2-pixel perturbation study produced
  valid reconstructed lengths from `94.108265 mm` to `98.220563 mm`. This remains below the
  corrected 104 mm lower bound, so small endpoint localization noise alone does not explain the
  discrepancy. The study is sensitivity evidence, not a formal uncertainty estimate.
- **Stage C evidence review:** the saved endpoint overlays place the selected points on the
  apparent printed front-face top-edge intersections in both views. The portrait-coordinate
  transform, intrinsic matrix, checkerboard-PnP pose, and projection matrices show no objectively
  demonstrated frame or projection mismatch. The user-reported product illustration is recorded
  separately as nominal `100 × 80 × 60 mm` secondary information only; it was not used as ground
  truth, scale, calibration input, or endpoint evidence. The new clear2 photograph measures the
  lower parallel front-face edge. It shows the metric zero reference and millimetre subdivisions
  and supports approximately 96.70 mm. The four straight boundary seams and physical corners
  support modeling the face as a rigid planar rectangle; equality of opposite edges is therefore
  an explicit geometric assumption, not an inference from projected parallelism alone.
- **Stage C evidence gate:** the inspected ruler evidence for 96.70 mm measures the corresponding
  front-face width and supports the retained ±1 mm uncertainty. Earlier superseded incorrect
  measurements and failed results are preserved only in
  `results/object_measurements/flashcard_validation_audit_history.json`. The current clear
  photographs support the corresponding front-face width. Stage C is therefore closed for the width
  dimension under the explicit equivalent-edge assumption; literal upper-edge pixel endpoint identity
  is not claimed. Do not adjust the current scale or coordinates.
- **Phase 3 gate:** opened by the user's explicit Phase 3 authorization after Phase 2B closure.

### Phase 3 — Object shape and dimension measurement

- **Goal:** implement rectangle, circle, and polygon measurements from reconstructed 3D
  landmarks.
- **Inputs/dependencies:** Phase 2 calibration/depth pipeline and real stereo object captures.
- **Files involved:** `src/module7/object_measurement.py`, `scripts/measure_object.py`, shared
  correspondence I/O, tests, object data/results, and the Q1 report sections.
- **Tasks:** implement landmark provenance; reconstruct metric 3D landmarks through the existing
  triangulation quality gates; calculate 3D Euclidean rectangle/polygon edge lengths; fit a circle
  in recovered 3D geometry; reject invalid correspondences; and generate auditable JSON records.
- **Acceptance criteria:** all three shape paths are implemented and tested; dimensions are
  computed from reconstructed 3D endpoints/contours; real values are labeled as experimental
  only after user measurements and validation.
- **Tests/validation:** analytic synthetic shapes, unit tests for edge ordering/lengths and
  invalid depth, then real object measurements against independent physical measurements.
- **Expected artifacts:** object-measurement results, figures, and validation records.
- **User involvement:** capture real stereo object images, identify shape/landmarks, measure
  ground truth, and review ambiguities.
- **Completion status:** core software implementation and the standalone Question 1 webpage are
  complete and deterministically tested; real shape-specific evidence is preserved with mixed
  validation outcomes. Dashboard/public deployment remains separate.
- **Entry criteria for Phase 4:** Q1 must demonstrate calibrated depth and at least one
  provenance-backed real-object workflow through the required webpage, with rectangle/circle/polygon
  paths and pending/rejected statuses exposed honestly. Additional shape experiments may remain
  physically unvalidated, but they must not be presented as accepted results.

#### Phase 3A — Rectangle physical validation

- **Authorization:** explicitly authorized by the user; circle and polygon validation remain out
  of scope.
- **Status:** `EXPERIMENT COMPLETE — PHYSICAL MEASUREMENT VERIFIED; STEREO ACCURACY NOT VALIDATED`.
- **Experiment:** one rigid rectangular reference, four verified corners, stationary 9×6
  checkerboard visible in both sequential views, and the existing iPhone 15 Pro Max calibration.
- **Metric pose:** reuse `scripts/process_stereo_pair.py --pose-method checkerboard_pnp`; the
  25.0 mm checkerboard supplies the metric board geometry. Do not replace it with an assumed
  phone-body displacement.
- **Correspondences:** `top_left, top_right, bottom_right, bottom_left`, recorded only after
  both genuine images are inspected.
- **Independent measurements:** width and height measured separately with repeated ruler/tape
  readings and recorded uncertainty. These values may be used for comparison only, never to
  rescale the reconstruction.
- **Supplied evidence:** `data/physical_validation/IMG_7514.JPG` and `IMG_7515.JPG`, their EXIF
  records, derived portrait calibration-frame copies, reviewed four-corner overlays, the
  correspondence CSV, stereo record, measurement record, and evidence manifest. The original
  contour-extreme attempt is retained as a rejected audit record because one point exceeded the
  5 px reprojection gate.
- **Observed result:** checkerboard-PnP baseline 44.6969976 mm, all 4/4 card landmarks valid,
  median object parallax 1.8394634 degrees, reconstructed dimensions 51.4434472 mm (image-order
  top edge) and 85.8989759 mm (image-order side edge). The latter compares with the user's long
  dimension mean 87.40 mm at −1.5010241 mm / 1.7174189%; the former compares with the user's
  short dimension mean 49.40 mm at +2.0434472 mm / 4.1365329%.
- **Physical-validation gate:** the user supplied three readings for each dimension and a 1 mm
  ruler subdivision. A provisional ±1.0 mm physical bound is conservatively supportable from the
  resolution and reading spread, but endpoint alignment/setup photographs for this rectangle are
  unavailable. The resulting width interval is 86.40–88.40 mm and the height interval is
  48.40–50.40 mm. The long-side estimate 85.8989759 mm is 0.5010241 mm below its interval; the
  short-side estimate 51.4434472 mm is 1.0434472 mm above its interval. Both fail. This is not
  stereo-system uncertainty, no percentage-error threshold was introduced, and no scale or
  coordinates were adjusted.
- **Decision:** geometric validity gates passed, but physical accuracy validation is `NOT
  VALIDATED`. The minimum justified next action is a controlled recapture with an independently
  measured rigid rectangle and a photograph/record showing the ruler endpoints, followed by a
  fresh correspondence review without changing the existing calibration or pose.
- **Second experiment record:** `IMG_7516.JPG` and `IMG_7517.JPG` were processed from preserved
  originals after clockwise portrait-frame normalization. Both detected 54/54 checkerboard
  corners; PnP RMS errors were 1.44438 px and 1.55534 px. The recovered metric baseline was only
  6.0410615 mm and median card parallax was 0.669038 degrees. All four landmarks passed positive
  depth and point-reprojection checks, but the existing rectangle gate rejected the shape because
  opposite-edge disagreement was 24.1595% for width and 17.8049% for height; planarity RMS/max
  were 5.08290 / 5.95519 mm and maximum right-angle deviation was 21.9274 degrees. No accepted
  dimensions were emitted. The raw diagnostic lengths are retained only as diagnostics.
- **Ruler evidence:** `IMG_7501.JPG` and `IMG_7502.JPG` were re-inspected and show the FREE
  ADMISSION rectangle. `IMG_7501.JPG` aligns the ruler with the long horizontal front-face edge;
  `IMG_7502.JPG` aligns it with the short edge. The zero reference, millimetre subdivisions, and
  both endpoints are visible sufficiently to support the recorded repeated readings 87.0/88.0/87.2
  mm and 49.0/49.8/49.4 mm. Their means remain 87.40 mm and 49.40 mm. The 1 mm subdivisions,
  endpoint alignment, perspective, and reading spread support a conservative ±1.00 mm physical
  uncertainty. This is physical-measurement uncertainty, not stereo-system uncertainty, and the
  measurements were not used to scale or optimize the reconstruction.
- **Controlled next option:** do not tune the current result. The physical ruler evidence is now
  available; no automatic recapture is requested. Any future follow-up would remain optional and
  would need to address the unresolved pose/model warning without changing this experiment.
- **Third experiment:** `DOCUMENTED — FREE ADMISSION MEASUREMENT VERIFIED; STEREO ACCURACY NOT
  VALIDATED`. The supplied full-resolution originals `IMG_7519.JPG` and `IMG_7520.JPG`
  were preserved and processed with the existing calibration and `checkerboard_pnp` workflow.
  Both are Apple iPhone 15 Pro Max images at 4284×5712 decoded resolution with EXIF orientation 6;
  OpenCV's decoded portrait arrays already match the 4284×5712 calibration frame, so no content
  rotation was applied. The 9×6 checkerboard was detected at 54/54 corners in both views.
  PnP RMS errors were 1.10839 px and 2.21646 px, the metric baseline was 166.387025 mm, and
  median card parallax was 17.073946 degrees.

  The four verified card corners passed positive-depth, point-reprojection, planarity, right-angle,
  and opposite-edge geometry gates. The reconstructed short and long sides were 52.336899 mm and
  92.973060 mm. Against the independent means 49.40 mm and 87.40 mm, the signed errors were
  +2.936899 mm and +5.573060 mm; absolute errors were the same, with percentage errors 5.945140%
  and 6.376499%. Both fall outside the provisional ±1.00 mm intervals [48.40,50.40] mm and
  [86.40,88.40] mm.

  The scene-consistency review did not establish a stationary common scene. The checkerboard
  homography residual median/max were 3.891/8.593 px, but the four card-corner residuals were
  14.937–46.805 px; this screen is decisive only if the card and checkerboard are coplanar. A
  calibrated card-homography decomposition was also reviewed. The previously reported 12.345324°
  discrepancy used raw distorted pixels; after distortion-aware point normalization, the closest
  decomposition discrepancy was 12.959758°. With only four card corners and no independently known
  card-plane geometry, this is a pose/model warning, not an independent pose estimate or proof of
  card movement. A 1 px perturbation sensitivity simulation gave 10.55°/13.11°/15.68° 5th/median/
  95th-percentile discrepancies; this is diagnostic only and is not an endpoint uncertainty claim.

  Visual review confirms that the saved points refer to the same apparent outer card corners in both
  views, in order `top_left, top_right, bottom_right, bottom_left`. The image-order horizontal edge
  is the shorter physical edge (52.336899 mm reconstructed), while the vertical side is the longer
  physical edge (92.973060 mm reconstructed). The individual stereo shape gates passed. The
  verified ruler evidence supports both physical means and the conservative ±1.00 mm intervals,
  but both reconstructed dimensions remain outside those intervals. This is a legitimate
  experimental accuracy limitation, not a reason to change the ground truth. The computed stereo
  record, measurement record, validation record, evidence manifest, annotated correspondence
  images, and the prior blocked-missing-originals audit record are preserved. No reprocessing
  defect was demonstrated and no recapture is requested.

#### Phase 3B — Marked yellow-lid circular-object validation

- **Authorization:** circle validation authorized by the user; polygon validation and Phase 4 remain out of scope.
  Polygon validation and Phase 4 remain out of scope.
- **Status:** `CAPTURED — CHECKERBOARD AND POINT-LEVEL STEREO GATES PASS; CIRCLE PLANARITY GATE REJECTED`.
- **Supplied originals:** `data/physical_validation/IMG_7543.JPG` and `IMG_7544.JPG` are preserved.
  Both identify as Apple iPhone 15 Pro Max with native 5712×4284 storage pixels. Derived
  90-degree-clockwise copies were used for the calibrated 4284×5712 portrait frame; the originals,
  calibration, and scale were not changed.
- **Checkerboard-PnP evidence:** 54/54 corners were detected in both views. PnP RMS errors were
  1.937996 px and 2.537212 px, metric baseline was 29.038850 mm, and checkerboard median parallax
  was 4.465225°.
- **Correspondences:** fourteen black markers are visible in both images and match in clockwise order.
  Marker centers are not circle points. The correspondence CSV records the visible outer-rim point
  on the marker-defined ray. The first-pass rejected CSV and the corrected CSV are preserved.
- **Geometry result:** all 14 corrected points pass positive-depth and reprojection checks. Maximum
  reprojection errors are 1.940798 px and 1.933694 px; median rim parallax is 4.168084°; depths are
  322.448297–334.273879 mm. Recovered 3D planarity RMS/max are 2.641814/3.817464 mm, exceeding
  the existing 2.635175 mm planarity limit. The existing `measure_circle` workflow therefore does
  not produce an accepted diameter.
- **Physical evidence:** four lid-specific ruler originals are now preserved under
  `data/physical_validation/`. `IMG_7531.JPG` supports an approximate 100 mm horizontal outer-rim
  span and `IMG_7532.JPG` supports an approximate 100 mm vertical outer-rim span. `IMG_7533.JPG`
  provides qualitative diagonal corroboration only, and `IMG_7539.JPG` is indeterminate because blur,
  occlusion, and endpoint ambiguity prevent a defensible numeric reading. The current physical reference
  is `100.0 ± 2.0 mm`, interval `98.0–102.0 mm`; this conservative uncertainty accounts for the 1 mm
  ruler subdivisions plus endpoint alignment, perspective, and the fact that the zero mark is not visible
  in the accepted spans. The accepted boundary is the outermost rim, not the inner recessed ring. The
  value is physical-reference evidence only and was not used for scale or optimization. The earlier
  approximate 100 mm report remains preserved separately.
- **Physical-evidence record:**
  `results/object_measurements/circle_yellow_marked/IMG_7531_IMG_7532_IMG_7533_IMG_7539_lid_physical_measurement_evidence.json`.
- **Decision:** `MARKED STEREO PAIR PROCESSED; CIRCLE VALIDATION NOT ACCEPTED — PLANARITY QUALITY GATE`.
- **Evidence manifest:** `results/stereo_diagnostics/circle_yellow_marked/IMG_7543_IMG_7544_circle_validation_manifest.json`.
- **Planarity-gate audit:** the existing `measure_circle` implementation uses the pre-existing default
  `max_planarity_fraction=0.05` and rejects on `planarity_max`, not `planarity_rms`. The corrected
  fitted radius is 52.703507 mm, giving the 2.635175 mm limit; measured RMS/max are 2.641814/3.817464
  mm. The threshold was not changed for this experiment. A structured signed-residual pattern and
  leave-one-out review do not identify one demonstrably wrong point. The low 29.038850 mm baseline and
  4.168084° rim parallax make triangulation sensitive to pixel and pose error; controlled perturbation
  diagnostics support this as a plausible contributor, not a proof.
- **Current classification:** `UNRESOLVED EXPERIMENTAL GEOMETRY — LOW PARALLAX, POSE/EDGE-LOCATION
  SENSITIVITY, AND POSSIBLE RAISED-RIM MODEL AMBIGUITY`. No implementation defect or correspondence
  identity defect has been demonstrated. No thresholds, calibration, pose, or saved coordinates are
  being changed.
- **Physical evidence gate:** lid-specific ruler photographs are present and reviewed. They document a
  provisional `100.0 ± 2.0 mm` outer-rim reference, but they do not produce an accepted stereo diameter:
  the marked-lid reconstruction remains rejected by the pre-existing 3D planarity gate. The physical
  reference is not used to rescale, optimize, or relax any geometry gate.
- **Supplied originals:** `data/physical_validation/IMG_7540.JPG` and `IMG_7541.JPG` are preserved. Both
  report Apple iPhone 15 Pro Max, EXIF orientation 1, and native 5712×4284 pixels. The calibrated
  frame is 4284×5712, so 90-degree-clockwise derived copies were used for processing; calibration,
  originals, and scale were not changed.
- **Checkerboard-PnP evidence:** the existing workflow detected 54/54 corners in each view. PnP RMS
  errors were 1.609630 px and 2.552749 px; the recovered metric baseline was 109.650619 mm; and
  54/54 checkerboard points passed triangulation with median parallax 15.108784 degrees.
- **Circle correspondence decision:** visual review identifies the outermost rim in both views, but the
  plain yellow rim has no 8–16 unique physical points that can be verified across views. No lid CSV,
  lid parallax, triangulation, or circle fit is reported. Equal angular samples on the two ellipses would
  be invented correspondence and are prohibited by the experimental protocol.
- **Physical evidence:** the approximately 100 mm diameter is not accepted as ground truth yet because
  uncertainty is unfinished and lid-specific ruler photographs were not found in the Module 7 workspace.
  The existing flashcard ruler photographs remain separate historical evidence.
- **Decision and next action:** `VALID STEREO PAIR FOR CHECKERBOARD POSE ONLY; CIRCLE VALIDATION BLOCKED`.
  Repeat the experiment only with 8–16 removable perimeter markers (or a naturally marked circular
  object), and provide at least three outer-diameter readings with units, ruler resolution, uncertainty,
  and photographs showing zero and both endpoints. Do not use the 100 mm report to rescale or optimize.
- **Evidence manifest:** `results/stereo_diagnostics/circle_yellow/IMG_7540_IMG_7541_circle_evidence_manifest.json`.
- **Existing implementation:** reuse `src/module7/object_measurement.py::measure_circle`, which
  fits a least-squares circle in the recovered 3D boundary plane and reports metric radius and
  diameter. Reuse `scripts/process_stereo_pair.py --pose-method checkerboard_pnp` for the metric
  camera pose and `scripts/measure_object.py --shape circle` for the shape measurement.
- **Object requirements:** select a rigid, flat, opaque circular object with a clear perimeter and
  enough visible texture or perimeter features for repeated correspondence. Avoid flexible,
  transparent, reflective, beveled, or partially occluded objects.
- **Independent measurement:** measure the straight outer-edge-to-outer-edge diameter, not the
  circumference. Take at least three readings across different diameters, record every reading in
  millimetres, record the ruler/caliper resolution, and estimate uncertainty from resolution,
  endpoint alignment, perspective, and reading spread. Photograph the zero mark and both measured
  endpoints. If readings vary beyond the stated uncertainty, report the object as non-circular or
  revise the measurement record rather than averaging away the discrepancy.
- **Capture setup:** keep the circular object flat and fixed on a rigid support. Keep the 9×6
  checkerboard stationary and fully visible in both views, preferably on the same support plane and
  adjacent to the object without occluding its perimeter. Use the validated iPhone 15 Pro Max,
  unchanged calibrated lens/zoom/resolution/settings, and preserve full-resolution originals.
- **Stereo views:** capture view 1, move the phone laterally by the documented useful target of
  approximately 8–12 cm, and capture view 2 with similar orientation, substantial overlap, sharp
  focus, and no motion blur. Do not rotate the phone enough to lose the board or circle. Mark the
  object/support positions so neither the object nor checkerboard moves between views.
- **Correspondences:** after capture, identify 8–16 physical perimeter locations distributed around
  the circle in clockwise order. Use natural markings or small removable marks just inside the
  perimeter to identify the same boundary locations; select the actual edge intersection rather than
  a nearby texture point. Record each point in both images in the existing
  `point_id,u1,v1,u2,v2` CSV format. No pixel coordinates should be guessed before image review.
- **Processing gates:** after the originals are supplied, verify metadata and image compatibility,
  detect 54/54 checkerboard corners, recover checkerboard-PnP pose and baseline, and inspect
  parallax, positive depth, reprojection errors, boundary coplanarity, and circle-fit residuals.
  Only after all required landmarks triangulate successfully will the existing circle fit calculate
  a diameter. Compare that diameter with the independently measured physical mean and uncertainty;
  do not use the physical diameter to scale or optimize the reconstruction.
- **User capture gate:** pending the user's object choice, repeated measurements, ruler evidence,
  two original stereo images, and capture metadata. No circle images will be processed before those
  inputs are supplied.

#### Phase 3C — Polygon edge-length validation

- **Authorization:** polygon validation is authorized by the user; Phase 4 remains out of scope.
- **Status:** `EXPERIMENT COMPLETE — PHYSICAL MEASUREMENTS DOCUMENTED; STEREO TRIANGLE ACCURACY NOT VALIDATED`.
- **Implementation to reuse:** `src/module7/object_measurement.py::measure_polygon_from_stereo`
  performs metric landmark reconstruction through the existing calibrated triangulation checks before
  `measure_polygon` computes each adjacent Euclidean 3D edge. The command-line entry point is
  `scripts/measure_object.py --shape polygon`, with ordered vertex IDs and the existing
  `point_id,u1,v1,u2,v2` correspondence schema. `--require-planar` is available as a hard gate for
  the flat-object experiment; otherwise planarity remains a reported diagnostic.
- **Object:** rigid, flat cardboard triangle with three visible sharp vertices. The earlier
  missing-originals attempt is retained as historical provenance; no substitute image was used.
- **Independent measurements:** measure every visible edge at least three times with a metric ruler or
  tape, record every reading in millimetres, calculate the mean, and justify uncertainty from ruler
  resolution, endpoint alignment, perspective, and repeated-reading spread. Photograph the zero mark,
  units, and both exact endpoints for every edge. Do not use these measurements to rescale or optimize.
- **Capture setup:** keep the polygon and the 9×6 checkerboard with 25 mm squares rigid and stationary
  on a stable support. Use the calibrated iPhone 15 Pro Max with unchanged resolution, orientation,
  focus, exposure, zoom, and camera mode. Capture two sharp, overlapping views after an approximately
  80–120 mm lateral phone displacement, preserving the board and all polygon vertices. The actual metric
  pose and baseline come from checkerboard-PnP, not an assumed phone-body displacement.
- **Correspondences:** label a triangle `v0,v1,v2` or a pentagon `v0`–`v4` in clockwise order. After
  the original images are inspected, select the same physical corners in both portrait-coordinate
  images and record them in the existing CSV format. Do not guess coordinates or substitute bounding-box
  extrema/nearby marker centers.
- **Processing and validation gate:** after user capture, verify 54/54 checkerboard corners, camera
  compatibility, baseline, polygon parallax, positive depth, reprojection error, vertex identity,
  planarity, and nonzero valid edges. Reconstruct every vertex before calculating edge lengths. Compare
  each reconstructed edge with its independent physical mean and uncertainty interval; passing geometry
  checks alone is not a physical-accuracy pass.
- **Protocol:** `docs/polygon_validation_protocol.md`.
- **Originals and compatibility:** `data/physical_validation/IMG_7548.JPG` and `IMG_7549.JPG` are
  preserved at native 5712×4284 storage resolution. Both are iPhone 15 Pro Max files with EXIF
  orientation 6. The existing CLI processed the untouched OpenCV raw frames, which match the calibrated
  4284×5712 `(width,height)` frame; rotated copies were inspection-only.
- **Checkerboard-PnP result:** 54/54 corners were detected in both views. PnP RMS errors were
  1.603085/2.428876 px; baseline was 37.879812 mm; checkerboard median parallax was 5.321177°;
  and all checkerboard points passed the existing metric geometry checks.
- **Triangle correspondences and reconstruction:** clockwise IDs are `v0` left/top, `v1` right/top,
  `v2` lower corner in the normalized inspection frame. The three metric vertices were reconstructed
  with positive depth. Median triangle parallax was 4.423674°; maximum vertex reprojection errors were
  4.986292/4.973531 px, below the existing 5 px gate. The edge lengths were 150.497091 mm (`v0-v1`),
  144.814945 mm (`v1-v2`), and 152.796371 mm (`v2-v0`). Three-point planarity is mathematically
  non-discriminating; right-angle and opposite-edge checks do not apply.
- **Independent physical mapping:** ruler review maps `v0-v1` to side 1 = 110.00 mm (`IMG_7545.JPG`),
  `v1-v2` to base = 140.00 mm (`IMG_7546.JPG`), and `v2-v0` to side 2 = 136.00 mm (`IMG_7547.JPG`).
  The repeated readings and provisional ±1.00 mm uncertainty remain independent and were not used for
  scaling or optimization.
- **Comparison and decision:** signed errors are +40.497091 mm / +36.815538% for side 1,
  +4.814945 mm / +3.439246% for the base, and +16.796371 mm / +12.350272% for side 2. All three
  estimates fall outside their provisional reference intervals. The geometry gates pass, but physical
  accuracy is `NOT VALIDATED`.
- **Focused diagnostic investigation:** the original ruler photographs support the fixed edge mapping
  (`v0-v1` = side 1, `v1-v2` = base, `v2-v0` = side 2) and approximate reported readings, but the
  repeated readings remain user-reported records and ±1.00 mm remains provisional physical
  uncertainty. Re-detection returned 54/54 checkerboard corners with less than 0.000001 px maximum
  disagreement from the saved corner CSV. Re-estimated PnP changed the saved baseline by only
  0.000003 mm and the relative rotation difference was 0.0 degrees; re-triangulation reproduced
  the saved triangle vertices. No coordinate-frame, software, vertex-identity, or edge-mapping
  defect was demonstrated. The `v1` landmark is close to the 5 px reprojection gate, and the
  sensitivity audit shows it is the most consequential landmark under ±0.5/±1.0 px diagnostic
  perturbations. Three-point planarity is not an independent accuracy check. The experiment remains
  physically unvalidated and no correction is justified.
- **Evidence:**
  `results/object_measurements/polygon_phase3c/IMG_7548_IMG_7549_triangle_validation.json`,
  `results/object_measurements/polygon_phase3c/IMG_7548_IMG_7549_triangle_measurement.json`,
  `data/physical_validation/IMG_7548_IMG_7549_triangle_vertex_correspondences.csv`, and
  `results/stereo_diagnostics/polygon_phase3c/IMG_7548_IMG_7549_triangle_vertex_correspondences.png`.
  The prior blocked-input audit remains preserved at
  `results/object_measurements/polygon_phase3c/IMG_7548_IMG_7549_blocked_missing_originals_audit.json`.
  The diagnostic record and evidence manifest are
  `results/object_measurements/polygon_phase3c/IMG_7548_IMG_7549_triangle_diagnostic_investigation.json`
  and
  `results/stereo_diagnostics/polygon_phase3c/IMG_7548_IMG_7549_triangle_evidence_manifest.json`.

### Phase 3 completion audit before Phase 4

- **Question 1 conclusion:** the local standalone webpage requirement is fulfilled by Phase 3D.
  The calibrated-stereo core satisfies the depth-before-dimension design: metric triangulation,
  positive depth, parallax, and reprojection checks precede rectangle, circle, and polygon
  calculations. `app.py` and `src/module7/webapp/` now expose the required demonstrations through
  the established provider contract. Public dashboard integration is intentionally separate.
- **Shape evidence:** the Phase 2B flashcard width is validated only under its explicit equivalent-
  rectangular-edge assumption. Phase 3 rectangle experiments remain not physically validated; the
  marked yellow-lid circle is rejected by the existing planarity gate and has no accepted diameter;
  the triangle passes point-level geometry gates but fails all three independent physical edge
  intervals. These results remain evidence-backed limitations, not missing values to be replaced.
- **Calibration/methodology evidence:** the Module 2 original calibration photographs were
  recomputed through Module 7. The 9×6/25 mm target, camera matrix, distortion coefficients,
  checkerboard-PnP metric poses, correspondence CSVs, triangulated points, diagnostics, ruler
  records, and historical audit files are preserved. Exact active-lens EXIF fields are absent.
- **Confirmed technical limitations:** calibration/PnP residuals are nonzero; point-level gates are
  not physical-accuracy guarantees; the physical ±1/±2 mm values are ruler/reference uncertainty,
  not propagated stereo uncertainty; manual endpoint/perimeter localization is not formally
  propagated; and the circle/triangle geometry checks do not establish successful physical accuracy.
- **Hypotheses, not findings:** calibration/pose sensitivity, modest object parallax, and manual
  landmark localization likely contribute to shape discrepancies, but no unique cause was proven and
  no algorithm or threshold change is justified.
- **Resolved local blocker:** the webpage now uses the existing core/evidence paths, exposes all
  three shape paths and depth/3D diagnostics, preserves pending/rejected classifications, and has
  provider/smoke coverage. No algorithm, threshold, calibration, ground truth, or historical
  evidence was changed. This does not authorize Phase 4, dashboard work, or report generation.
- **Audit record:** `results/object_measurements/phase3_completion_audit.json`.

### Phase 3D — Standalone Question 1 webpage

- **Status:** `IMPLEMENTED AND TESTED — USER REVIEW PENDING`.
- **Entry point:** `app.py`; launch with `streamlit run app.py` from `Module_7/`.
- **Provider contract:** `src/module7/webapp/_page.py`, `registry.py`, `pages.py`, and `shell.py`
  provide `module_label`, `page_label`, `order`, `render`, and `get_pages()` through the existing
  standalone provider pattern.
- **Demonstrations:** rectangle, circle, and polygon pages load genuine saved Module 7 artifacts,
  original stereo images, and diagnostics. The rectangle page shows recovered 3D points and
  dimensions; the circle page explicitly shows the rejected planarity result and no accepted
  diameter; the polygon page shows reconstructed vertices/edges and failed physical comparisons.
  Missing or malformed evidence renders a pending/error state instead of fabricated output.
- **Tests:** 42 automated tests pass, including the original 33 core tests plus provider,
  artifact-integrity, malformed-evidence, application-import, and Streamlit AppTest smoke checks.
  `python3 -m compileall -q src scripts tests` also passes.
- **Scope boundary:** no calibration, pose, reconstruction, threshold, correspondence, physical
  measurement, dashboard, report, commit, push, or Phase 4 work was performed.

### Phase 3D audit — repository, webpage alignment, Git, and deployment readiness

- **Audit status:** `AUDIT COMPLETE — ALIGNMENT IMPLEMENTED; PUBLICATION REVIEW PENDING`.
- The gap bullets below preserve the pre-alignment baseline; the dedicated alignment section
  records the completed corrections.
- **Confirmed previous-module conventions:** Modules 2, 3, 4, and 5-6 are independent source-
  layout repositories with a thin `app.py`, a module-local `webapp.pages.get_pages()` provider,
  a structural page contract, a vendored `csc8830-ui` design package at kit version 0.6.0, a
  generated `.streamlit/config.toml`, an optional `webapp/summary.py`, public-copy tests, design-
  parity tests, and Streamlit AppTest coverage. The root and deployment dashboards adapt page
  objects structurally and do not import module runtime code.
- **Historical Module 7 gaps:** before this task there was no `.git` repository, vendored design
  package, generated theme, public-copy test, or design-parity test. The provider contract was
  structurally compatible with the dashboard adapter; this task corrected the authorized UI gaps
  without creating Git state.
- **Historical webpage/configuration gaps:** before this task the shell used bespoke CSS/raw
  presentation and exposed internal paths or phase wording, while `pyproject.toml` declared
  `streamlit>=1.36` without the established floor. The current implementation uses the vendored
  kit, generated theme, and public-copy-safe rendering.
- **Evidence/deployment gap:** the current page catalog directly references raw files under
  `data/physical_validation/` and generated files under `results/`. The local raw-capture tree is
  approximately 61 MB and the diagnostics tree approximately 758 MB. The current `.gitignore`
  excludes several result directories but does not establish a curated public evidence bundle;
  a fresh clone therefore cannot be assumed to render the current page. No exact evidence path can
  be called deployable until it is tracked in the future Module 7 repository and verified with
  `git ls-files`.
- **Documentation correction:** `docs/architecture.md` and README now describe the implemented
  core/web boundary, standalone launch, proposed evidence bundle, and optional dashboard workflow.
- **Privacy/integrity finding:** no secret-like text files or credential filenames were found in
  the Module 7 workspace scan. The original iPhone and ruler photographs remain user-collected
  material whose visual privacy and public-release permission must be reviewed individually. They
  must not be published merely because the local page can read them.

### Phase 3D standalone UI alignment and proposed evidence preparation

- **Status:** `IMPLEMENTED AND TESTED — USER PUBLICATION REVIEW PENDING`.
- Vendor the established `csc8830-ui` 0.6.0 package into the Module 7 web layer and generate
  the matching Streamlit theme configuration without changing the stereo core or saved results.
- Keep `app.py` thin and preserve the page-provider contract. Use shared shell, headers, sections,
  metrics, image comparison, gallery, and status components.
- Remove internal paths, development labels, and prohibited punctuation from rendered copy while
  retaining real validation failures, uncertainty, and pending states.
- Build the local proposed bundle at `data/proposed_public_demo/`. It contains 29 files totaling
  2,347,343 bytes (approximately 2.35 MB) and is marked `publication_approved: false`. Originals and
  complete experimental records remain preserved outside the bundle.
- Update README and architecture documentation. Add design parity, public-copy, evidence
  manifest, and standalone Streamlit smoke coverage while preserving the original 42 tests.
- **Verification:** expanded `pytest -q` passes 60 tests. The standalone runtime uses only the
  curated bundle and clean-clone AppTest rendering passes for all pages and curated examples.
  Dashboard wiring, Git initialization,
  repository publication, deployment, report generation, and Phase 4 remain unauthorized.

### Final standalone UI and public evidence review

- **Status:** `LOCAL REVIEW COMPLETE - PUBLICATION APPROVAL PENDING`.
- Exercise all four standalone pages with AppTest and inspect the resized evidence contact sheets.
  The shared shell, navigation, units, metrics, image comparisons, result sections, and honest
  status labels render without exceptions. Browser screenshot QA was unavailable because the local
  browser connector could not be initialized; this remains a visual-QA limitation.
- Preserve the complete 29-file inventory in `docs/public_evidence_review.md`. No reviewed image
  showed a face or explicit personal identifier, but workspace/background content remains visible
  and must be reviewed by the owner before publication.
- The proposed bundle is now the clean-clone runtime source. A clean clone containing only source,
  configuration, dependencies, and `data/proposed_public_demo/` renders all four pages and all
  seven curated examples without exceptions. The original 36-file local evidence set remains
  outside the runtime path.
- **Next approval gate:** review the 29 proposed assets image by image and decide whether any are
  approved for future tracking or publication. Do not initialize Git until that decision is made.
- **Visual review materials:** use the local-only gallery and contact sheet under `local_review/`.
  They are excluded from the public navigation and ignored for future tracking.
- **Metadata review:** compact records are path-free and contain no credentials, location fields,
  or unique device identifiers. The iPhone model is retained only for calibration provenance.
- **Ignore-policy blocker:** `.gitignore` does not currently exclude the approximately 61 MB
  `data/physical_validation/` or 758 MB `results/stereo_diagnostics/` trees. Tighten those patterns
  before any future staging operation; this task does not stage or initialize Git.

#### Proposed tracking manifest for a future independent Module 7 repository

| Category | Proposed contents | Decision/status |
| --- | --- | --- |
| Required source/configuration | `app.py`, `pyproject.toml`, `src/module7/` core and webapp, approved CLI scripts, generated `.streamlit/config.toml` | Track after design alignment |
| Required academic documentation | README, approved protocol/reference docs, architecture documentation, reproducibility instructions | Track after stale claims are corrected |
| Required tests | Core tests, web/provider tests, design-parity/public-copy tests, evidence-manifest tests, clean-clone smoke checks | Track and run before repository publication |
| Reproducible public evidence | A user-approved, small real Q1 evidence bundle: selected display images/thumbnails, compact JSON records, correspondence/diagnostic figures, and provenance manifest | Pending user public-data approval; must match app paths exactly |
| Optional/private evidence | Full-resolution original captures, all ruler photographs, rejected/working crops, large diagnostic images, complete audit history | Keep local unless explicitly approved; preserve privately |
| Ignored development artifacts | `.venv/`, caches, `__pycache__/`, egg-info, local review gallery, `data/physical_validation/`, `results/stereo_diagnostics/`, temporary crops, local reports, raw room videos, uncurated generated output | Explicitly ignored via `.gitignore`; verify before future staging |
| Sensitive material | Any capture containing private surroundings or personally identifying content, secrets, credentials, or unapproved raw experiment data | Exclude; review before any staging |

- **Recommended evidence strategy:** keep original experiments locally unchanged, create only
  user-approved derived display assets for public deployment, and make the webapp consume a small
  manifest-defined bundle. Do not blindly track all of `data/` or `results/`.

#### Minimal follow-up sequence after this alignment

1. User reviews the proposed Q1 evidence assets and approves or rejects each asset for any future
   public use; the current bundle remains local-only.
2. Initialize `Module_7/` as its own repository on a normal task branch; do not initialize the
   workspace root or copy another module's `.git` directory.
3. If approved, decide the future repository tracking policy and verify exact tracked bundle paths.
4. After standalone approval, make the separate root/deployment dashboard changes, add the Module 7
   sync case, run the documented headless smoke check, and verify the live page after deployment.

- **Approval gates:** no Git initialization, branch creation, dashboard edit, public evidence
  selection, deployment, report generation, or Phase 4 work is authorized by this audit request.

### Local Git initialization and staging review

- **Authorized scope:** initialize the independent local Module 7 repository and prepare staging
  only. Commit, remote creation, push, deployment, dashboard changes, reports, and Phase 4 remain
  unauthorized.
- **Branch:** `task/module-7-initial-repository`, following the independent task-branch workflow.
- **Allowlist:** source/configuration, tests, approved academic documentation, governance files
  reviewed for repository suitability, required scripts, and the approved 29-file curated bundle.
- **Exclusions:** full-resolution captures, uncurated diagnostics and results, `local_review/`,
  virtual environments, caches, bytecode, secrets, and private evidence.
- **Bundle state:** manifest integrity and all 21 approved image hashes must be verified before
  staging. The manifest records `publication_approved: true` for the user's reviewed bundle, but
  no publication or deployment has occurred.
- **Stopping point:** staged validation is complete. Report the 107-file staged contents and await
  explicit authorization before the first commit.

### Phase 4 — Room measurement from video

- **Goal:** implement metric room geometry from calibrated moving-camera smartphone video and
  quantify coverage and measurement error.
- **Inputs/dependencies:** Phase 2 calibration, approved reference-assisted room protocol,
  real smartphone video, a measured reference, and independent physical measurements.
- **Files involved:** `room_measurement.py`, video/room scripts, room data/results, tests, and
  room documentation.
- **Tasks:** ingest video; select frames; detect/match features; anchor poses with a metric
  reference where visible; reconstruct room landmarks; fit floor/wall/ceiling planes; connect
  overlapping segments if justified; compute length/width/height; export provenance.
- **Acceptance criteria:** the application either produces evidence-backed room dimensions or
  clearly explains why a requested dimension is pending/invalid; no monocular-scale claim is
  made.
- **Tests/validation:** synthetic room geometry; frame-selection and plane-fit tests; real
  repeated-frame and independent-measurement comparison.
- **Expected artifacts:** room reconstruction figures, dimension table, error analysis, and
  failure/coverage notes.
- **User involvement:** record moving room video, provide the measured reference and independent
  physical measurements, identify room boundaries, and approve public/private data handling.
- **Completion status:** not started.
- **Entry criteria for Phase 5:** standalone core workflow is callable without Streamlit and
  has either real validated evidence or an honest pending state.

### Phase 5 — Dashboard integration and public deployment

- **Goal:** after approval, integrate the completed standalone provider into the course dashboard
  and verify public deployment.
- **Inputs/dependencies:** completed core APIs, real/public sample policy, and deployment rules.
- **Files involved:** `app.py`, `src/module7/webapp/`, module tests, and later the two dashboard
  app copies plus deployment sync script.
- **Tasks:** add a committed real sample only if the user authorizes it; verify the page contract
  in the deployment environment; wire the dashboard only after explicit authorization.
- **Acceptance criteria:** standalone install/run works; every required component is reachable;
  pages never show fabricated data; dashboard and public link are not claimed ready until
  deployment verification is complete.
- **Tests/validation:** page-provider contract tests, Streamlit smoke test, exact sample
  `git ls-files` check, and deployment-repository smoke test when authorized.
- **Expected artifacts:** working standalone app and, later, verified dashboard pages.
- **User involvement:** approve public sample/data, provide handwritten scan, review UI copy,
  and authorize deployment-repository changes.
- **Completion status:** standalone page work completed in Phase 3D; dashboard/deployment not started.
- **Entry criteria for Phase 6:** all pages render under standalone smoke test.

### Phase 6 — Testing and experimental validation

- **Goal:** complete deterministic tests and genuine physical validation.
- **Inputs/dependencies:** all core/app phases and real data.
- **Files involved:** `tests/`, validation scripts, results, figures, and provenance docs.
- **Tasks:** run unit/synthetic tests; run calibration and object/room experiments; calculate
  actual errors; inspect figures and logs; document limitations.
- **Acceptance criteria:** claimed test results are executed and recorded; empirical claims have
  source data and physical references; failed/blocked tests are explicit.
- **Tests/validation:** pytest, real calibration review, object dimension comparisons, room
  measurements, and repeatability checks.
- **Expected artifacts:** test log, validated result tables, figures, and limitations.
- **User involvement:** perform physical measurements and authorize publication of genuine data.
- **Completion status:** not started.
- **Entry criteria for Phase 7:** no unexplained fabricated or placeholder empirical values.

### Phase 7 — Handwritten derivation, DOCX/PDF report, citations, and demonstration

- **Goal:** complete the editable Word report, faithful PDF export, handwritten Q2 evidence,
  citations, screenshots, and video.
- **Inputs/dependencies:** approved implementation and validated results.
- **Files involved:** `docs/report/`, `docs/references.md`, `docs/DEMO_VIDEO_CHECKLIST.md`,
  scanned derivation, `Module_7_Assignment_Report.docx`,
  `Module_7_Assignment_Report.pdf`, and README.
- **Tasks:** build the editable DOCX from the report outline/evidence manifest; embed the user's
  scanned handwritten pages; add inline citations; export PDF with a documented mechanism;
  visually compare DOCX/PDF pagination and content; capture genuine screenshots; produce the
  demo checklist.
- **Acceptance criteria:** Q2 remains demonstrably handwritten in both outputs; all references
  are cited; every screenshot/result corresponds to an executed workflow; GitHub link is
  present; DOCX and PDF contain the same academic content.
- **Tests/validation:** DOCX render review, PDF render review, page-by-page DOCX/PDF comparison,
  citation audit, screenshot provenance audit, and video checklist review.
- **Expected artifacts:** editable Word source, faithful PDF export, citation ledger, scanned
  derivation, and demonstration recording.
- **User involvement:** supply original handwriting scan, review report wording, record video,
  and confirm submission links.
- **Completion status:** not started.
- **Entry criteria for Phase 8:** PDF and video draft contain all required evidence.

### Phase 8 — Final submission readiness

- **Goal:** verify that code, repository, app, public link if used, DOCX, PDF, video, and
  Classroom submissions are complete and consistent.
- **Inputs/dependencies:** all prior phase artifacts.
- **Files involved:** final repository, deployment mirror if used, DOCX, PDF, video, and status
  file.
- **Tasks:** run clean-clone checks; verify public repository access; verify deployment; compare
  report claims with committed evidence; confirm no secrets/private data/fabricated values.
- **Acceptance criteria:** independent clone installs and runs; required pages are reachable;
  all submitted claims are classified and supported; DOCX/PDF are content-consistent and ready
  for Classroom; video is playable.
- **Tests/validation:** clean-environment install, pytest, Streamlit smoke test, public-link
  check, DOCX/PDF render and content comparison, video playback review, and final traceability
  audit.
- **Expected artifacts:** final repository and submission package.
- **User involvement:** final approval and Google Classroom upload.
- **Completion status:** not started.
- **Entry criteria:** all required evidence and links are verified.

---

## 7. Citation strategy

The eventual `docs/references.md` must record title, author/organization, publication details,
URL or DOI, access date when appropriate, and the report section using each source. At minimum,
the report should cite authoritative sources for:

- camera calibration and distortion;
- stereo calibration, rectification, disparity-to-depth, and triangulation;
- epipolar geometry, fundamental/essential matrices, and projective reconstruction;
- metric reconstruction and scale ambiguity;
- the selected OpenCV algorithms and any public dataset or reference image;
- any room-measurement method beyond the project's own derivation.

The initial verified reference set for later citation review is:

1. OpenCV, **Camera Calibration**, OpenCV-Python Tutorials,
   <https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html>.
2. OpenCV, **Camera Calibration and 3D Reconstruction**, OpenCV 4.x `calib3d` reference,
   <https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html>.
3. Richard Hartley and Andrew Zisserman, **Multiple View Geometry in Computer Vision**, 2nd
   ed., Cambridge University Press, 2004, publisher information and sample chapters at
   <https://robots.ox.ac.uk/~vgg/hzbook/index.html> and DOI
   <https://doi.org/10.1017/CBO9780511811685>.

These references are a starting strategy, not a completed report bibliography. Additional
sources must be verified before inclusion; no DOI, dataset, or citation should be invented.

---

## 8. Risks and decisions requiring approval

| Risk/decision | Why it matters | Proposed response |
| --- | --- | --- |
| One phone has no simultaneous stereo pair | Q1 still needs a defensible per-pair pose and metric scale | Use sequential calibrated stereo, measured camera-center displacement, essential-matrix pose, and cheirality/reprojection checks |
| Camera baseline too small or unknown | Depth uncertainty and scale failure | Measure/record baseline and validate on known distances |
| One room path cannot see all boundaries | A partial reconstruction cannot determine the room | Use overlapping reference-assisted video segments, or mark unobserved dimensions pending |
| Poor texture/occlusion | Correspondence and plane fitting fail | Use visible landmarks/texture, quality checks, and honest invalid states |
| Q2 scanned work unavailable | Final PDF cannot satisfy the handwritten requirement | Keep the page pending; user supplies original scan before Phase 7 completion |
| Public data/privacy | Room video may reveal private information | Keep raw videos private unless user explicitly authorizes a small public evidence subset |
| Dashboard integration before standalone readiness | Deployment can mask module defects | Defer root/deployment edits until Phase 5 acceptance |
| Exact assignment wording versus recommendations | Recommendations must not become hidden requirements | Keep confirmed requirements and recommendations labeled separately in the instructions |

The main unresolved dependencies after Phase 3 implementation are: shape-specific stationary
validation objects, verified landmark correspondences, ruler/tape measurements, room reference
geometry, room access, independent measurements, and a decision about whether any real sample may
be committed publicly. Phase 4 remains separately approval-gated.
