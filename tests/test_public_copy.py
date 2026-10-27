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
    assert not problems, problems


def test_public_ui_source_does_not_render_record_paths() -> None:
    text = (ROOT / "src/module7/webapp/pages.py").read_text(encoding="utf-8")
    assert "Evidence source" not in text
