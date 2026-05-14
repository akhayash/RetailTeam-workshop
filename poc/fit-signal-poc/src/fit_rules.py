"""Rule-based fit recommendation.

At PoC stage we do not use ML; we compare estimated fit signals against
garment measurements and pick the size with the smallest weighted delta.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import pandas as pd

from .measurement import FitSignals

FitPreference = Literal["tight", "regular", "loose"]

# Target ease (cm) — tentative values, tops-focused.
# A garment's (chest|shoulder|body|sleeve) width close to body + ease is a good fit.
EASE_TABLE: dict[FitPreference, dict[str, float]] = {
    "tight":   {"shoulder": 0.0, "chest": 2.0,  "body": 0.0, "sleeve": -1.0},
    "regular": {"shoulder": 1.5, "chest": 6.0,  "body": 2.0, "sleeve":  1.0},
    "loose":   {"shoulder": 4.0, "chest": 12.0, "body": 5.0, "sleeve":  3.0},
}

# Average grading per size step (cm) — used to normalize the score.
GRADING_STEP_CM = {
    "shoulder": 1.0,
    "chest": 2.0,
    "body": 1.5,
    "sleeve": 1.5,
}


@dataclass
class SizeRecommendation:
    size: str
    score: float            # smaller is a better fit (0 is ideal)
    confidence: float       # 0-1
    reasons: list[str]
    per_dim_delta_cm: dict[str, float]


def _score_row(
    row: pd.Series,
    signals: FitSignals,
    preference: FitPreference,
) -> tuple[float, dict[str, float], list[str]]:
    """Return (score, deltas, reasons) for one garment size row."""
    ease = EASE_TABLE[preference]

    # The estimated "body chest width (cm) — front projection" is a rough
    # multiple of the shoulder width. Circumferences are out of PoC scope; we
    # compare width-level signals only.
    body_chest_width_proxy = signals.shoulder_width_cm * 1.05

    deltas: dict[str, float] = {}
    if "shoulder_width_cm" in row and pd.notna(row["shoulder_width_cm"]):
        deltas["shoulder"] = float(row["shoulder_width_cm"]) - (
            signals.shoulder_width_cm + ease["shoulder"]
        )
    if "chest_width_cm" in row and pd.notna(row["chest_width_cm"]):
        deltas["chest"] = float(row["chest_width_cm"]) - (
            body_chest_width_proxy + ease["chest"]
        )
    if "body_length_cm" in row and pd.notna(row["body_length_cm"]):
        deltas["body"] = float(row["body_length_cm"]) - (
            signals.torso_length_cm + ease["body"]
        )
    if "sleeve_length_cm" in row and pd.notna(row["sleeve_length_cm"]):
        deltas["sleeve"] = float(row["sleeve_length_cm"]) - (
            signals.arm_length_cm + ease["sleeve"]
        )

    # Normalized score: divide each axis by its grading step, then RMSE.
    if not deltas:
        return float("inf"), deltas, ["no_garment_dimensions"]
    norm = [
        (d / GRADING_STEP_CM[k]) ** 2 for k, d in deltas.items() if k in GRADING_STEP_CM
    ]
    score = float((sum(norm) / len(norm)) ** 0.5)

    reasons: list[str] = []
    for k, d in deltas.items():
        step = GRADING_STEP_CM.get(k, 1.0)
        if d < -step:
            reasons.append(f"{k}_too_tight({d:+.1f}cm)")
        elif d > step:
            reasons.append(f"{k}_too_loose({d:+.1f}cm)")
    if not reasons:
        reasons.append("good_fit")
    return score, deltas, reasons


def recommend_size(
    garment_table: pd.DataFrame,
    signals: FitSignals,
    *,
    preference: FitPreference = "regular",
    category: str | None = None,
    garment_id: str | None = None,
) -> SizeRecommendation:
    """Pick the best-fitting size from a garment_measurements table.

    Expected columns: garment_id, category, size,
                      shoulder_width_cm, chest_width_cm, body_length_cm, sleeve_length_cm
    """
    df = garment_table.copy()
    if category is not None and "category" in df.columns:
        df = df[df["category"] == category]
    if garment_id is not None and "garment_id" in df.columns:
        df = df[df["garment_id"] == garment_id]
    if df.empty:
        raise ValueError("No garment rows match the given filters.")

    scored = []
    for _, row in df.iterrows():
        score, deltas, reasons = _score_row(row, signals, preference)
        scored.append((row["size"], score, deltas, reasons))
    scored.sort(key=lambda x: x[1])

    best_size, best_score, best_deltas, best_reasons = scored[0]
    # Confidence: pose visibility * (1 / (1 + score))
    rec_confidence = float(signals.confidence * (1.0 / (1.0 + best_score)))
    return SizeRecommendation(
        size=str(best_size),
        score=best_score,
        confidence=rec_confidence,
        reasons=best_reasons,
        per_dim_delta_cm=best_deltas,
    )


__all__ = [
    "EASE_TABLE",
    "GRADING_STEP_CM",
    "FitPreference",
    "SizeRecommendation",
    "recommend_size",
]
