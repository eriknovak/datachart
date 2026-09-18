"""Points nbconvert at this directory so the kernels mkdocs-jupyter starts
pick up `jupyter_nbconvert_config.py` (mkdocs-jupyter exposes no such knob)."""

import os
from pathlib import Path

HOOKS_DIR = str(Path(__file__).resolve().parent)


def on_startup(command, dirty):
    paths = [HOOKS_DIR, os.environ.get("JUPYTER_CONFIG_PATH", "")]
    os.environ["JUPYTER_CONFIG_PATH"] = os.pathsep.join(p for p in paths if p)
