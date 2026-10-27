# CSc 8830: Computer Vision

## Module 7 Assignment — Questions and Requirements

> **Global requirement:** **ALL REFERENCES MUST BE CITED IN YOUR ASSIGNMENT REPORTS.**

This document preserves the authoritative Module 7 requirements supplied for this assignment.
Implementation planning notes are clearly labeled and do not replace the requirements.

---

## Question 1 — Object Size Estimation Using Calibrated Stereo

Re-implement and demonstrate on the webpage the object-size estimation method from Assignment
1, this time using **CALIBRATED STEREO**.

The implementation must first estimate the distance/depth `Z` between a point in 3D space and
the camera, then use the estimated depth to determine physical object dimensions. The webpage
must demonstrate the actual calibrated-stereo workflow; it must not simply accept a manually
entered camera-to-object distance and reuse Module 2's original method.

Required shape handling:

- **Rectangular:** estimate width and length, or width and height, depending on the view.
- **Circular:** estimate diameter.
- **Other polygonal shapes:** estimate all visible polygon edge dimensions.

The final measurement path must use real stereo image observations, calibrated camera
parameters, and metric geometry. Any result requiring user-captured data remains pending until
that data is supplied and processed.

## Question 2 — Uncalibrated Stereo Mathematical Derivation

**NO IMPLEMENTATION NECESSARY.**

Derive by hand the procedure for estimating object dimensions using **UNCALIBRATED STEREO**.
Show the mathematical procedure, all calculations and intermediate steps, the mathematical
relationships, and the assumptions.

**Handwritten derivations are required. Typed derivations are explicitly NOT ACCEPTED for this
question.** Do not replace the handwritten work with a typed mathematical report, digitally
typeset equations, or an automatically generated solution presented as handwriting.

The user must complete the handwritten derivation. The application and documentation may
provide a theory overview, instructions, a verification checklist, and a place to display the
scanned work. The scanned handwritten solution must be included in the final PDF.

The derivation must explicitly identify the metric-scale ambiguity: uncalibrated stereo does
not generally recover unique real-world dimensions from two images alone. Any additional
metric reference or assumption required for absolute dimensions must be stated.

## Question 3 — Video-Based Room Dimension Estimation

Implement an application that estimates the dimensions of a room in a house using videos.
Stereo camera setups are permitted.

The application should ultimately support estimation of room dimensions such as:

- room length;
- room width;
- room height.

The method must explain how video observations produce metric 3D measurements, including
calibration, camera geometry, camera movement, reconstruction, and scale recovery where
applicable. The submission must not claim that an ordinary uncalibrated monocular video
automatically provides accurate absolute dimensions.

Room dimensions, accuracy values, and validation results must come from real recordings and
physical measurements. Until they exist, they are `PENDING USER EXPERIMENT`.

---

## Traceability notes for the implementation plan

The plan maps the requirements as follows:

| Requirement | Planned evidence |
| --- | --- |
| Calibrated stereo object measurement | Calibration record, rectification/depth evidence, 3D landmarks, shape-specific dimensions, validation table, web page |
| Uncalibrated stereo derivation | User's scanned handwritten derivation, verification checklist, theory page, final PDF appendix |
| Video-based room measurement | Captured video provenance, calibration/scale record, reconstructed room geometry, measurements, validation comparison, web page |
| Citation requirement | `docs/references.md`, inline citations in report sections, cited equations/figures/datasets |
