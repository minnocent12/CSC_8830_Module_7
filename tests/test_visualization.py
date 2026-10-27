from __future__ import annotations

import numpy as np

from module7.visualization import draw_correspondences, draw_reprojection_overlay


def test_visualization_helpers_do_not_mutate_input_images() -> None:
    image1 = np.zeros((40, 50, 3), dtype=np.uint8)
    image2 = np.zeros((40, 50, 3), dtype=np.uint8)
    before1 = image1.copy()
    before2 = image2.copy()
    points1 = np.array([[10.0, 10.0], [20.0, 20.0]])
    points2 = np.array([[12.0, 10.0], [22.0, 20.0]])

    side_by_side = draw_correspondences(image1, image2, points1, points2)
    overlay = draw_reprojection_overlay(image1, points1, points1 + 1.0)

    assert side_by_side.shape == (40, 100, 3)
    assert overlay.shape == image1.shape
    np.testing.assert_array_equal(image1, before1)
    np.testing.assert_array_equal(image2, before2)
