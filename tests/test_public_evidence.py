"""Integrity checks for the proposed local public evidence bundle."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from module7.webapp.evidence import load_curated_bundle
from module7.webapp.pages import CIRCLE_SPECS, POLYGON_SPECS, RECTANGLE_SPECS

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "data" / "proposed_public_demo"


def test_approved_manifest_is_complete() -> None:
    manifest = json.loads((BUNDLE / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["publication_approved"] is True
    assert manifest["asset_count"] == len(manifest["assets"]) + 1
    assert manifest["total_size_bytes"] > 0
    for asset in manifest["assets"]:
        path = BUNDLE / asset["relative_path"]
        assert path.is_file(), asset
        data = path.read_bytes()
        assert len(data) == asset["size_bytes"]
        assert hashlib.sha256(data).hexdigest() == asset["sha256"]


def test_proposed_records_are_compact_and_path_free() -> None:
    records = sorted((BUNDLE / "records").glob("*.json"))
    assert len(records) == 7
    for path in records:
        text = path.read_text(encoding="utf-8")
        assert len(text) < 20_000
        for forbidden in ("/Users/", "data/", "results/", "src/", "docs/", "scripts/"):
            assert forbidden not in text, path
        assert "IMG_" not in text
        assert "flashcard_ruler" not in text


def test_proposed_bundle_contains_all_shape_examples() -> None:
    manifest = json.loads((BUNDLE / "manifest.json").read_text(encoding="utf-8"))
    labels = {asset["source_label"] for asset in manifest["assets"]}
    assert any("Flashcard" in label for label in labels)
    assert any("FREE ADMISSION" in label for label in labels)
    assert any("Yellow lid" in label for label in labels)
    assert any("Cardboard triangle" in label for label in labels)


def test_curated_loader_validates_all_referenced_records_and_images() -> None:
    bundle, error = load_curated_bundle(ROOT)
    assert error is None and bundle is not None
    specs = (*RECTANGLE_SPECS, *CIRCLE_SPECS, *POLYGON_SPECS)
    for spec in specs:
        record = bundle.load_record(spec.record_asset)
        assert record.error is None and record.data is not None
        for relative_path in (*spec.view_assets, *spec.diagnostic_assets):
            path = bundle.asset_path(relative_path)
            assert path is not None and path.is_file()


def test_curated_statuses_remain_validated_rejected_or_pending() -> None:
    bundle, error = load_curated_bundle(ROOT)
    assert error is None and bundle is not None
    records = [bundle.load_record(spec.record_asset).data for spec in (*RECTANGLE_SPECS, *CIRCLE_SPECS, *POLYGON_SPECS)]
    statuses = {record["status"] for record in records if record}
    assert any("VALIDATED" in status or "COMPLETE" in status for status in statuses)
    assert any("REJECTED" in status or "NOT VALIDATED" in status for status in statuses)
    assert any("PENDING" in status for status in statuses)


def test_curated_loader_reports_malformed_manifest_and_missing_asset(tmp_path: Path) -> None:
    malformed_root = tmp_path / "malformed"
    (malformed_root / "data" / "proposed_public_demo").mkdir(parents=True)
    (malformed_root / "data" / "proposed_public_demo" / "manifest.json").write_text("not json", encoding="utf-8")
    bundle, error = load_curated_bundle(malformed_root)
    assert bundle is None and error

    missing_root = tmp_path / "missing"
    shutil.copytree(ROOT / "data" / "proposed_public_demo", missing_root / "data" / "proposed_public_demo")
    (missing_root / "data" / "proposed_public_demo" / "records" / "experiment_01.json").unlink()
    bundle, error = load_curated_bundle(missing_root)
    assert bundle is None and error and "missing" in error.lower()


def test_page_catalog_contains_no_original_data_or_results_paths() -> None:
    source = (ROOT / "src" / "module7" / "webapp" / "pages.py").read_text(encoding="utf-8")
    assert "data/" not in source
    assert "results/" not in source
