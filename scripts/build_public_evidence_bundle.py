"""Build the proposed, review-only public evidence bundle for the local preview.

The source captures and full result records are never modified. The output contains
display-sized derivatives and a compact, path-free subset of each saved experiment record.
It is deliberately marked as not publication-approved until the user reviews the assets.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

import cv2

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "proposed_public_demo"
sys.path.insert(0, str(ROOT / "src"))

from module7.webapp.pages import CIRCLE_SPECS, POLYGON_SPECS, RECTANGLE_SPECS  # noqa: E402


ORIGINAL_SOURCE_BY_LABEL = {
    "Flashcard - validated under equivalent-edge assumption": (
        "results/object_measurements/IMG_7485_IMG_7486_flashcard_validation.json",
        ("data/physical_validation/IMG_7485.JPG", "data/physical_validation/IMG_7486.JPG"),
        ("results/stereo_diagnostics/IMG_7485_IMG_7486_correspondences.jpg",),
    ),
    "FREE ADMISSION - first experiment": (
        "results/object_measurements/IMG_7514_IMG_7515_free_admission_rectangle_validation.json",
        ("data/physical_validation/IMG_7514.JPG", "data/physical_validation/IMG_7515.JPG"),
        ("results/stereo_diagnostics/IMG_7514_IMG_7515_free_admission_rectangle_correspondences.png",),
    ),
    "FREE ADMISSION - second experiment": (
        "results/object_measurements/rectangle_second/IMG_7516_IMG_7517_free_admission_rectangle_validation.json",
        ("data/physical_validation/IMG_7516.JPG", "data/physical_validation/IMG_7517.JPG"),
        ("results/stereo_diagnostics/rectangle_second/IMG_7516_IMG_7517_free_admission_rectangle_correspondences.png",),
    ),
    "FREE ADMISSION - third experiment": (
        "results/object_measurements/rectangle_third/IMG_7519_IMG_7520_free_admission_rectangle_validation.json",
        ("data/physical_validation/IMG_7519.JPG", "data/physical_validation/IMG_7520.JPG"),
        ("results/stereo_diagnostics/rectangle_third/IMG_7519_IMG_7520_free_admission_rectangle_correspondences.png",),
    ),
    "Yellow lid - marked perimeter experiment": (
        "results/stereo_diagnostics/circle_yellow_marked/IMG_7543_IMG_7544_circle_validation_manifest.json",
        ("data/physical_validation/IMG_7543.JPG", "data/physical_validation/IMG_7544.JPG"),
        ("results/stereo_diagnostics/circle_yellow_marked/IMG_7543_IMG_7544_checkerboard_correspondences.png",),
    ),
    "Yellow lid - unmarked pair pending perimeter correspondence": (
        "results/stereo_diagnostics/circle_yellow/IMG_7540_IMG_7541_circle_evidence_manifest.json",
        ("data/physical_validation/IMG_7540.JPG", "data/physical_validation/IMG_7541.JPG"),
        ("results/stereo_diagnostics/circle_yellow/IMG_7540_IMG_7541_checkerboard_correspondences.png",),
    ),
    "Cardboard triangle - three visible edges": (
        "results/object_measurements/polygon_phase3c/IMG_7548_IMG_7549_triangle_validation.json",
        ("data/physical_validation/IMG_7548.JPG", "data/physical_validation/IMG_7549.JPG"),
        ("results/stereo_diagnostics/polygon_phase3c/IMG_7548_IMG_7549_triangle_vertex_correspondences.png",),
    ),
}


HIDDEN_KEYS = {
    "path", "paths", "file", "files", "source", "source_images", "original_inputs",
    "processing_images", "annotated_diagnostics", "correspondence_csv", "csv", "provenance",
    "audit_history", "historical_preservation", "evidence_photographs", "evidence_record",
    "record", "orientation_adjustment", "orientation_normalization", "experiment",
}
PATH_TEXT = re.compile(r"(?:^|[/\\])(?:data|results|src|docs|tests|scripts)(?:[/\\])|(?:^|[/\\])Users[/\\]|\.(?:py|json|csv|JPG|jpg|PNG|png)$")
SOURCE_FILENAME_TEXT = re.compile(
    r"\b(?:IMG_\d{4}(?:[_A-Za-z0-9-]+)?|flashcard_ruler(?:\*|[_A-Za-z0-9-]*)?)\.(?:JPG|jpg|PNG|png|csv)\b"
)
SOURCE_FILENAME_RANGE = re.compile(r"\bIMG_\d{4}[-–]IMG_\d{4}\b")


def public_value(value: Any, key: str | None = None) -> Any:
    """Keep empirical values while removing file and internal provenance references."""
    key_lower = key.lower() if key else ""
    if key and (key_lower in HIDDEN_KEYS or any(token in key_lower for token in ("audit", "history", "provenance"))):
        return None
    if isinstance(value, dict):
        cleaned = {}
        for child_key, child_value in value.items():
            item = public_value(child_value, child_key)
            if item is not None:
                public_key = SOURCE_FILENAME_RANGE.sub("original_evidence_range", child_key)
                public_key = SOURCE_FILENAME_TEXT.sub("original_evidence_file", public_key)
                if public_key in cleaned:
                    suffix = 2
                    while f"{public_key}_{suffix}" in cleaned:
                        suffix += 1
                    public_key = f"{public_key}_{suffix}"
                cleaned[public_key] = item
        return cleaned
    if isinstance(value, list):
        return [public_value(item) for item in value]
    if isinstance(value, str):
        value = SOURCE_FILENAME_RANGE.sub("[original evidence range]", value)
        value = SOURCE_FILENAME_TEXT.sub("[original evidence file]", value)
        if PATH_TEXT.search(value) or any(token in value for token in ("data/", "results/", "src/", "docs/", "tests/", "scripts/", "/Users/")):
            return None
        return value.replace("—", "-").replace("–", "-")
    return value


def write_display_image(source: Path, destination: Path, max_dimension: int = 1280) -> dict[str, Any]:
    image = cv2.imread(str(source), cv2.IMREAD_COLOR)
    if image is None:
        raise RuntimeError(f"Could not decode evidence image: {source}")
    height, width = image.shape[:2]
    scale = min(1.0, max_dimension / max(height, width))
    if scale < 1.0:
        image = cv2.resize(image, (round(width * scale), round(height * scale)), interpolation=cv2.INTER_AREA)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(destination), image, [cv2.IMWRITE_JPEG_QUALITY, 84]):
        raise RuntimeError(f"Could not write display image: {destination}")
    return {"width_px": image.shape[1], "height_px": image.shape[0]}


def asset_entry(
    path: Path,
    *,
    role: str,
    source_label: str,
    page: str,
    dimensions: dict[str, Any] | None = None,
) -> dict[str, Any]:
    data = path.read_bytes()
    entry = {
        "relative_path": path.relative_to(OUTPUT).as_posix(),
        "role": role,
        "source_label": source_label,
        "page": page,
        "size_bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "essential_for_demonstration": True,
        "publication_recommendation": "USER REVIEW REQUIRED - proposed candidate only",
    }
    if role == "compact_evidence_record":
        entry["content_review"] = "Path-free academic record; no visual personal content."
        entry["privacy_status"] = "No visual privacy issue; user approval still required."
        entry["display_transform"] = "Compact JSON selection only; no scientific coordinates changed."
    else:
        entry["content_review"] = (
            "Real experiment image showing the checkerboard and validation object; surrounding "
            "workspace/background remains visible. No face or explicit personal identifier was "
            "observed in the local visual review."
        )
        entry["privacy_status"] = "Potential private workspace background; owner review required."
        entry["display_transform"] = "Resized for preview only; no crop or coordinate remapping applied."
    if dimensions:
        entry["dimensions"] = dimensions
    return entry


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    assets: list[dict[str, Any]] = []
    specs = (*RECTANGLE_SPECS, *CIRCLE_SPECS, *POLYGON_SPECS)
    for index, spec in enumerate(specs, start=1):
        experiment_id = f"experiment_{index:02d}"
        page = {
            "rectangle": "Rectangle measurements",
            "circle": "Circle measurements",
            "polygon": "Polygon measurements",
        }[spec.shape]
        record_relative, view_sources, diagnostic_sources = ORIGINAL_SOURCE_BY_LABEL[spec.label]
        record_source = ROOT / record_relative
        if not record_source.is_file():
            raise FileNotFoundError(record_source)
        record = json.loads(record_source.read_text(encoding="utf-8"))
        public_record = public_value(record)
        record_path = OUTPUT / "records" / f"{experiment_id}.json"
        record_path.parent.mkdir(parents=True, exist_ok=True)
        record_path.write_text(json.dumps(public_record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        assets.append(asset_entry(record_path, role="compact_evidence_record", source_label=spec.label, page=page))

        for view_index, source_relative in enumerate(view_sources, start=1):
            source = ROOT / source_relative
            if not source.is_file():
                raise FileNotFoundError(source)
            destination = OUTPUT / "images" / f"{experiment_id}_view{view_index}.jpg"
            dimensions = write_display_image(source, destination)
            assets.append(
                asset_entry(
                    destination,
                    role="stereo_view_display",
                    source_label=spec.label,
                    page=page,
                    dimensions=dimensions,
                )
            )

        if diagnostic_sources:
            source = ROOT / diagnostic_sources[0]
            if source.is_file():
                destination = OUTPUT / "images" / f"{experiment_id}_diagnostic.jpg"
                dimensions = write_display_image(source, destination, max_dimension=1600)
                assets.append(
                    asset_entry(
                        destination,
                        role="annotated_diagnostic_display",
                        source_label=spec.label,
                        page=page,
                        dimensions=dimensions,
                    )
                )

    manifest = {
        "bundle_version": "0.1.0-proposed",
        "purpose": "Compact local preview for academic review of Question 1 evidence.",
        "publication_approved": False,
        "review_status": "PENDING USER REVIEW",
        "approval_note": "User review is required before any public publication.",
        "asset_count": len(assets) + 1,
        "assets": assets,
    }
    manifest_path = OUTPUT / "manifest.json"
    manifest["total_size_bytes"] = 0
    for _ in range(4):
        rendered = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
        non_manifest_size = sum(
            path.stat().st_size for path in OUTPUT.rglob("*") if path.is_file() and path != manifest_path
        )
        declared_size = non_manifest_size + len(rendered.encode("utf-8"))
        manifest["total_size_bytes"] = declared_size
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        actual_size = sum(path.stat().st_size for path in OUTPUT.rglob("*") if path.is_file())
        if actual_size == declared_size:
            break
    total_size = sum(path.stat().st_size for path in OUTPUT.rglob("*") if path.is_file())
    print(f"Wrote {manifest['asset_count']} proposed assets ({total_size / 1_000_000:.2f} MB) to {OUTPUT}")


if __name__ == "__main__":
    main()
