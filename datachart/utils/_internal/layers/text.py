"""The text layer."""

from .base import Layer


# the carrier keeps post-hoc texts on the layer seam (ADR 0018)
class TextLayer(Layer):
    """A carrier for post-hoc text annotations.

    Appended to a figure's panel by `Annotate`; it draws no marks and claims
    no color-cycle slot, legend entry, hatch, orientation, or projection.
    """

    kind = "text"
    projection = None
    takes_color = False

    def __init__(self, texts):
        super().__init__({"texts": texts}, {})

    def draw(self, ax, ctx):
        """No marks; the panel draws the texts with the other annotations."""
