"""Public-copy checks for text rendered by the standalone application."""
from __future__ import annotations

import re
from pathlib import Path

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
DASHES = (chr(0x2013), chr(0x2014))
INTERNAL = re.compile(
    r"IMPLEMENTATION_PLAN|\b[A-Za-z_]+\.md\b|\bdocs/|\bresults/|\bdata/|\bscripts/|\bsrc/|\.py\b|\bPhase \d",
    re.IGNORECASE,
)
DEVELOPER_COPY = re.compile(r"publication|manifest|deployment|curated bundle|developer", re.IGNORECASE)


def _visible_text(app: AppTest) -> list[str]:
    texts: list[str] = []
    for kind in ("title", "header", "subheader", "markdown", "caption", "info", "warning", "success", "error"):
        texts.extend(str(element.value) for element in getattr(app, kind))
    texts.extend(str(metric.label) for metric in app.metric)
    texts.extend(str(metric.value) for metric in app.metric)
    for kind in ("radio", "selectbox"):
        texts.extend(str(widget.label) for widget in getattr(app, kind))
    texts.extend(element.proto.body for element in app.get("html") if "<style" not in element.proto.body)
    return texts


def _table_text(app: AppTest) -> str:
    return "\n".join(table.value.to_string(index=False) for table in app.table)


def test_public_page_source_has_no_prohibited_dash_punctuation() -> None:
    for path in (ROOT / "src/module7/webapp/pages.py", ROOT / "src/module7/webapp/ui.py", ROOT / "src/module7/webapp/shell.py"):
        assert not any(dash in path.read_text(encoding="utf-8") for dash in DASHES), path


def test_all_rendered_pages_omit_internal_copy_and_retain_real_statuses() -> None:
    app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=120).run()
    assert not app.exception
    page_labels = list(app.sidebar.radio[0].options)
    problems = []
    for page in page_labels:
        app.sidebar.radio[0].set_value(page).run()
        assert not app.exception, page
        for text in _visible_text(app):
            if any(dash in text for dash in DASHES):
                problems.append((page, "dash", text[:100]))
            references = INTERNAL.findall(text)
            if references:
                problems.append((page, references, text[:100]))
            if DEVELOPER_COPY.search(text):
                problems.append((page, "developer copy", text[:100]))
    assert not problems, problems


def test_public_ui_source_does_not_render_record_paths() -> None:
    text = (ROOT / "src/module7/webapp/pages.py").read_text(encoding="utf-8")
    assert "Evidence source" not in text


def test_public_metadata_uses_readable_labels() -> None:
    app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=120).run()
    assert not app.exception
    app.sidebar.radio[0].set_value("Rectangle measurements").run()
    assert not app.exception
    visible = "\n".join(_visible_text(app))
    assert "Calibration source" in visible
    assert "module2-originals-module7-recompute" not in visible
    assert "Metric baseline" in visible


def test_status_labels_are_student_facing_but_machine_statuses_remain_supported() -> None:
    from module7.webapp.ui import status_text

    assert status_text("PHYSICAL VALIDATION COMPLETE UNDER EQUIVALENT-RECTANGULAR-EDGE ASSUMPTION") == (
        "Validated under stated assumption"
    )
    assert status_text("EXPERIMENT DOCUMENTED — PHYSICAL REFERENCE ESTABLISHED; STEREO CIRCLE GEOMETRY REJECTED") == (
        "Circle geometry rejected"
    )
    assert status_text("EXPERIMENT COMPLETE — PHYSICAL MEASUREMENTS DOCUMENTED; STEREO TRIANGLE ACCURACY NOT VALIDATED") == (
        "Physical accuracy not validated"
    )


def test_long_metadata_is_not_ellipsized_in_primary_values() -> None:
    app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=120).run()
    app.sidebar.radio[0].set_value("Circle measurements").run()
    assert not app.exception
    assert all("..." not in str(metric.value) for metric in app.metric)
    assert "322.448" in _table_text(app)
    assert "334.274" in _table_text(app)

    app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=120).run()
    app.sidebar.radio[0].set_value("Rectangle measurements").run()
    assert not app.exception
    assert "M2 -> M7" in " ".join(str(metric.value) for metric in app.metric)
    assert "Module 2 calibration, recomputed in Module 7" in _table_text(app)


def test_rectangle_geometry_and_physical_accuracy_are_separate() -> None:
    from module7.webapp.evidence import load_curated_bundle
    from module7.webapp.pages import RECTANGLE_SPECS
    from module7.webapp.ui import rectangle_geometry_state

    bundle, error = load_curated_bundle(ROOT)
    assert error is None and bundle is not None
    rejected = bundle.load_record(RECTANGLE_SPECS[2].record_asset).data
    accepted_but_inaccurate = bundle.load_record(RECTANGLE_SPECS[3].record_asset).data
    assert rejected is not None and accepted_but_inaccurate is not None
    assert rectangle_geometry_state(rejected)[1] is False
    assert rectangle_geometry_state(rejected)[0] == "Diagnostic reconstruction only"
    assert rectangle_geometry_state(accepted_but_inaccurate)[1] is True
    assert rectangle_geometry_state(accepted_but_inaccurate)[0] == "Geometry accepted"

    app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=120).run()
    app.sidebar.radio[0].set_value("Rectangle measurements").run()
    app.selectbox[0].set_value("FREE ADMISSION - second experiment").run()
    assert not app.exception
    rendered = "\n".join(_visible_text(app) + [_table_text(app)])
    assert "Diagnostic reconstruction only" in rendered
    assert "not accepted" in rendered.lower()


def test_physical_comparison_summary_is_concise_and_honest() -> None:
    app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=120).run()
    app.sidebar.radio[0].set_value("Circle measurements").run()
    assert not app.exception
    rendered = _table_text(app)
    assert "Physical diameter" in rendered
    assert "Stereo diameter" in rendered
    assert "Not accepted" in rendered

    app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=120).run()
    app.sidebar.radio[0].set_value("Polygon measurements").run()
    assert not app.exception
    rendered = _table_text(app)
    assert "Dimension" in rendered
    assert "Physical accuracy not validated" in rendered


def test_technical_json_records_remain_collapsed_by_default() -> None:
    source = (ROOT / "src/module7/webapp/ui.py").read_text(encoding="utf-8")
    assert "with st.expander(label, expanded=False)" in source
