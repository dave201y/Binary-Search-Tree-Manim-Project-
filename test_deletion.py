import random
from bst import BST  # adjust the import to match Person 1's module


def build(keys):
    t = BST()
    for k in keys:
        t.insert(k)
    return t


def inorder(node):
    return inorder(node.left) + [node.key] + inorder(node.right) if node else []


def height(node):
    return 0 if node is None else 1 + max(height(node.left), height(node.right))


def is_valid_bst(node, lo=float("-inf"), hi=float("inf")):
    if node is None:
        return True
    if not (lo < node.key < hi):
        return False
    return is_valid_bst(node.left, lo, node.key) and is_valid_bst(node.right, node.key, hi)


SAMPLE = [50, 30, 70, 20, 40, 60, 80, 65]


def test_delete_leaf():
    t = build(SAMPLE)
    assert t.delete(20) is True
    assert t.root.left.left is None
    assert inorder(t.root) == [30, 40, 50, 60, 65, 70, 80]


def test_delete_one_child():
    t = build(SAMPLE)
    assert t.delete(60) is True
    assert t.root.right.left.key == 65
    assert inorder(t.root) == [20, 30, 40, 50, 65, 70, 80]


def test_delete_two_children():
    t = build(SAMPLE)
    assert t.delete(70) is True
    assert t.root.right.key == 80  # successor of 70 is 80
    assert inorder(t.root) == [20, 30, 40, 50, 60, 65, 80]
    assert is_valid_bst(t.root)


def test_delete_root_two_children():
    t = build(SAMPLE)
    assert t.delete(50) is True
    assert t.root.key == 60
    assert t.root.right.left.key == 65
    assert inorder(t.root) == [20, 30, 40, 60, 65, 70, 80]


def test_delete_root_one_child():
    t = build([10, 20, 30])
    assert t.delete(10) is True
    assert t.root.key == 20


def test_delete_only_node():
    t = build([5])
    assert t.delete(5) is True
    assert t.root is None


def test_delete_missing_key():
    t = build(SAMPLE)
    before = inorder(t.root)
    assert t.delete(999) is False
    assert inorder(t.root) == before


def test_delete_from_empty_tree():
    t = BST()
    assert t.delete(1) is False
    assert t.root is None


def test_inorder_stays_sorted_after_random_deletes():
    rng = random.Random(7)
    keys = rng.sample(range(1000), 60)
    t = build(keys)
    remaining = set(keys)
    for k in rng.sample(keys, 40):
        assert t.delete(k) is True
        remaining.discard(k)
        result = inorder(t.root)
        assert result == sorted(remaining)
        assert is_valid_bst(t.root)


def test_inorder_successor():
    t = build(SAMPLE)
    assert t.inorder_successor(50).key == 60   # min of right subtree
    assert t.inorder_successor(40).key == 50   # no right child, ancestor
    assert t.inorder_successor(80) is None     # largest key
    assert t.inorder_successor(999) is None    # missing key


def test_sorted_input_is_right_skewed():
    t = build([10, 20, 30, 40, 50, 60, 70])
    assert height(t.root) == 7
    node = t.root
    while node is not None:
        assert node.left is None
        node = node.right
