# AGENTS.md — CSc 8830 Module 7

This file refines the root `Assignments/AGENTS.md`; the root rules remain authoritative.

## Sources of truth

Before changing Module 7, read:

1. `../AGENTS.md`, `../GIT_WORKFLOW.md`, and `../DEPLOYMENT.md` when available.
2. `MODULE_7_ASSIGNMENT_QUESTIONS.md`.
3. `MODULE_7_ASSIGNMENT_INSTRUCTIONS.md`.
4. `IMPLEMENTATION_PLAN.md` and `IMPLEMENTATION_STATUS.md`.

The professor requirements in `MODULE_7_ASSIGNMENT_QUESTIONS.md` take precedence over this
plan and over implementation convenience.

## Phase gate

Phase 0 is approved and Phase 1 is the current technical-design phase. Do not implement
calibrated-stereo, uncalibrated-stereo, room-measurement, Streamlit, or final-report-generation
code until the user reviews and approves the Phase 1 artifacts. Question 2 has no measurement
implementation requirement; its final derivation must be the user's original handwritten work,
scanned with a document-scanner workflow and included in both the DOCX and PDF reports.

## Integrity

- Never invent calibration values, stereo baselines, depth values, room dimensions,
  correspondence counts, error metrics, screenshots, timings, or validation results.
- Mark unavailable empirical material as `PENDING USER EXPERIMENT`, `NOT MEASURED`, or
  `NOT VALIDATED`.
- Synthetic fixtures may verify deterministic software only; they are not real experimental
  evidence.
- Keep raw recordings and private captures out of the public repository unless the user
  explicitly chooses to publish them and the repository policy permits it.
- Cite every external methodological claim, equation, dataset, or figure used in reports.

## Independence and architecture

Module 7 must be independently installable and runnable. It may reuse architectural patterns
from other modules, but it must not import another module's runtime code. Core geometry and
measurement code must remain separate from Streamlit UI code. The future web provider must
expose page objects with `module_label`, `page_label`, `order`, and callable `render`, plus a
`get_pages()` provider.

## Git

Treat `Module_7/` as a future independent repository, consistent with Modules 2, 3, 4, and
5–6. Inspect repository state before creating a branch or changing history. Do not initialize
or modify a Git repository at the `Assignments/` root. Do not commit or push Phase 0 artifacts
without the user's authorization.
