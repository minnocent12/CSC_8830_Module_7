from __future__ import annotations

import cv2
import numpy as np
import pytest

from module7.calibration import (
    CalibrationResult,
    calibrate_camera_from_points,
    checkerboard_object_points,
    validate_pattern_size,
    validate_square_size,
)


def _synthetic_calibration_observations() -> tuple[list[np.ndarray], list[np.ndarray], tuple[int, int]]:
    """Create deterministic software-only observations; not real camera evidence."""
    pattern_size = (6, 5)
    object_template = checkerboard_object_points(pattern_size, 0.03, square_unit="m")
    K = np.array([[800.0, 0.0, 320.0], [0.0, 790.0, 240.0], [0.0, 0.0, 1.0]])
    distortion = np.zeros(5, dtype=np.float64)
    poses = [
        (np.array([0.02, -0.04, 0.01]), np.array([0.0, 0.0, 3.0])),
        (np.array([-0.10, 0.06, 0.02]), np.array([0.10, -0.05, 3.4])),
        (np.array([0.08, 0.12, -0.04]), np.array([-0.15, 0.08, 3.8])),
        (np.array([-0.05, -0.08, 0.06]), np.array([0.20, 0.02, 4.2])),
        (np.array([0.12, 0.03, 0.09]), np.array([-0.08, -0.12, 4.6])),
    ]
    object_points = []
    image_points = []
    for rvec, tvec in poses:
        projected, _ = cv2.projectPoints(object_template, rvec, tvec, K, distortion)
        object_points.append(object_template.copy())
        image_points.append(projected.reshape(-1, 2))
    return object_points, image_points, (640, 480)


def test_checkerboard_object_points_use_metric_square_size() -> None:
    points = checkerboard_object_points((3, 2), 25.0, square_unit="mm")

    np.testing.assert_allclose(
        points,
        [[0, 0, 0], [25, 0, 0], [50, 0, 0], [0, 25, 0], [25, 25, 0], [50, 25, 0]],
    )


def test_pattern_and_square_validation_reject_invalid_values() -> None:
    with pytest.raises(ValueError, match="at least 2"):
        validate_pattern_size((1, 8))
    with pytest.raises(ValueError, match="positive"):
        validate_square_size(0, "mm")
    with pytest.raises(ValueError, match="square_unit"):
        validate_square_size(10, "cm")


def test_synthetic_calibration_returns_valid_intrinsics_and_errors() -> None:
    object_points, image_points, image_size = _synthetic_calibration_observations()

    result = calibrate_camera_from_points(
        object_points,
        image_points,
        image_size,
        pattern_size=(6, 5),
        square_size=0.03,
        square_unit="m",
        calibration_id="synthetic-test-only",
        source_image_ids=[f"synthetic_{index}" for index in range(len(object_points))],
    )

    assert result.camera_matrix.shape == (3, 3)
    assert result.distortion_coefficients.size >= 4
    assert len(result.per_view_reprojection_error_px) == 5
    assert result.rms_reprojection_error_px < 1e-3
    assert result.status == "tested"


def test_calibration_serialization_roundtrip(tmp_path) -> None:
    object_points, image_points, image_size = _synthetic_calibration_observations()
    result = calibrate_camera_from_points(
        object_points,
        image_points,
        image_size,
        pattern_size=(6, 5),
        square_size=0.03,
        square_unit="m",
        calibration_id="roundtrip-test-only",
        source_image_ids=["a", "b", "c", "d", "e"],
    )
    path = tmp_path / "calibration.json"
    from module7.calibration import load_calibration, save_calibration

    save_calibration(result, path)
    restored = load_calibration(path)

    assert restored.calibration_id == result.calibration_id
    assert restored.image_size == result.image_size
    np.testing.assert_allclose(restored.camera_matrix, result.camera_matrix)
    np.testing.assert_allclose(restored.distortion_coefficients, result.distortion_coefficients)
    np.testing.assert_allclose(restored.per_view_reprojection_error_px, result.per_view_reprojection_error_px)


def test_calibration_result_rejects_malformed_intrinsics() -> None:
    with pytest.raises(ValueError, match="shape"):
        CalibrationResult(
            calibration_id="bad",
            image_size=(640, 480),
            pattern_size=(6, 5),
            square_size=1,
            square_unit="mm",
            camera_matrix=np.eye(2),
            distortion_coefficients=np.zeros(5),
            rms_reprojection_error_px=0,
            per_view_reprojection_error_px=(0,),
        )

    with pytest.raises(ValueError, match="positive focal lengths"):
        CalibrationResult(
            calibration_id="bad-focal-length",
            image_size=(640, 480),
            pattern_size=(6, 5),
            square_size=1,
            square_unit="mm",
            camera_matrix=np.array([[-1.0, 0.0, 320.0], [0.0, 800.0, 240.0], [0.0, 0.0, 1.0]]),
            distortion_coefficients=np.zeros(5),
            rms_reprojection_error_px=0,
            per_view_reprojection_error_px=(0,),
        )
