"""Aggregate fonts, colors, and element types across all slide content YAML files."""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(r"c:\Repos\RetailTeam-workshop\.copilot-tracking\ppt\2026-05-13\solution-architecture\content")

fonts: Counter[str] = Counter()
colors: Counter[str] = Counter()
element_types: Counter[str] = Counter()
shape_types: Counter[str] = Counter()
layouts: Counter[str] = Counter()


def walk(value, parent_key: str = "") -> None:
    if isinstance(value, dict):
        for k, v in value.items():
            walk(v, k)
    elif isinstance(value, list):
        for item in value:
            walk(item, parent_key)
    elif isinstance(value, str):
        if parent_key in {"font", "text_font", "bullet_font"} and value:
            fonts[value] += 1
        if parent_key in {
            "font_color",
            "text_color",
            "color",
            "line_color",
            "fill",
        } and re.fullmatch(r"#[0-9A-Fa-f]{6}", value):
            colors[value.upper()] += 1


for slide_dir in sorted(ROOT.glob("slide-*")):
    yaml_path = slide_dir / "content.yaml"
    if not yaml_path.exists():
        continue
    with yaml_path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        continue
    layouts[str(data.get("layout") or "(none)")] += 1
    for el in data.get("elements", []) or []:
        if not isinstance(el, dict):
            continue
        element_types[str(el.get("type"))] += 1
        if el.get("type") == "shape" and el.get("shape"):
            shape_types[str(el["shape"])] += 1
        walk(el)

print("=== Element types ===")
for k, v in element_types.most_common():
    print(f"  {k}: {v}")

print("\n=== Shape types ===")
for k, v in shape_types.most_common():
    print(f"  {k}: {v}")

print("\n=== Layouts ===")
for k, v in layouts.most_common():
    print(f"  {k}: {v}")

print("\n=== Fonts (count) ===")
for k, v in fonts.most_common():
    print(f"  {k}: {v}")

print("\n=== Colors (count, top 25) ===")
for k, v in colors.most_common(25):
    print(f"  {k}: {v}")
