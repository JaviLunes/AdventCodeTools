# coding=utf-8
"""Tests for the daily-puzzle-building tools."""

# Standard library imports:
from pathlib import Path
from string import Template
import unittest
from unittest import mock

# Local application imports:
from aoc_tools.build.puzzle_building import AdventBuilder
from aoc_tools.build.paths_manager import PathsManager

# Set constants:
BUILDER = AdventBuilder(year=3057, puzzle_names=["A", "B"], build_base_path=Path(r"Z:"))
PATHS = PathsManager(year=3057, build_base_path=Path(r"Z:"))
N_DAYS = len(BUILDER.puzzles)


def mock_build_write(day: int) -> dict[str, tuple[Path, list[str]]]:
    """Mock-write each file built for a single day, and register its path and lines."""
    attr = BUILDER.write_file.__name__
    with mock.patch.object(target=BUILDER, attribute=attr) as mocked_write:
        BUILDER.build_templates(day=day)
    return {
        call.kwargs["file_path"].name: (call.kwargs["file_path"], call.kwargs["lines"])
        for call in mocked_write.call_args_list}


class BuildFileInputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Define tools to be tested."""
        cls.file_name = "puzzle_input.txt"
        cls.mock_written_list = [mock_build_write(day=i + 1) for i in range(N_DAYS)]

    def test_file_is_written(self):
        """Assert that the target file is written."""
        for i in range(N_DAYS):
            self.assertIn(self.file_name, self.mock_written_list[i])

    def test_file_path_is_as_expected(self):
        """Assert that the file path matches the expected write path."""
        for i in range(N_DAYS):
            file_path, _ = self.mock_written_list[i][self.file_name]
            expected_path = PATHS.build_paths_map(day=i + 1)[self.file_name]
            self.assertEqual(expected_path, file_path)

    def test_file_is_empty(self):
        """The target file must be created empty."""
        for i in range(N_DAYS):
            _, written_lines = self.mock_written_list[i][self.file_name]
            self.assertEqual(1, len(written_lines))
            self.assertEqual("", written_lines[0])


class BuildFileSolutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Define tools to be tested."""
        cls.file_name = "solution.py"
        cls.mock_written_list = [mock_build_write(day=i + 1) for i in range(N_DAYS)]

    def test_file_is_written(self):
        """Assert that the target file is written."""
        for i in range(N_DAYS):
            self.assertIn(self.file_name, self.mock_written_list[i])

    def test_file_path_is_as_expected(self):
        """Assert that the file path matches the expected write path."""
        for i in range(N_DAYS):
            file_path, _ = self.mock_written_list[i][self.file_name]
            expected_path = PATHS.build_paths_map(day=i + 1)[self.file_name]
            self.assertEqual(expected_path, file_path)

    def test_puzzle_name_on_module_docstring(self):
        """The module docstring must include the full name of the target puzzle."""
        for i in range(N_DAYS):
            _, lines = self.mock_written_list[i][self.file_name]
            expected_name = BUILDER.puzzles[i]
            self.assertIn(expected_name, lines[1])

    def test_this_package_on_third_party_imports(self):
        """The imports from this package are built using the expected module pattern."""
        expected_import = f"from {PATHS.this_package} import "
        for i in range(N_DAYS):
            _, lines = self.mock_written_list[i][self.file_name]
            lines_start = lines.index("# Third party imports:\n") + 1
            lines_end = lines.index("\n", lines_start)
            for target_line in lines[lines_start:lines_end]:
                self.assertIn(expected_import, target_line)

    def test_daily_tools_module_on_local_imports(self):
        """The tools module import path is built using the expected module pattern."""
        for i in range(N_DAYS):
            _, lines = self.mock_written_list[i][self.file_name]
            module = PATHS.build_modules_map(day=i + 1)["tools.py"]
            expected_import = f"from {module}"
            lines_start = lines.index("# Local application imports:\n") + 1
            lines_end = lines.index("\n", lines_start)
            target_lines = lines[lines_start:lines_end]
            self.assertTrue(any(expected_import in line for line in target_lines))

    def test_input_file_relative_path(self):
        """Code the input file path and name using the expected path pattern."""
        for i in range(N_DAYS):
            _, lines = self.mock_written_list[i][self.file_name]
            expected_path = PATHS.get_path_input_from_solution()
            line_mark = "    input_file = "
            target_line = list(filter(lambda a: a.startswith(line_mark), lines))[0]
            self.assertIn(expected_path, target_line)


class BuildFileToolsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Define tools to be tested."""
        cls.file_name = "tools.py"
        cls.mock_written_list = [mock_build_write(day=i + 1) for i in range(N_DAYS)]

    def test_file_is_written(self):
        """Assert that the target file is written."""
        for i in range(N_DAYS):
            self.assertIn(self.file_name, self.mock_written_list[i])

    def test_file_path_is_as_expected(self):
        """Assert that the file path matches the expected write path."""
        for i in range(N_DAYS):
            file_path, _ = self.mock_written_list[i][self.file_name]
            expected_path = PATHS.build_paths_map(day=i + 1)[self.file_name]
            self.assertEqual(expected_path, file_path)

    def test_puzzle_name_on_module_docstring(self):
        """The module docstring must include the full name of the target puzzle."""
        for i in range(N_DAYS):
            _, lines = self.mock_written_list[i][self.file_name]
            expected_name = BUILDER.puzzles[i]
            self.assertIn(expected_name, lines[1])


class BuildFileTestsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Define tools to be tested."""
        cls.file_name = Template("tests.py")
        cls.mock_written_list = [mock_build_write(day=i + 1) for i in range(N_DAYS)]

    def test_file_is_written(self):
        """Assert that the target file is written."""
        for i in range(N_DAYS):
            file_name = self.file_name.substitute(day=i + 1)
            self.assertIn(file_name, self.mock_written_list[i])

    def test_file_path_is_as_expected(self):
        """Assert that the file path matches the expected write path."""
        for i in range(N_DAYS):
            file_name = self.file_name.substitute(day=i + 1)
            file_path, _ = self.mock_written_list[i][file_name]
            expected_path = PATHS.build_paths_map(day=i + 1)[file_name]
            self.assertEqual(expected_path, file_path)

    def test_puzzle_name_on_module_docstring(self):
        """The module docstring must include the full name of the target puzzle."""
        for i in range(N_DAYS):
            file_name = self.file_name.substitute(day=i + 1)
            _, lines = self.mock_written_list[i][file_name]
            expected_name = BUILDER.puzzles[i]
            self.assertIn(expected_name, lines[1])

    def test_source_daily_module_on_local_imports(self):
        """The local application imports are built using the expected module pattern."""
        for i in range(N_DAYS):
            file_name = self.file_name.substitute(day=i + 1)
            _, lines = self.mock_written_list[i][file_name]
            expected_import = f"from {PATHS._get_module_day_scripts(day=i + 1)}."
            lines_start = lines.index("# Local application imports:\n") + 1
            lines_end = lines.index("\n", lines_start)
            for file_line in lines[lines_start:lines_end]:
                self.assertIn(expected_import, file_line)

    def test_input_file_relative_path(self):
        """Code the input file path and name using the expected path pattern."""
        for i in range(N_DAYS):
            file_name = self.file_name.substitute(day=i + 1)
            _, lines = self.mock_written_list[i][file_name]
            expected_path = PATHS.get_path_input_from_tests(day=i + 1)
            line_mark = "        input_file = "
            target_line = list(filter(lambda a: a.startswith(line_mark), lines))[0]
            self.assertIn(expected_path, target_line)
