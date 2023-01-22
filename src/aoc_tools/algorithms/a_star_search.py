# coding=utf-8
"""Search function and node ABC for implementing the A* search algorithm."""

# Standard library imports:
import abc
from collections.abc import Callable, Hashable, Iterable
import heapq
import math
from typing import TypeVar

# Define custom types:
Node = TypeVar("Node", bound="ASNode")
GoalFunc = Callable[[Node], bool]


class ASNode(metaclass=abc.ABCMeta):
    """ABC for an individual node in an A* search algorithm."""
    __slots__ = ["_parent"]

    def __init__(self: Node, parent: Node = None):
        self._parent = parent

    def __hash__(self) -> int:
        return hash(self.id)

    def __lt__(self: Node, other: Node) -> bool:
        return self.f < other.f

    def __repr__(self) -> str:
        return f"{self.id}: {self.g}"

    @property
    @abc.abstractmethod
    def id(self) -> Hashable:
        """Provide a hashable identifier unique to this ASNode."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def g(self) -> int:
        """Compute the cost for reaching this ASNode from the search start point."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def h(self) -> int:
        """Estimate the cost for reaching the search goal from this ASNode."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_successors(self: Node) -> Iterable[Node]:
        """List all nodes to search that are directly reachable from this ASNode."""
        raise NotImplementedError

    @property
    def parent(self: Node) -> Node | None:
        """Provide the parent node of this ASNode (or None, if no parent)."""
        return self._parent

    @property
    def f(self) -> int:
        """Provide the sum of the known 'g' and estimated 'h' costs."""
        return self.g + self.h

    @property
    def lineage(self: Node) -> list[Node]:
        """List this ASNode and its recursive parents (if any)."""
        return [self] + (self.parent.lineage if self.parent else [])


def a_star_search(start: Node, goal_func: GoalFunc) -> Node:
    """Find the path of lesser cost for reaching a goal objective from a start node."""
    # Build search registers:
    pending_nodes = [start]
    visited_nodes = set()
    best_g_costs = {start.id: start.g}
    # Check each pending node one at a time, from lowest to greatest g cost:
    while pending_nodes:
        q_node = heapq.heappop(pending_nodes)
        # Stop if the goal is reached:
        if goal_func(q_node):
            return q_node
        if q_node in visited_nodes:
            continue  # Skip node if its location was already visited.
        # For each possible successor node:
        for s_node in q_node.get_successors():
            if s_node in visited_nodes:
                continue  # Skip successor if it was already visited:
            if s_node.g >= best_g_costs.get(s_node.id, math.inf):
                continue  # Skip successor if worse than its hash's best cost.
            # Register successor node for future checking:
            heapq.heappush(pending_nodes, s_node)
            best_g_costs[s_node.id] = s_node.g
        # Register the original node as already seen:
        visited_nodes.add(q_node)
    # If code reaches this point, the goal was never reached:
    raise ValueError("The search could not reach the goal node.")
