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

    def search_path(self, value: T) -> list[tuple[Optional[T], str]]:
        """Return comparison decisions made while searching for ``value``.

        Each item contains the current node key and either ``"LEFT"``,
        ``"RIGHT"``, or ``"FOUND"``.  A missing value ends with
        ``(None, "NOT_FOUND")``.
        """
        path: list[tuple[Optional[T], str]] = []
        current = self.root

        while current is not None:
            if value == current.key:
                path.append((current.key, "FOUND"))
                return path

            direction = "LEFT" if value < current.key else "RIGHT"
            path.append((current.key, direction))
            current = current.left if direction == "LEFT" else current.right

        path.append((None, "NOT_FOUND"))
        return path

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

    def _find_node(self, value: T) -> Optional[BSTNode[T]]:
        """Return the node containing ``value``, if present."""
        current = self.root
        while current is not None:
            if value == current.key:
                return current
            current = current.left if value < current.key else current.right
        return None

    def _transplant(
        self,
        old: BSTNode[T],
        new: Optional[BSTNode[T]],
    ) -> None:
        """Replace one subtree with another and preserve parent pointers."""
        if old.parent is None:
            self.root = new
        elif old is old.parent.left:
            old.parent.left = new
        else:
            old.parent.right = new

        if new is not None:
            new.parent = old.parent

    def _minimum_node(self, node: BSTNode[T]) -> BSTNode[T]:
        """Return the leftmost node in a non-empty subtree."""
        while node.left is not None:
            node = node.left
        return node

    def inorder_successor(self, value: T) -> Optional[BSTNode[T]]:
        """Return the in-order successor of ``value``, if it exists."""
        node = self._find_node(value)
        if node is None:
            return None

        if node.right is not None:
            return self._minimum_node(node.right)

        successor = node.parent
        while successor is not None and node is successor.right:
            node = successor
            successor = successor.parent
        return successor

    def delete(self, value: T) -> bool:
        """Delete ``value`` and return whether a node was removed."""
        node = self._find_node(value)
        if node is None:
            return False

        if node.left is None:
            self._transplant(node, node.right)
        elif node.right is None:
            self._transplant(node, node.left)
        else:
            successor = self._minimum_node(node.right)
            if successor.parent is not node:
                self._transplant(successor, successor.right)
                successor.right = node.right
                successor.right.parent = successor

            self._transplant(node, successor)
            successor.left = node.left
            successor.left.parent = successor

        node.parent = None
        node.left = None
        node.right = None
        return True

    def remove(self, value: T) -> bool:
        """Alias for delete for compatibility with tree terminology."""
        return self.delete(value)


BST = BinarySearchTree
Tree = BinarySearchTree

__all__ = ["BinarySearchTree", "BST", "Tree", "BSTNode", "Node"]
