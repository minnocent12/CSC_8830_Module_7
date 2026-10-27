#!/usr/bin/env python3
"""Process one sequential smartphone stereo pair using verified correspondences.

The default essential-matrix mode reads a correspondence CSV with the columns
``point_id,u1,v1,u2,v2`` and requires a measured camera-center baseline. The optional
``checkerboard_pnp`` mode automatically detects the calibration board in both views, derives a
metric relative pose from the two board poses, and uses the indexed board corners as
correspondences when no CSV is supplied. No output is produced when calibration, pose, or
triangulation quality checks fail.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import numpy as np

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from module7.calibration import (  # noqa: E402
    checkerboard_object_points,
    detect_checkerboard_corners,
    load_calibration,
)
from module7.io_utils import (  # noqa: E402
    ensure_same_image_size,
    load_image_bgr,
    read_correspondence_csv,
    write_json,
)
from module7.stereo_geometry import (  # noqa: E402
    estimate_checkerboard_pose,
    estimate_relative_pose,
    relative_pose_from_checkerboard_poses,
    rectify_sequential_views,
    triangulate_correspondences,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--calibration", type=Path, required=True)
    parser.add_argument("--view1", type=Path, required=True)
    parser.add_argument("--view2", type=Path, required=True)
    parser.add_argument("--correspondences", type=Path, help="CSV for arbitrary landmark pairs")
    parser.add_argument("--pose-method", choices=("essential", "checkerboard_pnp"), default="essential")
    parser.add_argument("--baseline", type=float, help="measured camera-center baseline for essential mode")
    parser.add_argument("--baseline-unit", choices=("m", "mm"), help="unit for --baseline")
    parser.add_argument("--baseline-uncertainty", type=float, help="optional measured baseline uncertainty")
    parser.add_argument(
        "--auto-correspondences-output",
        type=Path,
        help="optional CSV path for automatically detected checkerboard corner pairs",
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--diagnostic-image", type=Path)
    return parser


def _checkerboard_correspondences(
    image1: np.ndarray,
    image2: np.ndarray,
    pattern_size: tuple[int, int],
) -> tuple[list[str], np.ndarray, np.ndarray]:
    """Detect and index the same checkerboard corner order in both images."""
    corners1 = detect_checkerboard_corners(image1, pattern_size)
    corners2 = detect_checkerboard_corners(image2, pattern_size)
    if corners1 is None or corners2 is None:
        raise ValueError("checkerboard was not detected in both stereo views")
    first = corners1.reshape(-1, 2)
    second = corners2.reshape(-1, 2)
    if first.shape != second.shape:
        raise ValueError(f"checkerboard corner counts differ: {first.shape} versus {second.shape}")
    columns, rows = pattern_size
    point_ids = [f"checkerboard_r{row:02d}_c{column:02d}" for row in range(rows) for column in range(columns)]
    return point_ids, first, second


def _write_correspondences(path: Path, point_ids: list[str], points1: np.ndarray, points2: np.ndarray) -> None:
    """Write indexed raw-pixel correspondences without altering either source image."""
    if not (len(point_ids) == len(points1) == len(points2)):
        raise ValueError("point IDs and correspondence arrays must have matching lengths")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["point_id", "u1", "v1", "u2", "v2"])
        writer.writeheader()
        for point_id, first, second in zip(point_ids, points1, points2, strict=True):
            writer.writerow(
                {
                    "point_id": point_id,
                    "u1": f"{first[0]:.6f}",
                    "v1": f"{first[1]:.6f}",
                    "u2": f"{second[0]:.6f}",
                    "v2": f"{second[1]:.6f}",
                }
            )


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        calibration = load_calibration(args.calibration)
        image1 = load_image_bgr(args.view1)
        image2 = load_image_bgr(args.view2)
        image_size = ensure_same_image_size([image1, image2])
        if image_size != calibration.image_size:
            raise ValueError(
                f"pair image size {image_size} does not match calibration image size {calibration.image_size}"
            )
        if args.pose_method == "essential":
            if args.correspondences is None:
                raise ValueError("--correspondences is required for essential pose mode")
            if args.baseline is None or args.baseline_unit is None:
                raise ValueError("--baseline and --baseline-unit are required for essential pose mode")
            point_ids, points1, points2 = read_correspondence_csv(args.correspondences)
            pose = estimate_relative_pose(
                points1,
                points2,
                calibration.camera_matrix,
                distortion_coefficients=calibration.distortion_coefficients,
                baseline=args.baseline,
                baseline_unit=args.baseline_unit,
                baseline_uncertainty=args.baseline_uncertainty,
                scale_source="measured_camera_center_displacement",
            )
            correspondence_source = "user_verified_csv"
        else:
            board_points = checkerboard_object_points(
                calibration.pattern_size,
                calibration.square_size,
                square_unit=calibration.square_unit,
            )
            board_pose1_points = detect_checkerboard_corners(image1, calibration.pattern_size)
            board_pose2_points = detect_checkerboard_corners(image2, calibration.pattern_size)
            if board_pose1_points is None or board_pose2_points is None:
                raise ValueError("checkerboard was not detected in both stereo views")
            board_pose1 = estimate_checkerboard_pose(
                board_pose1_points,
                board_points,
                calibration.camera_matrix,
                calibration.distortion_coefficients,
            )
            board_pose2 = estimate_checkerboard_pose(
                board_pose2_points,
                board_points,
                calibration.camera_matrix,
                calibration.distortion_coefficients,
            )
            pose = relative_pose_from_checkerboard_poses(
                board_pose1,
                board_pose2,
                baseline_unit=calibration.square_unit,
            )
            if args.correspondences is None:
                point_ids, points1, points2 = _checkerboard_correspondences(
                    image1,
                    image2,
                    calibration.pattern_size,
                )
                correspondence_source = "auto_detected_checkerboard_corners"
            else:
                point_ids, points1, points2 = read_correspondence_csv(args.correspondences)
                correspondence_source = "user_verified_csv_with_checkerboard_pnp_pose"
            if args.auto_correspondences_output is not None:
                _write_correspondences(args.auto_correspondences_output, point_ids, points1, points2)
        if args.auto_correspondences_output is not None and args.pose_method == "essential":
            raise ValueError("--auto-correspondences-output is only supported in checkerboard_pnp mode")
        reconstruction = triangulate_correspondences(
            points1,
            points2,
            calibration.camera_matrix,
            pose,
            distortion_coefficients=calibration.distortion_coefficients,
        )
        rectification = rectify_sequential_views(
            calibration.camera_matrix,
            calibration.distortion_coefficients,
            pose,
            calibration.image_size,
        )
        if args.diagnostic_image:
            from module7.visualization import draw_correspondences, save_image

            save_image(draw_correspondences(image1, image2, points1, points2), args.diagnostic_image)
        payload = {
            "schema_version": 1,
            "status": "tested" if reconstruction.valid_mask.all() else "not_validated",
            "calibration_id": calibration.calibration_id,
            "view1": str(args.view1),
            "view2": str(args.view2),
            "correspondence_ids": point_ids,
            "correspondence_source": correspondence_source,
            "pose": {
                "method": pose.method,
                "rotation": pose.rotation,
                "translation_unit": pose.translation_unit,
                "translation_metric": pose.translation_metric,
                "baseline": pose.baseline,
                "baseline_unit": pose.baseline_unit,
                "scale_source": pose.scale_source,
                "baseline_uncertainty": pose.baseline_uncertainty,
                "relative_scale_uncertainty": pose.relative_scale_uncertainty,
                "inlier_mask": pose.inlier_mask,
                "median_parallax_degrees": pose.median_parallax_degrees,
            },
            "triangulation": {
                "points_3d": reconstruction.points_3d,
                "valid_mask": reconstruction.valid_mask,
                "reprojection_error_view1_px": reconstruction.reprojection_error_view1_px,
                "reprojection_error_view2_px": reconstruction.reprojection_error_view2_px,
                "median_parallax_degrees": reconstruction.median_parallax_degrees,
                "unit": reconstruction.unit,
                "metric": reconstruction.metric,
            },
            "rectification": {
                "R1": rectification.R1,
                "R2": rectification.R2,
                "P1": rectification.P1,
                "P2": rectification.P2,
                "Q": rectification.Q,
                "valid_roi1": rectification.valid_roi1,
                "valid_roi2": rectification.valid_roi2,
            },
        }
        write_json(args.output, payload)
    except (OSError, ValueError) as exc:
        print(f"stereo-pair processing failed: {exc}", file=sys.stderr)
        return 1
    print(f"saved sequential-stereo record: {args.output}")
    print(f"valid reconstructed points: {int(reconstruction.valid_mask.sum())}/{len(reconstruction.valid_mask)}")
    print(f"median triangulation parallax: {reconstruction.median_parallax_degrees:.6f} degrees")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
