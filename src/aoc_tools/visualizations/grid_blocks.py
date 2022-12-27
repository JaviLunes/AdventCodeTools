# coding=utf-8
"""Create plots of geometrical regions composed of discrete regular cells."""

# Standard library imports:
from typing import Iterable, TypeVar

# Third party imports:
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.colors import BASE_COLORS, to_rgb
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Patch
import numpy

# Local application imports:
from aoc_tools.algorithms.grid_blocks import CellND


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


class _GridNDPlotter:
    """Base class for plotting mosaic-like regions composed of regular cells."""
    def __init__(self, cells: list[CellND], empty_value: Scalar = 0,
                 palette: dict[Scalar, str | RGB] = None, legend: bool = True):
        self._cells = cells
        self._legend = legend
        self._empty_value = empty_value
        self._values = sorted({cell.value for cell in cells} | {empty_value})
        self._limits = self._build_coord_limits()
        self._palette = self._build_palette(palette=palette)

    def _build_coord_limits(self) -> dict[str, tuple[int, ...]]:
        """Find the lowest and highest values of the stored cells' coordinates."""
        coord_limits = {}
        coordinates = self._cells[0].coord_map.keys()
        for c in coordinates:
            sorted_c = sorted(self._cells, key=lambda cell: cell.coord_map[c])
            min_c, max_c = sorted_c[0].coord_map[c], sorted_c[-1].coord_map[c]
            coord_limits.update({c: (min_c, max_c)})
        return coord_limits

    def _build_palette(self, palette: dict[Scalar, str | RGB] = None) -> ValuePalette:
        """Create a new ValuePalette instance from provided Palette or known values."""
        if palette is None:
            return ValuePalette.from_values(possible_values=self._values)
        return ValuePalette(value_map=palette)

    def _plot_hv(self, h_coord: str, v_coord: str, **other_coord_values: int):
        """Plot the stored cells along an HV plane."""
        fig, axe = plt.subplots()
        data_array = self._build_2d_array(h=h_coord, v=v_coord, **other_coord_values)
        self._draw_grid_values(axe=axe, data_array=data_array)
        self._draw_grid_borders(axe=axe)
        self._draw_labels(axe=axe, h=h_coord, v=v_coord)
        if self._legend:
            self._draw_legend(fig=fig)
        fig.tight_layout(rect=(0, 0.01, 1, 0.95 if self._legend else 1))
        plt.show()

    def _build_2d_array(self, h: str, v: str, **other_coord_values: int):
        """Prepare a 2D array with values of cells inside the target HV plane."""
        # Build 2D array of empty values:
        value_type = type(self._cells[0].value)
        if value_type == str:
            value_type = object
        shape = self._build_hv_shape(h=h, v=v)
        data_array = numpy.full(shape, fill_value=self._empty_value, dtype=value_type)
        # Add target cells' values to array:
        target_cells = self._build_target_cells(**other_coord_values)
        hv_value_map = self._build_hv_value_map(cells=target_cells, h=h, v=v)
        for index, value in hv_value_map.items():
            data_array[index] = value
        return data_array

    def _draw_grid_values(self, axe: Axes, data_array: numpy.ndarray):
        """Add a 2D square tessellation coloured according to the cell values."""
        rgb_array = self._palette.apply_palette(value_array=data_array)
        axe.imshow(rgb_array, origin="upper", aspect="equal")

    def _build_hv_shape(self, h: str, v: str) -> tuple[int, int]:
        """Prepare the shape of the 2D array to be drawn."""
        h_lim, v_lim = self._limits[h], self._limits[v]
        return v_lim[1] - v_lim[0] + 1, h_lim[1] - h_lim[0] + 1

    def _build_target_cells(self, **other_coord_values: int) -> Iterable[CellND]:
        """Filter in stored cells matching target values of non-HV coordinates."""
        for cell in self._cells:
            for c, value in other_coord_values.items():
                if cell.coord_map[c] != value:
                    continue
            yield cell

    def _build_hv_value_map(self, cells: Iterable[CellND], h: str, v: str) \
            -> dict[tuple[int, int], Scalar]:
        """Prepare a mapping of cell hv coordinates to cell values."""
        max_v, min_h = self._limits[v][1], self._limits[h][0]
        return {(max_v - cell.coord_map[v], cell.coord_map[h] - min_h): cell.value
                for cell in cells}

    @staticmethod
    def _draw_grid_borders(axe: Axes):
        """Add the four edge lines of each plotted cell."""
        [spine.set_linewidth(3) for spine in axe.spines.values()]
        axe.grid(which="minor", color="black", linewidth=3)

    def _draw_labels(self, axe: Axes, h: str, v: str):
        """Add ticks and text labels to the plot's spines."""
        h_labels, v_labels = self._build_hv_labels(h=h, v=v)
        axe.tick_params(width=3)
        axe.set_xticks(range(len(h_labels)), labels=h_labels, weight="bold", minor=False)
        axe.set_yticks(range(len(v_labels)), labels=v_labels, weight="bold", minor=False)
        axe.set_xticks(numpy.arange(-0.5, len(h_labels) + 0.5), minor=True)
        axe.set_yticks(numpy.arange(-0.5, len(v_labels) + 0.5), minor=True)
        axe.tick_params(which="minor", length=0)

    def _build_hv_labels(self, h: str, v: str) -> tuple[list[int], list[int]]:
        """Prepare tick ranges for the horizontal- and vertical-axis."""
        h_labels = list(range(self._limits[h][0], self._limits[h][1] + 1))
        v_labels = list(range(self._limits[v][0], self._limits[v][1] + 1))[::-1]
        return h_labels, v_labels

    def _draw_legend(self, fig: Figure):
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
        """Prepare a Patch artist filled with the palette colour for the target value."""
        return Patch(facecolor=self._palette[value], edgecolor="black", linewidth=2)


class Grid2DPlotter(_GridNDPlotter):
    """Create a 2D mosaic-like plot from a list of XY cell objects."""
    def plot_xy(self):
        """Plot the stored 2D cells in a regular tessellation of squares."""
        self._plot_hv(h_coord="x", v_coord="y")
