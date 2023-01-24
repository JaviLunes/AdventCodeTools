# coding=utf-8
"""Tools used for building template files for individual advent puzzles."""

# Standard library imports:
from pathlib import Path

# Local application imports:
from aoc_tools.constants import DAILY_MODULE, DAILY_PATH
from aoc_tools.constants import FILE_INPUT, FILE_SOLUTION, FILE_TOOLS, FILE_TESTS
from aoc_tools.constants import PACKAGE_NAME

# Set constants:
TEMPLATES_PATH = Path(__file__).parent / "templates"


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
        for file_path in self._build_file_paths(day=day):
            file_lines = self._prepare_file_lines(file_path=file_path, day=day)
            self._write_file(file_path=file_path, lines=file_lines)

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

    def _build_file_paths(self, day: int) -> list[Path]:
        """Generate absolute paths to all files to be built."""
        return [self.get_source_path_dir(day=day) / FILE_INPUT,
                self.get_source_path_dir(day=day) / FILE_SOLUTION,
                self.get_source_path_dir(day=day) / FILE_TOOLS,
                self._tests / FILE_TESTS.substitute(day=day)]

    def _prepare_file_lines(self, file_path: Path, day: int) -> list[str]:
        """Generate the file lines to include inside the target file path."""
        file_name = file_path.name
        if file_name.startswith("tests"):
            file_name = "tests.py"
        template_file = TEMPLATES_PATH / f"{file_name}.txt"
        with open(template_file, mode="r", encoding="utf-8") as file:
            lines_str = "|".join(file.readlines())
        for mark, value in self.get_replace_map(day=day).items():
            lines_str = lines_str.replace(mark, value)
        return lines_str.split("|")

    def get_source_path_dir(self, day: int) -> Path:
        """Generate an absolute path to the source directory for the target day."""
        return self._source / DAILY_PATH.substitute(year=self.year, day=day)

    def get_replace_map(self, day: int) -> dict[str, str]:
        """Map string marks used in the template files to their matching values."""
        project_path = self.get_source_path_dir(day=day).parent
        input_path = self.get_source_path_dir(day=day) / FILE_INPUT
        day_module = DAILY_MODULE.substitute(year=self.year, day=day)
        return {
            "&@puzzle_name@&": self._puzzles[day - 1],
            "&@this_package@&": PACKAGE_NAME,
            "&@year@&": str(self.year),
            "&@day@&": str(day),
            "&@input_file_rel@&": input_path.relative_to(project_path).as_posix(),
            "&@tools_module@&": f"{day_module}.{FILE_TOOLS.split('.')[0]}"}
