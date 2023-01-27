# coding=utf-8
"""Tests for the buildable-files-info-managing tools."""

# Standard library imports:
from pathlib import Path
import unittest

# Local application imports:
from aoc_tools.build.paths_manager import PathsManager, TEMPLATES_PATH

# Set constants:
BASE_PATH = Path(r"Z:")
DAYS = [1, 10, 25]
YEAR = 3057


class PathsTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define tools to be tested."""
        self.manager = PathsManager(year=YEAR, build_base_path=BASE_PATH)

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
        middle_path = "day_&@day_z@&" if script else "tests_day_&@day_z@&"
        return TEMPLATES_PATH / middle_path / f"{name}.template"

    def test_input_buildable_path(self):
        """Assert that the file path for this file is as expected."""
        for day in DAYS:
            paths_data = self.manager.get_daily_data(day=day)
            expected_path = self._get_buildable_path(
                name="puzzle_input.txt", day=day, script=True)
            self.assertIn(expected_path, paths_data.file_paths)

    def test_input_template_path(self):
        """Assert that the template path for this file is as expected."""
        for day in DAYS:
            paths_data = self.manager.get_daily_data(day=day)
            expected_path = self._get_template_path(script=True, name="puzzle_input.txt")
            self.assertIn(expected_path, paths_data.file_templates)

    def test_solution_buildable_path(self):
        """Assert that the file path for this file is as expected."""
        for day in DAYS:
            paths_data = self.manager.get_daily_data(day=day)
            expected_path = self._get_buildable_path(
                name="solution.py", day=day, script=True)
            self.assertIn(expected_path, paths_data.file_paths)

    def test_solution_template_path(self):
        """Assert that the template path for this file is as expected."""
        for day in DAYS:
            paths_data = self.manager.get_daily_data(day=day)
            expected_path = self._get_template_path(script=True, name="solution.py")
            self.assertIn(expected_path, paths_data.file_templates)

    def test_tools_buildable_path(self):
        """Assert that the file path for this file is as expected."""
        for day in DAYS:
            paths_data = self.manager.get_daily_data(day=day)
            expected_path = self._get_buildable_path(
                name="tools.py", day=day, script=True)
            self.assertIn(expected_path, paths_data.file_paths)

    def test_tools_template_path(self):
        """Assert that the template path for this file is as expected."""
        for day in DAYS:
            paths_data = self.manager.get_daily_data(day=day)
            expected_path = self._get_template_path(script=True, name="tools.py")
            self.assertIn(expected_path, paths_data.file_templates)

    def test_tests_init_buildable_path(self):
        """Assert that the file path for this file is as expected."""
        for day in DAYS:
            paths_data = self.manager.get_daily_data(day=day)
            expected_path = self._get_buildable_path(
                name="__init__.py", day=day, script=False)
            self.assertIn(expected_path, paths_data.file_paths)

    def test_tests_init_template_path(self):
        """Assert that the template path for this file is as expected."""
        for day in DAYS:
            paths_data = self.manager.get_daily_data(day=day)
            expected_path = self._get_template_path(script=False, name="__init__.py")
            self.assertIn(expected_path, paths_data.file_templates)

    def test_tests_example_buildable_path(self):
        """Assert that the file path for this file is as expected."""
        for day in DAYS:
            paths_data = self.manager.get_daily_data(day=day)
            expected_path = self._get_buildable_path(
                name="tests_example.py", day=day, script=False)
            self.assertIn(expected_path, paths_data.file_paths)

    def test_tests_example_template_path(self):
        """Assert that the template path for this file is as expected."""
        for day in DAYS:
            paths_data = self.manager.get_daily_data(day=day)
            expected_path = self._get_template_path(
                script=False, name="tests_example.py")
            self.assertIn(expected_path, paths_data.file_templates)

    def test_tests_solution_buildable_path(self):
        """Assert that the file path for this file is as expected."""
        for day in DAYS:
            paths_data = self.manager.get_daily_data(day=day)
            expected_path = self._get_buildable_path(
                name="tests_solution.py", day=day, script=False)
            self.assertIn(expected_path, paths_data.file_paths)

    def test_tests_solution_template_path(self):
        """Assert that the template path for this file is as expected."""
        for day in DAYS:
            paths_data = self.manager.get_daily_data(day=day)
            expected_path = self._get_template_path(
                script=False, name="tests_solution.py")
            self.assertIn(expected_path, paths_data.file_templates)

    def test_input_path_from_solution(self):
        """Assert that the relative file path for this file is as expected."""
        for day in DAYS:
            paths_data = self.manager.get_daily_data(day=day)
            base = "Path(__file__).parent / "
            expected_path_str = base + '"' + "puzzle_input.txt" + '"'
            self.assertEqual(expected_path_str, paths_data.path_input_from_solution)

    def test_input_path_from_tests(self):
        """Assert that the relative file path for this file is as expected."""
        for day in DAYS:
            paths_data = self.manager.get_daily_data(day=day)
            base = "Path(__file__).parents[2] / "
            middle = f"src/aoc{YEAR}/day_{self._get_day_z(day=day)}/"
            expected_path_str = base + '"' + middle + "puzzle_input.txt" + '"'
            self.assertEqual(expected_path_str, paths_data.path_input_from_tests)

    def test_project_path(self):
        """Assert that the project path is as expected."""
        for day in DAYS:
            paths_data = self.manager.get_daily_data(day=day)
            expected_path = BASE_PATH / f"AdventCode{YEAR}"
            self.assertEqual(expected_path, paths_data.path_project)


class ModulesTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define tools to be tested."""
        self.manager = PathsManager(year=YEAR, build_base_path=BASE_PATH)

    @staticmethod
    def _get_day_z(day: int) -> str:
        """Add the expected amount of leading zeros to the string of the target day."""
        return str(day).zfill(2)

    def test_day_scripts_module(self):
        """Assert that the module import string is as expected."""
        for day in DAYS:
            paths_data = self.manager.get_daily_data(day=day)
            expected_str = f"aoc{YEAR}.day_{self._get_day_z(day=day)}"
            self.assertEqual(expected_str, paths_data.module_day_scripts)

    def test_solution_scripts_module(self):
        """Assert that the module import string is as expected."""
        for day in DAYS:
            paths_data = self.manager.get_daily_data(day=day)
            expected_str = f"aoc{YEAR}.day_{self._get_day_z(day=day)}.solution"
            self.assertEqual(expected_str, paths_data.module_solution)

    def test_tools_scripts_module(self):
        """Assert that the module import string is as expected."""
        for day in DAYS:
            paths_data = self.manager.get_daily_data(day=day)
            expected_str = f"aoc{YEAR}.day_{self._get_day_z(day=day)}.tools"
            self.assertEqual(expected_str, paths_data.module_tools)
