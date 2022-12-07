# coding=utf-8
"""Constant values and string templates used in other modules."""

# Standard library imports:
from string import Template

PACKAGE_NAME = "aoc_tools"
MODULE_DAILY_SCRIPT = Template("aoc$year.day$day.solution")
FILE_DAILY_INPUT = Template("$day_$day/puzzle_input.txt")
FILE_DAILY_SCRIPT = Template("$day_$day/solution.py")
FILE_DAILY_TESTS = Template("tests_day_$day.py")
FILE_DAILY_TOOLS = Template("$day_$day/tools.py")
URL_ADVENT_PUZZLE = Template("https://adventofcode.com/$year/day/$day")
URL_GITHUB_SCRIPT = Template("https://github.com/JaviLunes/AdventCode$year/tree/master"
                             "/src/aoc$year/day_$day/solution.py")
