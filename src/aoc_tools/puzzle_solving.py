# coding=utf-8
"""Tools used when computing and storing the solutions of advent puzzles."""

# Standard library imports:
from importlib import import_module
from pathlib import Path
from time import time


def read_puzzle_input(input_file: Path) -> list[str]:
    """Read, process and return each line in the input file for the target day."""
    with open(input_file, mode="r") as file:
        lines = [line.removesuffix("\n") for line in file]
    return lines


class AdventSolver:
    """Manage puzzle solving tasks."""
    def __init__(self, year: int, puzzle_names: list[str]):
        self._year = year
        self._puzzles = puzzle_names

    def print_day(self, day: int):
        """Print the solutions and execution time for the target day's puzzles."""
        print(self._puzzles[day - 1])
        solution_1, solution_2, timing = self.solve_day(day=day)
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
        for day in range(1, len(self._puzzles) + 1):
            self.print_day(day=day)

    def solve_day(self, day: int) -> tuple[int | None, int | None, str]:
        """Get the solutions and execution time for the target day's puzzles."""
        try:
            module = import_module(f"aoc{self._year}.day_{day}.solution")
        except ModuleNotFoundError:
            return None, None, ""
        start = time()
        solution_1, solution_2 = module.compute_solution()
        timing = self.format_timing(value=time() - start)
        return solution_1, solution_2, timing

    @staticmethod
    def format_timing(value: float) -> str:
        """Format a time value in seconds into a time string with sensitive units."""
        if value >= 1.5 * 3600:
            return f"{value / 3600:.2f} h"
        elif value >= 1.5 * 60:
            return f"{value / 60:.2f} min"
        elif value <= 1e-4:
            return f"{value * 1e6:.2f} μs"
        elif value <= 1e-1:
            return f"{value * 1e3:.2f} ms"
        else:
            return f"{value:.2f} s"

    @staticmethod
    def parse_timing(value: str) -> float:
        """Convert a time string with sensitive units into a time value in seconds."""
        if value == "-":
            return 0
        value, units = value.split(" ")
        if units == "h":
            return float(value) * 3600
        elif units == "min":
            return float(value) * 60
        elif units == "μs":
            return float(value) / 1e6
        elif units == "ms":
            return float(value) / 1e3
        else:
            return float(value)
