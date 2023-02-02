# coding=utf-8
"""Tools used for building template files for individual advent puzzles."""

# Standard library imports:
from pathlib import Path

# Local application imports:
from aoc_tools.build.paths_manager import PathsManager, PathsData
from aoc_tools.project_calendar import AdventCalendar

# Define custom types:
ReplaceMap = dict[str, str]


class AdventBuilder:
    """Manage template file building tasks."""
    def __init__(self, year: int, calendar: AdventCalendar, build_base_path: Path):
        self.year = year
        self.paths = PathsManager(year=year, build_base_path=build_base_path)
        self.calendar = calendar

    def build_templates(self, day: int):
        """Built input, tools, solving and tests template files for the provided day."""
        paths_data = self.paths.get_daily_data(day=day)
        replace_map = self._get_replace_map(day=day, paths_data=paths_data)
        zipped = zip(paths_data.file_paths, paths_data.file_templates)
        for file_path, template_file in zipped:
            file_lines = self._prepare_lines(
                template_file=template_file, replace_map=replace_map)
            self.write_file(file_path=file_path, lines=file_lines)

    def build_all_templates(self):
        """Built input, tools, solving and tests template files for all days."""
        for day in range(1, len(self.calendar.puzzle_names) + 1):
            self.build_templates(day=day)

    @staticmethod
    def _prepare_lines(template_file: Path, replace_map: ReplaceMap) -> list[str]:
        """Generate the file lines to include inside the target file path."""
        with open(template_file, mode="r", encoding="utf-8") as file:
            lines_str = "|".join(file.readlines())
        for mark, value in replace_map.items():
            lines_str = lines_str.replace(mark, value)
        return lines_str.split("|")

    def _get_replace_map(self, day: int, paths_data: PathsData) -> ReplaceMap:
        """Map string marks used in the template files to their matching values."""
        return {
            "&@puzzle_name@&": self.calendar.puzzle_names[day - 1],
            "&@this_package@&": paths_data.this_package,
            "&@year@&": str(self.year),
            "&@day@&": str(day),
            "&@input_from_solution@&": paths_data.path_input_from_solution,
            "&@input_from_tests@&": paths_data.path_input_from_tests,
            "&@tools_module@&": paths_data.module_tools}

    @staticmethod
    def write_file(file_path: Path, lines: list[str]):
        """Create a new file and write lines, or silently fail if it already exists."""
        if not file_path.exists():
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file=file_path, mode="w") as file:
                file.writelines(lines)
