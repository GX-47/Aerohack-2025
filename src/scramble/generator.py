"""
Rubik's Cube Scramble Generator

This module provides functions to generate random scramble sequences for
Rubik's cube practice and testing. Scrambles use standard WCA notation
and create sufficiently randomized cube states for solving practice.

The generator creates sequences of 40 moves using:
- Basic moves: F, R, U, L, B, D (90° clockwise)
- Double moves: F2, R2, U2, L2, B2, D2 (180°)
- Prime moves: F', R', U', L', B', D' (90° counter-clockwise)

Generated scrambles follow competition standards and provide good
randomization for cube solving practice.
"""

from typing import List
import random


def gen_n_scrambles(n: int) -> List[str]:
    """
    Generate multiple random scramble sequences.
    
    Args:
        n (int): Number of scrambles to generate
        
    Returns:
        List[str]: List of scramble strings in standard notation
    """
    scrambles = []

    for _ in range(n):
        scrambles.append(gen_scramble())

    return scrambles


def gen_scramble() -> str:
    """
    Generate a single random scramble sequence.
    
    Creates a 40-move scramble using standard Rubik's cube notation.
    The sequence uses random face rotations with random modifiers
    (normal, double, or prime moves).
    
    Returns:
        str: Scramble sequence in standard notation (e.g., "R U R' D2 F")
        
    Note:
        - Uses all 6 faces: U(p), R(ight), L(eft), B(ack), D(own), F(ront)
        - Includes normal (90°), double (180°), and prime (270°) rotations
        - 40 moves provides sufficient randomization for practice
    """
    # Standard cube face notation
    moves = ["U", "R", "L", "B", "D", "F"]
    scramble = []

    for _ in range(40):
        # Generate random move type (0-3 for better distribution)
        rand_num = random.randint(0, 3)

        if rand_num == 0:
            # Normal 90-degree move
            scramble.append(random.choice(moves))
        elif rand_num == 1:
            # 180-degree double move
            scramble.append(random.choice(moves) + "2")
        else:
            # 90-degree counter-clockwise (prime) move
            scramble.append(random.choice(moves) + "'")

    return " ".join(scramble)
