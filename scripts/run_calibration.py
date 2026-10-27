#!/usr/bin/env python3
"""Run real checkerboard calibration from user-supplied smartphone images.

Example after real captures exist:

    python scripts/run_calibration.py \
        --input-dir data/calibration \
        --pattern-cols 9 --pattern-rows 6 \
        --square-size 25 --square-unit mm \
        --output results/calibration/phone_calibration.json

The script fails when the requested images or checkerboard observations are unavailable. It
never creates placeholder calibration values.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from module7.calibration import calibrate_camera_from_image_paths  # noqa: E402
from module7.io_utils import SUPPORTED_IMAGE_SUFFIXES  # noqa: E402


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--input-dir", type=Path, help="directory containing calibration images")
    source.add_argument("--images", nargs="+", type=Path, help="explicit calibration image paths")
    parser.add_argument("--pattern-cols", type=int, required=True, help="checkerboard inner corners across")
    parser.add_argument("--pattern-rows", type=int, required=True, help="checkerboard inner corners down")
    parser.add_argument("--square-size", type=float, required=True, help="measured square side")
    parser.add_argument("--square-unit", choices=("m", "mm"), default="mm")
    parser.add_argument("--calibration-id", default="phone-calibration")
    parser.add_argument("--output", type=Path, required=True, help="JSON output path")
    parser.add_argument("--no-refine", action="store_true", help="disable classic corner refinement")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.input_dir is not None:
        if not args.input_dir.is_dir():
            print(f"error: calibration input directory does not exist: {args.input_dir}", file=sys.stderr)
            return 2
        image_paths = sorted(
            path for path in args.input_dir.iterdir() if path.is_file() and path.suffix.lower() in SUPPORTED_IMAGE_SUFFIXES
        )
    else:
        image_paths = list(args.images)
    if not image_paths:
        print("error: no calibration images were found", file=sys.stderr)
        return 2
    try:
        result = calibrate_camera_from_image_paths(
            image_paths,
            pattern_size=(args.pattern_cols, args.pattern_rows),
            square_size=args.square_size,
            square_unit=args.square_unit,
            calibration_id=args.calibration_id,
            refine=not args.no_refine,
        )
        from module7.calibration import save_calibration

        save_calibration(result, args.output)
    except (OSError, ValueError) as exc:
        print(f"calibration failed: {exc}", file=sys.stderr)
        return 1
    print(f"saved calibration record: {args.output}")
    print(f"accepted views: {len(result.source_image_ids)}")
    print(f"image size: {result.image_size[0]}x{result.image_size[1]} px")
    print(f"RMS reprojection error: {result.rms_reprojection_error_px:.6f} px")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
