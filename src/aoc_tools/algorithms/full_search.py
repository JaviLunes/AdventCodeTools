# coding=utf-8
"""Search function and node ABC for finding all nodes reachable from a start node."""

# Standard library imports:
import abc
from typing import TypeVar

Node = TypeVar("Node", bound="FNode")


class FNode(metaclass=abc.ABCMeta):
    """ABC for an individual node in a Full search algorithm."""
    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return self.id

    @property
    @abc.abstractmethod
    def id(self) -> str:
        """Provide a string identifier unique to this FNode."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_successors(self) -> set["FNode"]:
        """List all nodes to search that are directly reachable from this FNode."""
        raise NotImplementedError


def full_search(start: Node) -> set[Node]:
    """Find all nodes that can be reached from a start FNode."""
    # Build search registers:
    pending_nodes = [start]
    visited_nodes = set()
    # Check every pending node one at a time (order doesn't matter):
    while pending_nodes:
        q_node = pending_nodes.pop()
        # Register all non-visited successor nodes for future checking:
        s_nodes = q_node.get_successors() - visited_nodes
        pending_nodes.extend(s_nodes)
        # Register the original node as already seen:
        visited_nodes.add(q_node)
    # When the code reaches this point, all reachable nodes have been visited:
    return visited_nodes
