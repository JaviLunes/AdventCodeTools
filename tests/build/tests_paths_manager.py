# coding=utf-8
"""Tests for the buildable-files-info-managing tools."""

# Standard library imports:
from pathlib import Path
import unittest
from unittest import mock

# Local application imports:
from aoc_tools.build.paths_manager import PathsManager, TEMPLATES_PATH

# Set constants:
BASE_PATH = Path(r"Z:")
DAYS = [1, 10, 25]
YEAR = 3057


class ChangeDateTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define tools to be tested."""
        self.manager = PathsManager(build_base_path=BASE_PATH, year=YEAR)

    def test_default_day_is_day_1(self):
        """If not specified, a PathsManager starts with 1 as the current day."""
        self.assertEqual(1, self.manager.day)

    def test_re_build_file_paths_on_year_change(self):
        """When the target year is changed, the map of file paths is rebuilt."""
        new_year = YEAR + 1
        self.assertNotEqual(new_year, self.manager.year)
        attr = self.manager._build_file_paths.__name__
        with mock.patch.object(target=self.manager, attribute=attr) as mocked_build:
            self.manager.year = new_year
        self.assertEqual(1, mocked_build.call_count)
        self.assertEqual(new_year, self.manager.year)

    def test_re_build_file_paths_on_day_change(self):
        """When the target day is changed, the map of file paths is rebuilt."""
        new_day = 20
        self.assertNotEqual(new_day, self.manager.day)
        attr = self.manager._build_file_paths.__name__
        with mock.patch.object(target=self.manager, attribute=attr) as mocked_build:
            self.manager.day = new_day
        self.assertEqual(1, mocked_build.call_count)
        self.assertEqual(new_day, self.manager.day)


class PathsTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define tools to be tested."""
        self.manager = PathsManager(build_base_path=BASE_PATH, year=YEAR)

    @staticmethod
    def _get_day_z(day: int) -> str:
        """Add the expected amount of leading zeros to the string of the target day."""
        return str(day).zfill(2)

    def _get_buildable_path(self, name: str, day: int, script: bool) -> Path:
        """Get the expected absolute file path for the target buildable file."""
        day_z = self._get_day_z(day=day)
        if script:
            middle_path = f"AdventCode{YEAR}/src/aoc{YEAR}/day_{day_z}"
        else:
            middle_path = f"AdventCode{YEAR}/tests/tests_day_{day_z}"
        return BASE_PATH / middle_path / name

    @staticmethod
    def _get_template_path(name: str, script: bool) -> Path:
        """Get the expected absolute file path for the target template file."""
        if script:
            middle_path = "AdventCode&@year@&/src/aoc&@year@&/day_&@day_z@&"
        else:
            middle_path = f"AdventCode&@year@&/tests/tests_day_&@day_z@&"
        return TEMPLATES_PATH / middle_path / f"{name}.template"

    def test_input_buildable_path(self):
        """Assert that the file path for this file is as expected."""
        for day in DAYS:
            self.manager.day = day
            expected_path = self._get_buildable_path(
                name="puzzle_input.txt", day=day, script=True)
            self.assertIn(expected_path, self.manager.file_paths)

    def test_input_template_path(self):
        """Assert that the template path for this file is as expected."""
        for day in DAYS:
            self.manager.day = day
            expected_path = self._get_template_path(script=True, name="puzzle_input.txt")
            self.assertIn(expected_path, self.manager.file_templates)

    def test_solution_buildable_path(self):
        """Assert that the file path for this file is as expected."""
        for day in DAYS:
            self.manager.day = day
            expected_path = self._get_buildable_path(
                name="solution.py", day=day, script=True)
            self.assertIn(expected_path, self.manager.file_paths)

    def test_solution_template_path(self):
        """Assert that the template path for this file is as expected."""
        for day in DAYS:
            self.manager.day = day
            expected_path = self._get_template_path(script=True, name="solution.py")
            self.assertIn(expected_path, self.manager.file_templates)

    def test_tools_buildable_path(self):
        """Assert that the file path for this file is as expected."""
        for day in DAYS:
            self.manager.day = day
            expected_path = self._get_buildable_path(
                name="tools.py", day=day, script=True)
            self.assertIn(expected_path, self.manager.file_paths)

    def test_tools_template_path(self):
        """Assert that the template path for this file is as expected."""
        for day in DAYS:
            self.manager.day = day
            expected_path = self._get_template_path(script=True, name="tools.py")
            self.assertIn(expected_path, self.manager.file_templates)

    def test_tests_init_buildable_path(self):
        """Assert that the file path for this file is as expected."""
        for day in DAYS:
            self.manager.day = day
            expected_path = self._get_buildable_path(
                name="__init__.py", day=day, script=False)
            self.assertIn(expected_path, self.manager.file_paths)

    def test_tests_init_template_path(self):
        """Assert that the template path for this file is as expected."""
        for day in DAYS:
            self.manager.day = day
            expected_path = self._get_template_path(script=False, name="__init__.py")
            self.assertIn(expected_path, self.manager.file_templates)

    def test_tests_example_buildable_path(self):
        """Assert that the file path for this file is as expected."""
        for day in DAYS:
            self.manager.day = day
            expected_path = self._get_buildable_path(
                name="tests_example.py", day=day, script=False)
            self.assertIn(expected_path, self.manager.file_paths)

    def test_tests_example_template_path(self):
        """Assert that the template path for this file is as expected."""
        for day in DAYS:
            self.manager.day = day
            expected_path = self._get_template_path(
                script=False, name="tests_example.py")
            self.assertIn(expected_path, self.manager.file_templates)

    def test_tests_solution_buildable_path(self):
        """Assert that the file path for this file is as expected."""
        for day in DAYS:
            self.manager.day = day
            expected_path = self._get_buildable_path(
                name="tests_solution.py", day=day, script=False)
            self.assertIn(expected_path, self.manager.file_paths)

    def test_tests_solution_template_path(self):
        """Assert that the template path for this file is as expected."""
        for day in DAYS:
            self.manager.day = day
            expected_path = self._get_template_path(
                script=False, name="tests_solution.py")
            self.assertIn(expected_path, self.manager.file_templates)

    def test_input_path(self):
        """Assert that the file path for this file is as expected."""
        for day in DAYS:
            self.manager.day = day
            expected_path = self._get_buildable_path(
                name="puzzle_input.txt", day=day, script=True)
            self.assertEqual(expected_path, self.manager.path_input)

    def test_input_path_from_solution(self):
        """Assert that the relative file path for this file is as expected."""
        for day in DAYS:
            self.manager.day = day
            base = "Path(__file__).parent / "
            expected_path_str = base + '"' + "puzzle_input.txt" + '"'
            self.assertEqual(expected_path_str, self.manager.path_input_from_solution)

    def test_input_path_from_tests(self):
        """Assert that the relative file path for this file is as expected."""
        for day in DAYS:
            self.manager.day = day
            base = "Path(__file__).parents[2] / "
            middle = f"src/aoc{YEAR}/day_{self._get_day_z(day=day)}/"
            expected_path_str = base + '"' + middle + "puzzle_input.txt" + '"'
            self.assertEqual(expected_path_str, self.manager.path_input_from_tests)

    def test_project_path(self):
        """Assert that the project path is as expected."""
        for day in DAYS:
            self.manager.day = day
            expected_path = BASE_PATH / f"AdventCode{YEAR}"
            self.assertEqual(expected_path, self.manager.path_project)

    def test_source_path(self):
        """Assert that the 'src' path is as expected."""
        for day in DAYS:
            self.manager.day = day
            expected_path = BASE_PATH / f"AdventCode{YEAR}" / "src"
            self.assertEqual(expected_path, self.manager.path_src)

    def test_readme_path(self):
        """Assert that the README file path is as expected."""
        for day in DAYS:
            self.manager.day = day
            expected_path = BASE_PATH / f"AdventCode{YEAR}" / "README.md"
            self.assertEqual(expected_path, self.manager.path_readme)


class ModulesTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define tools to be tested."""
        self.manager = PathsManager(build_base_path=BASE_PATH, year=YEAR)

    @staticmethod
    def _get_day_z(day: int) -> str:
        """Add the expected amount of leading zeros to the string of the target day."""
        return str(day).zfill(2)

    def test_solution_scripts_module(self):
        """Assert that the module import string is as expected."""
        for day in DAYS:
            self.manager.day = day
            expected_str = f"aoc{YEAR}.day_{self._get_day_z(day=day)}.solution"
            self.assertEqual(expected_str, self.manager.module_solution)

    def test_tools_scripts_module(self):
        """Assert that the module import string is as expected."""
        for day in DAYS:
            self.manager.day = day
            expected_str = f"aoc{YEAR}.day_{self._get_day_z(day=day)}.tools"
            self.assertEqual(expected_str, self.manager.module_tools)
