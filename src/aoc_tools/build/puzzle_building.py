# coding=utf-8
"""Tools used for building template files for individual advent puzzles."""

# Standard library imports:
from pathlib import Path

# Local application imports:
from aoc_tools.constants import DAILY_MODULE, DAILY_PATH
from aoc_tools.constants import FILE_INPUT, FILE_SOLUTION, FILE_TOOLS, FILE_TESTS
from aoc_tools.constants import PACKAGE_NAME


class AdventBuilder:
    """Manage template file building tasks."""
    def __init__(self, year: int, puzzle_names: list[str], source_path: Path,
                 tests_path: Path):
        self.year = year
        self._puzzles = puzzle_names
        self._source = source_path
        self._tests = tests_path

    def build_templates(self, day: int):
        """Built input, tools, solving and tests template files for the provided day."""
        self._write_file(*self._prepare_input(day=day))
        self._write_file(*self._prepare_solution(day=day))
        self._write_file(*self._prepare_tests(day=day))
        self._write_file(*self._prepare_tools(day=day))

    def build_all_templates(self):
        """Built input, tools, solving and tests template files for all days."""
        for day in range(1, len(self._puzzles) + 1):
            self.build_templates(day=day)

    @staticmethod
    def _write_file(file_path: Path, lines: list[str]):
        """Create a new file and write lines, or silently fail if it already exists."""
        if not file_path.exists():
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file=file_path, mode="w") as file:
                file.writelines(lines)

    def _prepare_input(self, day: int) -> tuple[Path, list[str]]:
        """Get file path and content lines for the puzzle input file."""
        return self.get_source_path_dir(day=day) / FILE_INPUT, [""]

    def _prepare_solution(self, day: int) -> tuple[Path, list[str]]:
        """Get file path and content lines for the puzzle-solving script file."""
        file_path = self.get_source_path_dir(day=day) / FILE_SOLUTION
        input_file_rel = f"{file_path.parent.name}/{FILE_INPUT}"
        tools_module = f"{self.get_source_module(day=day)}.{FILE_TOOLS.split('.')[0]}"
        lines = [
            '# coding=utf-8\n',
            f'"""Compute the solution of the {self._puzzles[day - 1]} puzzle."""\n',
            '\n',
            '# Standard library imports:\n',
            'from pathlib import Path\n',
            '\n',
            '# Third party imports:\n',
            f'from {PACKAGE_NAME} import read_puzzle_input\n',
            '\n',
            '# Local application imports:\n',
            f'from {tools_module} import ...\n',
            '\n', '\n',
            'def compute_solution() -> tuple[int, int]:\n',
            '    """Compute the answers for the two parts of this day."""\n',
            f'    input_file = Path(__file__).parents[1] / "{input_file_rel}"\n',
            '    lines = read_puzzle_input(input_file=input_file)\n',
            '    ...\n',
            '    return None, None\n']
        return file_path, lines

    def _prepare_tests(self, day: int) -> tuple[Path, list[str]]:
        """Get file path and content lines for the tool-testing script file."""
        file_path = self.get_tests_path_file(day=day)
        tools_module = f"{self.get_source_module(day=day)}.{FILE_TOOLS.split('.')[0]}"
        lines = [
            '# coding=utf-8\n',
            f'"""Tests for the {self._puzzles[day - 1]} puzzle."""\n',
            '\n',
            '# Standard library imports:\n',
            'import unittest\n',
            '\n',
            '# Local application imports:\n',
            f'from {tools_module} import ...\n',
            '\n', '\n',
            'class ExampleTests(unittest.TestCase):\n',
            '    def setUp(self) -> None:\n',
            '        """Define objects to be tested."""\n',
            '        ...\n']
        return file_path, lines

    def _prepare_tools(self, day: int):
        """Get file path and content lines for the tool module file."""
        file_path = self.get_source_path_dir(day=day) / FILE_TOOLS
        lines = [
            '# coding=utf-8\n',
            f'"""Tools used for solving the {self._puzzles[day - 1]} puzzle."""\n',
            '\n']
        return file_path, lines

    def get_source_path_dir(self, day: int) -> Path:
        """Generate an absolute path to the source directory for the target day."""
        return self._source / DAILY_PATH.substitute(year=self.year, day=day)

    def get_source_module(self, day: int) -> str:
        """Generate a Python import path to the source module for the target day."""
        return DAILY_MODULE.substitute(year=self.year, day=day)

    def get_tests_path_file(self, day: int) -> Path:
        """Generate an absolute path to the tests file for the target day."""
        return self._tests / FILE_TESTS.substitute(day=day)
