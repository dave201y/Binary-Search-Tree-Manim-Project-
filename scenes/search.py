from manim import *

from animation.nodes import (
    create_node,
    create_edge,
    highlight_node,
    unhighlight_node,
    highlight_found_node,
)

from animation.paths import create_path_edge

from animation.styles import (
    CURRENT_COLOR,
    FOUND_COLOR,
    NORMAL_TIME,
    PAUSE_TIME,
    TITLE_TEXT_SIZE,
    INFO_TEXT_SIZE,
)


class SearchScene(Scene):

    def construct(self):

        # Title
        title = Text(
            "Search for 40",
            font_size=TITLE_TEXT_SIZE,
        )

        title.to_edge(UP)

        self.play(Write(title))
        self.wait(PAUSE_TIME)

        # Create the BST nodes
        node_50 = create_node(50)
        node_30 = create_node(30)
        node_70 = create_node(70)
        node_20 = create_node(20)
        node_40 = create_node(40)

        # Position the tree
        node_50.move_to(UP * 1.5)

        node_30.move_to(
            node_50.get_center() + LEFT * 2 + DOWN * 1.2
        )

        node_70.move_to(
            node_50.get_center() + RIGHT * 2 + DOWN * 1.2
        )

        node_20.move_to(
            node_30.get_center() + LEFT * 1 + DOWN * 1.2
        )

        node_40.move_to(
            node_30.get_center() + RIGHT * 1 + DOWN * 1.2
        )

        # Create tree edges
        edge_50_30 = create_edge(node_50, node_30)
        edge_50_70 = create_edge(node_50, node_70)
        edge_30_20 = create_edge(node_30, node_20)
        edge_30_40 = create_edge(node_30, node_40)

        # Draw the tree
        self.play(
            Create(edge_50_30),
            Create(edge_50_70),
            Create(edge_30_20),
            Create(edge_30_40),
            FadeIn(node_50),
            FadeIn(node_30),
            FadeIn(node_70),
            FadeIn(node_20),
            FadeIn(node_40),
            run_time=NORMAL_TIME,
        )

        self.wait(PAUSE_TIME)

        # Search information
        search_text = Text(
            "Searching for 40",
            font_size=INFO_TEXT_SIZE,
        )

        search_text.to_edge(DOWN)

        self.play(Write(search_text))
        self.wait(PAUSE_TIME)

        # Step 1: compare 40 with 50
        self.play(
            highlight_node(node_50),
            run_time=NORMAL_TIME,
        )

        comparison_1 = Text(
            "40 < 50  →  LEFT",
            font_size=INFO_TEXT_SIZE,
        )

        comparison_1.next_to(search_text, UP)

        self.play(Write(comparison_1))

        path_1 = create_path_edge(
            node_50,
            node_30,
        )

        self.play(
            Create(path_1),
            run_time=NORMAL_TIME,
        )

        self.wait(PAUSE_TIME)

        self.play(
            FadeOut(comparison_1),
            unhighlight_node(node_50),
        )

        # Step 2: compare 40 with 30
        self.play(
            highlight_node(node_30),
            run_time=NORMAL_TIME,
        )

        comparison_2 = Text(
            "40 > 30  →  RIGHT",
            font_size=INFO_TEXT_SIZE,
        )

        comparison_2.next_to(search_text, UP)

        self.play(Write(comparison_2))

        path_2 = create_path_edge(
            node_30,
            node_40,
        )

        self.play(
            Create(path_2),
            run_time=NORMAL_TIME,
        )

        self.wait(PAUSE_TIME)

        self.play(
            FadeOut(comparison_2),
            unhighlight_node(node_30),
        )

        # Step 3: found 40
        self.play(
            highlight_found_node(node_40),
            run_time=NORMAL_TIME,
        )

        comparison_3 = Text(
            "40 = 40  →  FOUND!",
            font_size=INFO_TEXT_SIZE,
        )

        comparison_3.next_to(search_text, UP)

        self.play(Write(comparison_3))

        self.wait(1)

        self.play(
            FadeOut(search_text),
            FadeOut(comparison_3),
        )

        result = Text(
            "Search complete: 40 found",
            font_size=INFO_TEXT_SIZE,
        )

        result.to_edge(DOWN)

        self.play(Write(result))

        self.wait(2)