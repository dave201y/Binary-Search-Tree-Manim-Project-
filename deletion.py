"""Person 3: deletion scenes.

Render with:
    manim -pql scenes/deletion.py DeletionOverview
    manim -pql scenes/deletion.py LeafAndOneChildDeletion
    manim -pql scenes/deletion.py TwoChildDeletion
"""
from manim import *

from demo_config import KEYS, DELETE_KEY
from bst import BST  # adjust the import to match Person 1's module
from _p3_tree_view import (
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
        self._caption = None

        tree = build(KEYS)
        view = TreeView(tree.root, **TREE_KW)

        title = Text(
            f"Delete {DELETE_KEY}",
            font_size=34
        ).to_edge(UP)

        self.play(Write(title))
        view.show(self)

        target = tree.search(DELETE_KEY)

        if target is None:
            self.say(
                f"{DELETE_KEY} is not in the tree. Nothing changes."
            )
            self.wait(2)
            return

        target_visual = view.nodes[DELETE_KEY]
        self.play(highlight(target_visual, YELLOW))
        self.say(f"Delete {DELETE_KEY}.")

        # Case 1: no children.
        if target.left is None and target.right is None:
            self.say("This node is a leaf. Remove it directly.")

            self.play(FadeOut(target_visual))
            del view.nodes[DELETE_KEY]

            tree.delete(DELETE_KEY)
            view.relayout(self, tree.root)

        # Case 2: one child.
        elif target.left is None or target.right is None:
            child = target.left or target.right

            self.say(
                f"One child: {child.key} takes its place."
            )

            self.play(FadeOut(target_visual))
            del view.nodes[DELETE_KEY]

            tree.delete(DELETE_KEY)
            view.relayout(self, tree.root)

        # Case 3: two children.
        else:
            self.say(
                f"{DELETE_KEY} has two children."
            )
            self.say(
                "Find the smallest key in its right subtree."
            )

            pointer = Circle(
                radius=0.42,
                color=GREEN,
                stroke_width=6
            ).move_to(target_visual)

            self.play(Create(pointer))

            successor = target.right

            self.play(
                pointer.animate.move_to(
                    view.nodes[successor.key]
                )
            )
            self.say(
                "Go right once, then left as far as possible."
            )

            while successor.left is not None:
                successor = successor.left

                self.play(
                    pointer.animate.move_to(
                        view.nodes[successor.key]
                    )
                )

            successor_key = successor.key
            successor_child = successor.right

            self.play(
                highlight(view.nodes[successor_key], GREEN)
            )
            self.say(
                f"Successor = {successor_key}.",
                color=GREEN
            )
            self.say(
                f"{successor_key} replaces {DELETE_KEY}."
            )

            successor_copy = view.nodes[successor_key].copy()

            self.play(
                successor_copy.animate.move_to(
                    target_visual.get_center()
                ),
                FadeOut(target_visual),
                FadeOut(pointer)
            )

            if successor_child is None:
                self.say(
                    f"Remove {successor_key}'s old position."
                )
            else:
                self.say(
                    f"Its child {successor_child.key} "
                    "takes the old successor position."
                )

            self.play(
                FadeOut(view.nodes[successor_key])
            )

            del view.nodes[DELETE_KEY]
            view.nodes[successor_key] = successor_copy

            tree.delete(DELETE_KEY)

            view.relayout(
                self,
                tree.root,
                extra=[unhighlight(successor_copy)]
            )

        order = inorder_keys(tree.root)

        self.say(
            "Inorder: "
            + ", ".join(map(str, order))
            + ". Still sorted."
        )
        self.say("Deletion complete.")
        self.wait(2)