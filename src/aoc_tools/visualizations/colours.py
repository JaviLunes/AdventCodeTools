# coding=utf-8
"""Tools for setting and working with plot colours."""

# Standard library imports:
from typing import TypeVar

# Third party imports:
from matplotlib.colors import BASE_COLORS, to_rgb
import numpy


Scalar = TypeVar("Scalar", str, int, float)
RGB = tuple[float, float, float]
RGB255 = tuple[int, int, int]
Colour = str | RGB | RGB255


class ValuePalette:
    """Map scalar values to specific RGB colours."""
    def __init__(self, value_map: dict[Scalar, Colour]):
        self._palette = {v: self._translate_colour(c) for v, c in value_map.items()}

    def __getitem__(self, value: Scalar) -> RGB:
        return self._palette[value]

    @staticmethod
    def _translate_colour(colour: Colour) -> RGB:
        """Translate a compatible colour definition into a RGB value."""
        if isinstance(colour, str):
            return to_rgb(c=colour)
        elif isinstance(colour, tuple) and len(colour) == 3:
            if all(isinstance(v, int) and 0 <= v <= 255 for v in colour):
                return colour[0] / 255, colour[1] / 255, colour[2] / 255
            elif all(isinstance(v, float) and 0 <= v <= 1 for v in colour):
                return colour
        raise ValueError(f"The colour {colour} could not be translated.")

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
