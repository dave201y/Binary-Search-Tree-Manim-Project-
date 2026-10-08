from __future__ import annotations

from typing import Generic, Iterable, Iterator, Optional, TypeVar

from .node import BSTNode, Node

T = TypeVar("T")


class BinarySearchTree(Generic[T]):
    """A binary search tree supporting insertion and searching."""

    def __init__(self, values: Optional[Iterable[T]] = None):
        self.root: Optional[BSTNode[T]] = None

        if values is not None:
            for value in values:
                self.insert(value)

    def insert(self, value: T) -> BSTNode[T]:
        """Insert a value into the BST and return the inserted node."""
        if self.root is None:
            self.root = BSTNode(value)
            return self.root

        current = self.root
        parent = None

        while current is not None:
            parent = current
            if value < current.key:
                current = current.left
            elif value > current.key:
                current = current.right
            else:
                return current

        new_node = BSTNode(value, parent=parent)

        if value < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        return new_node

    def search(self, value: T) -> Optional[BSTNode[T]]:
        """Return the node matching value, or None if the value is absent."""
        current = self.root

        while current is not None:
            if value == current.key:
                return current
            if value < current.key:
                current = current.left
            else:
                current = current.right

        return None

    def contains(self, value: T) -> bool:
        """Return True when the value exists in the tree."""
        return self.search(value) is not None

    def __contains__(self, value: T) -> bool:
        return self.contains(value)

    def in_order(self) -> Iterator[T]:
        """Yield values in sorted order."""
        yield from self._in_order(self.root)

    def _in_order(self, node: Optional[BSTNode[T]]) -> Iterator[T]:
        if node is None:
            return

        yield from self._in_order(node.left)
        yield node.key
        yield from self._in_order(node.right)

    def __iter__(self) -> Iterator[T]:
        return iter(self.in_order())

    def minimum(self) -> Optional[T]:
        """Return the minimum value in the tree, if it exists."""
        if self.root is None:
            return None

        current = self.root
        while current.left is not None:
            current = current.left
        return current.key

    def maximum(self) -> Optional[T]:
        """Return the maximum value in the tree, if it exists."""
        if self.root is None:
            return None

        current = self.root
        while current.right is not None:
            current = current.right
        return current.key

    def delete(self, value: T) -> None:
        """Delete is implemented by Person 3."""
        raise NotImplementedError("Delete operation is not implemented yet.")

    def remove(self, value: T) -> None:
        """Alias for delete for compatibility with tree terminology."""
        self.delete(value)


BST = BinarySearchTree
Tree = BinarySearchTree

__all__ = ["BinarySearchTree", "BST", "Tree", "BSTNode", "Node"]

