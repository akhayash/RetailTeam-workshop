# Fit Signal PoC — Plan

> **Goal**: Test whether *fit signals* extracted from a customer photo or
> webcam stream can raise size-recommendation confidence enough to reduce
> size-driven returns.
>
> **This is NOT a body-measurement product.** We treat outputs as
> *fit signals*, never as tailor-grade measurements.

---

## 1. Hypothesis

> **Can photo-based fit signals improve size recommendation enough to reduce size-related returns?**

- Inputs: one front photo (+ one side photo, optional) + user height in cm
- Method: MediaPipe Pose Landmarker → height-scaled cm estimates of
  shoulder / hip / torso / leg / arm
- Comparison: rule-based delta against garment measurement CSV
- Output: recommended size + confidence score + per-axis reasoning

---

## 2. Scope

### In scope
- 1 front photo (+ 1 side photo optional) + height input
- MediaPipe Pose Landmarker for landmark extraction
- Pixel-to-cm scaling via user-input height
- Basic estimates: shoulder / hip widths and torso / leg / arm / full-body
  length
- Rule-based comparison against a garment measurement CSV
- Confidence score and per-axis reasons
- Image-quality screening to reject unusable captures
- Live Streamlit demo with skeleton overlay and live metric panel

### Out of scope
- Tailor-grade measurement guarantees
- 3D body scans, medical accuracy
- Reliable chest / waist / hip circumference estimation
- Coverage of all garment categories (start with 1–2: tops and bottoms)
- Production API, cloud inference, multi-tenant isolation
- Learned size-recommendation models (we stay rule-based)

---

## 3. Architecture (PoC stage)

```
Front + Side Photo + Height (cm)
        |
        v
Image quality check
        |
        v
Pose landmark detection (MediaPipe)
        |
        v
Scale by user height
        |
        v
Estimate fit signals
  (shoulder / hip / torso / leg / arm widths & lengths
   + full-body height as independent sanity check)
        |
        v
Compare with garment measurements (CSV)
        |
        v
Recommend size + confidence + reasoning
```

---

## 4. Notebooks

| # | Notebook | Purpose |
| - | --- | --- |
| 1 | `01_image_quality_check.ipynb`                 | Reject unusable captures (resolution, brightness, sharpness) |
| 2 | `02_pose_landmark_extraction.ipynb`            | Extract MediaPipe key points, visualize, record visibility |
| 3 | `03_measurement_estimation.ipynb`              | Height-scaled cm estimates (shoulder / hip / torso / leg / arm) |
| 4 | `04_fit_recommendation_rules.ipynb`            | Compare against garment CSV, produce S/M/L recommendation + confidence |
| 5 | `05_validation_against_manual_measurements.ipynb` | Compute MAE vs. manual measurements, recommendation accuracy |

---

## 5. Signal expectations and confidence

| Output                              | Confidence band                                |
| ----------------------------------- | ---------------------------------------------- |
| Shoulder width                      | Medium                                         |
| Hip width                           | Medium                                         |
| Torso length                        | Medium                                         |
| Leg length                          | Medium                                         |
| Full body height                    | Medium (independent world-landmark estimate)   |
| Chest circumference                 | Low unless side photo provided                 |
| Waist circumference                 | Low unless side photo provided                 |
| Garment size recommendation         | Medium when garment measurements are complete  |

---

## 6. Required inputs / capture guide

- User height (cm)
- Front photo (required), side photo (recommended)
- Capture guide:
  - Camera at waist-to-chest height
  - Full body in frame
  - Face the camera (or perfect side profile)
  - Arms slightly away from the body (A-pose)
  - Close-fitting clothing
  - Plain background

---

## 7. Evaluation metrics

| Metric                            | Meaning                                   |
| --------------------------------- | ---------------------------------------- |
| Landmark detection success rate   | Fraction of images with all key points |
| Measurement MAE (cm)              | Difference vs. manually measured truth |
| Confidence calibration            | High confidence → low error?           |
| Size recommendation accuracy      | Does the recommendation match the size the customer actually kept? |
| Return-risk reduction potential   | Hypothesised reduction in size-driven returns |

### Validation dataset target
- 20–50 participants, each contributing:
  - Front and side photos
  - Height
  - Manually measured shoulder / waist / hip
  - Their usual size, the size that fitted, and any size that did not

---

## 8. Timeline (four weeks)

### Week 1 — Notebook prototype
- [ ] Extract pose landmarks with MediaPipe
- [ ] Overlay key points on the front photo
- [ ] Estimate shoulder / hip / leg in cm

### Week 2 — Fit rule prototype
- [ ] Create a garment measurement CSV (1–2 categories)
- [ ] Compare estimated body dimensions to garment dimensions
- [ ] Produce S/M/L recommendation + confidence

### Week 3 — Validation
- [ ] Collect 20–50 samples and compare against manual measurements
- [ ] Compute estimation errors
- [ ] Tabulate failure rates by capture condition

### Week 4 — Business PoC
- [ ] Pilot on a category with high size-related return rates
- [ ] Surface size, confidence and "tight / loose" reasons in a UI
- [ ] Quantify a hypothesised return-reduction effect

---

## 9. Risks and notes

1. **Without camera calibration, accuracy is limited.**
   Lens distortion and varying camera distance affect pixel-to-cm scaling.
   Asking general users to perform calibration is unrealistic.
   - Mitigation: fix the capture guide and rely on height input.
2. **2D photos cannot reliably recover circumferences.**
   Side photos help with thickness but still fall short of tape-measure
   accuracy.
   - Mitigation: mark circumferences as low confidence; lean on width and
     length signals.
3. **Product messaging matters.**
   - Avoid: "We measure your body from a photo."
   - Prefer: "We use photo-based fit signals to improve size recommendations."
4. **Privacy.**
   - PoC photos live only under `data/raw/` (gitignored).
   - Production needs explicit consent, retention windows, encrypted storage,
     and deletion workflows.

---

## 10. Environment

- Python managed with [uv](https://docs.astral.sh/uv/) (`pyproject.toml`)
- Core libraries: `mediapipe`, `opencv-python`, `numpy`, `pandas`,
  `matplotlib`, `jupyter`, `streamlit`, `streamlit-webrtc`, `av`
- GPU: **NVIDIA GeForce RTX 4060 Laptop (8 GB VRAM)** is present.
  - Weeks 1–2 are CPU-only — MediaPipe Pose Landmarker on Windows uses the
    CPU delegate and runs in well under 100 ms per frame.
  - GPU becomes useful starting in Week 3+ for:
    - Segmentation (e.g., SAM2 / high-resolution Selfie Segmentation)
    - Depth estimation (ZoeDepth / Depth Anything) to add thickness signals
    - 3D body fitting (e.g., SMPL-X) for circumference estimates
  - The `gpu` optional dependency group in `pyproject.toml` pins PyTorch
    CUDA 12.1 + `onnxruntime-gpu` so these can be enabled without
    restructuring the project.

### GPU usage policy (by stage)
| Stage  | Workload                            | GPU? |
| ------ | ----------------------------------- | ---- |
| W1–W2  | Pose landmark extraction            | Not needed (CPU is fine) |
| W3     | Segmentation for contour accuracy   | Helpful |
| W4+    | Depth / 3D body fitting (circumf.)  | Strongly recommended |

---

## 11. Repository layout

```
poc/fit-signal-poc/
  PLAN.md
  README.md
  ARCHITECTURE.md
  LICENSE
  pyproject.toml
  .python-version
  .gitignore
  notebooks/
    01_image_quality_check.ipynb
    02_pose_landmark_extraction.ipynb
    03_measurement_estimation.ipynb
    04_fit_recommendation_rules.ipynb
    05_validation_against_manual_measurements.ipynb
  src/
    image_quality.py
    pose_detection.py
    measurement.py
    fit_rules.py
    visualization.py
  app/
    streamlit_app.py
  scripts/
    download_demo_images.ps1
  data/
    raw/front/                # gitignored
    raw/side/                 # gitignored
    raw/SOURCES.md
    processed/                # gitignored
    garment/
      garment_measurements.csv
      manual_measurements.csv  # template, no PII
```

---

## 12. Definition of done (PoC)

- [ ] Notebooks 01–05 run end-to-end on local sample data
- [ ] MAE vs. manual measurements is reported on ≥ 20 samples
- [ ] Size recommendation accuracy beats a height/weight-only baseline
- [ ] Confidence score and per-axis reasoning are surfaced together
- [ ] A clear decision-support write-up exists for the next step (productize
      vs. invest in segmentation/depth vs. integrate with cloud architecture)
