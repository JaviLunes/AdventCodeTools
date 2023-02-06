# coding=utf-8
"""Tools for computing the solutions of advent puzzles."""

# Standard library imports:
from collections.abc import Callable
from importlib import import_module
from pathlib import Path
from time import time

# Local application imports:
from aoc_tools.build.paths_manager import PathsManager
from aoc_tools.manage.project_calendar import AdventCalendar

# Define custom types:
SolFunc = Callable[[], tuple[str | None, str | None]]
SolutionsAndTime = tuple[str | None, str | None, float]


def read_puzzle_input(input_file: Path, encoding: str = "utf-8") -> list[str]:
    """Read, process and return each line in the input file for the target day."""
    with open(input_file, mode="r", encoding=encoding) as file:
        lines = [line.removesuffix("\n") for line in file]
    return lines


class AdventSolver:
    """Manage puzzle solving tasks."""
    def __init__(self, calendar: AdventCalendar, paths: PathsManager):
        self.calendar = calendar
        self.paths = paths

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

    def _solve_day(self, day: int) -> SolutionsAndTime:
        """Get the solutions and execution time for the target day's puzzle."""
        self.paths.day = day
        sol_func = self._import_solution_function()
        if sol_func is None:
            return None, None, 0
        return self._solve_and_time(sol_func=sol_func)

    def _import_solution_function(self) -> SolFunc | None:
        """Try to retrieve the solution function for the target day's puzzle."""
        try:
            module = import_module(self.paths.module_solution)
        except ModuleNotFoundError:
            return None
        else:
            return module.compute_solution()

    @staticmethod
    def _solve_and_time(sol_func: SolFunc) -> SolutionsAndTime:
        """Execute and return output and execution time for the provided function."""
        start = time()
        solution_1, solution_2 = sol_func()
        return solution_1, solution_2, time() - start
