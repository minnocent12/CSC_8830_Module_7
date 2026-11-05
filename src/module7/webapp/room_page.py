"""Public-safe Question 3 summary page.

The page deliberately reads one tracked summary artifact. Private room videos,
calibration files, reconstruction manifests, and held-out physical measurements
are never runtime dependencies of the public application.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import streamlit as st

from module7.webapp._page import PageSpec
from module7.webapp.ui import diagnostic_table, metric_row, page_header, section

_ROOT = Path(__file__).resolve().parents[3]
_PUBLIC_SUMMARY = _ROOT / "data" / "proposed_public_demo" / "question3_summary.json"
_EXPECTED_STATUS = "DIAGNOSTIC-ONLY PARTIAL RECONSTRUCTION — ROOM DIMENSIONS NOT RECOVERED."


def _load_public_summary() -> dict[str, Any] | None:
    """Load only the tracked, path-free public Question 3 summary."""
    try:
        value = json.loads(_PUBLIC_SUMMARY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def _metric_value(value: Any) -> str:
    return str(value) if value is not None else "N/A"


def render_room_page() -> None:
    """Render the public-safe Question 3 status and diagnostics."""
    page_header(
        "Question 3 room reconstruction",
        "Calibrated multiview room evidence with explicit metric-connectivity and endpoint gates.",
        eyebrow="Question 3 / Room dimension estimation",
    )
    summary = _load_public_summary()
    if summary is None:
        st.error("The tracked public Question 3 summary is unavailable or malformed.")
        st.info("PENDING: restore the public summary before this page can be displayed.")
        return

    status = summary.get("scientific_status")
    if status != _EXPECTED_STATUS:
        st.error("The public Question 3 summary has an unexpected scientific status.")
        return

    # The stored scientific status preserves the report wording. The UI uses
    # ASCII punctuation to match the established public-copy rendering rule.
    st.warning(status.replace("—", "-"))
    st.markdown(
        "The application presents public-safe aggregate diagnostics only. "
        "It does not bundle room footage, private calibration artifacts, or the independent physical reference."
    )

    method = summary.get("method", {})
    section("Research objective and method")
    st.markdown(
        "Question 3 estimates room length, width, and height from calibrated moving-camera video. "
        "The workflow uses video-mode calibration, checkerboard metric anchoring, feature correspondence, "
        "calibrated epipolar checks, triangulation, and metric 2D-3D pose checks. "
        "Image matches or homographies alone are never treated as metric registration."
    )
    diagnostic_table([
        ("Capture", method.get("capture", "not recorded")),
        ("Video condition", method.get("video_resolution", "not recorded")),
        ("Metric scale anchor", method.get("metric_scale", "not recorded")),
        ("Scale rule", method.get("scale_rule", "not recorded")),
    ])

    diagnostics = summary.get("aggregate_diagnostics", {})
    section("Aggregate reconstruction diagnostics")
    metric_row([
        ("Room recordings reviewed", _metric_value(diagnostics.get("room_recordings_reviewed"))),
        ("Accepted checkerboard poses", _metric_value(diagnostics.get("accepted_checkerboard_metric_poses"))),
        ("Metric bridge points", _metric_value(diagnostics.get("metric_anchor_triangulation_points"))),
        ("Accepted metric views", _metric_value(diagnostics.get("accepted_metric_camera_views"))),
    ])
    diagnostic_table([
        ("Epipolar-verified connections", diagnostics.get("epipolar_verified_connections", "not recorded")),
        ("Homography-only connections", diagnostics.get("homography_only_connections", "not recorded")),
        ("Weak connections", diagnostics.get("weak_connections", "not recorded")),
        ("Metric room-endpoint gate", diagnostics.get("metric_room_endpoint_gate", "not recorded")),
    ])
    st.caption("Aggregate connections are image/geometry diagnostics. They do not by themselves establish a common metric room frame.")

    section("Dimension availability")
    dimensions = summary.get("dimension_results", {})
    for name in ("room_length", "room_width", "room_height"):
        item = dimensions.get(name, {})
        st.write(f"{name.replace('_', ' ').title()}: {item.get('status', 'N/A')} - {item.get('reason', 'not available')}")

    validation = summary.get("validation", {})
    section("Independent validation boundary")
    diagnostic_table([
        ("Physical reference", validation.get("independent_physical_reference", "not recorded")),
        ("Comparison status", validation.get("comparison_status", "not recorded")),
        ("Percentage errors", validation.get("percentage_errors", "N/A")),
        ("Instrument uncertainty", validation.get("instrument_uncertainty", "not recorded")),
    ])
    st.caption("The independent physical reference is validation-only and its exact values are intentionally absent from the public application.")

    section("Limitations and reproducibility")
    for limitation in summary.get("limitations", []):
        st.markdown(f"- {limitation}")
    reproducibility = summary.get("reproducibility", {})
    diagnostic_table([
        ("Public runtime inputs", ", ".join(reproducibility.get("public_runtime_inputs", []))),
        ("Private experiment inputs", reproducibility.get("private_experiment_inputs", "not recorded")),
        ("Status classification", reproducibility.get("status_classification", "not recorded")),
    ])


def get_pages() -> tuple[PageSpec, ...]:
    return (PageSpec("Module 7", "Question 3 room reconstruction", 40, render_room_page),)
