# Sample image sources & licenses

## `_demo/` — pipeline smoke-test images

These images are used **only to verify the MediaPipe Pose Landmarker
pipeline runs end-to-end**. They are not suitable for fit-signal accuracy
validation because the subjects are not standing in an A-pose (one is a
yoga warrior pose, the other is a seated portrait). Use them when you want
to confirm that Notebook 02 can extract landmarks without errors.

| File | Source | License | Notes |
|---|---|---|---|
| `_demo/mediapipe_pose_sample.jpg` | `storage.googleapis.com/mediapipe-assets/pose.jpg` | Apache-2.0 (MediaPipe sample assets) | Yoga warrior pose, side profile |
| `_demo/pixabay_girl_4051811.jpg`  | `cdn.pixabay.com/photo/2019/03/12/20/39/girl-4051811_960_720.jpg` | Pixabay Content License (commercial use allowed, attribution not required) | Seated pose; used in the official MediaPipe Colab |

To re-download:

```pwsh
pwsh -ExecutionPolicy Bypass -File scripts/download_demo_images.ps1
```

---

## `front/`, `side/` — PoC validation photos (collect manually)

For real PoC validation, place photos you have explicit consent to use
under these folders. Both directories are gitignored, so they will never be
pushed to the repository.

### Required capture conditions

- **Front photo** — Subject facing the camera, arms slightly away from the
  body (A-pose), full body in frame
- **Side photo** — Subject in a perfect side profile, arms by the body,
  full body in frame
- Close-fitting clothing (no loose silhouettes)
- Plain background
- Camera at waist-to-chest height
- Consistent distance to the camera across captures
- Record the subject's height (cm) separately

### If you need stock photos for prototyping

Always re-check the license at the source before publishing anything.

- Pixabay: <https://pixabay.com/photos/search/standing/?orientation=vertical&people_age=adult>
- Pexels: <https://www.pexels.com/search/full%20body%20standing/>
- Unsplash: <https://unsplash.com/s/photos/standing-full-body>

Useful search terms:
- "A-pose full body"
- "fashion lookbook standing"
- "anthropometric reference"
- "fitness model standing front"
