"""Streamlit live-camera fit signal demo (retail-style UI).

Run:
    uv run streamlit run app/streamlit_app.py
"""

from __future__ import annotations

import sys
import time
from collections import deque
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
from src.measurement import estimate_fit_signals  # noqa: E402
from src.pose_detection import (  # noqa: E402
    NAME_TO_INDEX,
    PoseResult,
    build_pose_landmarker,
    detect_pose,
)

# =============================================================================
# Page config & global style
# =============================================================================
st.set_page_config(
    page_title="ATELIER · Fit Studio",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
    .stApp {
        background: linear-gradient(180deg, #fafafa 0%, #f1eee9 100%);
        color: #1a1a1a;
    }
    section[data-testid="stSidebar"] {
        background: #111111;
        color: #f4f1ec;
    }
    section[data-testid="stSidebar"] * { color: #f4f1ec !important; }
    section[data-testid="stSidebar"] .stNumberInput input,
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {
        background: #1f1f1f !important;
        color: #f4f1ec !important;
        border-radius: 6px;
    }
    #MainMenu, footer, header { visibility: hidden; }

    .brand-bar {
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        padding: 18px 0 6px 0;
        border-bottom: 1px solid #d9d3c8;
        margin-bottom: 24px;
    }
    .brand-mark {
        font-family: 'Playfair Display', 'Times New Roman', serif;
        font-size: 30px;
        letter-spacing: 0.18em;
        font-weight: 600;
        color: #111;
    }
    .brand-mark span { color: #b08b4f; }
    .brand-tag {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.32em;
        color: #6d6660;
    }

    .hero {
        font-family: 'Playfair Display', 'Times New Roman', serif;
        font-size: 28px;
        line-height: 1.25;
        margin: 0 0 6px 0;
        color: #1a1a1a;
    }
    .hero-sub { color: #6d6660; font-size: 13px; margin: 0 0 20px 0; }

    .card {
        background: #ffffff;
        border: 1px solid #e7e2d8;
        border-radius: 14px;
        padding: 18px 22px;
        box-shadow: 0 6px 24px rgba(0,0,0,0.04);
        margin-bottom: 16px;
    }
    .card-title {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.28em;
        color: #8a8378;
        margin: 0 0 12px 0;
    }
    .metric-row { display: flex; gap: 14px; flex-wrap: wrap; }
    .metric {
        flex: 1 1 110px;
        min-width: 110px;
        background: #fbf9f5;
        border: 1px solid #ece6da;
        border-radius: 10px;
        padding: 12px 14px;
    }
    .metric-label {
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 0.22em;
        color: #8a8378;
        margin-bottom: 4px;
    }
    .metric-value {
        font-family: 'Playfair Display', serif;
        font-size: 24px;
        font-weight: 600;
        color: #1a1a1a;
    }
    .metric-unit { font-size: 12px; color: #8a8378; margin-left: 2px; }
    .metric.accent { background: #1a1a1a; border-color: #1a1a1a; }
    .metric.accent .metric-label { color: #b08b4f; }
    .metric.accent .metric-value { color: #ffffff; }
    .metric.accent .metric-unit { color: #b08b4f; }

    .size-hero { text-align: center; padding: 18px 0 6px 0; }
    .size-pill {
        display: inline-block;
        font-family: 'Playfair Display', serif;
        font-size: 56px;
        font-weight: 700;
        padding: 4px 36px;
        border: 2px solid #1a1a1a;
        border-radius: 999px;
        color: #1a1a1a;
        letter-spacing: 0.08em;
    }
    .size-caption {
        margin-top: 10px;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.28em;
        color: #6d6660;
    }
    .reason-chip {
        display: inline-block;
        background: #f1ece2;
        border: 1px solid #e1d9c8;
        border-radius: 999px;
        padding: 4px 12px;
        margin: 3px 4px 0 0;
        font-size: 11px;
        color: #6d6660;
    }
    .reason-chip.bad { background: #fdecec; border-color: #f3c8c8; color: #a23a3a; }
    .reason-chip.good { background: #ecf6ed; border-color: #cfe6d2; color: #2f7a3a; }

    .badge {
        display: inline-block;
        font-size: 10px;
        letter-spacing: 0.25em;
        text-transform: uppercase;
        padding: 4px 10px;
        border-radius: 999px;
        margin-right: 6px;
    }
    .badge.live    { background: #1a1a1a; color: #fff; }
    .badge.waiting { background: #f1ece2; color: #6d6660; }
    .badge.error   { background: #fdecec; color: #a23a3a; }

    .disclaimer { font-size: 11px; color: #8a8378; margin-top: 18px; line-height: 1.6; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.markdown(
    """
    <div class="brand-bar">
        <div class="brand-mark">ATELIER<span>·</span>FIT</div>
        <div class="brand-tag">In-store size assistant · PoC</div>
    </div>
    """,
    unsafe_allow_html=True,
)

MODEL_PATH = ROOT / "models" / "pose_landmarker_heavy.task"
GARMENT_CSV = ROOT / "data" / "garment" / "garment_measurements.csv"

# =============================================================================
# Sidebar
# =============================================================================
with st.sidebar:
    st.markdown("### 👤 Client")
    user_height_cm = st.number_input(
        "Height (cm)", min_value=120.0, max_value=220.0, value=170.0, step=0.5
    )
    fit_preference = st.selectbox("Fit preference", ["tight", "regular", "loose"], index=1)

    st.markdown("### 👕 Garment")
    if GARMENT_CSV.exists():
        garments = pd.read_csv(GARMENT_CSV)
        garment_ids = ["(none)"] + sorted(garments["garment_id"].unique().tolist())
        selected_garment = st.selectbox("Garment ID", garment_ids, index=1)
    else:
        garments = None
        selected_garment = "(none)"
        st.warning("garment_measurements.csv not found")

    st.markdown("### 🎛 Detection")
    smoothing_n = st.slider("Smoothing frames", 1, 30, 8)
    draw_skeleton = st.checkbox("Draw skeleton", value=True)
    draw_measurement_lines = st.checkbox("Draw measurement lines", value=True)
    mirror = st.checkbox("Mirror camera", value=True)

if not MODEL_PATH.exists():
    st.error(
        f"Pose Landmarker model not found at `{MODEL_PATH}`. "
        "See README.md section 4 to download `pose_landmarker_heavy.task`."
    )
    st.stop()


# =============================================================================
# Shared state
# =============================================================================
@st.cache_resource(show_spinner="Loading MediaPipe Pose Landmarker…")
def get_landmarker():
    return build_pose_landmarker(MODEL_PATH, delegate="cpu")


class SharedState:
    def __init__(self) -> None:
        self.lock = Lock()
        self.latest_pose: PoseResult | None = None
        self.latest_ts: float = 0.0
        self.history: deque[np.ndarray] = deque(maxlen=30)
        self.world_history: deque[np.ndarray] = deque(maxlen=30)
        self.fps_samples: deque[float] = deque(maxlen=30)

    def update(self, pose: PoseResult, dt: float) -> None:
        with self.lock:
            self.latest_pose = pose
            self.latest_ts = time.time()
            if pose.detected:
                self.history.append(pose.landmarks_px.copy())
                self.world_history.append(pose.landmarks_world.copy())
            if dt > 0:
                self.fps_samples.append(1.0 / dt)

    def snapshot(self, smoothing_n: int) -> tuple[PoseResult | None, float, float]:
        with self.lock:
            pose = self.latest_pose
            fps = float(np.mean(self.fps_samples)) if self.fps_samples else 0.0
            if pose is not None and pose.detected and self.history:
                recent_px = list(self.history)[-smoothing_n:]
                recent_w = list(self.world_history)[-smoothing_n:]
                pose = PoseResult(
                    landmarks_px=np.mean(np.stack(recent_px, axis=0), axis=0).astype(np.float32),
                    landmarks_world=np.mean(np.stack(recent_w, axis=0), axis=0).astype(np.float32),
                    image_width=pose.image_width,
                    image_height=pose.image_height,
                    detected=True,
                )
        return pose, 0.0, fps


if "shared" not in st.session_state:
    st.session_state.shared = SharedState()
shared: SharedState = st.session_state.shared


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

# BGR
GOLD = (79, 139, 176)
GOLD_2 = (115, 175, 200)
INK = (40, 40, 40)
WHITE = (245, 245, 245)


def _midpoint(lm: np.ndarray, a: str, b: str) -> np.ndarray:
    return 0.5 * (lm[NAME_TO_INDEX[a], :2] + lm[NAME_TO_INDEX[b], :2])


def draw_overlay(
    image_bgr: np.ndarray,
    pose: PoseResult,
    *,
    show_skeleton: bool,
    show_measurement: bool,
) -> np.ndarray:
    h, w = image_bgr.shape[:2]
    overlay = image_bgr.copy()
    cv2.rectangle(overlay, (0, 0), (w, h), (0, 0, 0), -1)
    image_bgr = cv2.addWeighted(image_bgr, 0.92, overlay, 0.08, 0)

    if not pose.detected:
        cv2.putText(image_bgr, "Stand fully in frame", (24, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, WHITE, 2, cv2.LINE_AA)
        return image_bgr

    lm = pose.landmarks_px
    if show_skeleton:
        for a, b in SKELETON_EDGES:
            ia, ib = NAME_TO_INDEX[a], NAME_TO_INDEX[b]
            pa = tuple(np.round(lm[ia, :2]).astype(int))
            pb = tuple(np.round(lm[ib, :2]).astype(int))
            cv2.line(image_bgr, pa, pb, GOLD, 2, cv2.LINE_AA)
        for name in KEY_POINTS:
            i = NAME_TO_INDEX[name]
            p = tuple(np.round(lm[i, :2]).astype(int))
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

        # full body height guide
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

    return image_bgr


# =============================================================================
# Video callback
# =============================================================================
class _State:
    last_frame_t: float = 0.0


_state = _State()


def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
    img_bgr = frame.to_ndarray(format="bgr24")
    if mirror:
        img_bgr = cv2.flip(img_bgr, 1)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    landmarker = get_landmarker()
    pose = detect_pose(landmarker, img_rgb)

    now = time.time()
    dt = now - _state.last_frame_t if _state.last_frame_t else 0.0
    _state.last_frame_t = now
    shared.update(pose, dt)

    img_bgr = draw_overlay(
        img_bgr, pose,
        show_skeleton=draw_skeleton,
        show_measurement=draw_measurement_lines,
    )
    return av.VideoFrame.from_ndarray(img_bgr, format="bgr24")


# =============================================================================
# Layout
# =============================================================================
left, right = st.columns([3, 2], gap="large")

with left:
    st.markdown('<div class="hero">Find your perfect fit.</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-sub">Step into the frame · keep arms slightly away from your body · we’ll size you in seconds.</div>',
        unsafe_allow_html=True,
    )
    ctx = webrtc_streamer(
        key="fit-signal-live",
        mode=WebRtcMode.SENDRECV,
        video_frame_callback=video_frame_callback,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    )

with right:
    status_placeholder = st.empty()
    metrics_placeholder = st.empty()
    rec_placeholder = st.empty()

status_placeholder.markdown(
    '<span class="badge waiting">Waiting</span> Start the camera to begin.',
    unsafe_allow_html=True,
)
metrics_placeholder.markdown(
    """
    <div class="card">
        <div class="card-title">Body Measurements</div>
        <div class="metric-row">
            <div class="metric accent"><div class="metric-label">Full height</div><div class="metric-value">—<span class="metric-unit"> cm</span></div></div>
            <div class="metric"><div class="metric-label">Shoulder</div><div class="metric-value">—<span class="metric-unit"> cm</span></div></div>
            <div class="metric"><div class="metric-label">Hip</div><div class="metric-value">—<span class="metric-unit"> cm</span></div></div>
        </div>
        <div class="metric-row" style="margin-top:10px;">
            <div class="metric"><div class="metric-label">Torso</div><div class="metric-value">—<span class="metric-unit"> cm</span></div></div>
            <div class="metric"><div class="metric-label">Leg</div><div class="metric-value">—<span class="metric-unit"> cm</span></div></div>
            <div class="metric"><div class="metric-label">Arm</div><div class="metric-value">—<span class="metric-unit"> cm</span></div></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


def _classify_reason(reason: str) -> str:
    if reason.endswith("good_fit"):
        return "good"
    if "too_tight" in reason or "too_loose" in reason:
        return "bad"
    return ""


def _render_metrics(sig, fps: float) -> None:
    # Defensive: tolerate older FitSignals without full_body_height_cm
    # (e.g. if Streamlit kept a cached import of src.measurement).
    body_height_est = getattr(sig, "full_body_height_cm", float("nan"))
    body_height_str = f"{body_height_est:.1f} cm" if body_height_est == body_height_est else "n/a"
    html = f"""
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
                <div class="metric-label">Hip width</div>
                <div class="metric-value">{sig.hip_width_cm:,.1f}<span class="metric-unit"> cm</span></div>
            </div>
        </div>
        <div class="metric-row" style="margin-top:10px;">
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
            Estimates are <b>fit signals</b>, not tailor-grade measurements.
            Stream {fps:.1f} fps · Confidence {sig.confidence:.2f} ·
            Model-independent height check: {body_height_str}
            (input {sig.user_height_cm:.1f} cm).
        </div>
    </div>
    """
    metrics_placeholder.markdown(html, unsafe_allow_html=True)


def _render_recommendation(rec) -> None:
    chips = "".join(
        f'<span class="reason-chip {_classify_reason(r)}">{r}</span>'
        for r in rec.reasons
    )
    deltas = " · ".join(
        f"{k}: {v:+.1f} cm" for k, v in rec.per_dim_delta_cm.items()
    ) if rec.per_dim_delta_cm else ""
    html = f"""
    <div class="card">
        <div class="card-title">Recommended Size</div>
        <div class="size-hero">
            <div class="size-pill">{rec.size}</div>
            <div class="size-caption">Confidence {rec.confidence:.0%} · Score {rec.score:.2f}</div>
        </div>
        <div style="margin-top:14px;">{chips}</div>
        <div class="disclaimer">{deltas}</div>
    </div>
    """
    rec_placeholder.markdown(html, unsafe_allow_html=True)


poll_interval = 0.25
while ctx and ctx.state.playing:
    pose, _age, fps = shared.snapshot(smoothing_n)

    if pose is None or not pose.detected:
        status_placeholder.markdown(
            f'<span class="badge waiting">Detecting</span> Step fully into frame. '
            f'<span style="color:#8a8378">({fps:.1f} fps)</span>',
            unsafe_allow_html=True,
        )
        rec_placeholder.empty()
    else:
        try:
            sig = estimate_fit_signals(pose, user_height_cm)
        except ValueError as e:
            status_placeholder.markdown(
                f'<span class="badge error">Error</span> {e}',
                unsafe_allow_html=True,
            )
            time.sleep(poll_interval)
            continue

        status_placeholder.markdown(
            f'<span class="badge live">Live</span> Pose locked · '
            f'visibility {sig.confidence:.2f} · {fps:.1f} fps',
            unsafe_allow_html=True,
        )
        _render_metrics(sig, fps)

        if garments is not None and selected_garment != "(none)":
            try:
                rec = recommend_size(
                    garments, sig,
                    preference=fit_preference,
                    garment_id=selected_garment,
                )
                _render_recommendation(rec)
            except Exception as e:  # noqa: BLE001
                rec_placeholder.markdown(
                    f'<div class="card"><div class="card-title">Recommendation</div>'
                    f'<div class="disclaimer">Error: {e}</div></div>',
                    unsafe_allow_html=True,
                )
        else:
            rec_placeholder.markdown(
                '<div class="card"><div class="card-title">Recommended Size</div>'
                '<div class="disclaimer">Select a garment in the sidebar to see a size suggestion.</div></div>',
                unsafe_allow_html=True,
            )

    time.sleep(poll_interval)

if ctx and not ctx.state.playing:
    status_placeholder.markdown(
        '<span class="badge waiting">Idle</span> Stream stopped · press START to resume.',
        unsafe_allow_html=True,
    )
