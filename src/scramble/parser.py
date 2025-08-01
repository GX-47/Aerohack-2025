"""
Rubik's Cube Move Notation Parser

This module provides utilities for converting between string-based move notation
and structured Move objects. It handles the standard WCA notation for Rubik's
cube moves and provides bidirectional conversion capabilities.

Standard notation examples:
- "R U R' D2": Normal, Up, Right-prime, Down-double
- "F' L2 B": Front-prime, Left-double, Back

The parser correctly handles:
- Prime notation (') for counter-clockwise moves
- Double notation (2) for 180-degree moves  
- Move sequence inversion for undo operations
"""

from typing import List, Tuple
from ..cube.move import Move


def scramble_to_moves(scramble: str) -> List[Move]:
    """
    Convert a scramble string to a list of Move objects.
    
    Parses standard cube notation and creates structured Move objects
    that can be executed by the cube engine.
    
    Args:
        scramble (str): Space-separated move sequence (e.g., "R U R' D2")
        
    Returns:
        List[Move]: List of Move objects representing the scramble
        
    Examples:
        >>> scramble_to_moves("R U' F2")
        [Move('R', False, False), Move('U', True, False), Move('F', False, True)]
    """
    moves = []

    for move in scramble.split():
        is_prime = "'" in move    # Check for counter-clockwise notation
        is_double = "2" in move   # Check for double-turn notation
        face = move[0]            # Extract face letter (F, R, U, L, B, D)
        
        moves.append(Move(face, is_prime, is_double))

    return moves


def moves_to_scramble(moves: List[Move]) -> str:
    """
    Convert a list of Move objects back to standard notation string.
    
    Takes structured Move objects and creates a human-readable scramble
    string using standard WCA notation.
    
    Args:
        moves (List[Move]): List of Move objects to convert
        
    Returns:
        str: Space-separated move sequence in standard notation
        
    Examples:
        >>> moves = [Move('R', False, False), Move('U', True, False)]
        >>> moves_to_scramble(moves)
        "R U'"
    """
    scramble = []

    for move in moves:
        cur_move = move.face
        
        if move.double:
            cur_move += "2"      # Add double notation
        elif move.invert:
            cur_move += "'"      # Add prime notation

        scramble.append(cur_move)
    
    return " ".join(scramble)


def invert_moves(moves: List[Move]) -> List[Move]:
    """
    Create the inverse sequence of moves for undo operations.
    
    Generates a move sequence that undoes the given moves by:
    - Reversing the order of moves
    - Inverting each move (normal ↔ prime, double stays double)
    
    Args:
        moves (List[Move]): Original move sequence
        
    Returns:
        List[Move]: Inverted move sequence that undoes the original
        
    Examples:
        >>> original = [Move('R', False, False), Move('U', False, False)]
        >>> invert_moves(original)
        [Move('U', True, False), Move('R', True, False)]  # U' R'
    """
    inverted_moves = []

    for move in reversed(moves):
        # Invert the move: normal ↔ prime, double stays the same
        inverted_move = Move(move.face, not move.invert, move.double)
        inverted_moves.append(inverted_move)

    return inverted_moves


if __name__ == "__main__":
    # Example usage and testing
    scramble = "L U2 D B' R2 U2 F R B2 U2 R2 U R2 U2 F2 D R2 D F2"
    print("Example scramble parsing:")
    print(f"Input: {scramble}")
    print(f"Parsed: {scramble_to_moves(scramble)}")