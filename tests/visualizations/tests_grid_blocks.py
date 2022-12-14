# coding=utf-8
"""Tests for the grid-blocks-visualization tools."""

# Standard library imports:
import unittest

# Third party imports:
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

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
        fig = plotter._plot_hv(h_coord="x", v_coord="y")
        self.assertIsInstance(fig, Figure)
        fig.show()
        plt.close(fig)

    def test_non_matching_empty_value(self):
        """Assert the default empty value can be replaced with a custom one."""
        cells = [CellND(x=x, y=y, value=v) for x, y, v in self.cell_params]
        plotter = GridNDPlotter(cells=cells, empty_value=-10)
        fig = plotter._plot_hv(h_coord="x", v_coord="y")
        self.assertIsInstance(fig, Figure)
        fig.show()
        plt.close(fig)

    def test_string_cell_values(self):
        """Assert cells with string values can be successfully plotted."""
        value_map = {0: "Alpha", 1: "Beta", 2: "Gamma"}
        cells = [CellND(x=x, y=y, value=value_map[v]) for x, y, v in self.cell_params]
        plotter = GridNDPlotter(cells=cells, empty_value=value_map[0])
        fig = plotter._plot_hv(h_coord="x", v_coord="y")
        self.assertIsInstance(fig, Figure)
        fig.show()
        plt.close(fig)

    def test_custom_colour_palette(self):
        """Assert the default value-colour map can be replaced with a custom one."""
        cells = [CellND(x=x, y=y, value=v) for x, y, v in self.cell_params]
        plotter = GridNDPlotter(cells=cells, palette=self.palette)
        fig = plotter._plot_hv(h_coord="x", v_coord="y")
        self.assertIsInstance(fig, Figure)
        fig.show()
        plt.close(fig)

    def test_hidden_legend(self):
        """Assert the legend can be hidden, and the Axes bbox expands accordingly."""
        cells = [CellND(x=x, y=y, value=v) for x, y, v in self.cell_params]
        plotter = GridNDPlotter(cells=cells, legend=False)
        fig = plotter._plot_hv(h_coord="x", v_coord="y")
        self.assertIsInstance(fig, Figure)
        fig.show()
        plt.close(fig)

    def test_hidden_title(self):
        """Assert the title can be hidden, and the Axes bbox expands accordingly."""
        cells = [CellND(x=x, y=y, value=v) for x, y, v in self.cell_params]
        plotter = GridNDPlotter(cells=cells, title=False)
        fig = plotter._plot_hv(h_coord="x", v_coord="y")
        self.assertIsInstance(fig, Figure)
        fig.show()
        plt.close(fig)

    def test_different_coord_names(self):
        """Assert the names of the HV coordinates may be different from the usual XY."""
        cells = [CellND(n=x, m=y, value=v) for x, y, v in self.cell_params]
        plotter = GridNDPlotter(cells=cells)
        fig = plotter._plot_hv(h_coord="n", v_coord="m")
        self.assertIsInstance(fig, Figure)
        fig.show()
        plt.close(fig)

    def test_annotations_in_cells(self):
        """Assert that annotation texts defined in cells are drawn in the plot."""
        cells = [CellND(x=x, y=y, value=v, annotation=f"{x},{y}")
                 for x, y, v in self.cell_params]
        plotter = GridNDPlotter(cells=cells)
        fig = plotter._plot_hv(h_coord="x", v_coord="y")
        self.assertIsInstance(fig, Figure)
        fig.show()
        plt.close(fig)

    def test_annotations_in_some_cells(self):
        """Assert that annotation texts defined in cells are drawn in the plot."""
        cells = [CellND(x=x, y=y, value=v, annotation=f"{x},{y}" if v == 2 else "")
                 for x, y, v in self.cell_params]
        plotter = GridNDPlotter(cells=cells)
        fig = plotter._plot_hv(h_coord="x", v_coord="y")
        self.assertIsInstance(fig, Figure)
        fig.show()
        plt.close(fig)

    def test_annotations_with_custom_kwargs(self):
        """Assert that drawn annotations use the provided kwargs."""
        cells = [CellND(x=x, y=y, value=v, annotation=f"{x},{y}")
                 for x, y, v in self.cell_params]
        annotations_kwargs = dict(size=10, color="white", ha="left", va="top")
        plotter = GridNDPlotter(cells=cells, annotations_kwargs=annotations_kwargs)
        fig = plotter._plot_hv(h_coord="x", v_coord="y")
        self.assertIsInstance(fig, Figure)
        fig.show()
        plt.close(fig)


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
        fig = plotter.plot_xy()
        self.assertIsInstance(fig, Figure)
        fig.show()
        plt.close(fig)


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

    def test_plot_along_x_level(self):
        """Assert all YZ planes at each X level can be plotted."""
        cells = [CellND(x=x, y=y, z=z, value=v) for x, y, z, v in self.cell_params]
        plotter = Grid3DPlotter(cells=cells)
        for fig in plotter.plot_along_x():
            self.assertIsInstance(fig, Figure)
            fig.show()
            plt.close(fig)

    def test_plot_along_y_level(self):
        """Assert all XZ planes at each Y level can be plotted."""
        cells = [CellND(x=x, y=y, z=z, value=v) for x, y, z, v in self.cell_params]
        plotter = Grid3DPlotter(cells=cells)
        for fig in plotter.plot_along_y():
            self.assertIsInstance(fig, Figure)
            fig.show()
            plt.close(fig)

    def test_plot_along_z_level(self):
        """Assert all XY planes at each Z level can be plotted."""
        cells = [CellND(x=x, y=y, z=z, value=v) for x, y, z, v in self.cell_params]
        plotter = Grid3DPlotter(cells=cells)
        for fig in plotter.plot_along_z():
            self.assertIsInstance(fig, Figure)
            fig.show()
            plt.close(fig)
