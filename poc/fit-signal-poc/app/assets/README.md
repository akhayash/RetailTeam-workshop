# app/assets/

Branding assets for the Virtual Mirror demo.

> **Trademark notice.** Logos placed here are third-party trademarks owned by
> their respective holders (e.g. Walmart Inc. for the Walmart logo / Spark).
> They are used for an internal customer demo only and are **not** committed
> to this repository. Do not redistribute the binaries.

## Expected files (gitignored)

| File | Used by | Notes |
|---|---|---|
| `walmart_logo.png` | Brand bar on both Streamlit pages | PNG with transparent background, ~512 px wide. Falls back to a styled "Walmart ✨" text mark if missing. |

## How to place the logo

1. Obtain an approved PNG of the Walmart logo from the Walmart brand team
   (or the official press kit).
2. Save it as `app/assets/walmart_logo.png`.
3. Restart Streamlit — the brand bar will pick it up automatically.
