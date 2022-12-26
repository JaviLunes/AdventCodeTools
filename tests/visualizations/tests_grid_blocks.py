# coding=utf-8
"""Tests for the grid-blocks-visualization tools."""

# Standard library imports:
import unittest

# Local application imports:
from aoc_tools.visualizations.grid_blocks import Cell2D, Grid2DPlotter


class Grid2DTests(unittest.TestCase):
    def setUp(self) -> None:
        """Prepare the objects to be used during tests."""
        self.cell_params = [
            (1, 1, 1), (1, 2, 1), (2, 4, 1), (3, 2, 1), (3, 4, 1), (4, 1, 1), (4, 2, 1),
            (4, 5, 1), (2, 2, 1), (2, 3, 1), (5, 2, 1), (5, 3, 1), (5, 4, 1), (5, 5, 1),
            (6, 4, 1), (7, 2, 1), (3, 3, 2), (4, 3, 2), (4, 4, 2)]
        self.palette = {0: "cyan", 1: "red", 2: "orange"}

    def test_plot_default(self):
        """Assert a valid plot can be built providing only the list of cells."""
        cells = [Cell2D(x=x, y=y, value=v) for x, y, v in self.cell_params]
        plotter = Grid2DPlotter(cells=cells)
        plotter.plot_xy()

    def test_non_matching_empty_value(self):
        """Assert the default empty value can be replaced with a custom one."""
        cells = [Cell2D(x=x, y=y, value=v) for x, y, v in self.cell_params]
        plotter = Grid2DPlotter(cells=cells, empty_value=-10)
        plotter.plot_xy()

    def test_string_cell_values(self):
        """Assert cells with string values can be successfully plotted."""
        value_map = {0: "outside", 1: "lava", 2: "pocket"}
        cells = [Cell2D(x=x, y=y, value=value_map[v]) for x, y, v in self.cell_params]
        plotter = Grid2DPlotter(cells=cells, empty_value=value_map[0])
        plotter.plot_xy()

    def test_custom_colour_palette(self):
        """Assert the default value-colour map can be replaced with a custom one."""
        cells = [Cell2D(x=x, y=y, value=v) for x, y, v in self.cell_params]
        plotter = Grid2DPlotter(cells=cells, palette=self.palette)
        plotter.plot_xy()

    def test_hidden_legend(self):
        """Assert the legend can be hidden, and the Axes bbox expands accordingly."""
        cells = [Cell2D(x=x, y=y, value=v) for x, y, v in self.cell_params]
        plotter = Grid2DPlotter(cells=cells, legend=False)
        plotter.plot_xy()
