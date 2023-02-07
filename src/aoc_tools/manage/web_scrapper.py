# coding=utf-8
"""Tools for scrapping information from the Advent of Code website."""

# Standard library imports:
from collections.abc import Callable
import datetime
import re
from typing import TypeVar

# Third party imports:
from bs4 import BeautifulSoup
import requests

# Local application imports:
from aoc_tools.build.paths_manager import PathsManager

# Define custom types:
Parsed = TypeVar("Parsed")


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
            target_url=self.paths.url_advent_puzzle,
            parse_func=self._parse_web_puzzle_name)

    def _scrap(self, target_url: str, parse_func: Callable[[bytes], Parsed]) -> Parsed:
        """Try to scrap and parse the content of a target URL."""
        try:
            self._check_valid_day()
            web_content = self._get_page_content(url=target_url)
            return parse_func(web_content)
        except ScrapError:
            return None

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
    def _get_page_content(url: str) -> bytes:
        """Download a web page and return its content in HTML form."""
        request = requests.get(url)
        code = request.status_code
        if not code == 200:
            raise ScrapError(f"The request returned a {code} status code.")
        return request.content

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
