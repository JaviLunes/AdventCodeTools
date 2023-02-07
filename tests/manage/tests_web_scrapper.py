# coding=utf-8
"""Tests for the Advent-web-scrapping tool."""

# Standard library imports:
import datetime
import http
from pathlib import Path
import unittest
from unittest import mock

# Third party imports:
import responses

# Local application imports:
from aoc_tools.build.paths_manager import PathsManager
from aoc_tools.manage.web_scrapper import AdventScrapper, ScrapError

# Set constants:
DATA_PATH = Path(__file__).parent / "data"


class ScrapTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define tools to be tested."""
        past_year = datetime.date.today().year - 1
        self.paths = PathsManager(year=past_year, build_base_path=Path(r"Z:"))
        self.scrapper = AdventScrapper(paths=self.paths)

    def test_avoid_requesting_future_date(self):
        """If target date is future, do not make any request, and return None."""
        mocked_now = datetime.datetime(self.paths.year - 1, 12, self.paths.day)
        target, attr_1 = self.scrapper, self.scrapper._get_current_time.__name__
        attr_2 = self.scrapper._get_page_content.__name__
        with mock.patch.object(target=target, attribute=attr_1, return_value=mocked_now):
            with mock.patch.object(target=target, attribute=attr_2) as mocked_request:
                output = self.scrapper._scrap(target_url="", parse_func=mock.Mock())
        self.assertFalse(mocked_request.called)
        self.assertIsNone(output)

    @responses.activate
    def test_avoid_parsing_responses_with_non_200_status(self):
        """If the response's status is not 200, return None instead of parsing it."""
        target_url = "http://mocked_url.mock"
        non_ok_codes = [int(code) for code in http.HTTPStatus if code != 200]
        for code in non_ok_codes:
            responses.get(url=target_url, status=code)
            mocked_parse = mock.Mock()
            output = self.scrapper._scrap(target_url=target_url, parse_func=mocked_parse)
            self.assertIsNone(output)
            self.assertFalse(mocked_parse.called)

    @responses.activate
    def test_return_none_on_failed_content_parsing(self):
        """If the content-parsing method raises an ScrapError, return None."""
        target_url = "http://mocked_url.mock"
        responses.get(url=target_url)
        mocked_parse = mock.Mock(side_effect=ScrapError)
        output = self.scrapper._scrap(target_url=target_url, parse_func=mocked_parse)
        self.assertTrue(mocked_parse.called)
        self.assertIsNone(output)


class ParsePuzzleNameTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define tools to be tested."""
        past_year = datetime.date.today().year - 1
        self.paths = PathsManager(year=past_year, build_base_path=Path(r"Z:"))
        self.scrapper = AdventScrapper(paths=self.paths)

    def test_parse_puzzle_name_2022_1(self):
        """Verify that the correct puzzle name is extracted from the web page."""
        self.paths.day = 1
        with open(DATA_PATH / "web_puzzle_2022_01.html", mode="rb") as web_page:
            content = web_page.read()
        parsed_name = self.scrapper._parse_web_puzzle_name(web_content=content)
        self.assertEqual("Calorie Counting", parsed_name)

    def test_parse_puzzle_name_2021_2(self):
        """Verify that the correct puzzle name is extracted from the web page."""
        self.paths.day = 2
        with open(DATA_PATH / "web_puzzle_2021_02.html", mode="rb") as web_page:
            content = web_page.read()
        parsed_name = self.scrapper._parse_web_puzzle_name(web_content=content)
        self.assertEqual("Dive!", parsed_name)

    def test_fail_if_title_does_not_match_regex(self):
        """If the parsed title doesn't fit in the regex, raise an error."""
        self.paths.day = 1
        with open(DATA_PATH / "web_puzzle_2022_01.html", mode="rb") as web_page:
            content = web_page.read()
        content = content.replace(b"--- Day 1: Calorie Counting ---", b"Mocked Title!")
        with self.assertRaises(ScrapError):
            self.scrapper._parse_web_puzzle_name(web_content=content)

    def test_fail_if_title_day_does_not_match_target_day(self):
        """If the day in the parsed title doesn't match the target, raise an error."""
        self.paths.day = 2
        with open(DATA_PATH / "web_puzzle_2022_01.html", mode="rb") as web_page:
            content = web_page.read()
        with self.assertRaises(ScrapError):
            self.scrapper._parse_web_puzzle_name(web_content=content)


class ParsePuzzleInputTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define tools to be tested."""
        past_year = datetime.date.today().year - 1
        self.paths = PathsManager(year=past_year, build_base_path=Path(r"Z:"))
        self.scrapper = AdventScrapper(paths=self.paths)

    def test_keep_leading_white_spaces_on_first_line(self):
        """Verify that the first parsed line hasn't lost any leading white space."""
        with open(DATA_PATH / "puzzle_input_2022_05_cut.txt", mode="r") as text_file:
            expected_lines = text_file.readlines()
        with open(DATA_PATH / "web_input_2022_05_cut.html", mode="rb") as web_page:
            content = web_page.read()
        scrapped_lines = self.scrapper._parse_web_puzzle_input(web_content=content)
        self.assertListEqual(expected_lines, scrapped_lines)

    def test_keep_intermediate_empty_line(self):
        """Verify that all empty lines (except the last one) are not removed."""
        with open(DATA_PATH / "puzzle_input_2022_22_cut.txt", mode="r") as text_file:
            expected_lines = text_file.readlines()
        with open(DATA_PATH / "web_input_2022_22_cut.html", mode="rb") as web_page:
            content = web_page.read()
        scrapped_lines = self.scrapper._parse_web_puzzle_input(web_content=content)
        self.assertListEqual(expected_lines, scrapped_lines)

    def test_remove_last_empty_line(self):
        """Verify that the last parsed line is not an empty line."""
        with open(DATA_PATH / "puzzle_input_2021_06_cut.txt", mode="r") as text_file:
            expected_lines = text_file.readlines()
        with open(DATA_PATH / "web_input_2021_06_cut.html", mode="rb") as web_page:
            content = web_page.read()
        scrapped_lines = self.scrapper._parse_web_puzzle_input(web_content=content)
        self.assertListEqual(expected_lines, scrapped_lines)

    def test_use_unix_style_line_ending(self):
        """Verify that the parsed lines use the "\n" end-line character."""
        with open(DATA_PATH / "web_input_2022_05_cut.html", mode="rb") as web_page:
            content = web_page.read()
        scrapped_lines = self.scrapper._parse_web_puzzle_input(web_content=content)
        self.assertTrue(all(line.endswith("\n") for line in scrapped_lines[:-1]))
