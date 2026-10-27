#!/usr/bin/env python3
"""Validate and summarize saved Module 7 calibration/stereo records.

This command reports stored diagnostics only. It does not invent calibration values, rerun an
experiment, or convert a software result into physical validation.
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
from module7.io_utils import read_json, write_json  # noqa: E402


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--calibration", type=Path, required=True)
    parser.add_argument("--stereo-result", type=Path)
    parser.add_argument("--output", type=Path)
    return parser


def _finite_array(payload: object, *, name: str) -> np.ndarray:
    array = np.asarray(payload, dtype=np.float64)
    if not np.isfinite(array).all():
        raise ValueError(f"{name} contains non-finite values")
    return array


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        calibration = load_calibration(args.calibration)
        report: dict[str, object] = {
            "schema_version": 1,
            "status": "tested",
            "calibration": {
                "calibration_id": calibration.calibration_id,
                "image_size": calibration.image_size,
                "views": len(calibration.source_image_ids),
                "rms_reprojection_error_px": calibration.rms_reprojection_error_px,
                "maximum_per_view_reprojection_error_px": max(
                    calibration.per_view_reprojection_error_px,
                    default=None,
                ),
                "focal_length_px": calibration.focal_length_px,
            },
        }
        if args.stereo_result is not None:
            stereo = read_json(args.stereo_result)
            pose = stereo.get("pose")
            triangulation = stereo.get("triangulation")
            if not isinstance(pose, dict) or not isinstance(triangulation, dict):
                raise ValueError("stereo result must contain pose and triangulation objects")
            valid_mask = np.asarray(triangulation.get("valid_mask"), dtype=bool).reshape(-1)
            error1 = _finite_array(
                triangulation.get("reprojection_error_view1_px"),
                name="reprojection_error_view1_px",
            ).reshape(-1)
            error2 = _finite_array(
                triangulation.get("reprojection_error_view2_px"),
                name="reprojection_error_view2_px",
            ).reshape(-1)
            if error1.shape != valid_mask.shape or error2.shape != valid_mask.shape:
                raise ValueError("stereo validity and reprojection arrays must have matching lengths")
            report["stereo"] = {
                "status": stereo.get("status", "unknown"),
                "method": pose.get("method"),
                "baseline": pose.get("baseline"),
                "baseline_unit": pose.get("baseline_unit"),
                "relative_scale_uncertainty": pose.get("relative_scale_uncertainty"),
                "median_parallax_degrees": triangulation.get(
                    "median_parallax_degrees",
                    pose.get("median_parallax_degrees"),
                ),
                "point_count": int(valid_mask.size),
                "valid_point_count": int(valid_mask.sum()),
                "maximum_valid_reprojection_error_px": float(
                    np.max(np.concatenate((error1[valid_mask], error2[valid_mask])))
                )
                if valid_mask.any()
                else None,
            }
            if not valid_mask.all():
                report["status"] = "not_validated"
        if args.output is not None:
            write_json(args.output, report)
            print(f"saved diagnostics: {args.output}")
        else:
            print(report)
    except (OSError, ValueError, TypeError) as exc:
        print(f"diagnostics failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
