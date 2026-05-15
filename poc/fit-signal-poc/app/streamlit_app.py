"""Walmart Virtual Mirror — single-page live-camera fit + gesture demo.

Pose Landmarker + Gesture Recognizer run on the same webrtc stream:
- Pose drives size measurement and recommendation.
- Held gestures (~0.6 s) drive UI actions hands-free:
    👍 Thumb_Up      → lock the current recommended size
    👎 Thumb_Down    → unlock
    ✋ Open_Palm     → next garment in the catalog
    ✊ Closed_Fist   → save a snapshot to `output/snapshots/`
    ☝️ Pointing_Up  → rotate fit preference (tight → regular → loose)
    ✌️ Victory      → clear pose history (reset smoothing)

Run:
    uv run streamlit run app/streamlit_app.py
"""

from __future__ import annotations

import base64
import sys
import time
from collections import deque
from datetime import datetime
from pathlib import Path
from threading import Lock

import av
import cv2
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.fit_rules import recommend_size  # noqa: E402
from src.gesture_detection import (  # noqa: E402
    GestureResult,
    build_gesture_recognizer,
    recognize_gesture,
)
from src.measurement import estimate_fit_signals  # noqa: E402
from src.pose_detection import (  # noqa: E402
    NAME_TO_INDEX,
    PoseResult,
    build_pose_landmarker,
    detect_pose,
)

# =============================================================================
# Branding helpers (Walmart customer demo)
# =============================================================================
LOGO_PATH = ROOT / "app" / "assets" / "walmart_logo.png"
WALMART_BLUE = "#0071CE"
WALMART_YELLOW = "#FFC220"

POSE_MODEL_PATH = ROOT / "models" / "pose_landmarker_heavy.task"
GESTURE_MODEL_PATH = ROOT / "models" / "gesture_recognizer.task"
GARMENT_CSV = ROOT / "data" / "garment" / "garment_measurements.csv"
SNAPSHOT_DIR = ROOT / "output" / "snapshots"

PREFERENCES = ("tight", "regular", "loose")
GESTURE_MISS_GRACE_SEC = 0.25


def _logo_html(height_px: int = 40) -> str:
    """<img> tag if Walmart logo exists locally, else styled text fallback."""
    if LOGO_PATH.exists():
        data = base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")
        return (
            f'<img src="data:image/png;base64,{data}" '
            f'style="height:{height_px}px; display:block;" alt="Walmart"/>'
        )
    return (
        '<span style="font-family:Helvetica,Arial,sans-serif; font-weight:700; '
        f'font-size:{height_px - 8}px; color:{WALMART_BLUE}; letter-spacing:-0.01em;">'
        f'Walmart</span> <span style="color:{WALMART_YELLOW}; '
        f'font-size:{height_px - 10}px; vertical-align:0.1em;">✨</span>'
    )


# =============================================================================
# Page config & theme
# =============================================================================
st.set_page_config(
    page_title="Walmart · Virtual Mirror",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        .stApp { background: linear-gradient(180deg, #fafafa 0%, #f1eee9 100%); color:#1a1a1a;
            font-family:'Inter','Segoe UI',sans-serif; }
        section[data-testid="stSidebar"] { background:#111; color:#f4f1ec; }
        section[data-testid="stSidebar"] * { color:#f4f1ec !important; }
        section[data-testid="stSidebar"] .stNumberInput input,
        section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {
            background:#1f1f1f !important; color:#f4f1ec !important; border-radius:6px;
        }
        #MainMenu, footer { visibility:hidden; }
        /* Keep header transparent and slim, but DO NOT hide the whole
           toolbar — it contains the "expand sidebar" button when the
           sidebar is collapsed. Hide only the Streamlit-branded items. */
        header[data-testid="stHeader"] { background: transparent; }
        header[data-testid="stHeader"] [data-testid="stDecoration"],
        header[data-testid="stHeader"] [data-testid="stStatusWidget"],
        header[data-testid="stHeader"] [data-testid="stMainMenuButton"],
        header[data-testid="stHeader"] [data-testid="stBaseButton-header"] { display:none !important; }

        /* Walmart-blue pill for the "open sidebar" toggle. */
        [data-testid="stExpandSidebarButton"] {
            background: #0071CE !important;
            color: #fff !important;
            border-radius: 999px !important;
            padding: 6px 12px !important;
            box-shadow: 0 4px 14px rgba(0,113,206,0.35);
        }
        [data-testid="stExpandSidebarButton"] svg,
        [data-testid="stExpandSidebarButton"] span { color: #fff !important; fill: #fff !important; }
        [data-testid="stExpandSidebarButton"]:hover {
            background: #FFC220 !important;
            color: #1a1a1a !important;
        }
        [data-testid="stExpandSidebarButton"]:hover svg,
        [data-testid="stExpandSidebarButton"]:hover span { color: #1a1a1a !important; fill: #1a1a1a !important; }

        /* ===== Replace Streamlit's default red with Walmart palette ===== */
        /* Sliders */
        [data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
            background:#0071CE !important; border-color:#0071CE !important;
            box-shadow:0 0 0 4px rgba(0,113,206,0.18) !important;
        }
        [data-testid="stSlider"] [data-baseweb="slider"] > div > div > div:first-child {
            background:#0071CE !important;
        }
        /* Checkboxes — Streamlit uses baseweb checkbox whose check mark is
           a <span> sibling of the input. Recolor it to Walmart Blue. */
        [data-testid="stCheckbox"] label[data-baseweb="checkbox"] > span {
            background-color:#0071CE !important;
            border-color:#0071CE !important;
        }
        [data-testid="stCheckbox"] label[data-baseweb="checkbox"]:hover > span {
            background-color:#FFC220 !important;
            border-color:#FFC220 !important;
        }
        [data-testid="stCheckbox"] input:not(:checked) ~ span {
            background-color:transparent !important;
            border-color:#f4f1ec !important;
        }
        /* Generic primary / submit / form buttons */
        button[kind="primary"],
        button[kind="primaryFormSubmit"],
        button[data-testid="stBaseButton-primary"],
        button[data-testid="stBaseButton-secondary"] {
            background:#0071CE !important; color:#fff !important; border-color:#0071CE !important;
        }
        button[kind="primary"]:hover,
        button[kind="primaryFormSubmit"]:hover,
        button[data-testid="stBaseButton-primary"]:hover,
        button[data-testid="stBaseButton-secondary"]:hover {
            background:#FFC220 !important; color:#1a1a1a !important; border-color:#FFC220 !important;
        }
        /* Loading spinner */
        [data-testid="stSpinner"] svg { color:#0071CE !important; fill:#0071CE !important; }
        /* Number input +/- */
        [data-testid="stNumberInputStepUp"]:hover svg,
        [data-testid="stNumberInputStepDown"]:hover svg { color:#FFC220 !important; }

        /* ===== Webrtc START / STOP / SELECT DEVICE — neutral but Walmart-tinted ===== */
        [data-testid="column"]:first-of-type button {
            background:#0071CE !important; color:#fff !important;
            border:1px solid #0071CE !important; border-radius:999px !important;
            font-weight:600 !important; letter-spacing:0.04em;
            padding:8px 18px !important;
            box-shadow:0 4px 14px rgba(0,113,206,0.25);
            transition:all .15s ease;
        }
        [data-testid="column"]:first-of-type button:hover {
            background:#FFC220 !important; color:#1a1a1a !important;
            border-color:#FFC220 !important;
        }

        .brand-bar { display:flex; align-items:center; justify-content:space-between;
            gap:18px; padding:16px 0 14px 0; border-bottom:1px solid #d9d3c8; margin-bottom:18px; }
        .brand-left { display:flex; align-items:center; gap:16px; }
        .brand-mark { font-family:'Playfair Display','Times New Roman',serif;
            font-size:30px; letter-spacing:0.04em; font-weight:600; color:#0071CE; line-height:1; }
        .brand-mark .accent { color:#FFC220; }
        .brand-tag { font-size:11px; text-transform:uppercase; letter-spacing:0.32em; color:#6d6660; }

        .hero { font-family:'Playfair Display','Times New Roman',serif;
            font-size:28px; line-height:1.25; margin:0 0 4px 0; color:#1a1a1a; font-weight:700; }
        .hero-sub { color:#6d6660; font-size:13px; margin:0 0 16px 0; }

        /* START callout — only shown before the camera starts (covered once the stream begins) */
        .start-callout {
            background:linear-gradient(90deg, #0071CE 0%, #2a8fd8 100%);
            color:#fff; padding:12px 18px; border-radius:12px;
            display:flex; align-items:center; gap:14px; margin-bottom:10px;
            box-shadow:0 6px 24px rgba(0,113,206,0.22);
        }
        .start-callout .dot {
            width:10px; height:10px; border-radius:999px; background:#FFC220;
            box-shadow:0 0 0 4px rgba(255,194,32,0.35);
            animation: pulse 1.6s infinite;
        }
        @keyframes pulse {
            0% { box-shadow:0 0 0 0 rgba(255,194,32,0.55); }
            70% { box-shadow:0 0 0 10px rgba(255,194,32,0); }
            100% { box-shadow:0 0 0 0 rgba(255,194,32,0); }
        }
        .start-callout .label { font-size:11px; letter-spacing:0.28em; text-transform:uppercase; color:#FFC220; }
        .start-callout .msg { font-family:'Playfair Display',serif; font-size:18px; font-weight:600; line-height:1.2; }

        .card { background:#fff; border:1px solid #e7e2d8; border-radius:14px;
            padding:16px 20px; box-shadow:0 6px 24px rgba(0,0,0,0.04); margin-bottom:14px; }
        .card-title { font-size:11px; text-transform:uppercase; letter-spacing:0.28em;
            color:#8a8378; margin:0 0 10px 0; }

        /* Idle placeholder copy inside cards */
        .idle-hint {
            display:flex; align-items:center; gap:10px;
            background:#fbf9f5; border:1px dashed #e1d9c8; border-radius:10px;
            padding:10px 14px; color:#8a8378; font-size:12px;
        }
        .idle-hint .badge-yellow {
            background:#FFC220; color:#1a1a1a; font-size:10px; letter-spacing:0.22em;
            text-transform:uppercase; padding:3px 10px; border-radius:999px; font-weight:600;
        }

        .metric-row { display:flex; gap:12px; flex-wrap:wrap; }
        .metric { flex:1 1 110px; min-width:110px; min-height:64px; background:#fbf9f5;
            border:1px solid #ece6da; border-radius:10px; padding:10px 12px; }
        .metric-label { font-size:10px; text-transform:uppercase; letter-spacing:0.22em;
            color:#8a8378; margin-bottom:4px; }
        .metric-value { font-family:'Playfair Display',serif; font-size:22px; font-weight:600; color:#1a1a1a; }
        .metric-unit { font-size:12px; color:#8a8378; margin-left:2px; }
        .metric.accent { background:#0071CE; border-color:#0071CE; }
        .metric.accent .metric-label { color:#FFC220; }
        .metric.accent .metric-value { color:#fff; }
        .metric.accent .metric-unit { color:#FFC220; }

        .size-hero { text-align:center; padding:14px 0 4px 0; }
        .size-pill { display:inline-block; font-family:'Playfair Display',serif;
            font-size:50px; font-weight:700; padding:4px 32px; border:2px solid #0071CE;
            border-radius:999px; color:#0071CE; letter-spacing:0.08em;
            transition:box-shadow .25s ease;
        }
        .size-pill.live {
            box-shadow:0 0 0 6px rgba(0,113,206,0.12), 0 8px 30px rgba(0,113,206,0.25);
        }
        .size-caption { margin-top:8px; font-size:11px; text-transform:uppercase;
            letter-spacing:0.28em; color:#6d6660; }
        .lock-badge { display:inline-block; font-size:10px; letter-spacing:0.24em;
            text-transform:uppercase; padding:3px 10px; border-radius:999px;
            background:#0071CE; color:#fff; margin-left:6px; }
        .lock-badge.off { background:#FFC220; color:#1a1a1a; }

        .gesture-hero { text-align:center; padding:6px 0; }
        .gesture-pill { display:inline-block; font-family:'Playfair Display',serif;
            font-size:30px; font-weight:600; padding:6px 22px; border-radius:999px;
            background:#0071CE; color:#fff; letter-spacing:0.04em; }
        .gesture-idle { background:#f1ece2 !important; color:#6d6660 !important; }
        .gesture-caption { margin-top:6px; font-size:10px; text-transform:uppercase;
            letter-spacing:0.28em; color:#6d6660; }

        .map-row { display:flex; flex-wrap:wrap; gap:6px; }
        .map-chip { background:#fbf9f5; border:1px solid #ece6da; border-radius:8px;
            padding:6px 10px; font-size:11px; color:#3a3a3a; flex:1 1 150px; }
        .map-chip b { font-family:'Playfair Display',serif; font-size:13px; color:#1a1a1a; }

        .reason-chip { display:inline-block; background:#f1ece2; border:1px solid #e1d9c8;
            border-radius:999px; padding:4px 12px; margin:3px 4px 0 0; font-size:11px; color:#6d6660; }
        .reason-chip.bad  { background:#fdecec; border-color:#f3c8c8; color:#a23a3a; }
        .reason-chip.good { background:#ecf6ed; border-color:#cfe6d2; color:#2f7a3a; }

        .badge { display:inline-block; font-size:10px; letter-spacing:0.25em;
            text-transform:uppercase; padding:4px 10px; border-radius:999px; margin-right:6px; }
        .badge.live    { background:#0071CE; color:#fff; }
        .badge.waiting { background:#FFC220; color:#1a1a1a; }
        .badge.error   { background:#fdecec; color:#a23a3a; }

        .toast { background:#0071CE; color:#fff; padding:6px 12px; border-radius:999px;
            display:inline-block; font-size:12px; letter-spacing:0.06em; }

        .disclaimer { font-size:11px; color:#8a8378; margin-top:12px; line-height:1.6; }

        /* ----- Webrtc / camera stage ----- */
        [data-testid="column"]:first-of-type iframe {
            min-height: 460px !important;
            border-radius: 14px;
            background: #0e0e0e;
            border: 1px solid #e7e2d8;
        }
        [data-testid="column"]:first-of-type video {
            border-radius: 14px;
            background: #0e0e0e;
            width: 100% !important;
            object-fit: cover;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="brand-bar">
        <div class="brand-left">
            {_logo_html(40)}
            <div class="brand-mark">Virtual <span class="accent">Mirror</span></div>
        </div>
        <div class="brand-tag">Walmart · In-store size assistant · PoC</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =============================================================================
# Models pre-flight
# =============================================================================
for path, label in [
    (POSE_MODEL_PATH, "Pose Landmarker (`pose_landmarker_heavy.task`)"),
    (GESTURE_MODEL_PATH, "Gesture Recognizer (`gesture_recognizer.task`)"),
]:
    if not path.exists():
        st.error(f"Model not found at `{path}`. See README §4 for {label}.")
        st.stop()


# =============================================================================
# Sidebar
# =============================================================================
with st.sidebar:
    st.markdown("### 👤 Client")
    user_height_cm = st.number_input(
        "Height (cm)", min_value=120.0, max_value=220.0, value=170.0, step=0.5
    )

    st.markdown("### 👕 Garment")
    if GARMENT_CSV.exists():
        garments = pd.read_csv(GARMENT_CSV)
        garment_ids: list[str] = garments["garment_id"].drop_duplicates().tolist()
    else:
        garments = None
        garment_ids = []
        st.warning("garment_measurements.csv not found")

    st.markdown("### 🎛 Detection")
    smoothing_n = st.slider("Smoothing frames", 1, 30, 8)
    draw_skeleton = st.checkbox("Draw skeleton", value=True)
    draw_measurement_lines = st.checkbox("Draw measurement lines", value=True)
    mirror = st.checkbox("Mirror camera", value=True)

    st.markdown("### ✋ Gesture")
    enable_gestures = st.checkbox("Enable hands-free gestures", value=True)
    gesture_min_score = st.slider("Gesture min score", 0.1, 0.9, 0.35, step=0.05)
    gesture_hold_sec = st.slider("Gesture hold (s)", 0.1, 1.5, 0.35, step=0.05)
    cooldown_sec = st.slider("Cooldown (s)", 0.3, 4.0, 0.8, step=0.1)


# =============================================================================
# Session state
# =============================================================================
GESTURE_ACTIONS: dict[str, str] = {
    "Thumb_Up":    "lock_size",
    "Thumb_Down":  "unlock_size",
    "Open_Palm":   "next_garment",
    "Closed_Fist": "snapshot",
    "Pointing_Up": "rotate_preference",
    "Victory":     "reset",
}

if "fit_preference_idx" not in st.session_state:
    st.session_state.fit_preference_idx = 1  # "regular"
if "garment_idx" not in st.session_state:
    st.session_state.garment_idx = 0
if "size_locked" not in st.session_state:
    st.session_state.size_locked = False
if "locked_size" not in st.session_state:
    st.session_state.locked_size = None
if "toast_msg" not in st.session_state:
    st.session_state.toast_msg = ""
if "toast_until" not in st.session_state:
    st.session_state.toast_until = 0.0
if "last_rec_log_at" not in st.session_state:
    st.session_state.last_rec_log_at = 0.0


# =============================================================================
# Shared state (webrtc thread ↔ main loop)
# =============================================================================
class GestureBuffer:
    """Confirms a gesture only if it is held for `hold_sec` seconds."""

    def __init__(self) -> None:
        self.lock = Lock()
        self.current_label: str = "None"
        self.current_score: float = 0.0
        self.streak_label: str = ""
        self.streak_started_at: float = 0.0
        self.last_seen_at: float = 0.0
        self.last_fired_label: str = ""
        self.last_fired_at: float = 0.0
        self.last_logged_at: float = 0.0
        self.pending: deque[tuple[str, float]] = deque(maxlen=16)

    def feed(
        self,
        g: GestureResult,
        hold_sec: float,
        cooldown_sec: float,
        min_score: float,
    ) -> None:
        now = time.time()
        with self.lock:
            label = g.label if g.detected and g.score >= min_score else "None"
            self.current_label = label
            self.current_score = g.score

            if label == "None" or label not in GESTURE_ACTIONS:
                if now - self.last_seen_at > GESTURE_MISS_GRACE_SEC:
                    self.streak_label = ""
                    self.streak_started_at = 0.0
                return

            self.last_seen_at = now
            if label != self.streak_label or self.streak_started_at == 0.0:
                self.streak_label = label
                self.streak_started_at = now
                return

            if now - self.last_logged_at > 1.0:
                print(
                    f"gesture_seen label={label} score={g.score:.2f} "
                    f"held={now - self.streak_started_at:.2f}s",
                    flush=True,
                )
                self.last_logged_at = now

            if now - self.streak_started_at < hold_sec:
                return

            if (
                label == self.last_fired_label
                and now - self.last_fired_at < cooldown_sec
            ):
                return

            self.pending.append((label, now))
            print(f"gesture_fired label={label} score={g.score:.2f}", flush=True)
            self.last_fired_label = label
            self.last_fired_at = now
            self.streak_started_at = now

    def snapshot(self) -> tuple[str, float]:
        with self.lock:
            return self.current_label, self.current_score

    def drain(self) -> list[tuple[str, float]]:
        with self.lock:
            items = list(self.pending)
            self.pending.clear()
        return items


class PoseBuffer:
    def __init__(self) -> None:
        self.lock = Lock()
        self.latest: PoseResult | None = None
        self.history: deque[np.ndarray] = deque(maxlen=30)
        self.world_history: deque[np.ndarray] = deque(maxlen=30)
        self.fps_samples: deque[float] = deque(maxlen=30)
        self.last_frame_bgr: np.ndarray | None = None

    def update(self, pose: PoseResult, dt: float, frame_bgr: np.ndarray) -> None:
        with self.lock:
            self.latest = pose
            self.last_frame_bgr = frame_bgr
            if pose.detected:
                self.history.append(pose.landmarks_px.copy())
                self.world_history.append(pose.landmarks_world.copy())
            if dt > 0:
                self.fps_samples.append(1.0 / dt)

    def smoothed_snapshot(self, n: int) -> tuple[PoseResult | None, float]:
        with self.lock:
            pose = self.latest
            fps = float(np.mean(self.fps_samples)) if self.fps_samples else 0.0
            if pose is not None and pose.detected and self.history:
                recent_px = list(self.history)[-n:]
                recent_w = list(self.world_history)[-n:]
                pose = PoseResult(
                    landmarks_px=np.mean(np.stack(recent_px, axis=0), axis=0).astype(np.float32),
                    landmarks_world=np.mean(np.stack(recent_w, axis=0), axis=0).astype(np.float32),
                    image_width=pose.image_width,
                    image_height=pose.image_height,
                    detected=True,
                )
            return pose, fps

    def reset(self) -> None:
        with self.lock:
            self.history.clear()
            self.world_history.clear()


if "gesture_buffer" not in st.session_state:
    st.session_state.gesture_buffer = GestureBuffer()
if "pose_buffer" not in st.session_state:
    st.session_state.pose_buffer = PoseBuffer()

gesture_buf: GestureBuffer = st.session_state.gesture_buffer
pose_buf: PoseBuffer = st.session_state.pose_buffer


# =============================================================================
# Cached recognizers
# =============================================================================
@st.cache_resource(show_spinner="Loading MediaPipe Pose Landmarker…")
def get_pose_landmarker():
    return build_pose_landmarker(POSE_MODEL_PATH, delegate="cpu")


@st.cache_resource(show_spinner="Loading MediaPipe Gesture Recognizer…")
def get_gesture_recognizer():
    return build_gesture_recognizer(GESTURE_MODEL_PATH, delegate="cpu")


# =============================================================================
# Overlay drawing
# =============================================================================
SKELETON_EDGES = [
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

KEY_POINTS = [
    "left_shoulder", "right_shoulder",
    "left_hip", "right_hip",
    "left_knee", "right_knee",
    "left_ankle", "right_ankle",
    "left_wrist", "right_wrist",
    "nose",
]

GOLD = (79, 139, 176)
GOLD_2 = (115, 175, 200)
INK = (40, 40, 40)
WHITE = (245, 245, 245)


def _midpoint(lm: np.ndarray, a: str, b: str) -> np.ndarray:
    return 0.5 * (lm[NAME_TO_INDEX[a], :2] + lm[NAME_TO_INDEX[b], :2])


def draw_overlay(
    image_bgr: np.ndarray,
    pose: PoseResult,
    gesture_label: str,
    gesture_score: float,
    *,
    show_skeleton: bool,
    show_measurement: bool,
    show_gesture_hud: bool,
) -> np.ndarray:
    h, w = image_bgr.shape[:2]
    overlay = image_bgr.copy()
    cv2.rectangle(overlay, (0, 0), (w, h), (0, 0, 0), -1)
    image_bgr = cv2.addWeighted(image_bgr, 0.92, overlay, 0.08, 0)

    if not pose.detected:
        cv2.putText(image_bgr, "Stand fully in frame", (24, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, WHITE, 2, cv2.LINE_AA)
    else:
        lm = pose.landmarks_px
        if show_skeleton:
            for a, b in SKELETON_EDGES:
                pa = tuple(np.round(lm[NAME_TO_INDEX[a], :2]).astype(int))
                pb = tuple(np.round(lm[NAME_TO_INDEX[b], :2]).astype(int))
                cv2.line(image_bgr, pa, pb, GOLD, 2, cv2.LINE_AA)
            for name in KEY_POINTS:
                p = tuple(np.round(lm[NAME_TO_INDEX[name], :2]).astype(int))
                cv2.circle(image_bgr, p, 5, WHITE, -1, cv2.LINE_AA)
                cv2.circle(image_bgr, p, 5, INK, 1, cv2.LINE_AA)

        if show_measurement:
            ls = lm[NAME_TO_INDEX["left_shoulder"], :2]
            rs = lm[NAME_TO_INDEX["right_shoulder"], :2]
            lh = lm[NAME_TO_INDEX["left_hip"], :2]
            rh = lm[NAME_TO_INDEX["right_hip"], :2]
            la = lm[NAME_TO_INDEX["left_ankle"], :2]
            ra = lm[NAME_TO_INDEX["right_ankle"], :2]
            nose = lm[NAME_TO_INDEX["nose"], :2]
            sc = _midpoint(lm, "left_shoulder", "right_shoulder")
            hc = _midpoint(lm, "left_hip", "right_hip")
            ac = _midpoint(lm, "left_ankle", "right_ankle")

            for p1, p2, color in [
                (ls, rs, GOLD_2),
                (lh, rh, GOLD_2),
                (sc, hc, GOLD),
                (hc, ac, GOLD),
            ]:
                cv2.line(image_bgr,
                         tuple(np.round(p1).astype(int)),
                         tuple(np.round(p2).astype(int)),
                         color, 2, cv2.LINE_AA)

            head_top_y = float(nose[1] - 0.5 * abs(sc[1] - nose[1]))
            foot_y = float(max(la[1], ra[1]))
            x_guide = int(min(w - 30, max(30, lm[NAME_TO_INDEX["nose"], 0] - w * 0.32)))
            cv2.line(image_bgr, (x_guide, int(head_top_y)),
                     (x_guide, int(foot_y)), WHITE, 1, cv2.LINE_AA)
            cv2.line(image_bgr, (x_guide - 8, int(head_top_y)),
                     (x_guide + 8, int(head_top_y)), WHITE, 1, cv2.LINE_AA)
            cv2.line(image_bgr, (x_guide - 8, int(foot_y)),
                     (x_guide + 8, int(foot_y)), WHITE, 1, cv2.LINE_AA)
            cv2.putText(image_bgr, "HEIGHT",
                        (x_guide + 12, int((head_top_y + foot_y) / 2)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, WHITE, 1, cv2.LINE_AA)

    if show_gesture_hud:
        text = (
            f"{gesture_label}  {gesture_score*100:.0f}%"
            if gesture_label not in ("None", "")
            else "Gesture: —"
        )
        cv2.rectangle(image_bgr, (20, h - 56), (20 + 14 * len(text) + 32, h - 16),
                      (26, 26, 26), -1)
        cv2.putText(image_bgr, text, (36, h - 28),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, WHITE, 2, cv2.LINE_AA)

    return image_bgr


# =============================================================================
# Video callback (runs in webrtc worker thread)
# =============================================================================
_callback_state = {"last_t": 0.0}


def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
    img_bgr = frame.to_ndarray(format="bgr24")
    if mirror:
        img_bgr = cv2.flip(img_bgr, 1)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    pose = detect_pose(get_pose_landmarker(), img_rgb)

    if enable_gestures:
        gesture = recognize_gesture(get_gesture_recognizer(), img_rgb)
    else:
        gesture = GestureResult(label="None", score=0.0, handedness="", detected=False)

    now = time.time()
    dt = now - _callback_state["last_t"] if _callback_state["last_t"] else 0.0
    _callback_state["last_t"] = now

    pose_buf.update(pose, dt, img_bgr.copy())
    if enable_gestures:
        gesture_buf.feed(gesture, gesture_hold_sec, cooldown_sec, gesture_min_score)

    img_bgr = draw_overlay(
        img_bgr, pose,
        gesture.label if gesture.detected else "None",
        gesture.score,
        show_skeleton=draw_skeleton,
        show_measurement=draw_measurement_lines,
        show_gesture_hud=enable_gestures,
    )
    return av.VideoFrame.from_ndarray(img_bgr, format="bgr24")


# =============================================================================
# Layout
# =============================================================================
left, right = st.columns([3, 2], gap="large")

with left:
    st.markdown('<div class="hero">Find your perfect fit.</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-sub">Step into the frame · keep arms slightly away from your body · '
        'wave gestures to control the mirror hands-free.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="start-callout">
            <div class="dot"></div>
            <div>
                <div class="label">Tap to begin</div>
                <div class="msg">Press <b>START</b> below · allow camera</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    ctx = webrtc_streamer(
        key="virtual-mirror-live",
        mode=WebRtcMode.SENDRECV,
        video_frame_callback=video_frame_callback,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    )

with right:
    status_placeholder = st.empty()
    gesture_placeholder = st.empty()
    metrics_placeholder = st.empty()
    rec_placeholder = st.empty()
    map_placeholder = st.empty()


def _render_gesture_map() -> None:
    rows = "".join(
        f'<div class="map-chip">{emoji} <b>{label}</b><br/><span style="color:#6d6660">{desc}</span></div>'
        for emoji, label, desc in [
            ("👍", "Thumb_Up",    "Lock size"),
            ("👎", "Thumb_Down",  "Unlock"),
            ("✋", "Open_Palm",   "Next garment"),
            ("✊", "Closed_Fist", "Snapshot"),
            ("☝️", "Pointing_Up", "Rotate fit pref"),
            ("✌️", "Victory",     "Reset history"),
        ]
    )
    map_placeholder.markdown(
        f'<div class="card"><div class="card-title">Hands-free Gestures</div>'
        f'<div class="map-row">{rows}</div></div>',
        unsafe_allow_html=True,
    )


def _classify_reason(reason: str) -> str:
    if reason.endswith("good_fit"):
        return "good"
    if "too_tight" in reason or "too_loose" in reason:
        return "bad"
    return ""


def _toast(msg: str, seconds: float = 2.5) -> None:
    st.session_state.toast_msg = msg
    st.session_state.toast_until = time.time() + seconds


def _apply_action(label: str, current_rec) -> None:
    action = GESTURE_ACTIONS.get(label)
    if action == "lock_size":
        if current_rec is not None:
            st.session_state.size_locked = True
            st.session_state.locked_size = current_rec.size
            _toast(f"🔒 Locked at size {current_rec.size}")
        else:
            _toast("Cannot lock — no recommendation yet")
    elif action == "unlock_size":
        st.session_state.size_locked = False
        st.session_state.locked_size = None
        _toast("🔓 Unlocked")
    elif action == "next_garment":
        if garment_ids:
            st.session_state.garment_idx = (st.session_state.garment_idx + 1) % len(garment_ids)
            _toast(f"👕 {garment_ids[st.session_state.garment_idx]}")
        else:
            _toast("No garments loaded")
    elif action == "snapshot":
        SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
        frame = pose_buf.last_frame_bgr
        if frame is not None:
            fname = SNAPSHOT_DIR / f"snap_{datetime.now():%Y%m%d_%H%M%S}.jpg"
            cv2.imwrite(str(fname), frame)
            _toast(f"📸 Saved {fname.name}")
        else:
            _toast("No frame to save yet")
    elif action == "rotate_preference":
        st.session_state.fit_preference_idx = (st.session_state.fit_preference_idx + 1) % len(PREFERENCES)
        _toast(f"🎚 Preference → {PREFERENCES[st.session_state.fit_preference_idx]}")
    elif action == "reset":
        pose_buf.reset()
        _toast("♻️ Pose history cleared")


def _render_gesture_card(label: str, score: float, locked: bool,
                         preference: str, garment_id: str | None) -> None:
    if not enable_gestures:
        gesture_placeholder.markdown(
            '<div class="card"><div class="card-title">Hands-free Gestures</div>'
            '<div class="disclaimer">Disabled — enable from the sidebar to drive the mirror with gestures.</div></div>',
            unsafe_allow_html=True,
        )
        return
    pill_cls = "gesture-pill" if label not in ("None", "") else "gesture-pill gesture-idle"
    lock_html = (
        '<span class="lock-badge">Size Locked</span>'
        if locked
        else '<span class="lock-badge off">Unlocked</span>'
    )
    toast_html = ""
    if st.session_state.toast_msg and time.time() < st.session_state.toast_until:
        toast_html = (
            f'<div style="text-align:center; margin-top:6px;">'
            f'<span class="toast">{st.session_state.toast_msg}</span></div>'
        )
    gesture_placeholder.markdown(
        f"""
        <div class="card">
            <div class="card-title">Live Gesture</div>
            <div class="gesture-hero">
                <div class="{pill_cls}">{label if label not in ("None","") else "—"}</div>
                <div class="gesture-caption">Score {score:.2f}{lock_html}</div>
            </div>
            <div style="font-size:12px; color:#6d6660; margin-top:6px;">
                Preference: <b style="color:#1a1a1a">{preference}</b> ·
                Garment: <b style="color:#1a1a1a">{garment_id or '(none)'}</b>
            </div>
            {toast_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_metrics(sig, fps: float) -> None:
    body_height_est = getattr(sig, "full_body_height_cm", float("nan"))
    body_height_str = f"{body_height_est:.1f} cm" if body_height_est == body_height_est else "n/a"
    metrics_placeholder.markdown(
        f"""
        <div class="card">
            <div class="card-title">Body Measurements · live</div>
            <div class="metric-row">
                <div class="metric accent">
                    <div class="metric-label">Full height</div>
                    <div class="metric-value">{sig.user_height_cm:,.1f}<span class="metric-unit"> cm</span></div>
                </div>
                <div class="metric">
                    <div class="metric-label">Shoulder</div>
                    <div class="metric-value">{sig.shoulder_width_cm:,.1f}<span class="metric-unit"> cm</span></div>
                </div>
                <div class="metric">
                    <div class="metric-label">Hip</div>
                    <div class="metric-value">{sig.hip_width_cm:,.1f}<span class="metric-unit"> cm</span></div>
                </div>
            </div>
            <div class="metric-row" style="margin-top:8px;">
                <div class="metric">
                    <div class="metric-label">Torso</div>
                    <div class="metric-value">{sig.torso_length_cm:,.1f}<span class="metric-unit"> cm</span></div>
                </div>
                <div class="metric">
                    <div class="metric-label">Leg</div>
                    <div class="metric-value">{sig.leg_length_cm:,.1f}<span class="metric-unit"> cm</span></div>
                </div>
                <div class="metric">
                    <div class="metric-label">Arm</div>
                    <div class="metric-value">{sig.arm_length_cm:,.1f}<span class="metric-unit"> cm</span></div>
                </div>
            </div>
            <div class="disclaimer">
                Fit signals — not tailor-grade. Stream {fps:.1f} fps · Confidence {sig.confidence:.2f} ·
                Height check {body_height_str} (input {sig.user_height_cm:.1f} cm).
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_recommendation(rec, locked_size: str | None) -> None:
    if rec is None and not locked_size:
        rec_placeholder.empty()
        return

    if locked_size and (rec is None or rec.size != locked_size):
        display_size = locked_size
        caption = "Locked manually · gesture-held"
        chips_html = ""
        deltas = ""
    elif rec is not None:
        display_size = rec.size
        caption = f"Confidence {rec.confidence:.0%} · Score {rec.score:.2f}"
        chips_html = "".join(
            f'<span class="reason-chip {_classify_reason(r)}">{r}</span>'
            for r in rec.reasons
        )
        deltas = " · ".join(
            f"{k}: {v:+.1f} cm" for k, v in rec.per_dim_delta_cm.items()
        ) if rec.per_dim_delta_cm else ""
    else:
        return

    rec_placeholder.markdown(
        f"""
        <div class="card">
            <div class="card-title">Recommended Size</div>
            <div class="size-hero">
                <div class="size-pill live">{display_size}</div>
                <div class="size-caption">{caption}</div>
            </div>
            <div style="margin-top:12px;">{chips_html}</div>
            <div class="disclaimer">{deltas}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _log_recommendation(sig, rec, garment_id: str | None, preference: str) -> None:
    now = time.time()
    if rec is None or now - st.session_state.last_rec_log_at < 2.0:
        return
    st.session_state.last_rec_log_at = now
    print(
        "fit_recommendation "
        f"garment={garment_id} preference={preference} size={rec.size} "
        f"score={rec.score:.2f} confidence={rec.confidence:.2f} "
        f"height={sig.user_height_cm:.1f} shoulder={sig.shoulder_width_cm:.1f} "
        f"torso={sig.torso_length_cm:.1f} arm={sig.arm_length_cm:.1f} "
        f"deltas={rec.per_dim_delta_cm} reasons={rec.reasons}",
        flush=True,
    )


# Render the static gesture map once
_render_gesture_map()

status_placeholder.markdown(
    '<span class="badge waiting">Waiting</span> Press <b>START</b> to begin.',
    unsafe_allow_html=True,
)

# Empty-state cards so the layout is filled before the camera starts
metrics_placeholder.markdown(
    """
    <div class="card">
        <div class="card-title">Body Measurements</div>
        <div class="metric-row">
            <div class="metric accent"><div class="metric-label">Full height</div><div class="metric-value">—<span class="metric-unit"> cm</span></div></div>
            <div class="metric"><div class="metric-label">Shoulder</div><div class="metric-value">—<span class="metric-unit"> cm</span></div></div>
            <div class="metric"><div class="metric-label">Hip width</div><div class="metric-value">—<span class="metric-unit"> cm</span></div></div>
        </div>
        <div class="metric-row" style="margin-top:10px;">
            <div class="metric"><div class="metric-label">Torso</div><div class="metric-value">—<span class="metric-unit"> cm</span></div></div>
            <div class="metric"><div class="metric-label">Leg</div><div class="metric-value">—<span class="metric-unit"> cm</span></div></div>
            <div class="metric"><div class="metric-label">Arm</div><div class="metric-value">—<span class="metric-unit"> cm</span></div></div>
        </div>
        <div class="disclaimer">Awaiting camera — values appear once you step into frame.</div>
    </div>
    """,
    unsafe_allow_html=True,
)
rec_placeholder.markdown(
    """
    <div class="card">
        <div class="card-title">Recommended Size</div>
        <div class="size-hero">
            <div class="size-pill">—</div>
            <div class="size-caption">Awaiting pose</div>
        </div>
        <div class="idle-hint" style="margin-top:14px;">
            <span class="badge-yellow">Tip</span>
            <span>Stand fully in frame, arms slightly away from your body.</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# Main loop
# =============================================================================
poll_interval = 0.2
while ctx and ctx.state.playing:
    pose, fps = pose_buf.smoothed_snapshot(smoothing_n)
    label, score = gesture_buf.snapshot()
    preference = PREFERENCES[st.session_state.fit_preference_idx]
    current_garment = garment_ids[st.session_state.garment_idx] if garment_ids else None

    # 1. Compute current recommendation
    rec = None
    sig = None
    if pose is not None and pose.detected:
        try:
            sig = estimate_fit_signals(pose, user_height_cm)
            if garments is not None and current_garment:
                rec = recommend_size(
                    garments, sig,
                    preference=preference,
                    garment_id=current_garment,
                )
        except Exception:  # noqa: BLE001
            rec = None

    # 2. Apply any pending gesture triggers
    if enable_gestures:
        for trig_label, _ts in gesture_buf.drain():
            _apply_action(trig_label, rec)
            if GESTURE_ACTIONS.get(trig_label) in {"next_garment", "rotate_preference"}:
                current_garment = garment_ids[st.session_state.garment_idx] if garment_ids else None
                preference = PREFERENCES[st.session_state.fit_preference_idx]

    # 3. Status badge
    if pose is None or not pose.detected:
        status_placeholder.markdown(
            f'<span class="badge waiting">Detecting</span> Step fully into frame. '
            f'<span style="color:#8a8378">({fps:.1f} fps)</span>',
            unsafe_allow_html=True,
        )
    elif sig is not None:
        status_placeholder.markdown(
            f'<span class="badge live">Live</span> Pose locked · '
            f'visibility {sig.confidence:.2f} · {fps:.1f} fps',
            unsafe_allow_html=True,
        )

    # 4. Cards
    _render_gesture_card(
        label, score,
        locked=st.session_state.size_locked,
        preference=preference,
        garment_id=current_garment,
    )

    if sig is not None:
        _render_metrics(sig, fps)
        _log_recommendation(sig, rec, current_garment, preference)
    _render_recommendation(rec, st.session_state.locked_size if st.session_state.size_locked else None)

    time.sleep(poll_interval)
