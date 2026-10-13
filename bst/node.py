from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


@dataclass
class BSTNode(Generic[T]):
    """A single node in a binary search tree."""

    key: T
    left: Optional["BSTNode[T]"] = field(default=None, repr=False)
    right: Optional["BSTNode[T]"] = field(default=None, repr=False)
    parent: Optional["BSTNode[T]"] = field(default=None, repr=False)

    @property
    def value(self) -> T:
        """Alias for the stored key."""
        return self.key

    @value.setter
    def value(self, value: T) -> None:
        self.key = value

    def __lt__(self, other: object) -> bool:
        if isinstance(other, BSTNode):
            other = other.key
        return self.key < other

    def __le__(self, other: object) -> bool:
        if isinstance(other, BSTNode):
            other = other.key
        return self.key <= other

    def __gt__(self, other: object) -> bool:
        if isinstance(other, BSTNode):
            other = other.key
        return self.key > other

    def __ge__(self, other: object) -> bool:
        if isinstance(other, BSTNode):
            other = other.key
        return self.key >= other

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BSTNode):
            return self.key == other.key
        return self.key == other


Node = BSTNode

