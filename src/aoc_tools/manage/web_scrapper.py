# coding=utf-8
"""Tools for scrapping information from the Advent of Code website."""

# Standard library imports:
from collections.abc import Callable
import datetime
from pathlib import Path
import re
from typing import TypeVar

# Third party imports:
from bs4 import BeautifulSoup
import requests

# Local application imports:
from aoc_tools.build.paths_manager import PathsManager

# Set constants:
AOC_BAD_LOGIN_CODE = 500

# Define custom types:
Parsed = TypeVar("Parsed")
ParseFunc = Callable[[bytes], Parsed]


class LogInError(ConnectionError):
    """Exception raised for web-log-in-related issues."""
    def __init__(self, empty: bool = False, bad_format: bool = False,
                 rejected: bool = False):
        self._prepare_help_text()
        if empty:
            self._use_text_for_empty_log_in()
        elif bad_format:
            self._use_text_for_bad_formatted_log_in()
        elif rejected:
            self._use_text_for_rejected_log_in()
        else:
            self._use_text_for_generic_log_in()

    def _prepare_help_text(self):
        """Describe how to retrieve and store the required session ID."""
        text = """
        Some scrapping methods need to log into the AoC website, and thus try to read 
        a session ID string from a 'secrets' file, whose location is provided by the 
        PathsManager.path_secrets property.
        
        To find out your current session ID, log in to the AoC website, and use your 
        web browser to inspect the currently used cookies (on Firefox, right-click on 
        any AoC page > Inspect > Storage > Cookies > session). Copy the session value 
        (a large string of numbers and letters) and paste it in the 'secrets' file.
        
        The 'secrets' file must ONLY contain the session ID value. Remove any prefix or 
        extra characters added by your browser web copying the value (e.g. Firefox may 
        add the 'session:' prefix, and encapsulate the value in double quotation 
        marks). Ensure the file contains only one line."""
        self._help_text = text.replace("        ", "    ")

    def _use_text_for_empty_log_in(self):
        """Make a short statement about the log-in secrets file being empty."""
        text = "The secrets file is empty or does not exist."
        self._error_description = text

    def _use_text_for_bad_formatted_log_in(self):
        """Make a short statement about data in secrets file being bad-formatted."""
        text = "The data inside the secrets file is not as expected."
        self._error_description = text

    def _use_text_for_rejected_log_in(self):
        """Make a short statement about the log-in being rejected."""
        text = "The stored session ID was rejected by the AoC website."
        self._error_description = text

    def _use_text_for_generic_log_in(self):
        """Make a short statement about an unexpected log-in error."""
        text = """An unexpected log-in error occurred."""
        self._error_description = text

    def __str__(self) -> str:
        return f"{self._error_description}\n{self._help_text}"


class ScrapError(ConnectionError):
    """Exception raised for web-scrapping-related issues."""


class AdventScrapper:
    """Retrieve data from the Advent of Code website."""
    def __init__(self, paths: PathsManager):
        self.paths = paths

    def scrap_puzzle_name(self, day: int) -> str | None:
        """Try to extract the name of the target day's puzzle."""
        self.paths.day = day
        return self._scrap(
            target_url=self.paths.url_advent_puzzle, use_log_in=False,
            parse_func=self._parse_web_puzzle_name)

    def scrap_puzzle_input(self, day: int) -> list[str] | None:
        """Try to extract the lines of the target day's puzzle input."""
        self.paths.day = day
        return self._scrap(
            target_url=self.paths.url_advent_input, use_log_in=True,
            parse_func=self._parse_web_puzzle_input)

    def _scrap(self, target_url: str, parse_func: ParseFunc, use_log_in: bool) -> Parsed:
        """Try to scrap and parse the content of a target URL."""
        try:
            credentials = self._build_credentials(use_log_in=use_log_in)
            self._check_valid_day()
            web_content = self._get_page_content(url=target_url, credentials=credentials)
            return parse_func(web_content)
        except ScrapError:
            return None

    def _build_credentials(self, use_log_in: bool) -> dict[str, str]:
        """Generate the credentials required for logging into the AoC website."""
        if not use_log_in:
            return {}
        if not self.paths.path_secrets.exists():
            raise LogInError(empty=True)
        secrets_data = self._read_secrets(file_path=self.paths.path_secrets)
        if len(secrets_data) == 0:
            raise LogInError(empty=True)
        elif len(secrets_data) > 1:
            raise LogInError(bad_format=True)
        return dict(session=secrets_data[0])

    @staticmethod
    def _read_secrets(file_path: Path) -> list[str]:
        """Extract all data lines from the target secrets file."""
        with open(file_path, mode="r") as file:
            return file.readlines()

    def _check_valid_day(self):
        """Verify that the target day is not a future date."""
        now_dt = self._get_current_time()
        target_dt = datetime.datetime(year=self.paths.year, month=12, day=self.paths.day)
        if not target_dt <= now_dt:
            raise ScrapError(f"The target '{target_dt:%Y/%m/%d}' is a future date.")

    @staticmethod
    def _get_current_time() -> datetime.datetime:
        """Encapsulate the datetime.now function, for mock-testing purposes."""
        return datetime.datetime.now()

    @staticmethod
    def _get_page_content(url: str, credentials: dict[str, str]) -> bytes:
        """Download a web page and return its content in HTML form."""
        response = requests.get(url, cookies=credentials)
        code = response.status_code
        if code == AOC_BAD_LOGIN_CODE:
            raise LogInError(rejected=True)
        if not code == 200:
            raise ScrapError(f"The request returned a {code} status code.")
        return response.content

    @staticmethod
    def _parse_web_puzzle_input(web_content: bytes) -> list[str]:
        """Extract the lines of data of a daily puzzle input from its webpage."""
        soup = BeautifulSoup(markup=web_content, features="html.parser")
        lines = [line + "\n" for line in soup.text.split("\r\n")]
        if lines[-1] == "\n":
            lines.pop(-1)
            lines[-1] = lines[-1].removesuffix("\n")
        return lines

    def _parse_web_puzzle_name(self, web_content: bytes) -> str:
        """Extract the name of a daily puzzle from its description webpage."""
        soup = BeautifulSoup(markup=web_content, features="html.parser")
        article_tag = soup.find("article", attrs={"class": "day-desc"})
        page_title = article_tag.find_next("h2").text
        rx = f"^--- Day {self.paths.day}: (?P<name>.+) ---$"
        match = re.match(pattern=rx, string=page_title)
        if match is None:
            text = f"The extracted title '{page_title}' does not match the regex '{rx}'."
            raise ScrapError(text)
        return match["name"]
