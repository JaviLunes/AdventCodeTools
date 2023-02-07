# coding=utf-8
"""Provide tools for managing and accessing info related to buildable files."""

# Standard library imports:
from itertools import takewhile
from pathlib import Path

# Set constants:
TEMPLATES_PATH = Path(__file__).parents[3] / "build_templates"
PUZZLE_FILE_NAME_INPUT = "puzzle_input.txt"
PUZZLE_FILE_NAME_SOLUTION = "solution.py"
PUZZLE_FILE_NAME_TESTS = "tests_solution.py"
PUZZLE_FILE_NAME_TOOLS = "tools.py"
PROJECT_FILE_NAME_README = "README.md"


class PathsManager:
    """Provide paths, import strings and URLs required in an Advent of Code project."""
    def __init__(self, build_base_path: Path, year: int, day: int = 1):
        self._year, self._day = year, day
        self._base_path = build_base_path
        self._build_file_paths()
        self._build_templates()
        self._validate_assumptions()

    def _build_replace_map(self) -> dict[str, str]:
        """Create a map of template marks to their values using current year and day."""
        return {"&@year@&": str(self._year), "&@day@&": str(self._day),
                "&@day_z@&": str(self.day_z)}

    def _replace_marks(self, template_str: str) -> str:
        """Replace all '&@X@&' marks in a template string by their matching values."""
        for mark, value in self._build_replace_map().items():
            template_str = template_str.replace(mark, value)
        return template_str

    @staticmethod
    def _explore_template_tree() -> list[Path]:
        """Find all buildable template files nested inside the base template path."""
        return list(TEMPLATES_PATH.rglob(pattern="*.template"))

    def _build_file_paths(self):
        """Map the absolute file path of each known buildable file to a name."""
        paths = self._explore_template_tree()
        paths = [Path(self._replace_marks(template_str=str(p))) for p in paths]
        paths = [p.with_suffix("") for p in paths]
        paths = [self._base_path / p.relative_to(TEMPLATES_PATH) for p in paths]
        self._files_map = {path.name: path for path in paths}

    def _build_templates(self):
        """Map the absolute template path of each known buildable file to a name."""
        self._templates_map = {path.name: path for path in self._explore_template_tree()}

    def _validate_assumptions(self):
        """Assert that all assumptions required by this object are true."""
        self._validate_only_project_path_at_top_of_tree()
        self._validate_only_one_src_directory_in_nested_tree()
        self._validate_scripts_in_src()

    @staticmethod
    def _validate_only_project_path_at_top_of_tree():
        """At the templates' path, there must be only the built project's base path."""
        paths = list(TEMPLATES_PATH.glob("*"))
        assert len(paths) == 1
        assert paths[0].is_dir()

    @staticmethod
    def _validate_only_one_src_directory_in_nested_tree():
        """There must be only one 'src' dir nested inside the templates' base path."""
        paths = list(TEMPLATES_PATH.rglob("src"))
        assert len(paths) == 1
        assert paths[0].is_dir()

    def _validate_scripts_in_src(self):
        """Buildable non-test files must be nested inside a src path."""
        for file_path in self._files_map.values():
            if "tests" not in file_path.parts:
                assert file_path.is_relative_to(self.path_src)

    @property
    def year(self) -> int:
        """Year currently used by this PathsManager."""
        return self._year

    @year.setter
    def year(self, value: int):
        """Change the year currently used by this PathsManager."""
        self._year = value
        self._build_file_paths()

    @property
    def day(self) -> int:
        """Day currently used by this PathsManager."""
        return self._day

    @day.setter
    def day(self, value: int):
        """Change the day currently used by this PathsManager."""
        self._day = value
        self._build_file_paths()

    @property
    def day_z(self) -> str:
        """Leading-zero-filled string version of the target day."""
        return str(self.day).zfill(2)

    @property
    def file_paths(self) -> list[Path]:
        """List absolute file paths for all known buildable files."""
        return list(self._files_map.values())

    @property
    def file_templates(self) -> list[Path]:
        """List absolute template paths for all known buildable files."""
        return list(self._templates_map.values())

    @property
    def path_project(self) -> Path:
        """The main path of the built project package."""
        path = next(TEMPLATES_PATH.glob("*")).relative_to(TEMPLATES_PATH)
        return self._base_path / Path(self._replace_marks(str(path)))

    @property
    def path_src(self) -> Path:
        """The source path of the built project package."""
        path = next(TEMPLATES_PATH.glob("*/src")).relative_to(TEMPLATES_PATH)
        return self._base_path / Path(self._replace_marks(str(path)))

    @property
    def path_readme(self) -> Path:
        """The file path of the built project's README file."""
        path = next(TEMPLATES_PATH.rglob(PROJECT_FILE_NAME_README))
        path = path.relative_to(TEMPLATES_PATH)
        return self._base_path / Path(self._replace_marks(str(path)))

    @property
    def path_input(self) -> Path:
        """The file path of the input file for the daily puzzle."""
        return self._files_map[PUZZLE_FILE_NAME_INPUT]

    @property
    def path_input_from_solution(self) -> str:
        """File path to the target day's input file from the solution's file path."""
        return self._path_target_from_source(
            target_file=self._files_map[PUZZLE_FILE_NAME_INPUT],
            source_file=self._files_map[PUZZLE_FILE_NAME_SOLUTION])

    @property
    def path_input_from_tests(self) -> str:
        """File path to the target day's input file from the tests' file path."""
        return self._path_target_from_source(
            target_file=self._files_map[PUZZLE_FILE_NAME_INPUT],
            source_file=self._files_map[PUZZLE_FILE_NAME_TESTS])

    @staticmethod
    def _path_target_from_source(target_file: Path, source_file: Path) -> str:
        """String path to a target file from inside another source file."""
        shared_parents = list(takewhile(
            lambda pair: pair[0] == pair[1],
            list(zip(target_file.parents[::-1], source_file.parents[::-1]))))
        shared_path = shared_parents[-1][0]
        n_back = max(0, len(source_file.parents) - len(shared_path.parts))
        parents_str = "parent" if n_back == 0 else f"parents[{n_back}]"
        relative_path = target_file.relative_to(shared_path)
        return f'Path(__file__).{parents_str} / "{relative_path.as_posix()}"'

    @property
    def module_solution(self) -> str:
        """Absolute import path to the script module containing the daily solution."""
        file = self._files_map[PUZZLE_FILE_NAME_SOLUTION].relative_to(self.path_src)
        return file.with_suffix("").as_posix().replace("/", ".")

    @property
    def module_tools(self) -> str:
        """Absolute import path to the script module containing the daily tools."""
        file = self._files_map[PUZZLE_FILE_NAME_TOOLS].relative_to(self.path_src)
        return file.with_suffix("").as_posix().replace("/", ".")

    @property
    def url_advent_puzzle(self) -> str:
        """URL to the Advent of Code web page with the puzzle description."""
        return f"https://adventofcode.com/{self.year}/day/{self.day}"

    @property
    def url_advent_input(self) -> str:
        """URL to the Advent of Code web page with the puzzle input data."""
        return self.url_advent_puzzle + "/input"

    @property
    def url_github_solution(self) -> str:
        """URL to the GitHub repository page with the solution script."""
        return f"https://github.com/JaviLunes/AdventCode$year/tree/master" \
               f"/src/aoc{self.year}/day_{self.day_z}/solution.py"

    @property
    def this_package(self) -> str:
        """The name of this Python package."""
        return "aoc_tools"
