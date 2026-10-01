"""OWNER: Person 2 -- reusable node / edge / highlight / status-panel visuals.

A "tree" here is anything with .key, .left, .right (Person 1's Node works).
Functions that end in an animation return something you pass to scene.play(...).
"""
import numpy as np
from manim import (DOWN, GRAY, LEFT, RIGHT, UP, Circle, Line, RoundedRectangle,
                   Text, Transform, VGroup)

from animation.styles import (CURRENT_COLOR, EDGE_COLOR, FOUND_COLOR,
                              HIGHLIGHT_WIDTH, LABEL_FONT_SIZE, NODE_FILL,
                              NODE_FONT_SIZE, NODE_OUTLINE, NODE_RADIUS,
                              OUTLINE_WIDTH, TEXT_COLOR, X_GAP, Y_GAP,
                              BODY_FONT_SIZE)


# ---------- building blocks ----------
def create_node(key):
    """A circle with the key inside. node[0] is the circle, node[1] the label."""
    circle = Circle(radius=NODE_RADIUS, color=NODE_OUTLINE,
                    stroke_width=OUTLINE_WIDTH, fill_color=NODE_FILL,
                    fill_opacity=1)
    label = Text(str(key), font_size=NODE_FONT_SIZE, color=TEXT_COLOR)
    node = VGroup(circle, label)
    node.key = key
    return node


def create_edge(parent_node, child_node):
    """Line that stops at the circle borders instead of the centers."""
    return Line(parent_node.get_center(), child_node.get_center(),
                buff=NODE_RADIUS, color=EDGE_COLOR, stroke_width=3)


def layout_tree(root, center=UP):
    """Return {key: position}. x = in-order index, y = depth (so nothing overlaps)."""
    slots = {}
    counter = [0]

    def walk(node, depth):
        if node is None:
            return
        walk(node.left, depth + 1)
        slots[node.key] = (counter[0], depth)
        counter[0] += 1
        walk(node.right, depth + 1)

    walk(root, 0)
    total = counter[0]
    return {
        key: center + np.array([(i - (total - 1) / 2) * X_GAP, -d * Y_GAP, 0.0])
        for key, (i, d) in slots.items()
    }


def build_tree(root, center=LEFT * 1.5 + UP):
    """Draw a whole tree once.
    Returns (tree_group, node_map, edge_map):
      node_map[key] -> node,  edge_map[(parent_key, child_key)] -> edge.
    Build it once, then highlight/move -- never redraw the tree per comparison."""
    positions = layout_tree(root, center)
    node_map = {key: create_node(key).move_to(pos)
                for key, pos in positions.items()}

    edge_map = {}

    def link(node):
        if node is None:
            return
        for child in (node.left, node.right):
            if child is not None:
                edge_map[(node.key, child.key)] = create_edge(
                    node_map[node.key], node_map[child.key])
                link(child)

    link(root)
    tree = VGroup(*edge_map.values(), *node_map.values())  # edges first = behind nodes
    return tree, node_map, edge_map


# ---------- highlighting (each returns an animation for scene.play) ----------
def highlight_node(node):
    return node[0].animate.set_stroke(CURRENT_COLOR, width=HIGHLIGHT_WIDTH)


def unhighlight_node(node):
    return node[0].animate.set_stroke(NODE_OUTLINE, width=OUTLINE_WIDTH)


def mark_found(node):
    return node[0].animate.set_fill(FOUND_COLOR).set_stroke(FOUND_COLOR, width=HIGHLIGHT_WIDTH)


def highlight_edge(edge):
    return edge.animate.set_color(CURRENT_COLOR)


# ---------- text helpers (return mobjects; you FadeIn / Write them) ----------
def show_decision(node, key, direction):
    """Small label beside a node: '40 < 50' (LEFT), '40 > 50' (RIGHT), '40 = 40' (FOUND).
    Sits to the side so it never covers the tree."""
    symbol = {"LEFT": "<", "RIGHT": ">", "FOUND": "="}[direction]
    label = Text(f"{key} {symbol} {node.key}", font_size=LABEL_FONT_SIZE,
                 color=CURRENT_COLOR)
    side = LEFT if direction == "LEFT" else RIGHT
    return label.move_to(node.get_center() + side * 1.1)


def show_result(message, color=FOUND_COLOR):
    """Result line at the bottom of the screen."""
    return Text(message, font_size=BODY_FONT_SIZE, color=color).to_edge(DOWN)


# ---------- status panel ----------
class StatusPanel(VGroup):
    """Small box:  CURRENT OPERATION / Key / Compare / Decision.
    Create it once, move it with .to_corner(UR), then update with update_text()."""

    WIDTH = 4.0
    HEIGHT = 2.0

    def __init__(self, operation, key):
        super().__init__()
        self.operation = operation
        self.key = key
        self.box = RoundedRectangle(corner_radius=0.15, width=self.WIDTH,
                                    height=self.HEIGHT, color=GRAY)
        self.lines = self._make_lines("-", "-")
        self.add(self.box, self.lines)

    def _make_lines(self, compare, decision):
        rows = VGroup(
            Text("CURRENT OPERATION", font_size=18, color=GRAY),
            Text(f"{self.operation} key: {self.key}", font_size=24),
            Text(f"Compare: {compare}", font_size=24),
            Text(f"Decision: {decision}", font_size=24, color=CURRENT_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        rows.align_to(self.box, LEFT).shift(RIGHT * 0.3)
        rows.match_y(self.box)
        return rows

    def update_text(self, compare="-", decision="-"):
        """Returns an animation that changes the text in place (no new panel)."""
        return Transform(self.lines, self._make_lines(compare, decision))
