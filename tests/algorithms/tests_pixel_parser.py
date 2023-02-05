# coding=utf-8
"""Tests for the PixelParser pixels-to-string conversion tool."""

# Standard library imports:
from pathlib import Path
import unittest

# Local application imports:
from aoc_tools.manage.puzzle_solving import read_puzzle_input
from aoc_tools.algorithms.pixel_parsing import PixelParser

# Set constants:
DATA_PATH = Path(__file__).parent / "data" / "pixel_parser"


# noinspection SpellCheckingInspection
class PixelParserTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define tools to be tested."""
        self.print_1 = read_puzzle_input(input_file=DATA_PATH / "example_1.txt")
        self.print_2 = read_puzzle_input(input_file=DATA_PATH / "example_2.txt")
        self.print_3 = read_puzzle_input(input_file=DATA_PATH / "example_3.txt")
        self.print_4 = read_puzzle_input(input_file=DATA_PATH / "example_4.txt")
        self.print_5 = read_puzzle_input(input_file=DATA_PATH / "example_5.txt")
        self.screen = PixelParser()

    def test_letters_in_screen_print_1(self):
        """The eight letters encoded in the 1st screen print are 'BGKAEREZ'."""
        self.assertEqual("BGKAEREZ", self.screen.process(pixel_lines=self.print_1))

    def test_letters_in_screen_print_2(self):
        """The eight letters encoded in the 2nd screen print are 'JZGUAPRB'."""
        self.assertEqual("JZGUAPRB", self.screen.process(pixel_lines=self.print_2))

    def test_letters_in_screen_print_3(self):
        """The eight letters encoded in the 3rd screen print are 'REHPRLUB'."""
        self.assertEqual("REHPRLUB", self.screen.process(pixel_lines=self.print_3))

    def test_letters_in_screen_print_4(self):
        """The eight letters encoded in the 4th screen print are 'EHZFZHCZ'."""
        self.assertEqual("EHZFZHCZ", self.screen.process(pixel_lines=self.print_4))

    def test_letters_in_screen_print_5(self):
        """The eight letters encoded in the 5th screen print are 'PHLHJGZA'."""
        self.assertEqual("PHLHJGZA", self.screen.process(pixel_lines=self.print_5))
