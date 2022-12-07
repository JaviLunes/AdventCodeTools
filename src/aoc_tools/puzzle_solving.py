# coding=utf-8
"""Tools used when computing and storing the solutions of advent puzzles."""

# Standard library imports:
from importlib import import_module
from pathlib import Path
from time import time

# Third party imports:
import pandas

# Local application imports:
from aoc_tools.constants import MODULE_DAILY_SCRIPT
from aoc_tools.constants import URL_ADVENT_PUZZLE, URL_GITHUB_SCRIPT


def read_puzzle_input(input_file: Path) -> list[str]:
    """Read, process and return each line in the input file for the target day."""
    with open(input_file, mode="r") as file:
        lines = [line.removesuffix("\n") for line in file]
    return lines


class AdventSolver:
    """Manage puzzle solving tasks."""
    def __init__(self, year: int, puzzle_names: list[str]):
        self.year = year
        self.puzzles = puzzle_names

    def print_day(self, day: int):
        """Print the solutions and execution time for the target day's puzzles."""
        print(self.puzzles[day - 1])
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
        for day in range(1, len(self.puzzles) + 1):
            self.print_day(day=day)

    def solve_day(self, day: int) -> tuple[int | None, int | None, str]:
        """Get the solutions and execution time for the target day's puzzles."""
        try:
            module_name = MODULE_DAILY_SCRIPT.substitute(year=self.year, day=day)
            module = import_module(module_name)
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


class AdventCalendar:
    """Manage the puzzle calendar table included in the README.md file."""
    def __init__(self, readme_file: Path, solver: AdventSolver,
                 data: pandas.DataFrame = None):
        self._readme_file = readme_file
        self._solver = solver
        self._table_start = self._find_table_start()
        self.data = data if data is not None else self._load_from_readme()

    def _find_table_start(self) -> int:
        """Locate the first line numbers of the README file's puzzle calendar table."""
        with open(self._readme_file, mode="r") as file:
            lines = file.readlines()
        section_found = True
        for n, line in enumerate(lines):
            if line == "### Puzzle calendar:\n":
                section_found = True
            if section_found and line.startswith("| "):
                return n

    def _load_from_readme(self) -> pandas.DataFrame:
        """Extract available data from the puzzle calendar printed in the README file."""
        lines = self._extract_readme_rows()
        return self._process_readme_rows(raw_rows=lines)

    def _extract_readme_rows(self) -> list[str]:
        """Extract all the puzzle calendar lines printed in the README file."""
        with open(self._readme_file, mode="r", encoding="utf-8") as file:
            lines = file.readlines()
        headers = lines[self._table_start]
        data_lines = lines[self._table_start + 2:self._table_start + 27]
        return [headers] + data_lines

    def _process_readme_rows(self, raw_rows: list[str]) -> pandas.DataFrame:
        """Convert raw calendar lines from the README file into a pandas.DataFrame."""
        rows = [row.removeprefix("|").removesuffix("|\n") for row in raw_rows]
        headers = [r.replace("**", "").strip() for r in rows[0].split("|")]
        data = [[value.strip() for value in row.split("|")] for row in rows[1:]]
        data = [[value if value != "" else "-" for value in row] for row in data]
        df = pandas.DataFrame(data=data, columns=headers)
        df = self._remove_hyper_links(data_frame=df)
        df["Day"] = df["Day"].astype(int)
        return df.set_index(keys="Day")

    @classmethod
    def from_scratch(cls, readme_file: Path, solver: AdventSolver) -> "AdventCalendar":
        """Create a new, empty AdventCalendar, overwriting the one in the README file."""
        empty_df = pandas.DataFrame(
            data="-", columns=["Puzzle", "Stars", "Solution 1", "Solution 2", "Time"],
            index=pandas.RangeIndex(start=1, stop=26, name="Day"))
        calendar = AdventCalendar(data=empty_df, readme_file=readme_file, solver=solver)
        calendar._write_to_readme()
        return calendar

    def register_all_days(self):
        """Add the data for each day's puzzles to the README file's calendar."""
        for day in range(1, len(self._solver.puzzles) + 1):
            self._solve_day(day=day)
        self._write_to_readme()

    def register_day(self, day: int):
        """Add the data for the target day's puzzles to the README file's calendar."""
        self._solve_day(day=day)
        self._write_to_readme()

    def _solve_day(self, day: int):
        """Fill rows with missing solutions or timing values."""
        s1, s2, timing = self._solver.solve_day(day=day)
        self.data.loc[day, "Solution 1"] = s1 or "-"
        self.data.loc[day, "Solution 2"] = s2 or "-"
        self.data.loc[day, "Time"] = timing or "-"
        stars = ":star::star:" if s1 and s2 else ":star:" if s1 or s2 else "-"
        self.data.loc[day, "Stars"] = stars

    def _write_to_readme(self):
        """Replace the calendar table in the README file with the stored one."""
        with open(self._readme_file, mode="r", encoding="utf-8") as file:
            lines = file.readlines()
        lines[self._table_start:self._table_start + 29] = self._table_as_lines()
        with open(self._readme_file, mode="w", encoding="utf-8") as file:
            file.writelines(lines)

    def _table_as_lines(self) -> list[str]:
        """Convert the stored calendar table into text lines."""
        data = self.data.copy(deep=True).reset_index(drop=False)
        total_time = sum(self._solver.parse_timing(value=value) for value in data["Time"])
        total_stars = sum(data["Stars"].str.count(":star:"))
        totals = pandas.DataFrame(data="-", columns=data.columns, index=[0])
        totals.loc[:, "Day"] = "**Totals**"
        totals.loc[:, "Stars"] = f"**{total_stars}**:star:"
        totals.loc[:, "Time"] = f"**{self._solver.format_timing(value=total_time)}**"
        data = self._add_puzzle_names(data_frame=data)
        data = self._add_hyper_links(data_frame=data)
        data = pandas.concat(objs=[data, totals], ignore_index=True)
        data.columns = [f"**{name}**" for name in data.columns]
        text = data.to_markdown(
            index=False, tablefmt="pipe",
            colalign=("center", "left", "center", "center", "center", "center"))
        return (text + "\n").splitlines(keepends=True)

    def _add_puzzle_names(self, data_frame: pandas.DataFrame) -> pandas.DataFrame:
        """Update the puzzle names from the global daily-names map."""
        data_frame["Puzzle"] = [
            name.split(": ")[1] if name != "-" else "-" for name in self._solver.puzzles]
        return data_frame

    def _add_hyper_links(self, data_frame: pandas.DataFrame) -> pandas.DataFrame:
        """Add hyperlinks to puzzle pages and to solution scripts in GitHub."""
        for idx, (day, puzzle, stars, s1, s2, timing) in data_frame.iterrows():
            link_puzzle = URL_ADVENT_PUZZLE.substitute(day=day, year=self._solver.year)
            link_solution = URL_GITHUB_SCRIPT.substitute(day=day, year=self._solver.year)
            data_frame.loc[idx, "Day"] = f"[{day}]({link_puzzle})"
            data_frame.loc[idx, "Puzzle"] = f"[{puzzle}]({link_puzzle})"
            if s1 != "-" or s2 != "-":
                data_frame.loc[idx, "Stars"] = f"[{stars}]({link_solution})"
                data_frame.loc[idx, "Solution 1"] = f"[{s1}]({link_solution})"
                data_frame.loc[idx, "Solution 2"] = f"[{s2}]({link_solution})"
                data_frame.loc[idx, "Time"] = f"[{timing}]({link_solution})"
        return data_frame

    @staticmethod
    def _remove_hyper_links(data_frame: pandas.DataFrame) -> pandas.DataFrame:
        """Remove web hyperlinks for all cells."""
        rx_find, rx_sub = r"^\[(?P<value>.+)]\(.+\)$", r"\g<value>"
        return data_frame.replace(to_replace=rx_find, value=rx_sub, regex=True)
