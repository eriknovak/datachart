"""The local cache the downloaded data lives in: the basemap outlines and the
theme faces (ADR 0062, 0063)."""

import os
import pathlib
import tempfile
from typing import Callable, IO

CACHE_ENV = "DATACHART_CACHE_DIR"
# 1:10m roads is a 50 MB GeoJSON; 60 s does not finish it (ADR 0062)
DOWNLOAD_TIMEOUT = 300


def cache_dir() -> pathlib.Path:
    """Where the downloaded data is kept."""

    configured = os.environ.get(CACHE_ENV)
    if configured:
        return pathlib.Path(configured)
    base = os.environ.get("XDG_CACHE_HOME") or pathlib.Path.home() / ".cache"
    return pathlib.Path(base) / "datachart"


def write_atomic(path: pathlib.Path, write: Callable[[IO[bytes]], None]) -> None:
    """Write the file through `write`, aside and renamed, so an interrupted
    write leaves no half file."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        dir=path.parent, suffix=path.suffix, delete=False
    ) as partial:
        write(partial)
    os.replace(partial.name, path)
