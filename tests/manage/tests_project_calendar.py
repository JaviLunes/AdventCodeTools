# coding=utf-8
"""Tests for the daily-puzzle-calendar tool."""

# Standard library imports:
from pathlib import Path
import unittest
from unittest import mock

# Local application imports:
from aoc_tools.build.paths_manager import PathsManager
from aoc_tools.manage.project_calendar import AdventCalendar


# noinspection PyProtectedMember
def build_test_calendar(year: int) -> AdventCalendar:
    """Create a new AdventCalendar without triggering read/write/scrap methods."""
    paths = PathsManager(year=year, build_base_path=Path(r"Z:"))
    target = AdventCalendar
    attr_read = target._read_readme.__name__
    attr_write = target._write_readme.__name__
    attr_update = target._update_missing_names.__name__
    lines = ["### Puzzle calendar:\n", "| "]
    with mock.patch.object(target=target, attribute=attr_read, return_value=lines):
        with mock.patch.object(target=target, attribute=attr_write):
            with mock.patch.object(target=target, attribute=attr_update):
                return AdventCalendar.from_scratch(paths=paths)


class UpdateNamesTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define tools to be tested."""
        self.calendar = build_test_calendar(year=2022)
        self.assertListEqual(["-"] * 25, list(self.calendar._data["Puzzle"]))

    def _mock_scrap_update_days(self, scrapped_names: list[str]) -> mock.Mock:
        """Make the AdventCalendar update missing titles, mocking the scrapping."""
        target = self.calendar.scrapper
        attr = target.scrap_puzzle_name.__name__
        with mock.patch.object(target, attribute=attr, side_effect=scrapped_names) \
                as mocked_scrapping:
            self.calendar._update_missing_names()
        return mocked_scrapping

    def test_update_unknown_puzzle_names(self):
        """All non-future days with unknown name must be updated from the web."""
        expected_names = [f"Puzzle {i + 1}" for i in range(25)]
        names = [f"Puzzle {i + 1}" for i in range(25)]
        self._mock_scrap_update_days(scrapped_names=names)
        self.assertListEqual(expected_names, list(self.calendar._data["Puzzle"]))

    def test_keep_unknown_names_if_not_possible_to_get_them(self):
        """For those unknown names that can't be scrapped, the '-' value is kept."""
        expected_names = [f"Puzzle {i + 1}" if i % 2 == 0 else "-" for i in range(25)]
        names = [f"Puzzle {i + 1}" if i % 2 == 0 else None for i in range(25)]
        self._mock_scrap_update_days(scrapped_names=names)
        self.assertListEqual(expected_names, list(self.calendar._data["Puzzle"]))

    def test_do_not_scrap_known_names(self):
        """Avoid requesting and scrapping those names already known."""
        already_known_names = ["Puzzle name" if i % 2 == 0 else "-" for i in range(25)]
        self.calendar._data["Puzzle"] = already_known_names
        names = [f"Puzzle {i + 1}" for i in range(1, 25, 2)]
        mocked_scrapping = self._mock_scrap_update_days(scrapped_names=names)
        requested_days = [call.kwargs["day"] for call in mocked_scrapping.call_args_list]
        self.assertListEqual(list(range(2, 25, 2)), requested_days)
