from __future__ import annotations

import cv2
import numpy as np
import pytest

from module7.calibration import checkerboard_object_points
from module7.stereo_geometry import (
    CheckerboardPose,
    StereoGeometryError,
    StereoPose,
    apply_metric_scale,
    estimate_checkerboard_pose,
    estimate_relative_pose,
    project_points,
    relative_pose_from_checkerboard_poses,
    rectify_sequential_views,
    triangulate_correspondences,
)


def _synthetic_scene() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return deterministic camera/scene values for software verification only."""
    K = np.array([[800.0, 0.0, 320.0], [0.0, 800.0, 240.0], [0.0, 0.0, 1.0]])
    rvec = np.array([0.015, -0.025, 0.01])
    R, _ = cv2.Rodrigues(rvec)
    translation = np.array([-0.35, 0.015, 0.02])
    rng = np.random.default_rng(1234)
    points = np.column_stack(
        [rng.uniform(-1.0, 1.0, 80), rng.uniform(-0.7, 0.7, 80), rng.uniform(4.0, 8.0, 80)]
    )
    points1 = project_points(points, K)
    points2 = project_points(points, K, R, translation)
    return K, R, translation, points, (points1, points2)


def _known_pose(K: np.ndarray, R: np.ndarray, translation: np.ndarray) -> StereoPose:
    return StereoPose(
        rotation=R,
        translation_unit=translation / np.linalg.norm(translation),
        translation_metric=translation,
        essential_matrix=None,
        inlier_mask=np.ones(80, dtype=bool),
        baseline=float(np.linalg.norm(translation)),
        baseline_unit="m",
        scale_source="synthetic-known-baseline",
        method="synthetic-known-pose",
        median_parallax_degrees=1.0,
    )


def test_metric_scale_normalizes_direction_and_preserves_magnitude() -> None:
    scaled = apply_metric_scale(np.array([0.0, 2.0, 0.0]), 0.25)

    np.testing.assert_allclose(scaled, [0.0, 0.25, 0.0])


def test_metric_scale_rejects_zero_or_nonfinite_inputs() -> None:
    with pytest.raises(ValueError, match="non-zero"):
        apply_metric_scale(np.zeros(3), 1.0)
    with pytest.raises(ValueError, match="positive"):
        apply_metric_scale(np.array([1.0, 0.0, 0.0]), 0.0)


def test_relative_pose_records_scale_uncertainty() -> None:
    K, _, translation, _, (points1, points2) = _synthetic_scene()
    pose = estimate_relative_pose(
        points1,
        points2,
        K,
        baseline=float(np.linalg.norm(translation)),
        baseline_unit="m",
        baseline_uncertainty=0.005,
        scale_source="synthetic-known-baseline",
        threshold_px=0.5,
        minimum_parallax_degrees=0.001,
    )

    assert pose.baseline_uncertainty == pytest.approx(0.005)
    assert pose.relative_scale_uncertainty == pytest.approx(0.005 / np.linalg.norm(translation))


def test_known_synthetic_pose_triangulates_metric_points() -> None:
    K, R, translation, points, (points1, points2) = _synthetic_scene()
    result = triangulate_correspondences(points1, points2, K, _known_pose(K, R, translation))

    assert result.metric
    assert result.valid_mask.all()
    assert result.median_parallax_degrees > 0
    np.testing.assert_allclose(result.points_3d, points, atol=1e-5)
    assert float(result.reprojection_error_view1_px.max()) < 1e-5
    assert float(result.reprojection_error_view2_px.max()) < 1e-5


def test_essential_matrix_pose_recovers_direction_and_rotation() -> None:
    K, R, translation, _, (points1, points2) = _synthetic_scene()
    pose = estimate_relative_pose(
        points1,
        points2,
        K,
        baseline=float(np.linalg.norm(translation)),
        baseline_unit="m",
        scale_source="synthetic-known-baseline",
        threshold_px=0.5,
        minimum_parallax_degrees=0.001,
    )

    assert pose.is_metric
    assert pose.inlier_mask.sum() >= 70
    np.testing.assert_allclose(pose.rotation, R, atol=2e-3)
    np.testing.assert_allclose(
        np.abs(np.dot(pose.translation_unit, translation / np.linalg.norm(translation))),
        1.0,
        atol=2e-3,
    )


def test_metric_triangulation_requires_scale() -> None:
    K, R, translation, _, (points1, points2) = _synthetic_scene()
    unscaled = StereoPose(
        rotation=R,
        translation_unit=translation / np.linalg.norm(translation),
        translation_metric=None,
        essential_matrix=None,
        inlier_mask=np.ones(80, dtype=bool),
        baseline=None,
        baseline_unit=None,
        scale_source=None,
        method="synthetic-unscaled",
        median_parallax_degrees=1.0,
    )
    with pytest.raises(StereoGeometryError, match="physical translation scale"):
        triangulate_correspondences(points1, points2, K, unscaled)


def test_metric_projection_and_rectification_require_and_preserve_units() -> None:
    K, R, translation, _, _ = _synthetic_scene()
    pose = _known_pose(K, R, translation)

    P1, P2 = pose.projection_matrices(K)
    assert P1.shape == (3, 4)
    assert P2.shape == (3, 4)
    np.testing.assert_allclose(P2[:, 3], K @ translation)

    rectified = rectify_sequential_views(K, np.zeros(5), pose, (640, 480))
    assert rectified.R1.shape == (3, 3)
    assert rectified.R2.shape == (3, 3)
    assert rectified.P1.shape == (3, 4)
    assert rectified.P2.shape == (3, 4)
    assert rectified.Q.shape == (4, 4)


def test_insufficient_parallax_is_rejected_before_triangulation() -> None:
    K, R, _, points, (points1, _) = _synthetic_scene()
    tiny_translation = np.array([-1e-5, 0.0, 0.0])
    points2 = project_points(points, K, R, tiny_translation)
    pose = _known_pose(K, R, tiny_translation)

    with pytest.raises(StereoGeometryError, match="insufficient median triangulation parallax"):
        triangulate_correspondences(
            points1,
            points2,
            K,
            pose,
            minimum_parallax_degrees=0.01,
        )


def test_excessive_reprojection_is_marked_invalid() -> None:
    K, R, translation, points, (points1, points2) = _synthetic_scene()
    noisy_points2 = points2.copy()
    noisy_points2[0] += [20.0, -20.0]
    result = triangulate_correspondences(
        points1,
        noisy_points2,
        K,
        _known_pose(K, R, translation),
        maximum_reprojection_error_px=1.0,
    )

    assert not result.valid_mask[0]
    assert result.reprojection_error_view2_px[0] > 1.0


def test_insufficient_correspondences_are_rejected() -> None:
    K, _, _, _, (points1, points2) = _synthetic_scene()
    with pytest.raises(ValueError, match="at least 5"):
        estimate_relative_pose(points1[:4], points2[:4], K)


def test_checkerboard_pose_fallback_is_metric_on_synthetic_points() -> None:
    K = np.array([[850.0, 0.0, 320.0], [0.0, 845.0, 240.0], [0.0, 0.0, 1.0]])
    D = np.zeros(5)
    board = checkerboard_object_points((6, 5), 0.04, square_unit="m")
    rvec = np.array([0.08, -0.06, 0.03])
    tvec = np.array([0.1, -0.08, 2.0])
    image_points, _ = cv2.projectPoints(board, rvec, tvec, K, D)
    estimated = estimate_checkerboard_pose(image_points.reshape(-1, 2), board, K, D)

    assert estimated.reprojection_error_px < 1e-5
    np.testing.assert_allclose(estimated.translation, tvec, atol=1e-4)


def test_checkerboard_poses_produce_relative_metric_pose() -> None:
    pose1 = CheckerboardPose(np.eye(3), np.array([0.0, 0.0, 2.0]), 0.0)
    pose2 = CheckerboardPose(np.eye(3), np.array([-0.3, 0.0, 2.0]), 0.0)

    relative = relative_pose_from_checkerboard_poses(pose1, pose2, baseline_unit="m")

    assert relative.is_metric
    np.testing.assert_allclose(relative.translation_metric, [-0.3, 0.0, 0.0])
    assert relative.baseline == pytest.approx(0.3)
