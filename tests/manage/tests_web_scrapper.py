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
from aoc_tools.manage.web_scrapper import AdventScrapper, LogInError, ScrapError
from aoc_tools.manage.web_scrapper import AOC_BAD_LOGIN_CODE
from aoc_tools.manage import web_scrapper as tested_module

# Set constants:
DATA_PATH = Path(__file__).parent / "data"
PAST_YEAR = datetime.date.today().year - 1


class PublicMethodsTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define tools to be tested."""
        self.paths = PathsManager(year=PAST_YEAR, build_base_path=Path(r"Z:"))
        self.scrapper = AdventScrapper(paths=self.paths)

    def test_puzzle_input_scrapping_uses_proper_url(self):
        """The URL to the input page of the target daily puzzle is used."""
        attr = self.scrapper._scrap.__name__
        with mock.patch.object(target=self.scrapper, attribute=attr) as mocked_scrap:
            self.scrapper.scrap_puzzle_input(day=1)
        expected_url = self.scrapper.paths.url_advent_input
        self.assertEqual(expected_url, mocked_scrap.call_args.kwargs["target_url"])

    def test_puzzle_input_scrapping_uses_proper_parse_func(self):
        """The puzzle-input-web-parsing method is used as parsing function."""
        attr = self.scrapper._scrap.__name__
        with mock.patch.object(target=self.scrapper, attribute=attr) as mocked_scrap:
            self.scrapper.scrap_puzzle_input(day=1)
        expected_func = self.scrapper._parse_web_puzzle_input
        self.assertEqual(expected_func, mocked_scrap.call_args.kwargs["parse_func"])

    def test_puzzle_input_scrapping_uses_log_in(self):
        """This scrapping method does require a log-in into the AoC web."""
        attr = self.scrapper._scrap.__name__
        with mock.patch.object(target=self.scrapper, attribute=attr) as mocked_scrap:
            self.scrapper.scrap_puzzle_input(day=1)
        self.assertTrue(mocked_scrap.call_args.kwargs["use_log_in"])

    def test_puzzle_name_scrapping_uses_proper_url(self):
        """The URL to the description page of the target daily puzzle is used."""
        attr = self.scrapper._scrap.__name__
        with mock.patch.object(target=self.scrapper, attribute=attr) as mocked_scrap:
            self.scrapper.scrap_puzzle_name(day=1)
        expected_url = self.scrapper.paths.url_advent_puzzle
        self.assertEqual(expected_url, mocked_scrap.call_args.kwargs["target_url"])

    def test_puzzle_name_scrapping_uses_proper_parse_func(self):
        """The puzzle-name-web-parsing method is used as parsing function."""
        attr = self.scrapper._scrap.__name__
        with mock.patch.object(target=self.scrapper, attribute=attr) as mocked_scrap:
            self.scrapper.scrap_puzzle_name(day=1)
        expected_func = self.scrapper._parse_web_puzzle_name
        self.assertEqual(expected_func, mocked_scrap.call_args.kwargs["parse_func"])

    def test_puzzle_name_scrapping_does_not_use_log_in(self):
        """This scrapping method does not require a log-in into the AoC web."""
        attr = self.scrapper._scrap.__name__
        with mock.patch.object(target=self.scrapper, attribute=attr) as mocked_scrap:
            self.scrapper.scrap_puzzle_name(day=1)
        self.assertFalse(mocked_scrap.call_args.kwargs["use_log_in"])


class ScrapTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define tools to be tested."""
        self.paths = PathsManager(year=PAST_YEAR, build_base_path=Path(r"Z:"))
        self.scrapper = AdventScrapper(paths=self.paths)

    def test_use_generated_credentials_on_request(self):
        """The credentials built by the corresponding method are included in request."""
        target_url = "http://mocked_url.mock"
        mocked_cookies = dict(user="TheseAreNotEven", password="TheExpectedParams")
        target_1, target_2 = self.scrapper, tested_module.requests
        attr_1 = target_1._build_credentials.__name__
        attr_2 = target_2.get.__name__
        with mock.patch.object(target_1, attribute=attr_1, return_value=mocked_cookies):
            with mock.patch.object(target_2, attribute=attr_2) as mocked_get:
                self.scrapper._scrap(
                    target_url=target_url, parse_func=mock.Mock, use_log_in=True)
        self.assertDictEqual(mocked_cookies, mocked_get.call_args.kwargs["cookies"])

    def test_avoid_requesting_future_date(self):
        """If target date is future, do not make any request, and return None."""
        mocked_now = datetime.datetime(self.paths.year - 1, 12, self.paths.day)
        target, attr_1 = self.scrapper, self.scrapper._get_current_time.__name__
        attr_2 = self.scrapper._get_page_content.__name__
        with mock.patch.object(target=target, attribute=attr_1, return_value=mocked_now):
            with mock.patch.object(target=target, attribute=attr_2) as mocked_request:
                output = self.scrapper._scrap(
                    target_url="", parse_func=mock.Mock(), use_log_in=False)
        self.assertFalse(mocked_request.called)
        self.assertIsNone(output)

    @responses.activate
    def test_avoid_parsing_responses_with_non_200_status(self):
        """If the response's status is not 200, return None instead of parsing it."""
        target_url = "http://mocked_url.mock"
        omitted = [200, AOC_BAD_LOGIN_CODE]
        non_ok_codes = [int(code) for code in http.HTTPStatus if code not in omitted]
        for code in non_ok_codes:
            with self.subTest(code=code):
                responses.get(url=target_url, status=code)
                mocked_parse = mock.Mock()
                output = self.scrapper._scrap(
                    target_url=target_url, parse_func=mocked_parse, use_log_in=False)
                self.assertIsNone(output)
                self.assertFalse(mocked_parse.called)

    @responses.activate
    def test_return_none_on_failed_content_parsing(self):
        """If the content-parsing method raises an ScrapError, return None."""
        target_url = "http://mocked_url.mock"
        responses.get(url=target_url)
        mocked_parse = mock.Mock(side_effect=ScrapError)
        output = self.scrapper._scrap(
            target_url=target_url, parse_func=mocked_parse, use_log_in=False)
        self.assertTrue(mocked_parse.called)
        self.assertIsNone(output)


class ParsePuzzleNameTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define tools to be tested."""
        self.paths = PathsManager(year=PAST_YEAR, build_base_path=Path(r"Z:"))
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
        self.paths = PathsManager(year=PAST_YEAR, build_base_path=Path(r"Z:"))
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


class SecretsTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define tools to be tested."""
        self.secrets_file = DATA_PATH / "credentials_fake.txt"
        self.secrets_file_missing = DATA_PATH / "credentials_missing.txt"
        self.secrets_file_empty = DATA_PATH / "credentials_empty.txt"
        self.secrets_file_bad_format = DATA_PATH / "credentials_bad_format.txt"

    @staticmethod
    def _mock_paths_manager(secrets_path: Path) -> mock.Mock:
        """Create a mocked PathsManager instance pointing to the target secrets file."""
        real_paths = PathsManager(year=PAST_YEAR, build_base_path=Path(r"Z:"))
        mocked_paths = mock.Mock(spec_set=real_paths)
        mocked_paths.path_secrets = secrets_path
        mocked_paths.year = PAST_YEAR
        return mocked_paths

    def test_read_credentials_from_file(self):
        """The log-in session ID must be read from the secrets file."""
        paths = self._mock_paths_manager(secrets_path=self.secrets_file)
        scrapper = AdventScrapper(paths=paths)
        attr = scrapper._read_secrets.__name__
        mocked_read = mock.Mock(return_value=["MockedSecretsContent"])
        with mock.patch.object(target=scrapper, attribute=attr, new=mocked_read):
            scrapper._build_credentials(use_log_in=True)
        self.assertEqual(self.secrets_file, mocked_read.call_args.kwargs["file_path"])

    def test_use_read_credentials(self):
        """The generated credentials map must use the read session ID."""
        paths = self._mock_paths_manager(secrets_path=self.secrets_file)
        scrapper = AdventScrapper(paths=paths)
        with open(paths.path_secrets, mode="r") as secrets_file:
            expected_id = secrets_file.readlines()[0]
        expected_credentials = dict(session=expected_id)
        built_credentials = scrapper._build_credentials(use_log_in=True)
        self.assertDictEqual(expected_credentials, built_credentials)

    def test_raise_if_file_does_not_exist(self):
        """If secrets file is empty, raise and ask user to introduce required data."""
        paths = self._mock_paths_manager(secrets_path=self.secrets_file_missing)
        scrapper = AdventScrapper(paths=paths)
        with self.assertRaises(LogInError):
            scrapper._build_credentials(use_log_in=True)

    def test_raise_if_no_credentials_in_file(self):
        """If secrets file is empty, raise and ask user to introduce required data."""
        paths = self._mock_paths_manager(secrets_path=self.secrets_file_empty)
        scrapper = AdventScrapper(paths=paths)
        with self.assertRaises(LogInError):
            scrapper._build_credentials(use_log_in=True)

    def test_raise_if_credentials_are_not_as_expected(self):
        """If read credentials data doesn't match expected format, raise and ask user."""
        paths = self._mock_paths_manager(secrets_path=self.secrets_file_bad_format)
        scrapper = AdventScrapper(paths=paths)
        with self.assertRaises(LogInError):
            scrapper._build_credentials(use_log_in=True)

    @responses.activate
    def test_raise_if_request_fails_due_to_credentials(self):
        """If the web request doesn't accept the read credentials, raise and ask user."""
        paths = self._mock_paths_manager(secrets_path=self.secrets_file)
        scrapper = AdventScrapper(paths=paths)
        paths.day = 1
        target_url = "http://mocked_url.mock"
        responses.get(url=target_url, status=AOC_BAD_LOGIN_CODE)
        with self.assertRaises(LogInError):
            scrapper._scrap(target_url=target_url, parse_func=mock.Mock, use_log_in=True)
