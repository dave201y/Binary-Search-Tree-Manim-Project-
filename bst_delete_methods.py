    # ---- Paste these methods inside Person 1's BST class ----
    # Assumes: self.root, and nodes with .key, .left, .right

    def _find_min(self, node):
        """Leftmost node of a subtree."""
        while node.left is not None:
            node = node.left
        return node

    def inorder_successor(self, key):
        """Smallest key greater than `key`, as a node. None if there is none."""
        node = self.root
        successor = None
        while node is not None:
            if key < node.key:
                successor = node
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                if node.right is not None:
                    return self._find_min(node.right)
                return successor
        return None

    def delete(self, key):
        """Delete key. Returns True if it was found, False otherwise."""
        self.root, deleted = self._delete(self.root, key)
        return deleted

    def _delete(self, node, key):
        if node is None:
            return None, False
        if key < node.key:
            node.left, deleted = self._delete(node.left, key)
            return node, deleted
        if key > node.key:
            node.right, deleted = self._delete(node.right, key)
            return node, deleted

        # Found the node to delete.
        if node.left is None:          # leaf, or only a right child
            return node.right, True
        if node.right is None:         # only a left child
            return node.left, True

        # Two children: copy the inorder successor's key here,
        # then delete the successor from the right subtree.
        successor = self._find_min(node.right)
        node.key = successor.key
        node.right, _ = self._delete(node.right, successor.key)
        return node, True
