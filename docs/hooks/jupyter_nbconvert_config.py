"""nbconvert config for the docs notebooks, loaded via `nbconvert_config.py`.

ipykernel 7.3 warns on every kernel start that TCP transport is unencrypted;
IPC transport avoids the warning and the network round trip. jupyter_client's
CurveZMQ provisioning (the other remedy) fails on 8.9 with a bytes/str error.
"""

import os
import sys

from jupyter_core.paths import jupyter_runtime_dir

c = get_config()  # noqa: F821 - injected by the traitlets config loader

# libzmq has no IPC transport on Windows
if sys.platform != "win32":
    c.KernelManager.transport = "ipc"
    # absolute socket prefix: the kernel runs in the notebook's directory and
    # the client in the repo root, so the relative default never connects
    c.KernelManager.ip = os.path.join(jupyter_runtime_dir(), "kernel-ipc")
