# coding=utf-8
"""Tools for setting and working with plot colours."""

# Standard library imports:
from typing import TypeVar

# Third party imports:
from matplotlib.colors import BASE_COLORS, to_rgb
import numpy


Scalar = TypeVar("Scalar", str, int, float)
RGB = tuple[float, float, float]


class ValuePalette:
    """Map scalar values to specific RGB colours."""
    def __init__(self, value_map: dict[Scalar, str | RGB]):
        self._palette = self._translate_palette(palette=value_map)

    def __getitem__(self, value: Scalar) -> RGB:
        return self._palette[value]

    @staticmethod
    def _translate_palette(palette: dict[Scalar, str | RGB]) -> dict[Scalar, RGB]:
        """Translate possible colour names into tuples of RGB values."""
        for value, colour in palette.items():
            if isinstance(colour, str):
                palette[value] = to_rgb(c=colour)
        return palette

    def apply_palette(self, value_array: numpy.ndarray) -> numpy.ndarray:
        """Transform a nD array with values into a (n+1)D array with a colour channel."""
        shape = (*value_array.shape, 3)
        rgb_array = numpy.ndarray(shape=shape, dtype=float)
        for index, value in numpy.ndenumerate(value_array):
            rgb_array[index] = self._palette[value]
        return rgb_array

    @classmethod
    def from_values(cls, possible_values: list[Scalar]) -> "ValuePalette":
        """Create a new ValuePalette with default colours from all possible values."""
        colour_list = iter(BASE_COLORS.values())
        palette = {v: next(colour_list) for v in possible_values}
        return cls(value_map=palette)
