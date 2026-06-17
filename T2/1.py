#!/usr/bin/env python3
"""Create a false-color visualization for the Salinas hyperspectral scene.

Default input:
  data/Salinas_corrected.mat

Default output:
  T2/1.png
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(".matplotlib").resolve()))

import matplotlib.pyplot as plt
import numpy as np

from hsi_utils import auto_rgb_bands, load_cube


def robust_normalize(channel: np.ndarray, low: float = 2.0, high: float = 98.0) -> np.ndarray:
    """Normalize one band with percentile clipping to improve visual contrast."""
    arr = channel.astype(np.float32, copy=False)
    lo, hi = np.percentile(arr, [low, high])
    if hi <= lo:
        return np.zeros(arr.shape, dtype=np.float32)
    return np.clip((arr - lo) / (hi - lo), 0.0, 1.0)


def build_false_color(cube: np.ndarray, bands_1based: tuple[int, int, int]) -> np.ndarray:
    band_count = cube.shape[2]
    if any(b < 1 or b > band_count for b in bands_1based):
        raise ValueError(f"Band numbers must be in 1..{band_count}, got {bands_1based}")

    # Extract only three bands, so memory stays small under the 1 GB limit.
    bands_0based = [b - 1 for b in bands_1based]
    channels = [robust_normalize(cube[:, :, b]) for b in bands_0based]
    return np.dstack(channels)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/Salinas_corrected.mat"))
    parser.add_argument("--output", type=Path, default=Path("T2/1.png"))
    parser.add_argument("--variable", help="Name of the 3-D image variable inside the .mat file.")
    parser.add_argument(
        "--bands",
        type=int,
        nargs=3,
        default=None,
        metavar=("R", "G", "B"),
        help="1-based band numbers mapped to red, green and blue. Auto-selected if omitted.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cube, variable = load_cube(args.input, args.variable)
    bands = tuple(args.bands) if args.bands else auto_rgb_bands(cube.shape[2])
    rgb = build_false_color(cube, bands)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    plt.imsave(args.output, rgb)
    print(f"Saved false-color image to {args.output}")
    print(f"Cube variable: {variable}; shape: {cube.shape}; RGB bands: {bands}")


if __name__ == "__main__":
    main()
