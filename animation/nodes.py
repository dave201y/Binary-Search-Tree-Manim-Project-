# Person 2: reusable node/edge/highlight visuals
from manim import *

from animation.styles import (
    NODE_RADIUS,
    NODE_STROKE_WIDTH,
    NODE_COLOR,
    EDGE_COLOR,
    CURRENT_COLOR,
    FOUND_COLOR,
    NODE_TEXT_SIZE,
)


def create_node(key):
    """Create one BST node with a circle and key label."""

    circle = Circle(
        radius=NODE_RADIUS,
        color=NODE_COLOR,
        stroke_width=NODE_STROKE_WIDTH,
    )

    label = Text(
        str(key),
        font_size=NODE_TEXT_SIZE,
    )

    label.move_to(circle.get_center())

    node = VGroup(circle, label)

    # Store the key so the animation can identify the node.
    node.key = key

    return node


def create_edge(start_node, end_node):
    """Create an edge between two BST nodes."""

    return Line(
        start_node.get_center(),
        end_node.get_center(),
        color=EDGE_COLOR,
        stroke_width=NODE_STROKE_WIDTH,
    )


def highlight_node(node):
    """Highlight the node currently being examined."""

    return node[0].animate.set_stroke(
        color=CURRENT_COLOR,
        width=NODE_STROKE_WIDTH + 2,
    )


def unhighlight_node(node):
    """Return a node to its normal appearance."""

    return node[0].animate.set_stroke(
        color=NODE_COLOR,
        width=NODE_STROKE_WIDTH,
    )


def highlight_found_node(node):
    """Highlight the node when the search key is found."""

    return node[0].animate.set_stroke(
        color=FOUND_COLOR,
        width=NODE_STROKE_WIDTH + 3,
    )