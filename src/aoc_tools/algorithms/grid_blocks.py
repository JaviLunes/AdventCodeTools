# coding=utf-8
"""Elemental blocks for defining discretized geometrical regions."""

# Standard library imports:
from typing import Any


class Cell2D:
    """Discrete location in a 2D grid region."""
    __slots__ = ["x", "y", "value"]

    def __init__(self, x: int, y: int, value: Any = None):
        self.x, self.y = x, y
        self.value = value

    def __repr__(self) -> str:
        return f"({self.x},{self.y})"

    def __eq__(self, other: "Cell2D") -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def distance(self, other: "Cell2D") -> int:
        """Compute the Manhattan distance between this and another Cell2D."""
        return abs(other.x - self.x) + abs(other.y - self.y)

    @property
    def xy(self) -> tuple[int, int]:
        """Provide the XY coordinates of this Cell2D as a tuple."""
        return self.x, self.y
