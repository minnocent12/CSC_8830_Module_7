from __future__ import annotations

import numpy as np
import pytest

from module7.depth_estimation import (
    depth_from_triangulated_points,
    rectified_depth_from_disparity,
    summarize_depth,
)


def test_rectified_depth_formula_is_explicitly_metric() -> None:
    result = rectified_depth_from_disparity(800.0, 0.2, np.array([80.0, 40.0]), unit="m")

    np.testing.assert_allclose(result.depth, [2.0, 4.0])
    assert result.valid_mask.all()
    assert result.unit == "m"
    assert result.source == "rectified_disparity_formula"


def test_rectified_depth_rejects_invalid_disparity_unless_requested() -> None:
    with pytest.raises(ValueError, match="positive"):
        rectified_depth_from_disparity(800.0, 0.2, np.array([80.0, 0.0]), unit="m")

    result = rectified_depth_from_disparity(
        800.0, 0.2, np.array([80.0, 0.0, np.nan]), unit="m", allow_invalid=True
    )
    np.testing.assert_allclose(result.depth[0], 2.0)
    assert result.valid_mask.tolist() == [True, False, False]


def test_triangulated_depth_requires_positive_finite_points() -> None:
    result = depth_from_triangulated_points(
        np.array([[1.0, 2.0, 3.0], [0.0, 0.0, -1.0], [np.nan, 0.0, 2.0]]),
        unit="mm",
        allow_invalid=True,
    )

    assert result.valid_mask.tolist() == [True, False, False]
    summary = summarize_depth(result)
    assert summary["count"] == 1
    assert summary["invalid_count"] == 2
    assert summary["mean"] == 3.0
