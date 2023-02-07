# coding=utf-8
"""Tool for reading and writing puzzle names and solution values and times."""

# Third party imports:
import pandas

# Local application imports:
from aoc_tools.build.paths_manager import PathsManager
from aoc_tools.manage.web_scrapper import AdventScrapper


class AdventCalendar:
    """Manage the puzzle calendar table included in the README.md file."""
    def __init__(self, paths: PathsManager, data: pandas.DataFrame = None):
        self.paths = paths
        self.scrapper = AdventScrapper(paths=paths)
        self._table_start = self._find_table_start()
        self._data = data if data is not None else self._load_from_readme()
        self._update_missing_names()

    def _find_table_start(self) -> int:
        """Locate the first line numbers of the README file's puzzle calendar table."""
        section_found = True
        for n, line in enumerate(self._read_readme()):
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
        lines = self._read_readme()
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

    def _update_missing_names(self):
        """Scrap and store missing puzzle names (if possible)."""
        for i, day_name in enumerate(self.puzzle_names):
            if day_name.split(": ")[1] == "-":
                scrapped_name = self.scrapper.scrap_puzzle_name(day=i + 1)
                if scrapped_name is not None:
                    self._data.loc[i + 1, "Puzzle"] = scrapped_name

    @property
    def puzzle_names(self) -> list[str]:
        """List the names (including day numbers) of all the daily puzzles."""
        return [f"Day {i + 1}: {name}" for i, name in enumerate(self._data["Puzzle"])]

    @classmethod
    def from_scratch(cls, paths: PathsManager) -> "AdventCalendar":
        """Create a new, empty AdventCalendar, overwriting the one in the README file."""
        empty_df = pandas.DataFrame(
            data="-", columns=["Puzzle", "Stars", "Solution 1", "Solution 2", "Time"],
            index=pandas.RangeIndex(start=1, stop=26, name="Day"))
        calendar = AdventCalendar(data=empty_df, paths=paths)
        calendar.write_to_readme()
        return calendar

    def update_day(self, day: int, s1: str | None, s2: str | None, timing: float):
        """Fill rows with missing solutions or timing values."""
        self._data.loc[day, "Solution 1"] = s1 or "-"
        self._data.loc[day, "Solution 2"] = s2 or "-"
        self._data.loc[day, "Time"] = timing or "-"
        stars = ":star::star:" if s1 and s2 else ":star:" if s1 or s2 else "-"
        self._data.loc[day, "Stars"] = stars

    def write_to_readme(self):
        """Replace the calendar table in the README file with the stored one."""
        lines = self._read_readme()
        lines[self._table_start:self._table_start + 29] = self._table_as_lines()
        self._write_readme(lines=lines)

    def _read_readme(self) -> list[str]:
        """Open and retrieve all content lines from the README file."""
        with open(self.paths.path_readme, mode="r", encoding="utf-8") as file:
            return file.readlines()

    def _write_readme(self, lines: list[str]):
        """Open and replace all content lines from the README file."""
        with open(self.paths.path_readme, mode="w", encoding="utf-8") as file:
            file.writelines(lines)

    def _table_as_lines(self) -> list[str]:
        """Convert the stored calendar table into text lines."""
        data = self._data.copy(deep=True).reset_index(drop=False)
        total_time = sum(self.parse_timing(value=value) for value in data["Time"])
        total_stars = sum(data["Stars"].str.count(":star:"))
        totals = pandas.DataFrame(data="-", columns=data.columns, index=[0])
        totals.loc[:, "Day"] = "**Totals**"
        totals.loc[:, "Stars"] = f"**{total_stars}**:star:"
        totals.loc[:, "Time"] = f"**{self.format_timing(value=total_time)}**"
        data = self._add_hyper_links(data_frame=data)
        data = pandas.concat(objs=[data, totals], ignore_index=True)
        data.columns = [f"**{name}**" for name in data.columns]
        text = data.to_markdown(
            index=False, tablefmt="pipe",
            colalign=("center", "left", "center", "center", "center", "center"))
        return (text + "\n").splitlines(keepends=True)

    def _add_hyper_links(self, data_frame: pandas.DataFrame) -> pandas.DataFrame:
        """Add hyperlinks to puzzle pages and to solution scripts in GitHub."""
        for idx, (day, puzzle, stars, s1, s2, timing) in data_frame.iterrows():
            self.paths.day = day
            link_puzzle = self.paths.url_advent_puzzle
            link_solution = self.paths.url_github_solution
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