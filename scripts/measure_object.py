#!/usr/bin/env python3
"""Estimate rectangle, circle, or polygon dimensions from a saved metric stereo pose.

The correspondence CSV must use the Phase 2 schema ``point_id,u1,v1,u2,v2``.  This command
loads the existing calibration and stereo-pose records, reconstructs every CSV landmark with
the existing calibrated triangulation checks, and only then applies the selected shape model.
It writes a derived result with physical units, 3D points, depths, quality diagnostics, and
explicit assumptions.  It does not claim independent physical validation.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from module7.calibration import load_calibration  # noqa: E402
from module7.io_utils import read_correspondence_csv, read_json, write_json  # noqa: E402
from module7.object_measurement import (  # noqa: E402
    measure_circle,
    measure_polygon,
    measure_rectangle,
    reconstruct_landmarks,
)
from module7.stereo_geometry import StereoPose  # noqa: E402


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--calibration", type=Path, required=True)
    parser.add_argument("--stereo-record", type=Path, required=True)
    parser.add_argument("--correspondences", type=Path, required=True)
    parser.add_argument("--shape", choices=("rectangle", "circle", "polygon"), required=True)
    parser.add_argument(
        "--landmark-ids",
        nargs="+",
        required=True,
        help="rectangle: TL TR BR BL; circle: boundary samples; polygon: ordered visible vertices",
    )
    parser.add_argument("--require-planar", action="store_true", help="make polygon planarity a hard quality gate")
    parser.add_argument("--output", type=Path, required=True)
    return parser


def _pose_from_record(payload: dict[str, object]) -> StereoPose:
    try:
        pose = payload["pose"]
        if not isinstance(pose, dict):
            raise ValueError("stereo record pose must be an object")
        translation_metric_value = pose.get("translation_metric")
        translation_metric = (
            None if translation_metric_value is None else np.asarray(translation_metric_value, dtype=np.float64)
        )
        baseline_value = pose.get("baseline")
        baseline = None if baseline_value is None else float(baseline_value)
        baseline_unit = pose.get("baseline_unit")
        return StereoPose(
            rotation=np.asarray(pose["rotation"], dtype=np.float64),
            translation_unit=np.asarray(pose["translation_unit"], dtype=np.float64),
            translation_metric=translation_metric,
            essential_matrix=(
                None
                if pose.get("essential_matrix") is None
                else np.asarray(pose["essential_matrix"], dtype=np.float64)
            ),
            inlier_mask=np.asarray(pose.get("inlier_mask", [True]), dtype=bool),
            baseline=baseline,
            baseline_unit=None if baseline_unit is None else str(baseline_unit),
            scale_source=None if pose.get("scale_source") is None else str(pose["scale_source"]),
            method=str(pose.get("method", "saved_stereo_pose")),
            median_parallax_degrees=float(pose.get("median_parallax_degrees", 0.0)),
            baseline_uncertainty=(
                None
                if pose.get("baseline_uncertainty") is None
                else float(pose["baseline_uncertainty"])
            ),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"invalid saved stereo pose record: {exc}") from exc


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        calibration = load_calibration(args.calibration)
        stereo_record = read_json(args.stereo_record)
        point_ids, points_view1, points_view2 = read_correspondence_csv(args.correspondences)
        pose = _pose_from_record(stereo_record)
        landmarks = reconstruct_landmarks(
            point_ids,
            points_view1,
            points_view2,
            calibration.camera_matrix,
            pose,
            distortion_coefficients=calibration.distortion_coefficients,
        )
        if args.shape == "rectangle":
            measurement = measure_rectangle(landmarks, args.landmark_ids)
        elif args.shape == "circle":
            measurement = measure_circle(landmarks, args.landmark_ids)
        else:
            measurement = measure_polygon(
                landmarks,
                args.landmark_ids,
                require_planar=args.require_planar,
            )
        result = {
            "schema_version": 1,
            "status": "computed_not_experimentally_validated",
            "experimental_validation": "PENDING USER MEASUREMENT",
            "calibration": {
                "path": str(args.calibration),
                "calibration_id": calibration.calibration_id,
                "image_size": list(calibration.image_size),
            },
            "stereo_record": str(args.stereo_record),
            "correspondence_csv": str(args.correspondences),
            "shape": args.shape,
            "reconstruction": landmarks.to_dict(),
            "measurement": measurement.to_dict(),
            "physical_ground_truth": None,
            "note": "This is a metric stereo computation. Independent ruler/tape validation is required before an experimental pass can be claimed.",
        }
        write_json(args.output, result)
    except (OSError, ValueError) as exc:
        print(f"object measurement failed: {exc}", file=sys.stderr)
        return 1
    print(f"saved object measurement: {args.output}")
    print(f"shape: {args.shape}; unit: {landmarks.unit}")
    print("experimental validation: PENDING USER MEASUREMENT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
