from __future__ import annotations

import numpy as np
import pytest

from module7.object_measurement import (
    ObjectMeasurementError,
    measure_circle,
    measure_polygon,
    measure_rectangle,
    reconstruct_landmarks,
)
from module7.stereo_geometry import StereoGeometryError, StereoPose, project_points


K = np.array([[900.0, 0.0, 320.0], [0.0, 900.0, 240.0], [0.0, 0.0, 1.0]])
DISTORTION = np.zeros(5)
ROTATION = np.eye(3)
TRANSLATION = np.array([-0.25, 0.01, 0.0])


def _pose(point_count: int, *, metric: bool = True) -> StereoPose:
    return StereoPose(
        rotation=ROTATION,
        translation_unit=TRANSLATION / np.linalg.norm(TRANSLATION),
        translation_metric=TRANSLATION if metric else None,
        essential_matrix=None,
        inlier_mask=np.ones(point_count, dtype=bool),
        baseline=float(np.linalg.norm(TRANSLATION)) if metric else None,
        baseline_unit="m" if metric else None,
        scale_source="synthetic-known-baseline" if metric else None,
        method="synthetic-known-pose",
        median_parallax_degrees=1.0,
    )


def _reconstruct(points: np.ndarray):
    ids = tuple(f"p{index}" for index in range(len(points)))
    points_view1 = project_points(points, K, distortion_coefficients=DISTORTION)
    points_view2 = project_points(points, K, ROTATION, TRANSLATION, DISTORTION)
    return reconstruct_landmarks(
        ids,
        points_view1,
        points_view2,
        K,
        _pose(len(points)),
        distortion_coefficients=DISTORTION,
        minimum_parallax_degrees=0.01,
        maximum_reprojection_error_px=0.1,
    )


def test_rectangle_dimensions_are_mean_opposite_3d_edges() -> None:
    points = np.array(
        [
            [-1.0, -0.5, 5.0],
            [1.0, -0.5, 5.0],
            [1.0, 0.5, 5.0],
            [-1.0, 0.5, 5.0],
        ]
    )
    landmarks = _reconstruct(points)
    result = measure_rectangle(landmarks, ["p0", "p1", "p2", "p3"])

    assert result.unit == "m"
    assert result.width == pytest.approx(2.0, abs=1e-6)
    assert result.height == pytest.approx(1.0, abs=1e-6)
    assert max(result.right_angle_deviations_degrees) < 1e-5
    assert result.planarity_max < 1e-8


def test_circle_diameter_comes_from_3d_plane_fit() -> None:
    angles = np.linspace(0.0, 2.0 * np.pi, 8, endpoint=False)
    points = np.column_stack((1.25 * np.cos(angles), 1.25 * np.sin(angles), np.full(8, 5.0)))
    landmarks = _reconstruct(points)
    result = measure_circle(landmarks, [f"p{index}" for index in range(8)])

    assert result.unit == "m"
    assert result.diameter == pytest.approx(2.5, abs=1e-6)
    np.testing.assert_allclose(result.center_3d, [0.0, 0.0, 5.0], atol=1e-6)
    assert result.fit_max < 1e-8


def test_polygon_reports_each_visible_adjacent_edge() -> None:
    points = np.array(
        [
            [0.0, 0.0, 5.0],
            [2.0, 0.0, 5.0],
            [2.0, 1.0, 5.0],
            [0.0, 1.0, 5.0],
        ]
    )
    result = measure_polygon(_reconstruct(points), ["p0", "p1", "p2", "p3"])

    np.testing.assert_allclose(result.edge_lengths, [2.0, 1.0, 2.0, 1.0], atol=1e-6)
    assert result.closed
    assert result.to_dict()["dimensions"] == {
        "edge_1": pytest.approx(2.0),
        "edge_2": pytest.approx(1.0),
        "edge_3": pytest.approx(2.0),
        "edge_4": pytest.approx(1.0),
    }


def test_reconstruction_rejects_non_metric_pose_before_measurement() -> None:
    points = np.array([[0.0, 0.0, 5.0], [1.0, 0.0, 5.0], [0.0, 1.0, 5.0]])
    points_view1 = project_points(points, K)
    points_view2 = project_points(points, K, ROTATION, TRANSLATION)

    with pytest.raises(StereoGeometryError, match="physical translation scale"):
        reconstruct_landmarks(
            ["a", "b", "c"],
            points_view1,
            points_view2,
            K,
            _pose(3, metric=False),
        )


def test_reconstruction_rejects_landmark_with_excessive_reprojection_error() -> None:
    points = np.array(
        [
            [-1.0, -0.5, 5.0],
            [1.0, -0.5, 5.0],
            [1.0, 0.5, 5.0],
            [-1.0, 0.5, 5.0],
        ]
    )
    points_view1 = project_points(points, K)
    points_view2 = project_points(points, K, ROTATION, TRANSLATION)
    points_view2[0] += [10.0, -10.0]

    with pytest.raises(ObjectMeasurementError, match="stereo quality checks rejected"):
        reconstruct_landmarks(
            ["p0", "p1", "p2", "p3"],
            points_view1,
            points_view2,
            K,
            _pose(4),
            maximum_reprojection_error_px=0.5,
        )


def test_circle_rejects_collinear_boundary_points() -> None:
    points = np.array(
        [
            [-1.0, 0.0, 5.0],
            [0.0, 0.0, 5.0],
            [1.0, 0.0, 5.0],
        ]
    )

    with pytest.raises(ObjectMeasurementError, match="collinear"):
        measure_circle(_reconstruct(points), ["p0", "p1", "p2"])


def test_rectangle_rejects_missing_or_duplicate_corner_ids() -> None:
    points = np.array(
        [
            [-1.0, -0.5, 5.0],
            [1.0, -0.5, 5.0],
            [1.0, 0.5, 5.0],
            [-1.0, 0.5, 5.0],
        ]
    )
    landmarks = _reconstruct(points)

    with pytest.raises(ObjectMeasurementError, match="unique"):
        measure_rectangle(landmarks, ["p0", "p1", "p1", "p3"])
    with pytest.raises(ObjectMeasurementError, match="missing"):
        measure_rectangle(landmarks, ["p0", "p1", "p2", "missing"])
