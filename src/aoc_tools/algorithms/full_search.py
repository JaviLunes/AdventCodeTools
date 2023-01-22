# coding=utf-8
"""Search function and node ABC for finding all nodes reachable from a start node."""

# Standard library imports:
import abc
from collections.abc import Hashable
from typing import TypeVar

# Define custom types:
Node = TypeVar("Node", bound="FNode")


class FNode(metaclass=abc.ABCMeta):
    """ABC for an individual node in a Full search algorithm."""
    __slots__ = ["_id", "_hash"]

    def __init__(self: Node, id_: Hashable, hash_: int):
        self._id = id_
        self._hash = hash_

    def __hash__(self) -> int:
        return self._hash

    def __repr__(self) -> str:
        return repr(self._id)

    @abc.abstractmethod
    def get_successors(self: Node) -> set[Node]:
        """List all nodes to search that are directly reachable from this FNode."""
        raise NotImplementedError


def full_search(start: Node) -> set[Node]:
    """Find all nodes that can be reached from a start node."""
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
