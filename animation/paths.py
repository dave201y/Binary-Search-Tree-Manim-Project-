"""OWNER: Person 2 -- reusable traversal animation (a pointer that travels, never teleports)."""
from manim import PI, UP, Triangle

from animation.styles import CURRENT_COLOR, NODE_RADIUS

POINTER_OFFSET = 0.35  # gap between the pointer tip and the node


def create_pointer():
    """Small downward-pointing triangle that sits above the current node."""
    return Triangle(color=CURRENT_COLOR, fill_opacity=1).scale(0.18).rotate(PI)


def pointer_position(node):
    return node.get_center() + UP * (NODE_RADIUS + POINTER_OFFSET)


def place_pointer(pointer, node):
    """Put the pointer above a node instantly (use once, at the start)."""
    pointer.move_to(pointer_position(node))
    return pointer


def animate_move(pointer, node):
    """Animation that slides the pointer to a node: scene.play(animate_move(p, n), run_time=T_MOVE)."""
    return pointer.animate.move_to(pointer_position(node))
