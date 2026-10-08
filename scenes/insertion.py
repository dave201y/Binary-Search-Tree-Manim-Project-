from manim import *

from animation.nodes import (
    create_node,
    create_edge,
    highlight_node,
    unhighlight_node,
)

from animation.paths import create_path_edge

from animation.styles import (
    CURRENT_COLOR,
    NORMAL_TIME,
    PAUSE_TIME,
    TITLE_TEXT_SIZE,
    INFO_TEXT_SIZE,
)


class InsertionScene(Scene):
    """Animate inserting a new node into a BST."""

    def construct(self):
        title = Text(
            "Insert 40 into the BST",
            font_size=TITLE_TEXT_SIZE,
        )
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(PAUSE_TIME)

        # Build the initial BST structure.
        node_50 = create_node(50)
        node_30 = create_node(30)
        node_70 = create_node(70)
        node_20 = create_node(20)

        node_50.move_to(UP * 1.5)
        node_30.move_to(node_50.get_center() + LEFT * 2 + DOWN * 1.2)
        node_70.move_to(node_50.get_center() + RIGHT * 2 + DOWN * 1.2)
        node_20.move_to(node_30.get_center() + LEFT * 1 + DOWN * 1.2)

        edge_50_30 = create_edge(node_50, node_30)
        edge_50_70 = create_edge(node_50, node_70)
        edge_30_20 = create_edge(node_30, node_20)

        self.play(
            Create(edge_50_30),
            Create(edge_50_70),
            Create(edge_30_20),
            FadeIn(node_50),
            FadeIn(node_30),
            FadeIn(node_70),
            FadeIn(node_20),
            run_time=NORMAL_TIME,
        )

        self.wait(PAUSE_TIME)

        info = Text(
            "Inserting 40",
            font_size=INFO_TEXT_SIZE,
        )
        info.to_edge(DOWN)
        self.play(Write(info))
        self.wait(PAUSE_TIME)

        # Compare 40 with the root.
        self.play(highlight_node(node_50), run_time=NORMAL_TIME)
        comparison_1 = Text(
            "40 < 50  →  LEFT",
            font_size=INFO_TEXT_SIZE,
        )
        comparison_1.next_to(info, UP)
        self.play(Write(comparison_1))

        path_1 = create_path_edge(node_50, node_30)
        self.play(Create(path_1), run_time=NORMAL_TIME)
        self.wait(PAUSE_TIME)
        self.play(FadeOut(comparison_1), unhighlight_node(node_50))

        # Compare 40 with 30.
        self.play(highlight_node(node_30), run_time=NORMAL_TIME)
        comparison_2 = Text(
            "40 > 30  →  RIGHT",
            font_size=INFO_TEXT_SIZE,
        )
        comparison_2.next_to(info, UP)
        self.play(Write(comparison_2))

        # We will insert 40 as the right child of 30.
        new_node_40 = create_node(40)
        new_node_40.move_to(node_30.get_center() + RIGHT * 1 + DOWN * 1.2)

        edge_30_40 = create_edge(node_30, new_node_40)

        self.play(
            Create(edge_30_40),
            FadeIn(new_node_40),
            run_time=NORMAL_TIME,
        )

        self.wait(PAUSE_TIME)

        comparison_3 = Text(
            "40 = inserted as the right child of 30",
            font_size=INFO_TEXT_SIZE,
        )
        comparison_3.next_to(info, UP)
        self.play(Transform(comparison_2, comparison_3))
        self.wait(1)

        self.play(
            FadeOut(info),
            FadeOut(comparison_3),
            FadeOut(title),
        )

        result = Text(
            "Insertion complete: 40 added to the tree",
            font_size=INFO_TEXT_SIZE,
        )
        result.to_edge(DOWN)
        self.play(Write(result))
        self.wait(2)

