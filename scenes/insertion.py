from __future__ import annotations

from manim import DOWN, LEFT, RIGHT, UP, Circle, Create, FadeIn, FadeOut
from manim import Line, Scene, Text, WHITE, YELLOW, Write

from bst import BST, BSTNode


# Change these values to create a different insertion animation.
KEYS = [50, 30, 70, 20, 40]
NODE_RADIUS = 0.32
LEVEL_GAP = 1.25
MIN_HORIZONTAL_GAP = 0.9


def _tree_depth(node: BSTNode[int] | None) -> int:
    if node is None:
        return 0
    return 1 + max(_tree_depth(node.left), _tree_depth(node.right))


def _assign_positions(
    node: BSTNode[int] | None,
    depth: int,
    left: float,
    right: float,
    positions: dict[int, tuple[float, float]],
) -> None:
    if node is None:
        return

    x = (left + right) / 2
    y = 1.8 - depth * LEVEL_GAP
    positions[node.key] = (x, y)
    _assign_positions(node.left, depth + 1, left, x, positions)
    _assign_positions(node.right, depth + 1, x, right, positions)


def _layout(tree: BST) -> dict[int, tuple[float, float]]:
    depth = _tree_depth(tree.root)
    width = max(6.0, (2 ** max(depth - 1, 0)) * MIN_HORIZONTAL_GAP)
    positions: dict[int, tuple[float, float]] = {}
    _assign_positions(tree.root, 0, -width / 2, width / 2, positions)
    return positions


def _node_mobject(value: int, position: tuple[float, float]) -> Circle:
    node = Circle(radius=NODE_RADIUS, color=WHITE)
    node.move_to((*position, 0))
    node.add(Text(str(value), font_size=24))
    return node


class InsertionScene(Scene):
    """Animate building a BST from the configurable ``KEYS`` list."""

    def construct(self):
        if not KEYS:
            raise ValueError("KEYS must contain at least one value.")

        title = Text("Build a Binary Search Tree", font_size=38)
        title.to_edge(UP)
        self.play(Write(title))
        tree = BST()
        displayed_nodes: dict[int, Circle] = {}
        displayed_edges: dict[tuple[int, int], Line] = {}

        for value in KEYS:
            if value in tree:
                continue

            path = tree.search_path(value)
            inserted = tree.insert(value)
            positions = _layout(tree)

            layout_animations = [
                old_mobject.animate.move_to((*positions[key], 0))
                for key, old_mobject in displayed_nodes.items()
            ]
            for (parent_key, child_key), edge in displayed_edges.items():
                layout_animations.append(
                    edge.animate.put_start_and_end_on(
                        (*positions[parent_key], 0),
                        (*positions[child_key], 0),
                    )
                )
            if layout_animations:
                self.play(*layout_animations, run_time=0.4)

            new_mobject = _node_mobject(value, positions[value])
            displayed_nodes[value] = new_mobject

            parent = inserted.parent
            if parent is not None:
                edge = Line(
                    (*positions[parent.key], 0),
                    (*positions[value], 0),
                    color=WHITE,
                )
                displayed_edges[(parent.key, value)] = edge
                self.play(Create(edge), FadeIn(new_mobject))
            else:
                self.play(FadeIn(new_mobject))

            for node in displayed_nodes.values():
                node.set_color(WHITE)

            comparison = Text(f"Insert {value}", font_size=28).to_edge(DOWN)
            self.play(Write(comparison))
            for node_key, direction in path:
                if node_key is not None and direction in {"LEFT", "RIGHT"}:
                    displayed_nodes[node_key].set_color(YELLOW)
                    decision = Text(
                        f"{value} {'<' if direction == 'LEFT' else '>'} "
                        f"{node_key} -> {direction}",
                        font_size=25,
                    ).next_to(comparison, UP)
                    self.play(Write(decision))
                    self.wait(0.4)
                    self.play(FadeOut(decision))
                    displayed_nodes[node_key].set_color(WHITE)
            self.play(FadeOut(comparison))

        result = Text("Insertion complete", font_size=30).to_edge(DOWN)
        self.play(Write(result))
        self.wait(1)
