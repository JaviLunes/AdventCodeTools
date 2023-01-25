# coding=utf-8
"""Tools used for building template files for individual advent puzzles."""

# Standard library imports:
from pathlib import Path

# Local application imports:
from aoc_tools.build.paths_manager import PathsManager


class AdventBuilder:
    """Manage template file building tasks."""
    def __init__(self, year: int, puzzle_names: list[str], build_base_path: Path):
        self.year = year
        self.paths = PathsManager(year=year, build_base_path=build_base_path)
        self.puzzles = puzzle_names

    def build_templates(self, day: int):
        """Built input, tools, solving and tests template files for the provided day."""
        for file_path in self._build_file_paths(day=day):
            file_lines = self._prepare_file_lines(file_path=file_path, day=day)
            self.write_file(file_path=file_path, lines=file_lines)

    def build_all_templates(self):
        """Built input, tools, solving and tests template files for all days."""
        for day in range(1, len(self.puzzles) + 1):
            self.build_templates(day=day)

    @staticmethod
    def write_file(file_path: Path, lines: list[str]):
        """Create a new file and write lines, or silently fail if it already exists."""
        if not file_path.exists():
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file=file_path, mode="w") as file:
                file.writelines(lines)

    def _build_file_paths(self, day: int) -> list[Path]:
        """Generate absolute paths to all files to be built."""
        return list(self.paths.build_paths_map(day=day).values())

    def _prepare_file_lines(self, file_path: Path, day: int) -> list[str]:
        """Generate the file lines to include inside the target file path."""
        template_file = self.paths.templates_map[file_path.name]
        with open(template_file, mode="r", encoding="utf-8") as file:
            lines_str = "|".join(file.readlines())
        for mark, value in self.get_replace_map(day=day).items():
            lines_str = lines_str.replace(mark, value)
        return lines_str.split("|")

    def get_replace_map(self, day: int) -> dict[str, str]:
        """Map string marks used in the template files to their matching values."""
        return {
            "&@puzzle_name@&": self.puzzles[day - 1],
            "&@this_package@&": self.paths.this_package,
            "&@year@&": str(self.year),
            "&@day@&": str(day),
            "&@input_from_solution@&": self.paths.get_path_input_from_solution(),
            "&@input_from_tests@&": self.paths.get_path_input_from_tests(day=day),
            "&@tools_module@&": self.paths.build_modules_map(day=day)["tools.py"]}
