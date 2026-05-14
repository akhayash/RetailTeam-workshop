"""MediaPipe Pose Landmarker wrapper.

PoC scope targets single still images. Pose Landmarker returns both 2D
image landmarks and 3D world landmarks.

GPU note:
- The Windows mediapipe Python wheel has limited GPU delegate support, so
  we default to the CPU delegate here. Inference is well under 100 ms per
  image, which is sufficient at PoC scale.
- On Linux / WSL2 the `delegate` argument can be switched to enable the GPU
  delegate.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import numpy as np

# Indices follow MediaPipe Pose Landmarker spec (33 landmarks).
# https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker
LANDMARK_NAMES: dict[int, str] = {
    0: "nose",
    1: "left_eye_inner",
    2: "left_eye",
    3: "left_eye_outer",
    4: "right_eye_inner",
    5: "right_eye",
    6: "right_eye_outer",
    7: "left_ear",
    8: "right_ear",
    9: "mouth_left",
    10: "mouth_right",
    11: "left_shoulder",
    12: "right_shoulder",
    13: "left_elbow",
    14: "right_elbow",
    15: "left_wrist",
    16: "right_wrist",
    17: "left_pinky",
    18: "right_pinky",
    19: "left_index",
    20: "right_index",
    21: "left_thumb",
    22: "right_thumb",
    23: "left_hip",
    24: "right_hip",
    25: "left_knee",
    26: "right_knee",
    27: "left_ankle",
    28: "right_ankle",
    29: "left_heel",
    30: "right_heel",
    31: "left_foot_index",
    32: "right_foot_index",
}

NAME_TO_INDEX: dict[str, int] = {v: k for k, v in LANDMARK_NAMES.items()}


@dataclass
class PoseResult:
    """Detection result for a single image."""

    # (33, 4): x, y, z, visibility — pixel coords for x/y, normalized z relative to hips
    landmarks_px: np.ndarray
    # (33, 4): world landmarks in meters relative to hip center, plus visibility
    landmarks_world: np.ndarray
    image_width: int
    image_height: int
    detected: bool

    def get(self, name: str) -> np.ndarray:
        """Return (x_px, y_px, z, visibility) for a named landmark."""
        return self.landmarks_px[NAME_TO_INDEX[name]]

    def get_world(self, name: str) -> np.ndarray:
        """Return (x, y, z, visibility) in meters from the world landmarks."""
        return self.landmarks_world[NAME_TO_INDEX[name]]


def build_pose_landmarker(
    model_path: str | Path = "models/pose_landmarker_heavy.task",
    *,
    delegate: Literal["cpu", "gpu"] = "cpu",
    min_pose_detection_confidence: float = 0.5,
    min_pose_presence_confidence: float = 0.5,
    min_tracking_confidence: float = 0.5,
):
    """Build a MediaPipe PoseLandmarker for IMAGE mode.

    NOTE: import is local so that simply importing this module does not require
    mediapipe to be installed for users who only need the dataclasses.
    """
    import mediapipe as mp  # noqa: PLC0415
    from mediapipe.tasks import python as mp_python  # noqa: PLC0415
    from mediapipe.tasks.python import vision as mp_vision  # noqa: PLC0415

    model_path = Path(model_path)
    if not model_path.exists():
        raise FileNotFoundError(
            f"Pose Landmarker model not found at {model_path}. "
            "See README.md section 4 to download pose_landmarker_heavy.task."
        )

    delegate_enum = (
        mp_python.BaseOptions.Delegate.GPU
        if delegate == "gpu"
        else mp_python.BaseOptions.Delegate.CPU
    )
    base_options = mp_python.BaseOptions(
        model_asset_path=str(model_path),
        delegate=delegate_enum,
    )
    options = mp_vision.PoseLandmarkerOptions(
        base_options=base_options,
        running_mode=mp_vision.RunningMode.IMAGE,
        num_poses=1,
        min_pose_detection_confidence=min_pose_detection_confidence,
        min_pose_presence_confidence=min_pose_presence_confidence,
        min_tracking_confidence=min_tracking_confidence,
        output_segmentation_masks=False,
    )
    _ = mp  # keep import for side-effects
    return mp_vision.PoseLandmarker.create_from_options(options)


def detect_pose(landmarker, image_rgb: np.ndarray) -> PoseResult:
    """Run Pose Landmarker on an RGB image array (H, W, 3) uint8."""
    import mediapipe as mp  # noqa: PLC0415

    h, w = image_rgb.shape[:2]
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
    result = landmarker.detect(mp_image)

    if not result.pose_landmarks:
        return PoseResult(
            landmarks_px=np.zeros((33, 4), dtype=np.float32),
            landmarks_world=np.zeros((33, 4), dtype=np.float32),
            image_width=w,
            image_height=h,
            detected=False,
        )

    lm = result.pose_landmarks[0]
    wl = result.pose_world_landmarks[0]
    landmarks_px = np.array(
        [[p.x * w, p.y * h, p.z, p.visibility] for p in lm], dtype=np.float32
    )
    landmarks_world = np.array(
        [[p.x, p.y, p.z, p.visibility] for p in wl], dtype=np.float32
    )
    return PoseResult(
        landmarks_px=landmarks_px,
        landmarks_world=landmarks_world,
        image_width=w,
        image_height=h,
        detected=True,
    )


__all__ = [
    "LANDMARK_NAMES",
    "NAME_TO_INDEX",
    "PoseResult",
    "build_pose_landmarker",
    "detect_pose",
]
