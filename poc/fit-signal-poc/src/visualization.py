"""Plot helpers for landmarks and fit signals."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from .pose_detection import NAME_TO_INDEX, PoseResult

# Connections subset to draw a skeleton overlay
POSE_EDGES: list[tuple[str, str]] = [
    ("left_shoulder", "right_shoulder"),
    ("left_shoulder", "left_elbow"),
    ("left_elbow", "left_wrist"),
    ("right_shoulder", "right_elbow"),
    ("right_elbow", "right_wrist"),
    ("left_shoulder", "left_hip"),
    ("right_shoulder", "right_hip"),
    ("left_hip", "right_hip"),
    ("left_hip", "left_knee"),
    ("left_knee", "left_ankle"),
    ("right_hip", "right_knee"),
    ("right_knee", "right_ankle"),
]

KEY_POINTS: list[str] = [
    "left_shoulder", "right_shoulder",
    "left_hip", "right_hip",
    "left_knee", "right_knee",
    "left_ankle", "right_ankle",
    "left_wrist", "right_wrist",
    "nose",
]


def plot_pose_overlay(
    image_rgb: np.ndarray,
    pose: PoseResult,
    *,
    figsize: tuple[int, int] = (6, 10),
    title: str | None = None,
) -> plt.Figure:
    """Overlay skeleton edges and key landmarks on the input image."""
    fig, ax = plt.subplots(figsize=figsize)
    ax.imshow(image_rgb)
    ax.axis("off")
    if title:
        ax.set_title(title)

    if not pose.detected:
        ax.text(10, 30, "No pose detected", color="red", fontsize=14)
        return fig

    lm = pose.landmarks_px
    for a, b in POSE_EDGES:
        ia, ib = NAME_TO_INDEX[a], NAME_TO_INDEX[b]
        ax.plot([lm[ia, 0], lm[ib, 0]], [lm[ia, 1], lm[ib, 1]], "-", lw=2, color="lime")

    for name in KEY_POINTS:
        i = NAME_TO_INDEX[name]
        ax.scatter(lm[i, 0], lm[i, 1], s=24, c="red", zorder=3)
    return fig


__all__ = ["POSE_EDGES", "KEY_POINTS", "plot_pose_overlay"]
