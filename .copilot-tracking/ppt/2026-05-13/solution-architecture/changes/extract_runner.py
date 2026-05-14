"""Lightweight runner for extract_content.py that stubs cairosvg.

The skill's extract_content.py imports cairosvg at module load. On Windows
the native libcairo DLL is not present by default, which makes the import
fail. The source PPTX for this extraction has no SVG images, so cairosvg
is never actually called. This wrapper injects a no-op stub into
sys.modules before importing the real script, then forwards CLI args.
"""

from __future__ import annotations

import runpy
import sys
import types
from pathlib import Path

SCRIPT_PATH = Path(
    r"c:\Users\ropotoc\.vscode\extensions\ise-hve-essentials.hve-core-all-3.3.101"
    r"\.github\skills\experimental\powerpoint\scripts\extract_content.py"
)

stub = types.ModuleType("cairosvg")


def _svg2png(*_args, **_kwargs):  # pragma: no cover - defensive only
    raise RuntimeError(
        "cairosvg is stubbed in this runner. The source PPTX must not "
        "contain SVG images for this extraction path."
    )


stub.svg2png = _svg2png
sys.modules.setdefault("cairosvg", stub)

# Ensure the skill's scripts directory is on sys.path for sibling imports
# (pptx_utils, pptx_colors, etc.).
sys.path.insert(0, str(SCRIPT_PATH.parent))

# Run the script as if invoked directly, forwarding the args we received.
# argv[0] is set to the script path so argparse prog name is preserved.
sys.argv = [str(SCRIPT_PATH), *sys.argv[1:]]
runpy.run_path(str(SCRIPT_PATH), run_name="__main__")
