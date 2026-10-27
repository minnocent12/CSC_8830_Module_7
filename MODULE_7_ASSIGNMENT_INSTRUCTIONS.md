# CSc 8830: Computer Vision

## Module 7 Assignment — Submission Instructions

The following confirmed submission conventions follow the established Module 2 and Module 4
instruction documents. Module 7-specific requirements are called out explicitly.

### 1. GitHub Repository

- Maintain the Module 7 source code in its own GitHub repository, consistent with the
  independent-repository convention used by earlier modules.
- The repository must be accessible to the instructor at submission time.
- Include the accessible GitHub repository link in the final PDF.
- Do not commit private recordings, secrets, fabricated results, or files excluded by the
  repository's documented data policy.

### 2. Source Code Documentation

Document every submitted script and the independent installation workflow. The README must
describe the purpose, dependencies, setup, standalone app execution, experiment execution,
reproducibility steps, and known limitations. Keep calibrated geometry and measurement logic
importable and separate from Streamlit code.

All methodological claims and externally derived equations used in the report must be cited.

### 3. Web Application Demonstration

Create a working web application that exposes all Module 7 assignment components.

- Question 1 must show a working calibrated-stereo object-measurement workflow, including
  calibrated depth rather than a manually entered distance substituted into the old method.
- Question 2 must show the theory overview and either the user's scanned handwritten derivation
  or a clearly marked pending state; it must not present typed mathematics as the required
  handwritten deliverable.
- Question 3 must show the working video-based room-measurement workflow once real recordings
  and calibration/scale data are available.
- Results pages must distinguish implemented, tested, experimentally validated, theoretically
  derived, and pending user-data claims.

The standalone app is required. Later, once the module is approved and implemented, the pages
may be mounted in the course dashboard through the established `get_pages()` contract. The
public dashboard link is not considered complete until deployment is actually wired and
verified under `DEPLOYMENT.md`.

### 4. Demonstration Video

Record a demonstration showing the application running, the relevant inputs, processing, and
outputs. For Module 7, the video must show the implemented Question 1 calibrated-stereo
features and the implemented Question 3 room-measurement features. It should also show the
Question 2 theory page and the scanned handwritten derivation when available.

Do not record or present fabricated calibration, depth, room-dimension, timing, or validation
values as experimental evidence.

### 5. Final PDF Documentation

The final assignment report must be produced in both Microsoft Word and PDF formats:

- `Module_7_Assignment_Report.docx` — editable primary report source;
- `Module_7_Assignment_Report.pdf` — faithful, submission-ready export.

The Word and PDF reports must contain the same academic content. The final PDF should include,
as applicable:

- assignment title and identification;
- problem description;
- implementation and architecture explanation;
- calibrated-stereo, reconstruction, and room-measurement methods;
- results, validation, error analysis, screenshots, and figures;
- a citation-backed references section;
- the accessible GitHub repository link;
- the handwritten Question 2 derivation as a scanned appendix or embedded pages;
- known limitations and any still-pending user experiment.

The Word document should use consistent heading styles, numbered sections, editable tables,
figure captions, units, equations, citations, and page layout. The PDF export must be visually
checked for page breaks, tables, equations, figures, citations, hyperlinks, and the embedded
handwritten derivation. Do not generate either final report during Phase 1; report production
belongs to Phase 7 after genuine implementation and experiment evidence exists.

The complete source code does not need to be pasted into the PDF; it belongs in the repository.

### 6. Solve-by-Hand Requirements

Question 2 requires an original handwritten mathematical derivation of uncalibrated stereo.
Typed derivations, digitally typeset equations, and automatically generated handwriting are
not acceptable substitutes for that requirement.

The completed handwriting must be scanned with a document-scanner workflow or equivalent
acceptable scanning process and embedded in or appended to the final PDF. A plain camera photo
of paper is not an acceptable final format under the established course convention.

The derivation must show the mathematical procedure, intermediate steps, assumptions,
fundamental matrix and epipolar relationships, projective reconstruction, object-dimension
relationships, and metric-scale ambiguity. The application may provide only a theory overview,
instructions, and a verification checklist.

### 7. Submission Checklist

- [ ] All three Module 7 questions are addressed.
- [ ] Question 1 uses a real calibrated-stereo depth and 3D measurement workflow.
- [ ] Question 2 handwritten derivation is original, scanned, and included in the PDF.
- [ ] Question 3 video-based room measurement is implemented and documented.
- [ ] No empirical values are fabricated; pending work is labeled honestly.
- [ ] All references are cited in the report, including equations, figures, datasets, and
      external algorithms where applicable.
- [ ] Source code is commented and the README explains setup and execution.
- [ ] The GitHub repository is accessible and its link appears in the PDF.
- [ ] The standalone web application works and exposes the required components.
- [ ] The public dashboard is wired and verified if it is used for the submitted web link.
- [ ] The demonstration video shows the implemented inputs, processing, and outputs.
- [ ] The final PDF contains results, figures/screenshots, limitations, and validation evidence.
- [ ] The editable Word report and faithful PDF report contain the same academic content.
- [ ] The handwritten derivation is embedded in both the Word and PDF reports.
- [ ] The final PDF and demonstration video are submitted through Google Classroom.

### 8. Final Submission

Submit the final PDF documentation and demonstration video through Google Classroom. The
GitHub repository itself need not be uploaded separately, but its accessible link must be
included in the PDF.

#### Confirmed requirements versus project recommendations

Confirmed requirements are the three questions, the handwritten Question 2 constraint, the
web demonstration, repository/PDF/video conventions, citation requirement, and integrity
requirements above. The following are project recommendations rather than additional
professor requirements: the exact page names, a fixed calibrated stereo rig as the preferred
room method, the proposed directory layout, the test categories, and the use of OpenCV's
specific stereo APIs.
