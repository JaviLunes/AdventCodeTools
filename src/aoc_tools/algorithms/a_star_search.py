# coding=utf-8
"""Define a function for A* search algorithm, and an ABC for a compatible search node."""

# Standard library imports:
import abc
import heapq
from typing import Callable, Iterable, Optional


class ASNode(metaclass=abc.ABCMeta):
    """ABC for an individual node in an A* search algorithm."""
    __slots__ = ["_parent"]

    def __init__(self, parent: "ASNode" = None):
        self._parent = parent

    def __hash__(self) -> int:
        return hash(self.id)

    def __lt__(self, other: "ASNode") -> bool:
        return self.f < other.f

    def __repr__(self) -> str:
        return f"{self.id}: {self.g}"

    @property
    @abc.abstractmethod
    def id(self) -> str:
        """Provide a string identifier unique to this ASNode."""
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
    def get_successors(self) -> Iterable["ASNode"]:
        """List all nodes to search that are directly reachable from this ASNode."""
        raise NotImplementedError

    @property
    def parent(self) -> Optional["ASNode"]:
        """Provide the parent node of this ASNode (or None, if no parent)."""
        return self._parent

    @property
    def f(self) -> int:
        """Provide the sum of the known 'g' and estimated 'h' costs."""
        return self.g + self.h

    @property
    def lineage(self) -> list["ASNode"]:
        """List this ASNode and its recursive parents (if any)."""
        return [self] + (self.parent.lineage if self.parent else [])


def a_star_search(start: ASNode, goal_func: Callable) -> ASNode:
    """Find the path of lesser cost for reaching a goal objective from a start ASNode."""
    # Build lists / queues / min heaps / sets / cost maps:
    pending_nodes = [start]
    visited_nodes = set()
    best_g_costs = {start.id: start.g}
    # Check each pending node one at a time, from lowest to greatest g cost:
    while pending_nodes:
        q_node = heapq.heappop(pending_nodes)
        # Stop if the goal is reached:
        if goal_func(node=q_node):
            return q_node
        if q_node in visited_nodes:
            continue  # Skip node if its location was already visited.
        # For each possible neighbour node:
        for s_node in q_node.get_successors():
            if s_node in visited_nodes:
                continue  # Skip successor if its location was already visited:
            if s_node.g >= best_g_costs.get(s_node.id, 99999):
                continue  # Skip successor if worse than its location's best cost.
            # Register successor node for future checking:
            heapq.heappush(pending_nodes, s_node)
            best_g_costs[s_node.id] = s_node.g
        # Register the parent node's location as already seen:
        visited_nodes.add(q_node)
    # If code reaches this point, the goal was never reached:
    raise ValueError("The search could not reach the end ASNode.")
