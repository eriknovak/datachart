"""The theme faces, fetched from Google Fonts on first use into the local
cache and registered with matplotlib (ADR 0063).

Every face is under the SIL Open Font License; see `FONTS.txt`.
"""

import functools
import pathlib
import urllib.request
import warnings

from matplotlib import font_manager

from .cache import DOWNLOAD_TIMEOUT, cache_dir, write_atomic

# google/fonts publishes no tags, so a commit is the only pin
COMMIT = "e44c4b011a820c2cbe2fd2cfa8052037d7edb571"
SOURCE = "https://raw.githubusercontent.com/google/fonts/" + COMMIT + "/{path}"
# matplotlib face name -> its files upstream
FACES = {
    "IM FELL English": [
        "ofl/imfellenglish/IMFeENrm28P.ttf",
        "ofl/imfellenglish/IMFeENit28P.ttf",
    ],
    "IM FELL English SC": ["ofl/imfellenglishsc/IMFeENsc28P.ttf"],
    "Comic Neue": [
        "ofl/comicneue/ComicNeue-Regular.ttf",
        "ofl/comicneue/ComicNeue-Bold.ttf",
    ],
}


def font_available(name: str) -> bool:
    """Whether matplotlib finds the face, installed or registered."""

    try:
        font_manager.findfont(
            font_manager.FontProperties(family=name), fallback_to_default=False
        )
        return True
    except ValueError:
        return False


def _download(path: str) -> pathlib.Path:
    """One face file in the cache, downloaded unless already there."""

    target = cache_dir() / "fonts" / path.rsplit("/", 1)[-1]
    if not target.exists():
        with urllib.request.urlopen(
            SOURCE.format(path=path), timeout=DOWNLOAD_TIMEOUT
        ) as response:
            content = response.read()
        write_atomic(target, lambda partial: partial.write(content))
    return target


def download_face(name: str) -> list:
    """Every file of the face in the cache; raises `OSError` when one cannot
    be downloaded."""

    return [_download(path) for path in FACES[name]]


@functools.lru_cache(maxsize=None)
def ensure_face(name: str) -> bool:
    """Download and register the face once per process; whether it is now
    available. An unreachable face warns and leaves the stack to its
    fallbacks."""

    if font_available(name):
        return True
    try:
        files = download_face(name)
    except OSError as error:
        return _unavailable(name, error)
    for file in files:
        try:
            font_manager.fontManager.addfont(str(file))
        except (RuntimeError, ValueError) as error:
            # not a font (a proxy's error page, say): fetch it afresh next time
            file.unlink(missing_ok=True)
            return _unavailable(name, error)
    return True


def _unavailable(name: str, error: Exception) -> bool:
    """Warn that the face cannot be used; always False."""

    urls = ", ".join(SOURCE.format(path=path) for path in FACES[name])
    warnings.warn(
        f"Cannot use the {name!r} face from {urls}: {error}. The chart falls "
        f"back to the next face in its stack; once downloaded, the face is "
        f"read from {cache_dir() / 'fonts'}.",
        stacklevel=3,
    )
    return False
