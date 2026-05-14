# Fit Signal PoC

Photo- and webcam-based **fit signal** extraction prototype for apparel size
recommendation. See [`ARCHITECTURE.md`](./ARCHITECTURE.md) for the technology
stack and [`PLAN.md`](./PLAN.md) for the four-week PoC plan.

> ⚠️ **This is not a body-measurement product.** The goal is to test whether
> photo-based *fit signals* can raise size-recommendation confidence enough
> to reduce size-driven returns — not to produce tailor-grade measurements.

This PoC complements the cloud and edge architecture concepts in the
workshop's [`Deliverable1.md`](../../Deliverable1.md) by providing a working,
local baseline for the measurement layer.

---

## TL;DR — Run the PoC in 5 minutes

```pwsh
# from poc/fit-signal-poc/
uv sync
uv run python -m ipykernel install --user --name fit-signal-poc --display-name "fit-signal-poc"

# Download the MediaPipe Pose Landmarker model (~31 MB)
New-Item -ItemType Directory -Force -Path models | Out-Null
Invoke-WebRequest `
  -Uri "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_heavy/float16/latest/pose_landmarker_heavy.task" `
  -OutFile "models/pose_landmarker_heavy.task"

# (Optional) Get sample images for a pipeline smoke test
pwsh -ExecutionPolicy Bypass -File scripts/download_demo_images.ps1

# Live retail-style demo (opens http://localhost:8501)
uv run streamlit run app/streamlit_app.py
```

For the notebook-driven workflow, open `notebooks/01_image_quality_check.ipynb`
in VS Code, pick the **fit-signal-poc** kernel, and run notebooks 01 to 05 in
order. Sections below explain each step in detail.

---

## 1. Setup

### Prerequisites

- Windows + PowerShell (tested) — macOS/Linux should work with minor changes
- Python 3.11
- (Optional) NVIDIA GPU + recent driver (only required if you later enable
  segmentation / depth / 3D body fitting)
- [uv](https://docs.astral.sh/uv/) for dependency management

### Install uv (if needed)

```pwsh
winget install --id=astral-sh.uv -e
```

### Install dependencies

```pwsh
# Core dependencies (CPU inference is enough for the baseline)
uv sync

# Register a Jupyter kernel
uv run python -m ipykernel install --user --name fit-signal-poc --display-name "fit-signal-poc"
```

### (Optional) GPU extras — Week 3+

MediaPipe Pose Landmarker runs comfortably on CPU (< 100 ms per frame), so
GPU is not required for Weeks 1–2. Enable the extras only when you start
exploring segmentation / depth / 3D body fitting:

```pwsh
# PyTorch (CUDA 12.1 wheels) — install via the official index
uv pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# Other GPU extras
uv sync --extra gpu
```

Verify GPU:

```pwsh
uv run python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no cuda')"
```

---

## 2. Repository layout

```
poc/fit-signal-poc/
  ARCHITECTURE.md
  PLAN.md
  README.md
  LICENSE
  pyproject.toml
  notebooks/          # 01–05 — run in order
  src/                # Reusable Python package
  app/                # Streamlit live demo
  data/
    raw/front/        # Front-view photos (gitignored)
    raw/side/         # Side-view photos (gitignored)
    processed/        # Landmarks / measurements (gitignored)
    garment/          # Garment measurement CSVs (committed)
  models/             # MediaPipe .task files (gitignored)
```

---

## 3. Run order (notebooks)

1. Place sample photos under `data/raw/front/` and `data/raw/side/`.
2. `notebooks/01_image_quality_check.ipynb` — basic capture quality checks
3. `notebooks/02_pose_landmark_extraction.ipynb` — MediaPipe landmark extraction
4. `notebooks/03_measurement_estimation.ipynb` — height-scaled cm estimates
5. `notebooks/04_fit_recommendation_rules.ipynb` — rule-based size suggestion
6. `notebooks/05_validation_against_manual_measurements.ipynb` — validation against manually measured ground truth

Open the `.ipynb` files in VS Code and select the **fit-signal-poc** kernel.

---

## 4. MediaPipe models

Download the MediaPipe `.task` model files into `models/` once.

### 4.1 Pose Landmarker (required)

- Reference: <https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker#models>
- Direct download (heavy / float16):
  <https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_heavy/float16/latest/pose_landmarker_heavy.task>

```pwsh
New-Item -ItemType Directory -Force -Path models | Out-Null
Invoke-WebRequest `
  -Uri "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_heavy/float16/latest/pose_landmarker_heavy.task" `
  -OutFile "models/pose_landmarker_heavy.task"
```

### 4.2 Gesture Recognizer (required for the Gesture Control demo)

- Reference: <https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer>
- Direct download (float16):
  <https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/latest/gesture_recognizer.task>

```pwsh
Invoke-WebRequest `
  -Uri "https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/latest/gesture_recognizer.task" `
  -OutFile "models/gesture_recognizer.task"
```

This model recognizes 7 built-in gestures:
`Closed_Fist`, `Open_Palm`, `Pointing_Up`, `Thumb_Down`, `Thumb_Up`,
`Victory`, `ILoveYou` (plus `None`).

---

## 5. Streamlit live camera demo — *Virtual Mirror*

A retail-style live demo that combines pose detection, fit signal
estimation and rule-based size recommendation in real time. Branded
as **Virtual Mirror** for the Walmart customer demo.

```pwsh
uv run streamlit run app/streamlit_app.py
```

### Walmart branding (optional logo)

The brand bar shows a Walmart logo when `app/assets/walmart_logo.png` is
present and falls back to a styled "Walmart ✨" text mark otherwise.

- Place an approved PNG (transparent background, ~512 px wide) at
  `app/assets/walmart_logo.png`.
- The file is **gitignored on purpose** — third-party trademarks must not
  be committed. See [`app/assets/README.md`](./app/assets/README.md).
- Walmart brand colors used in the UI: `#0071CE` (blue), `#FFC220` (yellow).

- The browser opens at `http://localhost:8501`.
- Click **START** on the left panel to enable the webcam (the browser will
  prompt for camera permission).
- Sidebar inputs:
  - Height (cm) — used as the pixel-to-cm scale anchor
  - Fit preference (tight / regular / loose)
  - Garment ID — selected from `data/garment/garment_measurements.csv`
- The right panel updates live with:
  - Skeleton + measurement-line overlay
  - Shoulder / Hip / Torso / Leg / Arm estimates in cm
  - Recommended size + confidence + per-axis reasons
- Frames are smoothed over a configurable rolling window (default 8 frames)
  to stabilise the numbers.

> Recommended capture conditions: full body in frame, standing A-pose,
> close-fitting clothes, plain background.
> The output is a *fit signal* (medium confidence), not a tailor-grade
> measurement.

### 5.1 Hands-free gestures (built-in)

The Virtual Mirror runs `Pose Landmarker` and `Gesture Recognizer` on the
same webrtc stream. Hold a gesture for ~0.6 s (configurable from the
sidebar) to trigger an action without touching the screen.

| Gesture | Action |
|---|---|
| 👍 `Thumb_Up`    | Lock the current recommended size |
| 👎 `Thumb_Down`  | Unlock |
| ✋ `Open_Palm`    | Cycle to the next garment in the catalog |
| ✊ `Closed_Fist`  | Save a snapshot to `output/snapshots/` |
| ☝️ `Pointing_Up` | Rotate fit preference (tight → regular → loose) |
| ✌️ `Victory`     | Clear pose history (reset smoothing) |

A short cooldown (default 1.2 s) prevents accidental re-triggers when the
same gesture is held continuously. The on-camera HUD shows the live
gesture label and confidence; a toast above the recommendation card
confirms each action.

---

## 6. Privacy

- Photos under `data/raw/` are **never** committed (`.gitignore` enforced).
- The Streamlit demo keeps the camera stream local; nothing is uploaded.
- After the PoC, delete local images or move them to encrypted storage.
- A production deployment must add consent, retention, and deletion
  workflows separately.

---

## 7. License

MIT — see [`LICENSE`](./LICENSE).
