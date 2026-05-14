"""Image quality checks for the fit signal PoC.

Poor capture quality makes landmark extraction unstable, so we reject
unsuitable images early.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np


@dataclass
class QualityReport:
    """Single image quality assessment."""

    path: Path
    width: int
    height: int
    brightness: float  # 0-255 mean luma
    sharpness: float  # variance of Laplacian
    is_color: bool
    passed: bool
    reasons: list[str]


def assess_image(
    image_path: str | Path,
    *,
    min_side: int = 480,
    min_brightness: float = 40.0,
    max_brightness: float = 230.0,
    min_sharpness: float = 50.0,
) -> QualityReport:
    """Return a QualityReport for a single image file.

    - `min_side`: minimum pixel count for the short side (below this, landmark accuracy degrades)
    - `min_brightness` / `max_brightness`: allowed mean luma range
    - `min_sharpness`: Laplacian variance (lower means blurrier)
    """
    path = Path(image_path)
    img = cv2.imread(str(path))
    if img is None:
        return QualityReport(
            path=path,
            width=0,
            height=0,
            brightness=0.0,
            sharpness=0.0,
            is_color=False,
            passed=False,
            reasons=["cannot_read_image"],
        )

    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    brightness = float(gray.mean())
    sharpness = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    is_color = img.ndim == 3 and img.shape[2] == 3

    reasons: list[str] = []
    if min(h, w) < min_side:
        reasons.append(f"too_small({min(h, w)}<{min_side})")
    if brightness < min_brightness:
        reasons.append(f"too_dark({brightness:.0f}<{min_brightness:.0f})")
    if brightness > max_brightness:
        reasons.append(f"too_bright({brightness:.0f}>{max_brightness:.0f})")
    if sharpness < min_sharpness:
        reasons.append(f"too_blurry({sharpness:.0f}<{min_sharpness:.0f})")

    return QualityReport(
        path=path,
        width=w,
        height=h,
        brightness=brightness,
        sharpness=sharpness,
        is_color=is_color,
        passed=len(reasons) == 0,
        reasons=reasons,
    )


def batch_assess(directory: str | Path, pattern: str = "*.jp*g") -> list[QualityReport]:
    """Run assess_image over a directory."""
    directory = Path(directory)
    reports: list[QualityReport] = []
    for p in sorted(directory.glob(pattern)):
        reports.append(assess_image(p))
    return reports


__all__ = ["QualityReport", "assess_image", "batch_assess"]
