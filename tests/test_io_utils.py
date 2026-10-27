from __future__ import annotations

import numpy as np
import pytest

from module7.io_utils import (
    ensure_same_image_size,
    read_correspondence_csv,
    read_json,
    validate_image_array,
    write_json,
)


def test_image_validation_preserves_array_without_mutation() -> None:
    image = np.zeros((12, 16, 3), dtype=np.uint8)
    validated = validate_image_array(image, require_color=True)

    assert validated is image
    assert validated.shape == (12, 16, 3)


def test_image_sizes_must_match() -> None:
    with pytest.raises(ValueError, match="one size"):
        ensure_same_image_size([np.zeros((10, 10, 3), dtype=np.uint8), np.zeros((11, 10, 3), dtype=np.uint8)])


def test_json_roundtrip_supports_numpy_values(tmp_path) -> None:
    path = tmp_path / "record.json"
    write_json(path, {"matrix": np.eye(2), "count": np.int64(3), "valid": np.bool_(True)})

    payload = read_json(path)

    assert payload == {"matrix": [[1.0, 0.0], [0.0, 1.0]], "count": 3, "valid": True}


def test_correspondence_csv_roundtrip_uses_shared_schema(tmp_path) -> None:
    path = tmp_path / "points.csv"
    path.write_text(
        "point_id,u1,v1,u2,v2\nA,10,20,11,21\nB,30,40,31,41\n",
        encoding="utf-8",
    )

    ids, first, second = read_correspondence_csv(path)

    assert ids == ["A", "B"]
    np.testing.assert_allclose(first, [[10.0, 20.0], [30.0, 40.0]])
    np.testing.assert_allclose(second, [[11.0, 21.0], [31.0, 41.0]])


def test_correspondence_csv_rejects_duplicate_ids(tmp_path) -> None:
    path = tmp_path / "duplicate.csv"
    path.write_text(
        "point_id,u1,v1,u2,v2\nA,10,20,11,21\nA,30,40,31,41\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="duplicate point_id"):
        read_correspondence_csv(path)
