# coding=utf-8
"""Define the PathsManager tool."""

# Standard library imports:
from pathlib import Path


class PathsManager:
    """Centralize the definition of all built file paths, module names and URLs."""
    __slots__ = ["_year", "_base_path"]

    def __init__(self, year: int, build_base_path: Path):
        self._year = year
        self._base_path = build_base_path

    def get_module_day(self, day: int) -> str:
        """Absolute import path for the base scripts module for the target day."""
        return f"aoc{self._year}.day_{day}"

    def get_module_solution(self, day: int) -> str:
        """Absolute import path for the target day's solution module."""
        return f"{self.get_module_day(day=day)}.solution"

    def get_module_tools(self, day: int) -> str:
        """Absolute import path for the target day's tools module."""
        return f"{self.get_module_day(day=day)}.tools"

    @staticmethod
    def get_module_tests(day: int) -> str:
        """Absolute import path for the target day's tests module."""
        return f"tests.tests_day_{day}"

    def get_path_day(self, day: int) -> Path:
        """Absolute file path for the base scripts directory for the target day."""
        return self.project_path / "src" / f"aoc{self._year}" / f"day_{day}"

    def get_path_input(self, day: int) -> Path:
        """Absolute file path to the target day's input file."""
        return self.get_path_day(day=day) / "puzzle_input.txt"

    @staticmethod
    def get_path_input_from_solution() -> str:
        """File path to the target day's input file from the solution's file path."""
        return f'Path(__file__).parent / "puzzle_input.txt"'

    def get_path_input_from_tests(self, day: int) -> str:
        """File path to the target day's input file from the tests' file path."""
        input_path = self.get_path_input(day=day).relative_to(self.project_path)
        return f'Path(__file__).parents[1] / "{input_path.as_posix()}"'

    def get_path_solution(self, day: int) -> Path:
        """Absolute file path to the target day's solution script."""
        return self.get_path_day(day=day) / "solution.py"

    def get_path_tools(self, day: int) -> Path:
        """Absolute file path to the target day's tools script."""
        return self.get_path_day(day=day) / "tools.py"

    def get_path_tests(self, day: int) -> Path:
        """Absolute file path to the target day's tests script."""
        return self.project_path / "tests" / f"tests_day_{day}.py"

    def get_url_advent_puzzle(self, day: int) -> str:
        """URL to the target day's puzzle description on the Advent of Code website."""
        return f"https://adventofcode.com/{self._year}/day/{day}"

    def get_url_github_solution(self, day: int) -> str:
        """URL to the target day's solution script on the GitHub repository."""
        return f"https://github.com/JaviLunes/AdventCode$year/tree/master" \
               f"/src/aoc{self._year}/day_{day}/solution.py"

    @property
    def this_package(self) -> str:
        """The name of this Python package."""
        return "aoc_tools"

    @property
    def project_path(self) -> Path:
        """The main path of the built project package."""
        return self._base_path / f"AdventCode{self._year}"
