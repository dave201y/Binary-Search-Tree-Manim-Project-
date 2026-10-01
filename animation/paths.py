from manim import *

from animation.styles import (
    PATH_COLOR,
    NORMAL_TIME,
)


def create_path_edge(start_node, end_node):
    """Create a highlighted path between two BST nodes."""

    return Line(
        start_node.get_center(),
        end_node.get_center(),
        color=PATH_COLOR,
        stroke_width=4,
    )


def animate_move(scene, start_node, end_node):
    """Animate the search moving from one node to the next."""

    path = create_path_edge(start_node, end_node)

    scene.play(
        Create(path),
        run_time=NORMAL_TIME,
    )

    return path


def highlight_path(scene, nodes):
    """Highlight the complete traversal path."""

    path_objects = []

    for i in range(len(nodes) - 1):
        path = create_path_edge(nodes[i], nodes[i + 1])
        path_objects.append(path)

        scene.play(
            Create(path),
            run_time=NORMAL_TIME,
        )

    return VGroup(*path_objects)


def clear_path(scene, path):
    """Remove a highlighted traversal path."""

    scene.play(
        FadeOut(path),
        run_time=NORMAL_TIME,
    )