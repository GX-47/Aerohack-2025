"""
Rubik's Cube Move Representation

This module defines the Move class which represents a single move operation
on a Rubik's cube using standard notation (F, R, U, L, B, D).

Move notation:
- F, R, U, L, B, D: Basic 90-degree clockwise rotations
- F', R', U', L', B', D': Counter-clockwise (inverse) rotations  
- F2, R2, U2, L2, B2, D2: 180-degree (double) rotations

The Move class encapsulates these variations in a simple data structure.
"""

from dataclasses import dataclass


@dataclass
class Move:
    """
    Represents a single move operation on a Rubik's cube.
    
    Attributes:
        face (str): The face to rotate (F, R, U, L, B, D, or y for cube rotation)
        invert (bool): True for counter-clockwise rotation (prime notation)
        double (bool): True for 180-degree rotation (2 notation)
    
    Examples:
        Move("R", False, False) -> R (90° clockwise)
        Move("U", True, False) -> U' (90° counter-clockwise) 
        Move("F", False, True) -> F2 (180°)
    """
    face: str
    invert: bool
    double: bool