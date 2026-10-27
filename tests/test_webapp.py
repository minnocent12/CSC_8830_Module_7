"""Deterministic contract and evidence-integrity tests for the Question 1 web app."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from module7.webapp._page import PageSpec
from module7.webapp.evidence import load_curated_bundle
from module7.webapp.pages import CIRCLE_SPECS, RECTANGLE_SPECS, get_pages
from module7.webapp.registry import collect_pages
from module7.webapp.ui import load_evidence_record

ROOT = Path(__file__).resolve().parents[1]


def test_page_provider_has_required_contract_and_stable_order() -> None:
    pages = collect_pages([get_pages])
    assert pages
    assert [page.page_label for page in pages] == [
        "Overview",
        "Rectangle measurements",
        "Circle measurements",
        "Polygon measurements",
    ]
    for page in pages:
        assert isinstance(page, PageSpec)
        assert page.module_label == "Module 7"
        assert callable(page.render)


def test_saved_examples_load_without_fabricating_data() -> None:
    bundle, error = load_curated_bundle(ROOT)
    assert error is None and bundle is not None
    for spec in (*RECTANGLE_SPECS, *CIRCLE_SPECS):
        loaded = bundle.load_record(spec.record_asset)
        assert loaded.error is None
        assert loaded.data is not None
        assert loaded.data.get("status")


def test_validation_labels_preserve_rejected_and_pending_evidence() -> None:
    bundle, error = load_curated_bundle(ROOT)
    assert error is None and bundle is not None
    marked_circle = bundle.load_record(CIRCLE_SPECS[0].record_asset).data
    unmarked_circle = bundle.load_record(CIRCLE_SPECS[1].record_asset).data
    assert marked_circle is not None and "REJECTED" in marked_circle["status"]
    assert unmarked_circle is not None and "PENDING" in unmarked_circle["status"]
    assert marked_circle["rim_reconstruction"]["circle_fit"].startswith("NOT ACCEPTED")


def test_missing_and_malformed_evidence_are_reported_without_raising(tmp_path: Path) -> None:
    missing = load_evidence_record(tmp_path / "missing.json")
    assert missing.data is None
    assert missing.error and "missing" in missing.error.lower()

    malformed_path = tmp_path / "malformed.json"
    malformed_path.write_text("not json", encoding="utf-8")
    malformed = load_evidence_record(malformed_path)
    assert malformed.data is None
    assert malformed.error and "could not be loaded" in malformed.error.lower()

    scalar_path = tmp_path / "scalar.json"
    scalar_path.write_text(json.dumps([1, 2, 3]), encoding="utf-8")
    scalar = load_evidence_record(scalar_path)
    assert scalar.data is None
    assert scalar.error and "object" in scalar.error.lower()


def test_no_circle_example_exposes_an_accepted_diameter() -> None:
    bundle, error = load_curated_bundle(ROOT)
    assert error is None and bundle is not None
    for spec in CIRCLE_SPECS:
        record = bundle.load_record(spec.record_asset).data
        assert record is not None
        rim = record.get("rim_reconstruction", {})
        if rim:
            assert "NOT ACCEPTED" in rim.get("circle_fit", "") or record.get("physical_measurement", {}).get("stereo_diameter_mm") is None


def test_standalone_app_imports_without_starting_phase_four() -> None:
    import importlib.util

    spec = importlib.util.spec_from_file_location("module7_standalone_app", ROOT / "app.py")
    assert spec is not None and spec.loader is not None
    app = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app)
    assert callable(app.main)
    assert not (ROOT / "src" / "module7" / "room_measurement.py").exists()


@pytest.mark.parametrize(
    "page_label, expected_errors",
    [
        ("Rectangle measurements", 0),
        ("Circle measurements", 2),
        ("Polygon measurements", 1),
    ],
)
def test_streamlit_shape_pages_smoke_without_exceptions(page_label: str, expected_errors: int) -> None:
    from streamlit.testing.v1 import AppTest

    app = AppTest.from_file(str(ROOT / "app.py")).run()
    assert not app.exception
    app.sidebar.radio[0].set_value(page_label).run()
    assert not app.exception
    assert len(app.selectbox) == 1
    assert len(app.error) == expected_errors


def test_clean_clone_renders_from_curated_bundle_without_original_evidence(tmp_path: Path) -> None:
    import shutil
    from streamlit.testing.v1 import AppTest

    shutil.copy(ROOT / "app.py", tmp_path / "app.py")
    shutil.copy(ROOT / "pyproject.toml", tmp_path / "pyproject.toml")
    shutil.copytree(ROOT / "src", tmp_path / "src")
    shutil.copytree(ROOT / ".streamlit", tmp_path / ".streamlit")
    shutil.copytree(ROOT / "data" / "proposed_public_demo", tmp_path / "data" / "proposed_public_demo")
    app = AppTest.from_file(str(tmp_path / "app.py"), default_timeout=120).run()
    assert not app.exception
    for page_label in ("Rectangle measurements", "Circle measurements", "Polygon measurements"):
        app.sidebar.radio[0].set_value(page_label).run()
        assert not app.exception, page_label


def test_every_curated_experiment_selection_renders_without_exceptions() -> None:
    from streamlit.testing.v1 import AppTest

    app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=120).run()
    for page_label in ("Rectangle measurements", "Circle measurements", "Polygon measurements"):
        app.sidebar.radio[0].set_value(page_label).run()
        for example in list(app.selectbox[0].options):
            app.selectbox[0].set_value(example).run()
            assert not app.exception, f"{page_label}: {example}"
