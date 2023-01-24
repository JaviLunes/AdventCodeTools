# coding=utf-8
"""Constant values and string templates used in other modules."""

# Standard library imports:
from string import Template

PACKAGE_NAME = "aoc_tools"
DAILY_MODULE = Template("aoc$year.day_$day")
DAILY_PATH = Template("aoc$year/day_$day")
FILE_INPUT = "puzzle_input.txt"
FILE_SOLUTION = "solution.py"
FILE_TOOLS = "tools.py"
FILE_TESTS = Template("tests_day_$day.py")
URL_ADVENT_PUZZLE = Template("https://adventofcode.com/$year/day/$day")
URL_GITHUB_SCRIPT = Template("https://github.com/JaviLunes/AdventCode$year/tree/master"
                             "/src/aoc$year/day_$day/solution.py")
