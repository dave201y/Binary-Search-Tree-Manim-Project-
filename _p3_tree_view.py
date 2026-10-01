"""Small local drawing helper for Person 3's scenes.

Kept separate so the shared animation framework is untouched. If Person 2's
reusable functions cover the same ground, swap this out during integration.
Assumes tree nodes have .key, .left and .right.
"""
from manim import *

NODE_RADIUS = 0.3
BASE_COLOR = BLUE


def inorder_keys(node):
    return inorder_keys(node.left) + [node.key] + inorder_keys(node.right) if node else []


def tree_height(node):
    return 0 if node is None else 1 + max(tree_height(node.left), tree_height(node.right))


def layout(root, origin=2.5 * UP, x_gap=0.9, y_gap=0.95):
    """x from inorder position, y from depth. Returns {key: position}."""
    order, depths = [], {}

    def walk(node, depth):
        if node is None:
            return
        walk(node.left, depth + 1)
        order.append(node.key)
        depths[node.key] = depth
        walk(node.right, depth + 1)

    walk(root, 0)
    n = len(order)
    return {
        k: np.array([origin[0] + (i - (n - 1) / 2) * x_gap, origin[1] - depths[k] * y_gap, 0.0])
        for i, k in enumerate(order)
    }


def make_node(key, pos):
    circle = Circle(radius=NODE_RADIUS, color=BASE_COLOR, fill_color=BLACK,
                    fill_opacity=1, stroke_width=3)
    label = Text(str(key), font_size=26)
    node = VGroup(circle, label).move_to(pos)
    node.set_z_index(2)
    return node


def highlight(node, color=YELLOW):
    return node[0].animate.set_stroke(color, width=6).set_fill(color, opacity=0.35)


def unhighlight(node):
    return node[0].animate.set_stroke(BASE_COLOR, width=3).set_fill(BLACK, opacity=1)


class TreeView:
    """Draws a BST. Edges follow their nodes through updaters."""

    def __init__(self, root, **layout_kwargs):
        self.kw = layout_kwargs
        self.nodes = {}
        for key, pos in layout(root, **self.kw).items():
            self.nodes[key] = make_node(key, pos)
        self._build_edges(root)

    def _build_edges(self, root):
        self.edges = VGroup()
        stack = [root] if root is not None else []
        while stack:
            node = stack.pop()
            for child in (node.left, node.right):
                if child is not None:
                    self.edges.add(self._edge(node.key, child.key))
                    stack.append(child)

    def _edge(self, parent_key, child_key):
        parent, child = self.nodes[parent_key], self.nodes[child_key]
        line = Line(ORIGIN, RIGHT, stroke_width=3, color=GREY_B)
        line.set_z_index(0)
        line.add_updater(
            lambda m, p=parent, c=child: m.put_start_and_end_on(p.get_center(), c.get_center())
        )
        line.update()
        return line

    def show(self, scene, run_time=1.0):
        anims = [FadeIn(n) for n in self.nodes.values()]
        if len(self.edges) > 0:
            anims.append(FadeIn(self.edges))
        scene.play(*anims, run_time=run_time)

    def relayout(self, scene, new_root, run_time=1.2, extra=()):
        """Animate to the shape of new_root. Missing nodes must be removed from
        self.nodes first; new keys are created and faded in."""
        pos = layout(new_root, **self.kw)
        stale = set(self.nodes) - set(pos)
        if stale:
            raise ValueError(f"Nodes still drawn but not in tree: {sorted(stale)}")
        old_edges = self.edges
        anims = list(extra)
        for key, p in pos.items():
            if key in self.nodes:
                anims.append(self.nodes[key].animate.move_to(p))
            else:
                node = make_node(key, p)
                self.nodes[key] = node
                anims.append(FadeIn(node))
        self._build_edges(new_root)
        if len(old_edges) > 0:
            anims.append(FadeOut(old_edges))
        if len(self.edges) > 0:
            anims.append(FadeIn(self.edges))
        scene.play(*anims, run_time=run_time)


class CaptionMixin:
    """Gives a scene say(text), which swaps the caption at the bottom."""

    _caption = None

    def say(self, text, color=WHITE, run_time=0.5, wait=0.8):
        new = Text(text, font_size=30, color=color).to_edge(DOWN, buff=0.5)
        if self._caption is not None:
            self.play(FadeOut(self._caption), FadeIn(new), run_time=run_time)
        else:
            self.play(FadeIn(new), run_time=run_time)
        self._caption = new
        self.wait(wait)
