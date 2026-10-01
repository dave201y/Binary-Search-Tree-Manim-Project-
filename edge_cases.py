"""Person 3: edge case scenes.

Render with:
    manim -pql scenes/edge_cases.py SortedInputDegeneration
"""
from manim import *

from bst import BST  # adjust the import to match Person 1's module
from scenes._p3_tree_view import CaptionMixin, TreeView, tree_height

KEYS = [10, 20, 30, 40, 50, 60, 70]


def height_label(h, color=WHITE):
    return Text(f"Height = {h}", font_size=30, color=color).to_corner(UR, buff=0.5)


class SortedInputDegeneration(CaptionMixin, Scene):
    def construct(self):
        title = Text("Insert sorted input: 10, 20, 30, 40, 50, 60, 70",
                     font_size=30).to_edge(UP)
        self.play(Write(title))

        tree = BST()
        view = TreeView(tree.root, origin=2.2 * UP, x_gap=0.9, y_gap=0.7)
        height = height_label(0)
        self.play(FadeIn(height))

        for key in KEYS:
            tree.insert(key)
            self.say(f"Insert {key}", wait=0.2)
            new_height = height_label(tree_height(tree.root))
            view.relayout(self, tree.root, run_time=0.9,
                          extra=[Transform(height, new_height)])
            self.wait(0.3)

        self.say("The BST degenerates into a linked list.", color=YELLOW)
        self.wait(0.5)
        final = height_label(f"{len(KEYS)} = n", color=YELLOW)
        self.play(Transform(height, final))
        self.say("Worst-case height: O(n).", color=YELLOW, wait=1.5)
