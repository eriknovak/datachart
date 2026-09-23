"""Downloads the Natural Earth outlines into the basemap cache ahead of use.

Fetches every feature Natural Earth publishes at each resolution given
(1:110m when none is) and converts it to the arrays the basemap chart reads,
so later renders need no network: an air-gapped machine, a locked-down CI,
or this repository's own builds. The cache folder is `DATACHART_CACHE_DIR`,
else `datachart` under `XDG_CACHE_HOME` or `~/.cache`.

Run from the repo root: python datachart/charts/_basemap/prewarm.py [110m 50m 10m]
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from datachart.constants import BASEMAP_RESOLUTION
from datachart.utils._internal.basemap import cache_dir, prewarm


def main(resolutions):
    for resolution in resolutions or [BASEMAP_RESOLUTION.DEFAULT]:
        features = prewarm(resolution)
        print(f"1:{resolution}: {', '.join(features)}")
    print(f"cached in {cache_dir()}")


if __name__ == "__main__":
    main(sys.argv[1:])
