# coding=utf-8
"""Provide tools for managing and accessing info related to buildable files."""

# Standard library imports:
from pathlib import Path

# Set constants:
TEMPLATES_PATH = Path(__file__).parents[3] / "build_templates"


class PathsManager:
    """Centralize the creation of PathsData containers."""
    __slots__ = ["_year", "_base_path"]

    def __init__(self, year: int, build_base_path: Path):
        self._year = year
        self._base_path = build_base_path

    def get_daily_data(self, day: int) -> "PathsData":
        """Generate a PathsData container for the target day."""
        return PathsData(year=self._year, day=day, build_base_path=self._base_path)


class PathsData:
    """Provide paths, import strings, templates and URLs for a single target day."""
    def __init__(self, year: int, day: int, build_base_path: Path):
        self._year, self._day = year, day
        self._base_path = build_base_path
        self._files_map = self._build_file_paths()
        self._templates_map = self._build_templates()
        assert self._files_map.keys() == self._templates_map.keys()

    def _build_file_paths(self) -> dict[str, Path]:
        """Map the absolute file path of each known buildable file to a name."""
        scripts = self.project_path / "src" / f"aoc{self._year}" / f"day_{self._day}"
        tests = self.project_path / "tests" / f"tests_day_{self._day}"
        return {"input": scripts / "puzzle_input.txt",
                "solution": scripts / "solution.py",
                "tools": scripts / "tools.py",
                "tests_init": tests / "__init__.py",
                "tests": tests / "tests.py"}

    @staticmethod
    def _build_templates() -> dict[str, Path]:
        """Map the absolute template path of each known buildable file to a name."""
        scripts = TEMPLATES_PATH / "day_&@day@&"
        tests = TEMPLATES_PATH / "tests_day_&@day@&"
        return {"input": scripts / "puzzle_input.txt.template",
                "solution": scripts / "solution.py.template",
                "tools": scripts / "tools.py.template",
                "tests_init": tests / "__init__.py.template",
                "tests": tests / "tests.py.template"}

    @property
    def file_paths(self) -> list[Path]:
        """List absolute file paths for all known buildable files."""
        return list(self._files_map.values())

    @property
    def file_templates(self) -> list[Path]:
        """List absolute template paths for all known buildable files."""
        return list(self._templates_map.values())

    @property
    def path_input_from_solution(self) -> str:
        """File path to the target day's input file from the solution's file path."""
        return f'Path(__file__).parent / "puzzle_input.txt"'

    @property
    def path_input_from_tests(self) -> str:
        """File path to the target day's input file from the tests' file path."""
        input_path = self._files_map["input"]
        relative_path = input_path.relative_to(self.project_path)
        return f'Path(__file__).parents[2] / "{relative_path.as_posix()}"'

    @property
    def path_project(self) -> Path:
        """The main path of the built project package."""
        return self._base_path / f"AdventCode{self._year}"

    @property
    def module_day_scripts(self) -> str:
        """Absolute import path for the base module containing the daily scripts."""
        return f"aoc{self._year}.day_{self._day}"

    @property
    def module_solution(self) -> str:
        """Absolute import path to the script module containing the daily solution."""
        return f"{self.module_day_scripts}.solution"

    @property
    def module_tools(self) -> str:
        """Absolute import path to the script module containing the daily tools."""
        return f"{self.module_day_scripts}.tools"

    @property
    def url_advent_puzzle(self) -> str:
        """URL to the Advent of Code web page with the puzzle description."""
        return f"https://adventofcode.com/{self._year}/day/{self._day}"

    @property
    def url_github_solution(self) -> str:
        """URL to the GitHub repository page with the solution script."""
        return f"https://github.com/JaviLunes/AdventCode$year/tree/master" \
               f"/src/aoc{self._year}/day_{self._day}/solution.py"

    @property
    def this_package(self) -> str:
        """The name of this Python package."""
        return "aoc_tools"

    @property
    def project_path(self) -> Path:
        """The main path of the built project package."""
        return self._base_path / f"AdventCode{self._year}"
