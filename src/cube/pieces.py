"""
Rubik's Cube Piece Definitions and Mapping

This module defines the individual pieces of a Rubik's cube (corners and edges)
and provides mapping dictionaries to convert any piece position to a standard
reference position for analysis.

Corner pieces have 3 stickers, edge pieces have 2 stickers.
The mapping sequences move each piece to a standard position:
- All edges are moved to the UF (Up-Front) position
- All corners are moved to the UFR (Up-Front-Right) position

This standardization allows for consistent piece analysis and solving algorithms.
"""

from typing import NewType, Dict, Literal
from .colour import Colour


# Type definitions for cube pieces
Corner = NewType("Corner", Dict[str, Colour])
Edge = NewType("Edge", Dict[str, Colour])


# Move sequences to bring each edge piece to the UF (Up-Front) position
# Format: "piece_position": "move_sequence"
EDGE_TO_UF = {
    "UF": "U2 U2",     # Already in position (no-op moves)
    "UL": "U'",        # Up-Left to Up-Front
    "UR": "U",         # Up-Right to Up-Front  
    "UB": "U2",        # Up-Back to Up-Front
    "LB": "L2 F",      # Left-Back to Up-Front
    "LD": "L' F",      # Left-Down to Up-Front
    "LF": "F",         # Left-Front to Up-Front
    "RB": "R2 F'",     # Right-Back to Up-Front
    "RD": "R F'",      # Right-Down to Up-Front
    "RF": "F'",        # Right-Front to Up-Front
    "DB": "D2 F2",     # Down-Back to Up-Front
    "DF": "F2"         # Down-Front to Up-Front
}


# Move sequences to bring each corner piece to the UFR (Up-Front-Right) position
# Format: "piece_position": "move_sequence"  
CORNER_TO_UFR = {
    "UFR": "U2 U2",    # Already in position (no-op moves)
    "DFR": "R",        # Down-Front-Right to Up-Front-Right
    "DBR": "R2",       # Down-Back-Right to Up-Front-Right
    "URB": "U",        # Up-Right-Back to Up-Front-Right
    "ULF": "U'",       # Up-Left-Front to Up-Front-Right
    "UBL": "U2",       # Up-Back-Left to Up-Front-Right
    "DFL": "L' U'",    # Down-Front-Left to Up-Front-Right
    "DBL": "L2 U'"     # Down-Back-Left to Up-Front-Right
}
