# coding=utf-8
"""Create plots of geometrical regions composed of discrete regular cells."""

# Standard library imports:
from typing import TypeVar

# Third party imports:
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import matplotlib.colors
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Patch
import numpy

# Local application imports:
from aoc_tools.algorithms.grid_blocks import Cell2D


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
                palette[value] = matplotlib.colors.to_rgb(c=colour)
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
        colour_list = iter(matplotlib.colors.BASE_COLORS.values())
        palette = {v: next(colour_list) for v in possible_values}
        return cls(value_map=palette)


class Grid2DPlotter:
    """Create a 2D mosaic-like plot from a list of Cell2D objects."""
    def __init__(self, cells: list[Cell2D], empty_value: Scalar = 0,
                 palette: dict[Scalar, str | RGB] = None, legend: bool = True):
        self._cells = cells
        self._legend = legend
        self._empty_value = empty_value
        self._values = sorted({cell.value for cell in cells} | {empty_value})
        self._palette = self._build_palette(palette=palette)
        self._limits = self._get_coord_limits()

    def _build_palette(self, palette: dict[Scalar, str | RGB] = None) -> ValuePalette:
        """Create a new ValuePalette instance from provided Palette or known values."""
        if palette is None:
            return ValuePalette.from_values(possible_values=self._values)
        return ValuePalette(value_map=palette)

    def _get_coord_limits(self) -> dict[str, tuple[int, int]]:
        """Find the lowest and highest values of the stored cells' coordinates."""
        sorted_x = sorted(self._cells, key=lambda cell: cell.x)
        sorted_y = sorted(self._cells, key=lambda cell: cell.y)
        min_x, max_x = sorted_x[0].x, sorted_x[-1].x
        min_y, max_y = sorted_y[0].y, sorted_y[-1].y
        return dict(x=(min_x, max_x), y=(min_y, max_y))

    def plot_xy(self):
        """Plot the stored cells in a 2D gridded, rectangular region."""
        fig, axe = plt.subplots()
        self._draw_grid_values(axe=axe)
        self._draw_grid_borders(axe=axe)
        self._set_labels(axe=axe)
        if self._legend:
            self._set_legend(fig=fig)
        fig.tight_layout(rect=(0, 0.01, 1, 0.95 if self._legend else 1))
        plt.show()

    def _draw_grid_values(self, axe: Axes):
        """Set the color of each plot's cell by the value of the matching Cell."""
        value_type = type(self._cells[0].value)
        if value_type == str:
            value_type = object
        x_lim, y_lim = self._limits["x"], self._limits["y"]
        shape = y_lim[1] - y_lim[0] + 1, x_lim[1] - x_lim[0] + 1
        cell_array = numpy.full(shape, fill_value=self._empty_value, dtype=value_type)
        for cell in self._cells:
            i, j = self._get_indices(cell=cell)
            cell_array[(i, j)] = cell.value
        rgb_array = self._palette.apply_palette(value_array=cell_array)
        axe.imshow(rgb_array, origin="lower", aspect="equal")

    def _get_indices(self, cell: Cell2D) -> tuple[int, int]:
        """Transform a Cell's XY coordinates into ij indices on a 2D array."""
        i = self._limits["y"][1] - cell.y
        j = cell.x - self._limits["x"][0]
        return i, j

    def _draw_grid_borders(self, axe: Axes):
        """Set the borders of each plotted cell."""
        x_labels, y_labels = self._build_axis_labels()
        axe.set_xlim(-0.5, len(x_labels) - 0.5)
        axe.set_ylim(len(y_labels) - 0.5, -0.5)
        for spine in axe.spines.values():
            spine.set_linewidth(3)
        axe.grid(which="minor", color="black", linewidth=3)

    def _set_labels(self, axe: Axes):
        """Add ticks and text labels to the plot's spines."""
        x_labels, y_labels = self._build_axis_labels()
        axe.tick_params(width=3)
        axe.set_xticks(range(len(x_labels)), labels=x_labels, weight="bold", minor=False)
        axe.set_yticks(range(len(y_labels)), labels=y_labels, weight="bold", minor=False)
        axe.set_xticks(numpy.arange(-0.5, len(x_labels) + 0.5), minor=True)
        axe.set_yticks(numpy.arange(-0.5, len(y_labels) + 0.5), minor=True)
        axe.tick_params(which="minor", length=0)

    def _build_axis_labels(self) -> tuple[list[int], list[int]]:
        """Generate X- and Y-axis tick positions for the plotted region."""
        x_labels = list(range(self._limits["x"][0], self._limits["x"][1] + 1))
        y_labels = list(range(self._limits["y"][0], self._limits["y"][1] + 1))[::-1]
        return x_labels, y_labels

    def _set_legend(self, fig: Figure):
        """Add a legend with drawn cell values."""
        patches = [self._build_legend_patch(value=value) for value in self._values]
        font_properties = FontProperties(weight="bold", size=10)
        legend_bbox = (0, 0.93, 1, 0.06)
        legend = fig.legend(
            handles=patches, labels=self._values, ncols=min(6, len(self._values)),
            loc="center", bbox_to_anchor=legend_bbox, prop=font_properties,
            frameon=True, fancybox=False, edgecolor="black")
        legend.set_in_layout(False)

    def _build_legend_patch(self, value) -> Patch:
        """Create a Patch artist using the palette colour of the provided value."""
        return Patch(facecolor=self._palette[value], edgecolor="black", linewidth=2)
