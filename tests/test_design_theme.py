"""Parity checks for the vendored csc8830-ui 0.6.0 presentation kit."""
from __future__ import annotations

import re
from pathlib import Path

from module7.webapp.design import KIT_VERSION, STREAMLIT_REQUIREMENT, render_config_toml

ROOT = Path(__file__).resolve().parents[1]


def test_vendored_design_kit_version_is_060() -> None:
    assert KIT_VERSION == "0.6.0"
    assert re.fullmatch(r"\d+\.\d+\.\d+", KIT_VERSION)


def test_generated_theme_matches_vendored_kit() -> None:
    assert (ROOT / ".streamlit" / "config.toml").read_text(encoding="utf-8") == render_config_toml()


def test_streamlit_dependency_matches_theme_runtime_floor() -> None:
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert f'"{STREAMLIT_REQUIREMENT}"' in text


def test_required_design_components_import() -> None:
    from module7.webapp.design import components

    for name in ("page_header", "section_header", "metric_row", "image_comparison", "image_gallery", "status_banner"):
        assert callable(getattr(components, name))


def test_module7_shell_is_a_thin_shared_shell_adapter() -> None:
    text = (ROOT / "src/module7/webapp/shell.py").read_text(encoding="utf-8")
    assert "from module7.webapp.design.shell import render_shell" in text
    assert "st.markdown" not in text
    assert "st.sidebar.radio" not in text


def test_standalone_shell_uses_module_context_and_page_radio() -> None:
    from streamlit.testing.v1 import AppTest

    app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=120).run()
    assert not app.exception
    assert not app.sidebar.selectbox
    assert any("Module 7" in m.value for m in app.sidebar.markdown)
    assert app.sidebar.radio[0].label == "Page"
