# coding=utf-8
"""Elemental blocks for defining discretized geometrical regions."""

# Standard library imports:
from typing import Any


class CellND:
    """Discrete location in a generic nD gridded region."""
    __slots__ = ["value", "coord_map"]

    def __init__(self, value: Any = None, **coord_values: int):
        self.value = value
        self.coord_map = coord_values

    def __repr__(self) -> str:
        return f"({tuple(self.coord_map.values())})"

    def __eq__(self, other: "CellND") -> bool:
        return self.coord_map == other.coord_map

    def __hash__(self) -> int:
        return hash(tuple(self.coord_map.values()))

    def distance(self, other: "CellND") -> int:
        """Compute the Manhattan distance between this and another CellND."""
        return sum(abs(other.coord_map[c] - self.coord_map[c])
                   for c in self.coord_map.keys())
