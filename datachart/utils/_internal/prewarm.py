"""Downloads the Natural Earth outlines and the theme faces into the cache
ahead of use.

`fonts` fetches every theme face; each resolution given fetches every feature
Natural Earth publishes at that scale (1:110m when neither is given). Later
renders need no network: an air-gapped machine, a locked-down CI, or this
repository's own builds. The cache folder is `DATACHART_CACHE_DIR`, else
`datachart` under `XDG_CACHE_HOME` or `~/.cache`.

Run from the repo root:
python datachart/utils/_internal/prewarm.py [fonts] [110m 50m 10m]
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from datachart.constants import BASEMAP_RESOLUTION
from datachart.utils._internal.basemap import prewarm
from datachart.utils._internal.cache import cache_dir
from datachart.utils._internal.fonts import FACES, download_face


def main(args):
    resolutions = [arg for arg in args if arg != "fonts"]
    if "fonts" in args:
        for face in FACES:
            download_face(face)
        print(f"fonts: {', '.join(FACES)}")
    if resolutions or "fonts" not in args:
        for resolution in resolutions or [BASEMAP_RESOLUTION.DEFAULT]:
            features = prewarm(resolution)
            print(f"1:{resolution}: {', '.join(features)}")
    print(f"cached in {cache_dir()}")


if __name__ == "__main__":
    main(sys.argv[1:])
