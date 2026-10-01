"""Person 3: deletion scenes.

Render with:
    manim -pql scenes/deletion.py DeletionOverview
    manim -pql scenes/deletion.py LeafAndOneChildDeletion
    manim -pql scenes/deletion.py TwoChildDeletion
"""
from manim import *

from bst import BST  # adjust the import to match Person 1's module
from scenes._p3_tree_view import (
    CaptionMixin, TreeView, highlight, unhighlight, inorder_keys,
)

SAMPLE = [50, 30, 70, 20, 40, 60, 80, 65]
TREE_KW = dict(origin=2.0 * UP, x_gap=1.0, y_gap=0.95)


def build(keys):
    tree = BST()
    for k in keys:
        tree.insert(k)
    return tree


class DeletionOverview(Scene):
    def construct(self):
        title = Text("Delete a Node", font_size=48).to_edge(UP, buff=0.8)
        lines = VGroup(
            Text("Leaf: remove directly.", font_size=34),
            Text("One child: replace with child.", font_size=34),
            Text("Two children: use inorder successor.", font_size=34, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(title, DOWN, buff=0.9)

        self.play(Write(title))
        for line in lines:
            self.play(FadeIn(line, shift=RIGHT * 0.3))
            self.wait(0.6)
        self.play(Indicate(lines[2], color=YELLOW, scale_factor=1.05))
        self.wait(1)


class LeafAndOneChildDeletion(CaptionMixin, Scene):
    def construct(self):
        tree = build(SAMPLE)
        view = TreeView(tree.root, **TREE_KW)
        title = Text("Easy cases", font_size=34).to_edge(UP)
        self.play(Write(title))
        view.show(self)

        # Case 1: leaf (delete 20)
        self.play(highlight(view.nodes[20], RED))
        self.say("Delete 20. It is a leaf, so remove it directly.")
        self.play(FadeOut(view.nodes[20]))
        del view.nodes[20]
        tree.delete(20)
        view.relayout(self, tree.root)

        # Case 2: one child (delete 60, which has only the child 65)
        self.play(highlight(view.nodes[60], RED))
        self.say("Delete 60. It has one child (65), so 65 replaces it.")
        self.play(FadeOut(view.nodes[60]))
        del view.nodes[60]
        tree.delete(60)
        view.relayout(self, tree.root)

        self.say("Inorder: " + " ".join(map(str, inorder_keys(tree.root))))
        self.wait(1)


class TwoChildDeletion(CaptionMixin, Scene):
    def construct(self):
        tree = build(SAMPLE)
        view = TreeView(tree.root, **TREE_KW)
        title = Text("Delete a node with two children", font_size=34).to_edge(UP)
        self.play(Write(title))
        view.show(self)

        # 1-2. Highlight 50 and detect two children
        node50 = view.nodes[50]
        self.play(highlight(node50, YELLOW))
        self.say("Delete 50.")
        self.say("Two children detected.")

        # 3-5. Walk to the smallest value in the right subtree
        self.say("Find inorder successor.")
        pointer = Circle(radius=0.42, color=GREEN, stroke_width=6).move_to(node50)
        self.play(Create(pointer))
        self.play(pointer.animate.move_to(view.nodes[70]))
        self.say("Go right once, then left as far as possible.")
        self.play(pointer.animate.move_to(view.nodes[60]))
        self.say("60 has no left child, so it is the smallest value.")
        self.play(highlight(view.nodes[60], GREEN))
        self.say("Successor = 60.", color=GREEN)

        # 6. Replace 50 with 60
        self.say("Copy 60 into the place of 50.")
        successor_copy = view.nodes[60].copy()
        self.play(
            successor_copy.animate.move_to(node50.get_center()),
            FadeOut(node50),
            FadeOut(pointer),
        )

        # 7. Remove the old successor position (its child 65 moves up)
        self.say("Remove the old 60. Its child 65 takes its place.")
        self.play(FadeOut(view.nodes[60]))
        del view.nodes[50]
        view.nodes[60] = successor_copy
        tree.delete(50)
        view.relayout(self, tree.root, extra=[unhighlight(successor_copy)])

        # 8. Final tree, ordering preserved
        order = inorder_keys(tree.root)
        self.say("Inorder: " + " ".join(map(str, order)) + ". Still sorted.")
        self.say("Left side is smaller than 60, right side is larger.")
        self.wait(1)
