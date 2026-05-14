"""MediaPipe Gesture Recognizer wrapper.

Mirrors the design of `src.pose_detection`: a thin functional layer over
`mediapipe.tasks.vision.GestureRecognizer` so the Streamlit page can stay
declarative.

Built-in gestures emitted by the default `gesture_recognizer.task` model:

    None, Closed_Fist, Open_Palm, Pointing_Up,
    Thumb_Down, Thumb_Up, Victory, ILoveYou

GPU note:
- On Windows, the MediaPipe Python wheel ships with limited GPU delegate
  support, so the recognizer defaults to CPU. Inference is well under
  20 ms per frame.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import numpy as np

# Canonical gesture labels emitted by the default model (lower-cased copies
# for case-insensitive matching).
GESTURE_LABELS: tuple[str, ...] = (
    "None",
    "Closed_Fist",
    "Open_Palm",
    "Pointing_Up",
    "Thumb_Down",
    "Thumb_Up",
    "Victory",
    "ILoveYou",
)


@dataclass
class GestureResult:
    """Top gesture detected for a single hand in a single image."""

    label: str          # e.g. "Thumb_Up" or "None" when no gesture matches
    score: float        # softmax score from the classifier (0..1)
    handedness: str     # "Left" / "Right" / "" (camera frame, not the person)
    detected: bool      # True if at least one hand was detected


_EMPTY_RESULT = GestureResult(label="None", score=0.0, handedness="", detected=False)


def build_gesture_recognizer(
    model_path: str | Path = "models/gesture_recognizer.task",
    *,
    delegate: Literal["cpu", "gpu"] = "cpu",
    num_hands: int = 1,
    min_hand_detection_confidence: float = 0.5,
    min_hand_presence_confidence: float = 0.5,
    min_tracking_confidence: float = 0.5,
):
    """Build a MediaPipe GestureRecognizer for IMAGE mode.

    NOTE: import is local so simply importing this module does not require
    `mediapipe` for callers that only need the dataclasses.
    """
    import mediapipe as mp  # noqa: PLC0415
    from mediapipe.tasks import python as mp_python  # noqa: PLC0415
    from mediapipe.tasks.python import vision as mp_vision  # noqa: PLC0415

    model_path = Path(model_path)
    if not model_path.exists():
        raise FileNotFoundError(
            f"Gesture Recognizer model not found at {model_path}. "
            "See README.md section 4 to download gesture_recognizer.task."
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
    options = mp_vision.GestureRecognizerOptions(
        base_options=base_options,
        running_mode=mp_vision.RunningMode.IMAGE,
        num_hands=num_hands,
        min_hand_detection_confidence=min_hand_detection_confidence,
        min_hand_presence_confidence=min_hand_presence_confidence,
        min_tracking_confidence=min_tracking_confidence,
    )
    _ = mp  # keep import for side-effects
    return mp_vision.GestureRecognizer.create_from_options(options)


def recognize_gesture(recognizer, image_rgb: np.ndarray) -> GestureResult:
    """Run Gesture Recognizer on an RGB image (H, W, 3) uint8.

    Returns the highest-confidence gesture for the first detected hand.
    """
    import mediapipe as mp  # noqa: PLC0415

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
    result = recognizer.recognize(mp_image)

    if not result.gestures or not result.gestures[0]:
        return _EMPTY_RESULT

    top = result.gestures[0][0]  # first hand, top-1 category
    handedness = ""
    if result.handedness and result.handedness[0]:
        handedness = result.handedness[0][0].category_name

    return GestureResult(
        label=top.category_name or "None",
        score=float(top.score),
        handedness=handedness,
        detected=True,
    )


__all__ = [
    "GESTURE_LABELS",
    "GestureResult",
    "build_gesture_recognizer",
    "recognize_gesture",
]
