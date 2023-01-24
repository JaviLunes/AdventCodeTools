# coding=utf-8
"""Tests for the daily-puzzle-building tools."""

# Standard library imports:
from pathlib import Path
import unittest

# Local application imports:
from aoc_tools.build.puzzle_building import AdventBuilder
from aoc_tools.constants import PACKAGE_NAME, DAILY_MODULE, DAILY_PATH
from aoc_tools.constants import FILE_INPUT, FILE_SOLUTION, FILE_TOOLS, FILE_TESTS

# Set constants:
PUZZLE_NAMES = ["Puzzle A", "Puzzle B", "Puzzle C"]
PATH_SOURCE = Path(r"Z:\AoC\src")
PATH_TESTS = Path(r"Z:\AoC\tests")
YEAR = 3057


class FilePathTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define tools to be tested."""
        builder = AdventBuilder(year=YEAR, puzzle_names=PUZZLE_NAMES,
                                source_path=PATH_SOURCE, tests_path=PATH_TESTS)
        self.paths_map = {day: builder._build_file_paths(day=day)
                          for day in range(1, len(PUZZLE_NAMES) + 1)}

    def test_input_path(self):
        """The path for the input file must match the expected path pattern."""
        for i in range(len(PUZZLE_NAMES)):
            day_path = DAILY_PATH.substitute(year=YEAR, day=i + 1)
            expected_path = PATH_SOURCE / day_path / FILE_INPUT
            file_path = self.paths_map[i + 1][0]
            self.assertEqual(expected_path, file_path)

    def test_solution_path(self):
        """The path for the solution file must match the expected path pattern."""
        for i in range(len(PUZZLE_NAMES)):
            day_path = DAILY_PATH.substitute(year=YEAR, day=i + 1)
            expected_path = PATH_SOURCE / day_path / FILE_SOLUTION
            file_path = self.paths_map[i + 1][1]
            self.assertEqual(expected_path, file_path)

    def test_tools_path(self):
        """The path for the tools file must match the expected path pattern."""
        for i in range(len(PUZZLE_NAMES)):
            day_path = DAILY_PATH.substitute(year=YEAR, day=i + 1)
            expected_path = PATH_SOURCE / day_path / FILE_TOOLS
            file_path = self.paths_map[i + 1][2]
            self.assertEqual(expected_path, file_path)

    def test_tests_path(self):
        """The path for the tests file must match the expected path pattern."""
        for i in range(len(PUZZLE_NAMES)):
            expected_path = PATH_TESTS / FILE_TESTS.substitute(day=i + 1)
            file_path = self.paths_map[i + 1][3]
            self.assertEqual(expected_path, file_path)


class InputTemplateTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define tools to be tested."""
        builder = AdventBuilder(year=YEAR, puzzle_names=PUZZLE_NAMES,
                                source_path=PATH_SOURCE, tests_path=PATH_TESTS)
        self.lines_map = {
            day: builder._prepare_file_lines(file_path=Path(FILE_INPUT), day=day)
            for day in range(1, len(PUZZLE_NAMES) + 1)}

    def test_empty_file(self):
        """The input file is created empty."""
        for i, puzzle_name in enumerate(PUZZLE_NAMES):
            file_lines = self.lines_map[i + 1]
            self.assertEqual(1, len(file_lines))
            self.assertEqual(0, len(file_lines[0]))


class SolutionTemplateTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define tools to be tested."""
        builder = AdventBuilder(year=YEAR, puzzle_names=PUZZLE_NAMES,
                                source_path=PATH_SOURCE, tests_path=PATH_TESTS)
        self.lines_map = {
            day: builder._prepare_file_lines(file_path=Path(FILE_SOLUTION), day=day)
            for day in range(1, len(PUZZLE_NAMES) + 1)}

    def test_puzzle_name_on_module_docstring(self):
        """The module docstring must include the full name of the target puzzle."""
        for i, puzzle_name in enumerate(PUZZLE_NAMES):
            file_line = self.lines_map[i + 1][1]
            self.assertIn(puzzle_name, file_line)

    def test_this_package_on_third_party_imports(self):
        """The imports from this package are built using the expected module pattern."""
        for i in range(len(PUZZLE_NAMES)):
            expected_import = f"from {PACKAGE_NAME} import "
            file_lines = self.lines_map[i + 1]
            lines_start = file_lines.index("# Third party imports:\n") + 1
            lines_end = file_lines.index("\n", lines_start)
            for file_line in file_lines[lines_start:lines_end]:
                self.assertIn(expected_import, file_line)

    def test_daily_tools_module_on_local_imports(self):
        """The tools module import path is built using the expected module pattern."""
        for i in range(len(PUZZLE_NAMES)):
            source_module = DAILY_MODULE.substitute(year=YEAR, day=i + 1)
            expected_import = f"from {source_module}.{FILE_TOOLS.split('.')[0]}"
            file_lines = self.lines_map[i + 1]
            lines_start = file_lines.index("# Local application imports:\n") + 1
            lines_end = file_lines.index("\n", lines_start)
            target_lines = file_lines[lines_start:lines_end]
            self.assertTrue(any(expected_import in line for line in target_lines))

    def test_input_file_relative_path(self):
        """Code the input file path and name using the expected path pattern."""
        for i in range(len(PUZZLE_NAMES)):
            file_lines = self.lines_map[i + 1]
            day_path_rel = Path(DAILY_PATH.substitute(year=YEAR, day=i + 1)).name
            line_mark = "    input_file = "
            file_line = list(filter(lambda a: a.startswith(line_mark), file_lines))[0]
            self.assertIn(f"{day_path_rel}/{FILE_INPUT}", file_line)


class ToolTemplateTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define tools to be tested."""
        builder = AdventBuilder(year=YEAR, puzzle_names=PUZZLE_NAMES,
                                source_path=PATH_SOURCE, tests_path=PATH_TESTS)
        self.lines_map = {
            day: builder._prepare_file_lines(file_path=Path(FILE_TOOLS), day=day)
            for day in range(1, len(PUZZLE_NAMES) + 1)}

    def test_puzzle_name_on_module_docstring(self):
        """The module docstring must include the full name of the target puzzle."""
        for i, puzzle_name in enumerate(PUZZLE_NAMES):
            file_line = self.lines_map[i + 1][1]
            self.assertIn(puzzle_name, file_line)


class TestsTemplateTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define tools to be tested."""
        builder = AdventBuilder(year=YEAR, puzzle_names=PUZZLE_NAMES,
                                source_path=PATH_SOURCE, tests_path=PATH_TESTS)
        self.lines_map = {
            day: builder._prepare_file_lines(
                file_path=Path(FILE_TESTS.substitute(day=day)), day=day)
            for day in range(1, len(PUZZLE_NAMES) + 1)}

    def test_puzzle_name_on_module_docstring(self):
        """The module docstring must include the full name of the target puzzle."""
        for i, puzzle_name in enumerate(PUZZLE_NAMES):
            file_line = self.lines_map[i + 1][1]
            self.assertIn(puzzle_name, file_line)

    def test_source_daily_module_on_local_imports(self):
        """The local application imports are built using the expected module pattern."""
        for i in range(len(PUZZLE_NAMES)):
            expected_import = f"from {DAILY_MODULE.substitute(year=YEAR, day=i + 1)}."
            file_lines = self.lines_map[i + 1]
            lines_start = file_lines.index("# Local application imports:\n") + 1
            lines_end = file_lines.index("\n", lines_start)
            for file_line in file_lines[lines_start:lines_end]:
                self.assertIn(expected_import, file_line)
