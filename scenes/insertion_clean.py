from manim import *
import numpy as np

KEYS = [50, 30, 70, 20, 40]


class InsertionScene(Scene):
    def construct(self):
        self.camera.background_color = "#101820"

        title = Text(
            "Build a Binary Search Tree",
            font_size=40,
            weight=BOLD
        ).to_edge(UP, buff=0.3)

        subtitle = Text(
            "Smaller keys go left | Larger keys go right",
            font_size=23,
            color=BLUE_A
        ).next_to(title, DOWN, buff=0.18)

        self.play(Write(title), FadeIn(subtitle), run_time=1.5)

        # Plan the tree layout so existing nodes stay in place.
        children = {}
        unique_keys = list(dict.fromkeys(KEYS))
        root = unique_keys[0] if unique_keys else None

        for key in unique_keys:
            children[key] = [None, None]

            if key == root:
                continue

            current = root

            while True:
                if key < current:
                    side = 0
                else:
                    side = 1

                if children[current][side] is None:
                    children[current][side] = key
                    break

                current = children[current][side]

        positions = {}
        depths = {}

        def layout(key, depth, left, right):
            if key is None:
                return

            x = (left + right) / 2
            positions[key] = np.array([x, 0.0, 0.0])
            depths[key] = depth

            layout(children[key][0], depth + 1, left, x)
            layout(children[key][1], depth + 1, x, right)

        layout(root, 0, -5.6, 0.6)

        deepest = max(depths.values(), default=0)
        level_gap = min(1.3, 3.7 / max(deepest, 1))

        for key in positions:
            positions[key][1] = 1.3 - depths[key] * level_gap

        points = list(positions.values())
        smallest_distance = min(
            (
                np.linalg.norm(points[i] - points[j])
                for i in range(len(points))
                for j in range(i + 1, len(points))
            ),
            default=1.5
        )

        radius = min(0.34, smallest_distance * 0.32)

        # Right-side heading, with no surrounding box.
        heading = Text(
            "INSERTION",
            font_size=24,
            color=BLUE_A
        ).move_to([3.6, 1.95, 0])

        input_label = Text(
            "Input: " + ", ".join(map(str, KEYS)),
            font_size=22,
            color=GRAY_B
        ).to_edge(DOWN, buff=0.35)

        if input_label.width > 12.5:
            input_label.scale_to_fit_width(12.5)

        self.play(FadeIn(heading), FadeIn(input_label))

        # Every new line stays on screen.
        history = VGroup()
        expected_lines = len(KEYS) + sum(depths.values()) + 1
        line_gap = min(0.43, 4.55 / max(expected_lines - 1, 1))
        text_size = min(24, line_gap * 54)

        def add_line(message, color=YELLOW):
            line = Text(
                message,
                font_size=text_size,
                color=color
            )

            if line.width > 5.1:
                line.scale_to_fit_width(5.1)

            line.move_to([
                0.95 + line.width / 2,
                1.45 - len(history) * line_gap,
                0
            ])

            history.add(line)
            self.play(Write(line), run_time=0.5)
            self.wait(1)

        nodes = {}
        edges = {}
        inserted = set()

        for key in KEYS:
            add_line(f"INSERT {key}", GREEN)

            if key in inserted:
                add_line(f"{key} already exists: skip")
                continue

            parent = None
            current = root if inserted else None

            # Show comparisons before placing the new node.
            while current is not None:
                node = nodes[current]

                self.play(
                    node[0].animate.set_stroke(YELLOW, width=5),
                    run_time=0.4
                )

                if key < current:
                    side = 0
                    add_line(f"{key} < {current}: go LEFT")
                else:
                    side = 1
                    add_line(f"{key} > {current}: go RIGHT")

                child = children[current][side]

                if child in inserted:
                    self.play(
                        edges[(current, child)].animate.set_color(YELLOW),
                        run_time=0.5
                    )

                self.play(
                    node[0].animate.set_stroke(BLUE_B, width=3),
                    run_time=0.4
                )

                parent = current
                current = child if child in inserted else None

            circle = Circle(
                radius=radius,
                stroke_color=BLUE_B,
                stroke_width=3,
                fill_color=BLUE_E,
                fill_opacity=1
            )

            number = Text(str(key), font_size=28)

            if number.width > radius * 1.5:
                number.scale_to_fit_width(radius * 1.5)

            # Move the circle and its centered number together.
            node = VGroup(circle, number)
            node.move_to(positions[key])
            node.set_z_index(2)
            nodes[key] = node

            if parent is not None:
                edge = Line(
                    nodes[parent].get_center(),
                    node.get_center(),
                    buff=radius,
                    color=GRAY_B,
                    stroke_width=3
                ).set_z_index(0)

                edges[(parent, key)] = edge
                self.play(Create(edge), run_time=0.7)

            self.play(
                FadeIn(node, shift=UP * 0.25),
                run_time=0.7
            )

            inserted.add(key)
            self.wait(0.8)

            if edges:
                self.play(
                    *[
                        edge.animate.set_color(GRAY_B)
                        for edge in edges.values()
                    ],
                    run_time=0.3
                )

        add_line("Insertion complete", GREEN)
        self.wait(3)