"""Convert pose landmarks to approximate body measurements (cm).

Strategy:
- pixel_to_cm = user_height_cm / detected_body_height_px
- detected_body_height_px = max(y) - min(y) of reliable landmarks (head <-> ankle/heel)
- All outputs are *fit signals* (medium confidence at best), NOT tailor measurements.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict

import numpy as np

from .pose_detection import NAME_TO_INDEX, PoseResult


@dataclass
class FitSignals:
    """Estimated body fit signals in centimeters."""

    shoulder_width_cm: float
    hip_width_cm: float
    torso_length_cm: float
    leg_length_cm: float
    arm_length_cm: float
    full_body_height_cm: float
    detected_body_height_px: float
    pixel_to_cm: float
    # Confidence — currently the min visibility of landmarks used (0-1).
    confidence: float
    user_height_cm: float

    def as_dict(self) -> dict[str, float]:
        return asdict(self)


def _xy(pose: PoseResult, name: str) -> np.ndarray:
    return pose.landmarks_px[NAME_TO_INDEX[name], :2]


def _visibility(pose: PoseResult, names: list[str]) -> float:
    return float(min(pose.landmarks_px[NAME_TO_INDEX[n], 3] for n in names))


def _euclid(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b))


def estimate_body_height_px(pose: PoseResult) -> float:
    """Crude full-body height in pixels — top of head proxy to lower foot."""
    # Use nose y as head-top proxy if ears not visible; subtract a small offset
    # to approximate the top of the head (~ head height ≈ shoulder-nose distance).
    nose_y = pose.landmarks_px[NAME_TO_INDEX["nose"], 1]
    shoulder_y = 0.5 * (
        pose.landmarks_px[NAME_TO_INDEX["left_shoulder"], 1]
        + pose.landmarks_px[NAME_TO_INDEX["right_shoulder"], 1]
    )
    head_top_proxy = nose_y - 0.5 * abs(shoulder_y - nose_y)

    foot_candidates = [
        pose.landmarks_px[NAME_TO_INDEX[n], 1]
        for n in ("left_heel", "right_heel", "left_ankle", "right_ankle")
    ]
    foot_y = float(max(foot_candidates))  # largest y = lowest point on image
    return float(foot_y - head_top_proxy)


def estimate_body_height_world_cm(pose: PoseResult) -> float:
    """Independent body-height estimate (cm) from MediaPipe *world* landmarks.

    World landmarks are returned in meters relative to the hip center, so this
    does NOT depend on the user-input height — it is the model's intrinsic
    prediction and can be used as a sanity check.
    """
    nose_y = pose.landmarks_world[NAME_TO_INDEX["nose"], 1]
    shoulder_y = 0.5 * (
        pose.landmarks_world[NAME_TO_INDEX["left_shoulder"], 1]
        + pose.landmarks_world[NAME_TO_INDEX["right_shoulder"], 1]
    )
    head_top_proxy = nose_y - 0.5 * abs(shoulder_y - nose_y)
    foot_candidates = [
        pose.landmarks_world[NAME_TO_INDEX[n], 1]
        for n in ("left_heel", "right_heel", "left_ankle", "right_ankle")
    ]
    foot_y = float(max(foot_candidates))
    # In image coords y grows downward; world landmarks follow image convention too.
    height_m = float(foot_y - head_top_proxy)
    return height_m * 100.0


def estimate_fit_signals(pose: PoseResult, user_height_cm: float) -> FitSignals:
    """Compute fit signals from pose landmarks and the user's reported height."""
    if not pose.detected:
        raise ValueError("Pose was not detected — cannot estimate measurements.")

    body_height_px = estimate_body_height_px(pose)
    if body_height_px <= 0:
        raise ValueError("Invalid detected body height (<= 0 px).")

    pixel_to_cm = float(user_height_cm) / body_height_px

    ls, rs = _xy(pose, "left_shoulder"), _xy(pose, "right_shoulder")
    lh, rh = _xy(pose, "left_hip"), _xy(pose, "right_hip")
    la, ra = _xy(pose, "left_ankle"), _xy(pose, "right_ankle")
    lw = _xy(pose, "left_wrist")

    shoulder_center = 0.5 * (ls + rs)
    hip_center = 0.5 * (lh + rh)
    ankle_center = 0.5 * (la + ra)

    shoulder_width_px = _euclid(ls, rs)
    hip_width_px = _euclid(lh, rh)
    torso_px = _euclid(shoulder_center, hip_center)
    leg_px = _euclid(hip_center, ankle_center)
    arm_px = _euclid(ls, lw)

    confidence = _visibility(
        pose,
        [
            "left_shoulder",
            "right_shoulder",
            "left_hip",
            "right_hip",
            "left_ankle",
            "right_ankle",
        ],
    )

    return FitSignals(
        shoulder_width_cm=shoulder_width_px * pixel_to_cm,
        hip_width_cm=hip_width_px * pixel_to_cm,
        torso_length_cm=torso_px * pixel_to_cm,
        leg_length_cm=leg_px * pixel_to_cm,
        arm_length_cm=arm_px * pixel_to_cm,
        full_body_height_cm=estimate_body_height_world_cm(pose),
        detected_body_height_px=body_height_px,
        pixel_to_cm=pixel_to_cm,
        confidence=confidence,
        user_height_cm=float(user_height_cm),
    )


__all__ = [
    "FitSignals",
    "estimate_body_height_px",
    "estimate_body_height_world_cm",
    "estimate_fit_signals",
]
