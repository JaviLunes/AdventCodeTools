# coding=utf-8
"""Tools for computing the solutions of advent puzzles."""

# Standard library imports:
from importlib import import_module
from pathlib import Path
from time import time

# Local application imports:
from aoc_tools.build.paths_manager import PathsManager
from aoc_tools.project_calendar import AdventCalendar


def read_puzzle_input(input_file: Path, encoding: str = "utf-8") -> list[str]:
    """Read, process and return each line in the input file for the target day."""
    with open(input_file, mode="r", encoding=encoding) as file:
        lines = [line.removesuffix("\n") for line in file]
    return lines


class AdventSolver:
    """Manage puzzle solving tasks."""
    def __init__(self, year: int, calendar: AdventCalendar, build_base_path: Path):
        self.paths = PathsManager(year=year, build_base_path=build_base_path)
        self.calendar = calendar

    def print_day(self, day: int):
        """Print the solutions and execution time for the target day's puzzles."""
        print(self.calendar.puzzle_names[day - 1])
        solution_1, solution_2, timing = self._solve_day(day=day)
        timing = self.calendar.format_timing(value=timing)
        if solution_1 is None:
            print("    The first puzzle remains unsolved!")
        else:
            print(f"    The first solution is {solution_1}.")
        if solution_2 is None:
            print("    The second puzzle remains unsolved!")
        else:
            print(f"    The second solution is {solution_2}.")
        if solution_1 is not None or solution_2 is not None:
            print(f"    This took {timing}.")

    def print_all_days(self):
        """Print the solutions and execution times for each day's puzzles."""
        for day in range(1, len(self.calendar.puzzle_names) + 1):
            self.print_day(day=day)

    def register_day(self, day: int):
        """Add the data for the target day's puzzles to the README file's calendar."""
        s1, s2, timing = self._solve_day(day=day)
        self.calendar.update_day(day=day, s1=s1, s2=s2, timing=timing)
        self.calendar.write_to_readme()

    def register_all_days(self):
        """Add the data for each day's puzzles to the README file's calendar."""
        for day in range(1, len(self.calendar.puzzle_names) + 1):
            s1, s2, timing = self._solve_day(day=day)
            self.calendar.update_day(day=day, s1=s1, s2=s2, timing=timing)
        self.calendar.write_to_readme()

    def _solve_day(self, day: int) -> tuple[str | None, str | None, float]:
        """Get the solutions and execution time for the target day's puzzles."""
        paths_data = self.paths.get_daily_data(day=day)
        try:
            module = import_module(paths_data.module_solution)
        except ModuleNotFoundError:
            return None, None, 0
        start = time()
        solution_1, solution_2 = module.compute_solution()
        return solution_1, solution_2, time() - start
