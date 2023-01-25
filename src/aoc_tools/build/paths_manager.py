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

    def _get_module_day_scripts(self, day: int) -> str:
        """Absolute import path for the base scripts module for the target day."""
        return f"aoc{self._year}.day_{day}"

    @staticmethod
    def _get_module_day_tests(day: int) -> str:
        """Absolute import path for the base tests module for the target day."""
        return f"tests.tests_day_{day}"

    def build_modules_map(self, day: int) -> dict[str, str]:
        """Map the absolute import paths of all buildable modules to their file names."""
        return {
            "solution.py": f"{self._get_module_day_scripts(day=day)}.solution",
            "tools.py": f"{self._get_module_day_scripts(day=day)}.tools",
            "tests.py": f"{self._get_module_day_tests(day=day)}.tests"}

    def _get_path_day_scripts(self, day: int) -> Path:
        """Absolute file path for the base scripts directory for the target day."""
        return self.project_path / "src" / f"aoc{self._year}" / f"day_{day}"

    def _get_path_day_tests(self, day: int) -> Path:
        """Absolute file path for the base tests directory for the target day."""
        return self.project_path / "tests" / f"tests_day_{day}"

    def build_paths_map(self, day: int) -> dict[str, Path]:
        """Map the absolute paths of all buildable files to their file names."""
        return {
            "puzzle_input.txt": self._get_path_day_scripts(day=day) / "puzzle_input.txt",
            "solution.py": self._get_path_day_scripts(day=day) / "solution.py",
            "tools.py": self._get_path_day_scripts(day=day) / "tools.py",
            "tests.py": self._get_path_day_tests(day=day) / "tests.py"}

    @staticmethod
    def get_path_input_from_solution() -> str:
        """File path to the target day's input file from the solution's file path."""
        return f'Path(__file__).parent / "puzzle_input.txt"'

    def get_path_input_from_tests(self, day: int) -> str:
        """File path to the target day's input file from the tests' file path."""
        input_path = self.build_paths_map(day=day)["puzzle_input.txt"]
        relative_path = input_path.relative_to(self.project_path)
        return f'Path(__file__).parents[2] / "{relative_path.as_posix()}"'

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
