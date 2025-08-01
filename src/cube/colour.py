"""
Rubik's Cube Color System

This module defines the color representation and standard color scheme
for a Rubik's cube. Colors are represented as RGB tuples and mapped
to their corresponding faces in the standard orientation.

Standard Rubik's Cube Color Scheme:
- White: Opposite Yellow (Up/Down faces)
- Green: Opposite Blue (Front/Back faces)  
- Red: Opposite Orange (Right/Left faces)

The initial mapping follows the standard cube orientation where:
- White is Up, Yellow is Down
- Green is Front, Blue is Back
- Red is Right, Orange is Left
"""

from typing import NewType, Tuple


# Type definition for RGB color representation
Colour = NewType("Colour", Tuple[int, int, int])

# Standard Rubik's cube colors as RGB tuples
WHITE = Colour((255, 255, 255))   # Up face
GREEN = Colour((0, 255, 0))       # Front face
ORANGE = Colour((255, 165, 0))    # Left face
YELLOW = Colour((255, 255, 0))    # Down face
BLUE = Colour((0, 0, 255))        # Back face
RED = Colour((255, 0, 0))         # Right face

# Initial face-to-color mapping for a solved cube
# Format: (face_identifier, color)
INITIAL_FACE_COLOUR_MAPPING = [
    ("U", WHITE),   # Up face - White
    ("F", GREEN),   # Front face - Green
    ("L", ORANGE),  # Left face - Orange
    ("B", BLUE),    # Back face - Blue
    ("R", RED),     # Right face - Red
    ("D", YELLOW)   # Down face - Yellow
]