from ._base import make_theme
from ..typings import StyleAttrs

DEFAULT_THEME: StyleAttrs = make_theme({})
"""The default theme: the package's baseline palette and furniture.

The palette is a softened Okabe–Ito set closed with charcoal, so every pair of
series stays apart for deutan, protan and tritan readers.
"""
