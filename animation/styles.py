"""OWNER: Person 2 -- one visual language for every scene (colors, sizes, timing).
Person 1 and Person 3: import from here instead of hard-coding values."""
from manim import BLUE_D, GRAY, GREEN, RED, WHITE, YELLOW

# Colors
NODE_FILL = BLUE_D
NODE_OUTLINE = WHITE
CURRENT_COLOR = YELLOW      # node/edge we are looking at right now
FOUND_COLOR = GREEN         # successful result
NOT_FOUND_COLOR = RED       # failed result
EDGE_COLOR = GRAY
TEXT_COLOR = WHITE

# Sizes
NODE_RADIUS = 0.4
NODE_FONT_SIZE = 30
TITLE_FONT_SIZE = 44
BODY_FONT_SIZE = 28
LABEL_FONT_SIZE = 22
OUTLINE_WIDTH = 2
HIGHLIGHT_WIDTH = 8

# Tree layout spacing
X_GAP = 1.3
Y_GAP = 1.2

# Timing (seconds) -- use these so every scene feels the same
T_FAST = 0.5       # routine step
T_MOVE = 0.8       # pointer travelling along an edge
T_PAUSE = 1.0      # let the viewer read a decision
T_EMPHASIS = 1.5   # final result
