from manim import *
from scenes.insertion_clean import InsertionScene
from scenes.search import SearchScene
from deletion import TwoChildDeletion
from _p3_tree_view import CaptionMixin


class BSTDemo(CaptionMixin, Scene):
    def construct(self):
        self.camera.background_color = "#101820"

        title = Text(
            "Binary Search Trees",
            font_size=44,
            weight=BOLD
        )

        subtitle = Text(
            "Build, search, and delete",
            font_size=28,
            color=BLUE_A
        ).next_to(title, DOWN)

        introduction = VGroup(title, subtitle)
        introduction.move_to(ORIGIN)

        self.play(Write(title), FadeIn(subtitle))
        self.wait(4)
        self.play(FadeOut(introduction))

        def explain(heading, lines):
            heading_text = Text(
                heading,
                font_size=36,
                color=BLUE_A
            )

            body = VGroup(*[
                Text(line, font_size=25)
                for line in lines
            ]).arrange(DOWN, buff=0.35)

            card = VGroup(
                heading_text,
                body
            ).arrange(DOWN, buff=0.6)

            if card.width > 12:
                card.scale_to_fit_width(12)

            card.move_to(ORIGIN)

            self.play(FadeIn(card), run_time=1)
            self.wait(10)
            self.play(FadeOut(card), run_time=1)

        def clear_phase():
            self.wait(1)
            self.play(*[
                FadeOut(item)
                for item in list(self.mobjects)
            ])
            self.clear()

        # 1. Insertion.
        explain("Insertion", [
            "Start at the root and compare the new key.",
            "A smaller key goes left; a larger key goes right.",
            "Insert when the chosen child position is empty."
        ])

        InsertionScene.construct(self)
        clear_phase()

        # 2. Search.
        explain("Search", [
            "Each comparison selects one subtree to explore.",
            "An equal key means the search succeeds.",
            "An empty branch means the key is not present."
        ])

        SearchScene.construct(self)
        clear_phase()

        # 3. Deletion.
        explain("Deletion", [
            "A leaf can be removed directly.",
            "A node with one child is replaced by that child.",
            "With two children, use the smallest key",
            "in the right subtree: the inorder successor."
        ])

        self._caption = None
        TwoChildDeletion.construct(self)
        self.wait(3)