# Binary Search Tree Manim Project

A Manim animation that teaches binary search tree
insertion, searching and deletion through comparisons, highlights
and explanations on screen.

## Setup

Install the project's Python dependencies:

```bash
python -m pip install -r requirements.txt
```

A working local Manim installation is required.

Run all commands from the repository root.

## Main Example

Set `demo_config.py` to:

```python
KEYS = [50, 30, 70, 20, 40]
SEARCH_KEY = 40
DELETE_KEY = 30
```

The animation builds the tree, searches for 40, and deletes 30.
Because 30 has two children, its inorder successor, 40, replaces it.

Render the complete animation:

```bash
python -m manim -pqh bst_demo.py BSTDemo -o "BST Final Demo"
```

The main presentation video runs approximately 2 minutes.

## Alternate Edge-Case Example

Change `demo_config.py` to:

```python
KEYS = [50, 30, 70, 20, 40, 60, 80, 65]
SEARCH_KEY = 65
DELETE_KEY = 50
```

Deleting 50 uses inorder successor 60. The successor's child,
65, reconnects at 60's former position, preserving BST ordering.

Render using the same code:

```bash
python -m manim -pql bst_demo.py BSTDemo -o "BST Edge Case Demo"
```

Restored the main example inputs afterward.

## Project Structure

- `bst_demo.py`: complete animation.
- `demo_config.py`: shared input parameters.
- `bst/`: BST data structure and operations.
- `scenes/insertion_clean.py`: insertion animation.
- `scenes/search.py`: search animation.
- `animation/`: shared search visuals, styles, and pointer helpers.
- `deletion.py`: deletion animations.
- `_p3_tree_view.py`: deletion visualization helpers.
- `test_deletion.py`: BST tests.

## Contributions

- `Person-1`: BST implementation and insertion foundation.
- `feature/search-animation`: search animation and visual helpers.
- `Person-3`: deletion animations, edge-case scene, and BST tests.
  
Git history records the original work and integration commits.

## Generated Files

Rendered videos are stored under `media/videos/`.
Videos and Python caches are excluded from version control.
