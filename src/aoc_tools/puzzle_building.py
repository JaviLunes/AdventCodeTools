# coding=utf-8
"""Shared tools used across different daily puzzles."""

# Standard library imports:
from pathlib import Path


class AdventBuilder:
    """Manage template file building tasks."""
    def __init__(self, year: int, puzzle_names: list[str], puzzles_base_path: Path,
                 tests_base_path: Path):
        self._year = year
        self._puzzles = puzzle_names
        self._puzzles_path = puzzles_base_path
        self._tests_path = tests_base_path

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
        return self._puzzles_path / f"day_{day}" / "puzzle_input.txt", [""]

    def _prepare_solution(self, day: int) -> tuple[Path, list[str]]:
        """Get file path and content lines for the puzzle-solving script file."""
        file_path = self._puzzles_path / f"day_{day}" / "solution.py"
        lines = [
            '# coding=utf-8\n',
            f'"""Compute the solution of the {self._puzzles[day - 1]} puzzle."""\n',
            '\n',
            '# Standard library imports:\n',
            'from pathlib import Path\n',
            '\n',
            '# Local application imports:\n',
            'from aoc_tools import read_puzzle_input\n',
            f'from aoc{self._year}.day_{day}.tools import ...\n',
            '\n', '\n',
            'def compute_solution() -> tuple[int, int]:\n',
            '    """Compute the answers for the two parts of this day."""\n',
            f'    input = Path(__file__).parent / "day_{day}" / "puzzle_input.txt"\n',
            '    lines = read_puzzle_input(input_file=input)\n',
            '    ...\n',
            '    return None, None\n']
        return file_path, lines

    def _prepare_tests(self, day: int) -> tuple[Path, list[str]]:
        """Get file path and content lines for the tool-testing script file."""
        file_path = self._tests_path / f"tests_day_{day}.py"
        lines = [
            '# coding=utf-8\n',
            f'"""Tests for the {self._puzzles[day - 1]} puzzle."""\n',
            '\n',
            '# Standard library imports:\n',
            'import unittest\n',
            '\n',
            '# Local application imports:\n',
            f'from aoc{self._year}.day_{day}.tools import ...\n',
            '\n', '\n',
            'class ExampleTests(unittest.TestCase):\n',
            '    def setUp(self) -> None:\n',
            '        """Define objects to be tested."""\n',
            '        ...\n']
        return file_path, lines

    def _prepare_tools(self, day: int):
        """Get file path and content lines for the tool module file."""
        file_path = self._puzzles_path / f"day_{day}" / "tools.py"
        lines = [
            '# coding=utf-8\n',
            f'"""Tools used for solving the {self._puzzles[day - 1]} puzzle."""\n',
            '\n']
        return file_path, lines
