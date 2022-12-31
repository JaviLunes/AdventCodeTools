# coding=utf-8
"""Tests for the grid-blocks-visualization tools."""

# Standard library imports:
import unittest

# Local application imports:
from aoc_tools.visualizations.grid_blocks import CellND, GridNDPlotter
from aoc_tools.visualizations.grid_blocks import Grid2DPlotter, Grid3DPlotter


class BaseFeaturesTests(unittest.TestCase):
    def setUp(self) -> None:
        """Prepare the objects to be used during tests."""
        self.cell_params = [
            (1, 1, 1), (1, 2, 1), (2, 4, 1), (3, 2, 1), (3, 4, 1), (4, 1, 1), (4, 2, 1),
            (4, 5, 1), (2, 2, 1), (2, 3, 1), (5, 2, 1), (5, 3, 1), (5, 4, 1), (5, 5, 1),
            (6, 4, 1), (7, 2, 1), (3, 3, 2), (4, 3, 2), (4, 4, 2)]
        self.palette = {0: "cyan", 1: "red", 2: "orange"}

    def test_plot_default(self):
        """Assert a valid plot can be built providing only the list of cells."""
        cells = [CellND(x=x, y=y, value=v) for x, y, v in self.cell_params]
        plotter = GridNDPlotter(cells=cells)
        plotter._plot_hv(h_coord="x", v_coord="y")

    def test_non_matching_empty_value(self):
        """Assert the default empty value can be replaced with a custom one."""
        cells = [CellND(x=x, y=y, value=v) for x, y, v in self.cell_params]
        plotter = GridNDPlotter(cells=cells, empty_value=-10)
        plotter._plot_hv(h_coord="x", v_coord="y")

    def test_string_cell_values(self):
        """Assert cells with string values can be successfully plotted."""
        value_map = {0: "Alpha", 1: "Beta", 2: "Gamma"}
        cells = [CellND(x=x, y=y, value=value_map[v]) for x, y, v in self.cell_params]
        plotter = GridNDPlotter(cells=cells, empty_value=value_map[0])
        plotter._plot_hv(h_coord="x", v_coord="y")

    def test_custom_colour_palette(self):
        """Assert the default value-colour map can be replaced with a custom one."""
        cells = [CellND(x=x, y=y, value=v) for x, y, v in self.cell_params]
        plotter = GridNDPlotter(cells=cells, palette=self.palette)
        plotter._plot_hv(h_coord="x", v_coord="y")

    def test_hidden_legend(self):
        """Assert the legend can be hidden, and the Axes bbox expands accordingly."""
        cells = [CellND(x=x, y=y, value=v) for x, y, v in self.cell_params]
        plotter = GridNDPlotter(cells=cells, legend=False)
        plotter._plot_hv(h_coord="x", v_coord="y")

    def test_different_coord_names(self):
        """Assert the names of the HV coordinates may be different from the usual XY."""
        cells = [CellND(n=x, m=y, value=v) for x, y, v in self.cell_params]
        plotter = GridNDPlotter(cells=cells)
        plotter._plot_hv(h_coord="n", v_coord="m")


class Grid2DTests(unittest.TestCase):
    def setUp(self) -> None:
        """Prepare the objects to be used during tests."""
        self.cell_params = [
            (1, 1, 1), (1, 2, 1), (2, 4, 1), (3, 2, 1), (3, 4, 1), (4, 1, 1), (4, 2, 1),
            (4, 5, 1), (2, 2, 1), (2, 3, 1), (5, 2, 1), (5, 3, 1), (5, 4, 1), (5, 5, 1),
            (6, 4, 1), (7, 2, 1), (3, 3, 2), (4, 3, 2), (4, 4, 2)]

    def test_plot_xy(self):
        """Assert the X and Y coordinates are used as HV plot coordinates."""
        cells = [CellND(x=x, y=y, value=v) for x, y, v in self.cell_params]
        plotter = Grid2DPlotter(cells=cells)
        plotter.plot_xy()


class Grid3DTests(unittest.TestCase):
    def setUp(self) -> None:
        """Prepare the objects to be used during tests."""
        self.cell_params = [
            # Level -2:
            (4, 3, -2, 1), (4, 4, -2, 1),
            # Level -1:
            (3, 3, -1, 1), (3, 4, -1, 1), (4, 2, -1, 1), (4, 3, -1, 2), (4, 4, -1, 2),
            (4, 5, -1, 1), (5, 3, -1, 1), (5, 4, -1, 1),
            # Level 0:
            (1, 1, 0, 1), (1, 2, 0, 1), (2, 2, 0, 1), (2, 3, 0, 1), (2, 4, 0, 1),
            (3, 2, 0, 1), (3, 3, 0, 2), (3, 4, 0, 1), (4, 1, 0, 1), (4, 2, 0, 1),
            (4, 3, 0, 2), (4, 4, 0, 2), (4, 5, 0, 1), (5, 2, 0, 1), (5, 3, 0, 1),
            (5, 4, 0, 1), (5, 5, 0, 1), (6, 4, 0, 1), (7, 2, 0, 1),
            # Level 1:
            (3, 3, 1, 1), (4, 3, 1, 2), (4, 4, 1, 1), (7, 2, 1, 1),
            # Level 2:
            (4, 3, 2, 1), (7, 2, 2, 2)]

    def test_plot_xy_at_z_levels(self):
        """Assert the XY planes at different Z levels can be plotted."""
        cells = [CellND(x=x, y=y, z=z, value=v) for x, y, z, v in self.cell_params]
        plotter = Grid3DPlotter(cells=cells)
        plotter.plot_xy(z=-2)
        plotter.plot_xy(z=-1)
        plotter.plot_xy(z=0)
        plotter.plot_xy(z=1)
        plotter.plot_xy(z=2)
