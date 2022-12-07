# coding=utf-8
"""Discover and run all tests defined for this package."""

# Standard library imports:
from pathlib import Path
import unittest


tests_path = Path(__file__).parent / "tests"
assert tests_path.exists()
tests_suite = unittest.TestLoader().discover(start_dir=str(tests_path))
unittest.TextTestRunner().run(tests_suite)
