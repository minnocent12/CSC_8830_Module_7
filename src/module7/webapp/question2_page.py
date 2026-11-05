"""Question 2 theory overview and honest handwritten-deliverable state."""
from __future__ import annotations

import streamlit as st

from module7.webapp._page import PageSpec
from module7.webapp.ui import page_header, section


def render_question2_page() -> None:
    page_header(
        "Question 2 uncalibrated stereo",
        "Theory overview for the required handwritten derivation of projective stereo geometry.",
        eyebrow="Question 2 / Uncalibrated stereo",
    )
    st.info("This public page is theory-only. The original handwritten scan is intentionally excluded from the runtime application and remains part of the private submission package.")
    section("Assignment requirement")
    st.markdown(
        "Question 2 requires a handwritten derivation of object-dimension estimation using "
        "uncalibrated stereo. Typed mathematics and automatically generated handwriting are not "
        "acceptable substitutes for the submitted derivation."
    )
    section("Theory overview")
    st.markdown(
        "For corresponding homogeneous image points x and x', unknown projective cameras P and P' "
        "satisfy x ~ P X and x' ~ P' X. Their correspondence obeys the fundamental-matrix relation:"
    )
    st.latex(r"{x'}^T F x = 0")
    st.markdown(
        "The fundamental matrix is defined up to a nonzero scalar and has rank two. Projective "
        "triangulation can recover a 3D point up to a projective transformation, but arbitrary "
        "projective transformations do not preserve Euclidean lengths. A metric reference, metric "
        "upgrade, or additional scene assumptions are therefore required before reporting physical "
        "object dimensions."
    )
    section("Required hand-copy sequence")
    st.markdown(
        "The guide covers the camera model, epipolar derivation, normalized eight-point SVD, rank-two "
        "enforcement, projective triangulation, dimension relationships, the projective ambiguity, "
        "and the metric-scale conclusion. It also specifies the required epipolar-geometry diagram."
    )
    st.info("The handwritten derivation guide and checklist are preparation aids; the original pages remain separate from this public runtime page.")


def get_pages() -> tuple[PageSpec, ...]:
    return (PageSpec("Module 7", "Question 2 uncalibrated stereo", 35, render_question2_page),)
