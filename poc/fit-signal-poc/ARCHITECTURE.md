# Architecture — Fit Signal PoC

> **Scope**: This document describes the *technology stack* and *runtime
> architecture* of the Fit Signal Proof of Concept, an experimental local
> prototype that explores whether a single webcam frame can produce useful
> **fit signals** for apparel size recommendation.
>
> **Relation to the workshop**: This PoC is an **edge-only, model-free
> exploration** that complements the cloud-centric and Foundry-based
> concepts described in [`Deliverable1.md`](../../Deliverable1.md). It uses
> none of Azure AI, Foundry, OpenAI, or any cloud service. Everything runs
> on the developer's laptop. It is intentionally minimal so that the
> *measurement layer* assumptions can be challenged before investing in
> cloud infrastructure.

---

## 1. Goals

1. Verify end-to-end that a single still image **or live webcam frame** can
   be turned into meaningful body fit signals (shoulder width, hip width,
   torso length, leg length, arm length, full-body height).
2. Compare those fit signals against a garment measurement table to produce
   a rule-based size recommendation with a confidence score and per-axis
   reasoning.
3. Validate the assumption that **MediaPipe Pose Landmarker** is sufficient
   for the *pose extraction* part of any production design, so that future
   work can focus on accuracy improvements (segmentation, depth, multi-view)
   rather than re-evaluating the pose detector.

Non-goals: tailor-grade body measurement, 3D body modelling, online
inference at scale, user authentication, persistence beyond local CSV /
JSON files.

---

## 2. Component Overview

```
+----------------------------------------------------------------+
|                       Developer laptop                         |
|                                                                |
|   +-------------------+      +---------------------------+     |
|   |  Browser          |<---->|  Streamlit app (Python)   |     |
|   |  (WebRTC camera)  |      |  app/streamlit_app.py     |     |
|   +-------------------+      +-------------+-------------+     |
|                                            |                   |
|                                            v                   |
|                              +---------------------------+     |
|                              | streamlit-webrtc worker   |     |
|                              | (per-frame callback, AV)  |     |
|                              +-------------+-------------+     |
|                                            |  RGB frame        |
|                                            v                   |
|   +-------------------+      +---------------------------+     |
|   | Jupyter notebooks |      |  src/ Python package      |     |
|   | (offline studies) |----->|                           |     |
|   +-------------------+      |  image_quality.py         |     |
|                              |  pose_detection.py  ----+ |     |
|                              |  measurement.py         | |     |
|                              |  fit_rules.py           | |     |
|                              |  visualization.py       | |     |
|                              +-------------------------|-+     |
|                                                        v       |
|                              +---------------------------+     |
|                              |  MediaPipe Pose Landmarker|     |
|                              |  (heavy, CPU delegate)    |     |
|                              |  models/                  |     |
|                              +---------------------------+     |
|                                            |                   |
|                                            v                   |
|   +-----------------+        +---------------------------+     |
|   | data/garment/   |------->|  Rule-based size matcher  |     |
|   | *.csv           |        |  fit_rules.recommend_size |     |
|   +-----------------+        +---------------------------+     |
|                                                                |
+----------------------------------------------------------------+
```

No code, no media, and no inference leaves the laptop.

---

## 3. Technology Stack

### 3.1 Runtime

| Layer | Technology | Why |
|---|---|---|
| Language | Python ≥ 3.11 | Strong ecosystem for vision + data + UI prototypes |
| Env / package manager | [uv](https://docs.astral.sh/uv/) (`pyproject.toml`, `uv.lock`) | Fast, reproducible installs; lockfile committed |
| Notebook IDE | Jupyter + VS Code Notebooks | Lets reviewers step through each stage |
| Web UI | [Streamlit](https://streamlit.io/) 1.57 | Minimal-effort interactive UI suitable for retail in-store demos |
| Live camera | [streamlit-webrtc](https://github.com/whitphx/streamlit-webrtc) + [PyAV](https://pyav.org/) | Browser WebRTC capture, per-frame callback in Python |

### 3.2 Computer vision

| Layer | Technology | Why |
|---|---|---|
| Pose estimation | [MediaPipe Pose Landmarker (heavy)](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker) | 33 anatomical landmarks with both 2D (image) and 3D (world) coordinates; CPU-friendly; battle-tested |
| Image I/O & overlays | OpenCV (`opencv-python`) | Fast image read/decode, drawing primitives for skeleton overlay |
| Numerical work | NumPy, SciPy | Euclidean distances, smoothing, statistics |
| Data | pandas | Garment table, fit signal export, validation joins |
| Plotting | Matplotlib | Notebook-side visualization (skeleton, dimension lines) |

### 3.3 Why **not** other stacks (for this PoC)

| Considered | Decision | Reason |
|---|---|---|
| Azure AI Vision / Custom Vision | Skipped | Costly to call per frame; not needed for landmark extraction; would couple PoC to cloud |
| Azure AI Foundry / OpenAI GPT-4o vision | Skipped | The PoC question is *can the geometry work*, not *can an LLM reason about photos*. Adding an LLM would hide whether the pose+scaling math is good enough. Foundry is in scope for the workshop's Concept A/B/C, not for this measurement-layer probe. |
| PyTorch / SMPL-X body fitting | Deferred to Week 4+ | Useful for circumference estimation, but requires GPU and large checkpoints; out of PoC scope |
| TensorFlow.js in-browser | Skipped | Python is faster to iterate; keeps the option to swap MediaPipe with a different model later |

### 3.4 GPU usage

- The developer machine has an **NVIDIA RTX 4060 Laptop (8 GB VRAM)**.
- The PoC currently runs MediaPipe with the **CPU delegate** because the
  Windows MediaPipe Tasks Python wheel has limited GPU delegate support and
  pose inference is already well under 100 ms per frame on CPU.
- GPU is wired into `pyproject.toml` as an optional `gpu` extras group
  (PyTorch CUDA 12.1, onnxruntime-gpu) so that depth estimation or 3D body
  fitting can be added later without restructuring the project.

---

## 4. Data Flow

### 4.1 Notebook pipeline (offline)

```
data/raw/front/<image>.jpg  ──►  01 image quality check  ──►  data/processed/quality_report.csv
                              ──►  02 pose extraction       ──►  data/processed/landmarks/<image>.json
                              ──►  03 measurement           ──►  data/processed/measurements/fit_signals.csv
                              ──►  04 size recommendation   ──►  data/processed/measurements/recommendations.csv
                              ──►  05 validation             ──►  reports against data/garment/manual_measurements.csv
data/garment/garment_measurements.csv ─────────────┘
```

### 4.2 Streamlit live pipeline

```
Browser camera (WebRTC)
     │ each VideoFrame
     ▼
streamlit-webrtc worker thread ─► OpenCV BGR ndarray
     │
     ▼
MediaPipe Pose Landmarker (image mode, single shot per frame)
     │ landmarks_px (33×4)  +  landmarks_world (33×4 in metres)
     ▼
SharedState (Lock-protected deque, last 30 frames)
     │
     ├──► overlay drawing (skeleton, key points, measurement lines, height guide)
     │
     ▼ (main Streamlit thread polls every 250 ms)
src.measurement.estimate_fit_signals(user_height_cm)
     │
     ▼
src.fit_rules.recommend_size(garment_table, fit_preference)
     │
     ▼
Retail-styled card UI (size pill + per-axis chips + disclaimer)
```

Key correctness choices:
- **Smoothing**: the live view averages the last *N* frames (default 8) of
  `landmarks_px` and `landmarks_world` before computing metrics. This trades
  100–200 ms of lag for visible stability.
- **Height anchor**: the user-input height is the *only* metric scale
  source for the image-pixel measurements. We also compute a fully
  independent height estimate from MediaPipe's *world* landmarks (in
  metres) so that disagreement between the two flags a bad pose.
- **Privacy**: there is no upload step. The webcam stream stays in
  the browser tab and in the local Python process; nothing is persisted
  to disk by the Streamlit app.

---

## 5. Algorithms (current PoC)

### 5.1 Pixel → centimetre scaling

```
detected_body_height_px = max(y of feet landmarks) - head_top_proxy_y
pixel_to_cm             = user_height_cm / detected_body_height_px
```

where `head_top_proxy_y = nose_y - 0.5 * |shoulder_mid_y - nose_y|` to
roughly account for the top of the skull above the nose, since MediaPipe
does not provide a dedicated head-top landmark.

### 5.2 Independent height check (world landmarks)

`landmarks_world` are predicted in metres relative to the hip centre.
We apply the same head-top proxy and report the result. If this value
disagrees with the user-entered height by more than ~10%, the user is
probably not standing fully in frame.

### 5.3 Fit signals

| Signal | Definition |
|---|---|
| Shoulder width | Euclidean distance between left/right shoulder landmarks, in pixels, scaled to cm |
| Hip width | Same for left/right hip |
| Torso length | Distance from shoulder midpoint to hip midpoint |
| Leg length | Distance from hip midpoint to ankle midpoint |
| Arm length | Distance from left shoulder to left wrist |
| Full body height | Independent world-landmark estimate (cm) |
| Confidence | Min of MediaPipe `visibility` over the shoulder/hip/ankle landmarks used |

### 5.4 Size recommendation rule

For each garment size row we compute, per dimension `d`:

```
ease       = EASE_TABLE[fit_preference][d]
delta_d    = garment_measurement_d - (estimated_body_d + ease)
score      = sqrt( mean( (delta_d / GRADING_STEP_CM[d])^2 ) )
```

The size with the smallest `score` wins. We emit human-readable reasons
(`shoulder_too_tight(-3.2cm)`, `body_too_loose(+1.4cm)`, `good_fit`) and a
confidence value computed as `pose_visibility * 1 / (1 + score)`.

This is intentionally not a learned model — the PoC is about whether the
*measurement* feeding the rule is good enough, not about ranking quality.

---

## 6. Repository Layout

```
poc/fit-signal-poc/
├─ ARCHITECTURE.md            # this file
├─ PLAN.md                    # 4-week PoC plan
├─ README.md                  # quickstart and operating instructions
├─ LICENSE                    # MIT
├─ pyproject.toml             # uv project + dependencies
├─ uv.lock
├─ .python-version
├─ .gitignore
├─ app/
│  └─ streamlit_app.py        # retail-styled live demo
├─ notebooks/
│  ├─ 01_image_quality_check.ipynb
│  ├─ 02_pose_landmark_extraction.ipynb
│  ├─ 03_measurement_estimation.ipynb
│  ├─ 04_fit_recommendation_rules.ipynb
│  └─ 05_validation_against_manual_measurements.ipynb
├─ src/
│  ├─ image_quality.py
│  ├─ pose_detection.py
│  ├─ measurement.py
│  ├─ fit_rules.py
│  └─ visualization.py
├─ scripts/
│  └─ download_demo_images.ps1
└─ data/
   ├─ garment/
   │  ├─ garment_measurements.csv   # sample SKUs (commit OK)
   │  └─ manual_measurements.csv    # manual measurement template (PII-free template)
   ├─ raw/
   │  ├─ front/                     # user photos (gitignored)
   │  ├─ side/                      # user photos (gitignored)
   │  └─ SOURCES.md                 # licences for demo images
   └─ processed/                    # gitignored intermediate outputs
```

Models (`models/pose_landmarker_heavy.task`, ~6 MB) and raw imagery are
**never** committed.

---

## 7. Security and Privacy

| Concern | Mitigation |
|---|---|
| Live user video | Stays in the local Python process; not written to disk by the Streamlit app; not uploaded |
| Sample photos in `data/raw/` | `.gitignore`-excluded; reviewers download or capture their own |
| Manual measurements (PII) | `data/garment/manual_measurements.csv` is a header-only template; real measurements live outside the repo |
| Inference model | `pose_landmarker_heavy.task` is downloaded by README instructions, not committed |
| Dependencies | Pinned in `uv.lock`; only well-known, actively maintained projects |

---

## 8. Limitations and Production Gap

What the PoC **proves**:
- MediaPipe Pose Landmarker is reliable enough for fit-signal extraction at
  > 90% landmark visibility on cooperative subjects.
- Pixel→cm scaling driven by user-input height is sufficient for *width
  and length* signals.
- A rule-based size matcher can produce explainable recommendations with
  per-axis reasons in real time.

What the PoC **does not** prove and would need to be addressed before
production (these align with Concept A in `Deliverable1.md`):
- Circumferences (chest, waist, hip). 2D photos cannot recover these
  reliably without depth or multi-view input.
- Camera distance / lens distortion robustness. A fixed in-store kiosk
  (constant distance and lens) would solve much of this; consumer phones
  would not.
- Garment data quality. The PoC uses a tiny sample table; production
  needs real merchant-supplied measurements per SKU, including grading
  rules.
- Identity, consent, audit, content safety, photo-purge SLA, multi-tenant
  isolation — all out of scope here and provided by the cloud designs in
  `Deliverable1.md`.

---

## 9. How This PoC Fits the Three Workshop Concepts

| Concept (Deliverable1.md) | What this PoC contributes |
|---|---|
| **A. Cloud-Centric Platform** | Replaces the "Vision T1" pose-extraction call with a *local* equivalent that can be load-tested without burning Azure quotas. The same `FitSignals` schema can be the contract a cloud Vision worker emits. |
| **B. Edge + AI Agent-Enabled Operations** | This *is* the edge prototype. The Streamlit app demonstrates an in-store mirror experience that could later wrap an agentic decision loop. |
| **C. Hybrid / Foundry-orchestrated** | Provides a baseline measurement layer whose outputs an agent can call. Foundry would orchestrate "if confidence < threshold then ask for a side photo / call a depth model / hand off to associate". |

The PoC therefore lets the workshop's three architecture concepts be
discussed with a working, measurable baseline rather than only on
whiteboards.
