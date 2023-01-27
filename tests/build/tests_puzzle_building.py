# coding=utf-8
"""Tests for the daily-puzzle-building tools."""

# Standard library imports:
from pathlib import Path
import unittest
from unittest import mock
from typing import Callable

# Local application imports:
from aoc_tools.build.puzzle_building import AdventBuilder
from aoc_tools.build.paths_manager import PathsManager

# Set constants:
BUILDER = AdventBuilder(year=3057, build_base_path=Path(r"Z:"),
                        puzzle_names=["Puzzle A", "puzzle B", "C-puzzle"])
PATHS = PathsManager(year=3057, build_base_path=Path(r"Z:"))
N_DAYS = len(BUILDER.puzzles)

# Define custom types:
MockedMap = dict[int, list[tuple[Path, list[str]]]]
FilterLambda = Callable[[tuple[Path, list[str]]], bool]


def mock_build_write() -> MockedMap:
    """Mock-write each file built for a single day, and register its path and lines."""
    mock_kwargs_map = {}
    attr = BUILDER.write_file.__name__
    for day in range(1, N_DAYS + 1):
        with mock.patch.object(target=BUILDER, attribute=attr) as mocked_write:
            BUILDER.build_templates(day=day)
        mock_kwargs_map[day] = [(call.kwargs["file_path"], call.kwargs["lines"])
                                for call in mocked_write.call_args_list]
    return mock_kwargs_map


def filter_mock_map(mock_map: MockedMap, filter_func: FilterLambda) -> MockedMap:
    """Keep the mocked call kwargs of each day that pass a target filter lambda."""
    filtered_map = {}
    for day, values_list in mock_map.items():
        filtered_map[day] = [a for a in values_list if filter_func(a)]
    return filtered_map


class BuildFileInputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Define tools to be tested."""
        cls.mock_map = filter_mock_map(
            mock_map=mock_build_write(),
            filter_func=lambda a: a[0].name == "puzzle_input.txt")

    def test_file_is_written(self):
        """Assert that the target file is written."""
        for i in range(N_DAYS):
            self.assertEqual(1, len(self.mock_map[i + 1]))

    def test_file_path_is_as_expected(self):
        """Assert that the file path matches the expected write path."""
        for i in range(N_DAYS):
            paths_data = PATHS.get_daily_data(day=i + 1)
            file_path, _ = self.mock_map[i + 1][0]
            self.assertIn(file_path, paths_data.file_paths)

    def test_file_is_empty(self):
        """The target file must be created empty."""
        for i in range(N_DAYS):
            _, lines = self.mock_map[i + 1][0]
            self.assertEqual(1, len(lines))
            self.assertEqual("", lines[0])


class BuildFileSolutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Define tools to be tested."""
        cls.mock_map = filter_mock_map(
            mock_map=mock_build_write(),
            filter_func=lambda a: a[0].name == "solution.py")

    def test_file_is_written(self):
        """Assert that the target file is written."""
        for i in range(N_DAYS):
            self.assertEqual(1, len(self.mock_map[i + 1]))

    def test_file_path_is_as_expected(self):
        """Assert that the file path matches the expected write path."""
        for i in range(N_DAYS):
            paths_data = PATHS.get_daily_data(day=i + 1)
            file_path, _ = self.mock_map[i + 1][0]
            self.assertIn(file_path, paths_data.file_paths)

    def test_puzzle_name_on_module_docstring(self):
        """The module docstring must include the full name of the target puzzle."""
        for i in range(N_DAYS):
            _, lines = self.mock_map[i + 1][0]
            expected_name = BUILDER.puzzles[i]
            self.assertIn(expected_name, lines[1])

    def test_this_package_on_third_party_imports(self):
        """The imports from this package are built using the expected module pattern."""
        for i in range(N_DAYS):
            paths_data = PATHS.get_daily_data(day=i + 1)
            _, lines = self.mock_map[i + 1][0]
            expected_name = BUILDER.puzzles[i]
            self.assertIn(expected_name, lines[1])
            expected_import = f"from {paths_data.this_package} import "
            lines_start = lines.index("# Third party imports:\n") + 1
            lines_end = lines.index("\n", lines_start)
            for target_line in lines[lines_start:lines_end]:
                self.assertIn(expected_import, target_line)

    def test_daily_tools_module_on_local_imports(self):
        """The tools module import path is built using the expected module pattern."""
        for i in range(N_DAYS):
            paths_data = PATHS.get_daily_data(day=i + 1)
            _, lines = self.mock_map[i + 1][0]
            module = paths_data.module_tools
            expected_import = f"from {module}"
            lines_start = lines.index("# Local application imports:\n") + 1
            lines_end = lines.index("\n", lines_start)
            target_lines = lines[lines_start:lines_end]
            self.assertTrue(any(expected_import in line for line in target_lines))

    def test_input_file_relative_path(self):
        """Code the input file path and name using the expected path pattern."""
        for i in range(N_DAYS):
            paths_data = PATHS.get_daily_data(day=i + 1)
            _, lines = self.mock_map[i + 1][0]
            expected_path = paths_data.path_input_from_solution
            line_mark = "    input_file = "
            target_line = list(filter(lambda a: a.startswith(line_mark), lines))[0]
            self.assertIn(expected_path, target_line)


class BuildFileToolsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Define tools to be tested."""
        cls.mock_map = filter_mock_map(
            mock_map=mock_build_write(),
            filter_func=lambda a: a[0].name == "tools.py")

    def test_file_is_written(self):
        """Assert that the target file is written."""
        for i in range(N_DAYS):
            self.assertEqual(1, len(self.mock_map[i + 1]))

    def test_file_path_is_as_expected(self):
        """Assert that the file path matches the expected write path."""
        for i in range(N_DAYS):
            paths_data = PATHS.get_daily_data(day=i + 1)
            file_path, _ = self.mock_map[i + 1][0]
            self.assertIn(file_path, paths_data.file_paths)

    def test_puzzle_name_on_module_docstring(self):
        """The module docstring must include the full name of the target puzzle."""
        for i in range(N_DAYS):
            _, lines = self.mock_map[i + 1][0]
            expected_name = BUILDER.puzzles[i]
            self.assertIn(expected_name, lines[1])


class BuildFileTestsInitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Define tools to be tested."""
        cls.mock_map = filter_mock_map(
            mock_map=mock_build_write(),
            filter_func=lambda a: a[0].name == "__init__.py")

    def test_file_is_written(self):
        """Assert that the target file is written."""
        for i in range(N_DAYS):
            self.assertEqual(1, len(self.mock_map[i + 1]))

    def test_file_path_is_as_expected(self):
        """Assert that the file path matches the expected write path."""
        for i in range(N_DAYS):
            paths_data = PATHS.get_daily_data(day=i + 1)
            file_path, _ = self.mock_map[i + 1][0]
            self.assertIn(file_path, paths_data.file_paths)

    def test_puzzle_name_on_module_docstring(self):
        """The module docstring must include the full name of the target puzzle."""
        for i in range(N_DAYS):
            _, lines = self.mock_map[i + 1][0]
            expected_name = BUILDER.puzzles[i]
            self.assertIn(expected_name, lines[1])


class BuildFileTestsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Define tools to be tested."""
        cls.mock_map = filter_mock_map(
            mock_map=mock_build_write(),
            filter_func=lambda a: a[0].name == "tests.py")

    def test_file_is_written(self):
        """Assert that the target file is written."""
        for i in range(N_DAYS):
            self.assertEqual(1, len(self.mock_map[i + 1]))

    def test_file_path_is_as_expected(self):
        """Assert that the file path matches the expected write path."""
        for i in range(N_DAYS):
            paths_data = PATHS.get_daily_data(day=i + 1)
            file_path, _ = self.mock_map[i + 1][0]
            self.assertIn(file_path, paths_data.file_paths)

    def test_puzzle_name_on_module_docstring(self):
        """The module docstring must include the full name of the target puzzle."""
        for i in range(N_DAYS):
            _, lines = self.mock_map[i + 1][0]
            expected_name = BUILDER.puzzles[i]
            self.assertIn(expected_name, lines[1])

    def test_source_daily_module_on_local_imports(self):
        """The local application imports are built using the expected module pattern."""
        for i in range(N_DAYS):
            paths_data = PATHS.get_daily_data(day=i + 1)
            _, lines = self.mock_map[i + 1][0]
            expected_import = f"from {paths_data.module_day_scripts}."
            lines_start = lines.index("# Local application imports:\n") + 1
            lines_end = lines.index("\n", lines_start)
            for file_line in lines[lines_start:lines_end]:
                self.assertIn(expected_import, file_line)

    def test_input_file_relative_path(self):
        """Code the input file path and name using the expected path pattern."""
        for i in range(N_DAYS):
            paths_data = PATHS.get_daily_data(day=i + 1)
            _, lines = self.mock_map[i + 1][0]
            expected_path = paths_data.path_input_from_tests
            line_mark = "        input_file = "
            target_line = list(filter(lambda a: a.startswith(line_mark), lines))[0]
            self.assertIn(expected_path, target_line)
