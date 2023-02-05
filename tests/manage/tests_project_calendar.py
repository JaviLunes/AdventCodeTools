# coding=utf-8
"""Tests for the daily-puzzle-calendar tool."""

# Standard library imports:
import datetime
from pathlib import Path
import unittest
from unittest import mock

# Local application imports:
from aoc_tools.project_calendar import AdventCalendar
from aoc_tools.build.paths_manager import PathsManager

# Set constants:
YEAR = 2022


class UpdateNamesTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define tools to be tested."""
        self.calendar = self._build_temporary_calendar()
        self.assertListEqual(["-"] * 25, list(self.calendar._data["Puzzle"]))

    @staticmethod
    def _build_temporary_calendar() -> AdventCalendar:
        """Create a new AdventCalendar without triggering undesired methods."""
        project_path = Path(r"Z:")
        paths = PathsManager(year=YEAR, build_base_path=project_path)
        attr_1 = AdventCalendar._find_table_start.__name__
        attr_2 = AdventCalendar.write_to_readme.__name__
        attr_3 = AdventCalendar._update_missing_names.__name__
        with mock.patch.object(target=AdventCalendar, attribute=attr_1):
            with mock.patch.object(target=AdventCalendar, attribute=attr_2):
                with mock.patch.object(target=AdventCalendar, attribute=attr_3):
                    return AdventCalendar.from_scratch(paths=paths)

    def _update_days_with_mocked_connections(self, titles: list[str]) \
            -> tuple[mock.Mock, mock.Mock]:
        """Make the AdventCalendar try to update missing titles, mocking requests."""
        target = self.calendar
        attr_1 = self.calendar._get_page_content.__name__
        attr_2 = self.calendar._scrap_html_text.__name__
        with mock.patch.object(target=target, attribute=attr_1) as mocked_request:
            with mock.patch.object(target, attr_2, side_effect=titles) as mocked_scrap:
                self.calendar._update_missing_names()
        return mocked_request, mocked_scrap

    def test_update_unknown_puzzle_names(self):
        """All non-future days with unknown name must be updated from the web."""
        expected_names = [f"Puzzle {i + 1}" for i in range(25)]
        titles = [f"--- Day {i + 1}: Puzzle {i + 1} ---" for i in range(25)]
        self._update_days_with_mocked_connections(titles=titles)
        self.assertListEqual(expected_names, list(self.calendar._data["Puzzle"]))

    def test_keep_unknown_names_if_not_possible_to_get_them(self):
        """For those unknown names that can't be scrapped, the '-' value is kept."""
        expected_names = [f"Puzzle {i + 1}" if i % 2 == 0 else "-" for i in range(25)]
        titles = [f"--- Day {i + 1}: Puzzle {i + 1} ---" if i % 2 == 0 else None
                  for i in range(25)]
        self._update_days_with_mocked_connections(titles=titles)
        self.assertListEqual(expected_names, list(self.calendar._data["Puzzle"]))

    def test_do_not_scrap_known_names(self):
        """Avoid requesting and scrapping those names already known."""
        names = ["Puzzle name" if i % 2 == 0 else "-" for i in range(25)]
        self.calendar._data["Puzzle"] = names
        titles = [f"--- Day {i + 1}: Puzzle {i + 1} ---" for i in range(1, 25, 2)]
        mocked_request, _ = self._update_days_with_mocked_connections(titles=titles)
        requested_days = [call.kwargs["day"] for call in mocked_request.call_args_list]
        self.assertListEqual(list(range(2, 25, 2)), requested_days)

    def test_do_not_scrap_future_names(self):
        """Avoid requesting and scrapping those names of days not yet published."""
        titles = [f"--- Day {i + 1}: Puzzle {i + 1} ---" for i in range(25)]
        target = self.calendar
        attr = target._get_current_time.__name__
        mocked_dt = datetime.datetime(year=YEAR, month=12, day=15, hour=0)
        with mock.patch.object(target=target, attribute=attr, return_value=mocked_dt):
            mocked_request, _ = self._update_days_with_mocked_connections(titles=titles)
        requested_days = [call.kwargs["day"] for call in mocked_request.call_args_list]
        self.assertListEqual(list(range(1, 16)), requested_days)
