"""OWNER: Person 2 -- "2. Search for a Key" scene.
Render:  manim -pql scenes/search.py SearchScene
"""
from manim import (DOWN, UL, UR, FadeIn, FadeOut, Scene, Text, Write)

from animation.nodes import (StatusPanel, build_tree, highlight_edge,
                             highlight_node, mark_found, show_decision,
                             show_result, unhighlight_node)
from animation.paths import animate_move, create_pointer, place_pointer
from animation.styles import (BODY_FONT_SIZE, CURRENT_COLOR, NOT_FOUND_COLOR,
                              T_EMPHASIS, T_FAST, T_MOVE, T_PAUSE,
                              TITLE_FONT_SIZE)

# Demo inputs -- must match the team's storyboard.
# (The guide's example is keys 50,30,70,20,40,60,65 and SEARCH_KEY = 65.)
DEMO_KEYS = [50, 30, 70, 20, 40]
SEARCH_KEY = 40


# ---------------------------------------------------------------------------
# TEMPORARY stand-in until Person 1's BST is merged into main.
# Contract we need from Person 1:
#   tree.root                -> node with .key / .left / .right
#   tree.search(key)         -> list of (node_key, direction), direction is
#                               "LEFT" | "RIGHT" | "FOUND";
#                               if the key is missing, end with (None, "NOT_FOUND")
# When it is merged, delete the TEMP block and use the commented lines instead.
# ---------------------------------------------------------------------------
class _TempNode:
    def __init__(self, key):
        self.key, self.left, self.right = key, None, None


def _temp_build(keys):
    root = None
    for key in keys:
        if root is None:
            root = _TempNode(key)
            continue
        cur = root
        while True:
            side = "left" if key < cur.key else "right"
            nxt = getattr(cur, side)
            if nxt is None:
                setattr(cur, side, _TempNode(key))
                break
            cur = nxt
    return root


def _temp_search(root, key):
    steps, cur = [], root
    while cur is not None:
        if key == cur.key:
            steps.append((cur.key, "FOUND"))
            return steps
        direction = "LEFT" if key < cur.key else "RIGHT"
        steps.append((cur.key, direction))
        cur = cur.left if direction == "LEFT" else cur.right
    steps.append((None, "NOT_FOUND"))
    return steps


def get_tree_and_path(keys, target):
    # from bst.tree import BST
    # tree = BST()
    # for k in keys:
    #     tree.insert(k)
    # return tree.root, tree.search(target)
    root = _temp_build(keys)
    return root, _temp_search(root, target)


# ---------------------------------------------------------------------------
class SearchScene(Scene):
    def construct(self):
        root, path = get_tree_and_path(DEMO_KEYS, SEARCH_KEY)

        # 1. Title
        title = Text("2. Search for a Key", font_size=TITLE_FONT_SIZE)
        self.play(Write(title))
        self.wait(T_PAUSE)
        subtitle = Text(f"Searching for {SEARCH_KEY}", font_size=BODY_FONT_SIZE,
                        color=CURRENT_COLOR).to_corner(UL)
        self.play(FadeOut(title), FadeIn(subtitle))

        # 2. Tree + panel + pointer (drawn once, then only highlighted)
        tree, node_map, edge_map = build_tree(root)
        panel = StatusPanel("Search", SEARCH_KEY).to_corner(UR)
        self.play(FadeIn(tree, shift=DOWN * 0.2), FadeIn(panel))

        pointer = create_pointer()
        place_pointer(pointer, node_map[path[0][0]])
        self.play(FadeIn(pointer))

        # 3. Follow the real comparison path
        prev_key = None
        for node_key, direction in path:
            if node_key is None:  # fell off the tree
                self.play(panel.update_text("-", "NOT FOUND"), run_time=T_FAST)
                result = show_result(f"{SEARCH_KEY} is not in the tree", NOT_FOUND_COLOR)
                self.play(Write(result))
                break

            node = node_map[node_key]
            if prev_key is not None:  # travel down the edge, don't teleport
                self.play(animate_move(pointer, node),
                          unhighlight_node(node_map[prev_key]),
                          highlight_edge(edge_map[(prev_key, node_key)]),
                          run_time=T_MOVE)

            # compare
            self.play(highlight_node(node),
                      panel.update_text(f"{SEARCH_KEY} vs {node_key}"),
                      run_time=T_FAST)

            # decide
            label = show_decision(node, SEARCH_KEY, direction)
            self.play(panel.update_text(f"{SEARCH_KEY} vs {node_key}", direction),
                      FadeIn(label), run_time=T_FAST)
            self.wait(T_PAUSE)
            self.play(FadeOut(label), run_time=T_FAST)

            if direction == "FOUND":
                result = show_result(f"FOUND! {SEARCH_KEY} is in the tree")
                self.play(mark_found(node), Write(result))
                break
            prev_key = node_key

        self.wait(T_EMPHASIS)
