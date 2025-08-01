"""
Rubik's Cube Move Sequence Optimizer

This module provides functionality to optimize and clean move sequences by
removing unnecessary moves and combining consecutive moves on the same face.
This is essential for creating efficient solutions and reducing algorithm length.

The cleaner handles all combinations of consecutive moves:
- Normal + Normal = Double (R R → R2)
- Normal + Prime = Cancellation (R R' → [removed])
- Prime + Prime = Double (R' R' → R2)
- Double + Normal = Prime (R2 R → R')
- Double + Double = Cancellation (R2 R2 → [removed])

This optimization is particularly important for generated solutions which
often contain redundant move sequences.
"""


def clean_moves(scramble):
    """
    Optimize a move sequence by removing unnecessary and redundant moves.
    
    This function processes a scramble string and eliminates consecutive moves
    on the same face that can be combined or cancelled. The optimization
    reduces the total move count and creates cleaner, more efficient sequences.
    
    Args:
        scramble (str): Space-separated move sequence to optimize
        
    Returns:
        str: Optimized move sequence with redundant moves removed
        
    Examples:
        >>> clean_moves("R R U U'")
        "R2"
        >>> clean_moves("F F' U2 U2")
        ""
        >>> clean_moves("R2 R")
        "R'"
        
    The function handles all standard notation including normal moves,
    prime moves ('), and double moves (2).
    """
    split_scramble = scramble.split()
    seq = 0

    while seq < len(split_scramble):
        try:
            # Check if current and next move are on the same face
            if split_scramble[seq][0] == split_scramble[seq + 1][0]:
                # Process based on first move type
                if not is_prime(split_scramble[seq]) and not is_double(split_scramble[seq]):
                    # First move is normal (90° clockwise)
                    if not is_prime(split_scramble[seq + 1]) and not is_double(split_scramble[seq + 1]):
                        # Normal + Normal = Double (R R → R2)
                        del split_scramble[seq + 1]
                        split_scramble[seq] += "2"

                    elif is_prime(split_scramble[seq + 1]):
                        # Normal + Prime = Cancellation (R R' → [removed])
                        del split_scramble[seq], split_scramble[seq]

                    elif is_double(split_scramble[seq + 1]):
                        # Normal + Double = Prime (R R2 → R')
                        del split_scramble[seq + 1]
                        split_scramble[seq] += "'"

                elif is_prime(split_scramble[seq]):
                    # First move is prime (90° counter-clockwise)
                    if not is_prime(split_scramble[seq + 1]) and not is_double(split_scramble[seq + 1]):
                        # Prime + Normal = Cancellation (R' R → [removed])
                        del split_scramble[seq], split_scramble[seq]

                    elif is_prime(split_scramble[seq + 1]):
                        # Prime + Prime = Double (R' R' → R2)
                        del split_scramble[seq + 1]
                        split_scramble[seq] = split_scramble[seq][0] + "2"

                    elif is_double(split_scramble[seq + 1]):
                        # Prime + Double = Normal (R' R2 → R)
                        del split_scramble[seq + 1]
                        split_scramble[seq] = split_scramble[seq][0]

                elif is_double(split_scramble[seq]):
                    # First move is double (180°)
                    if not is_prime(split_scramble[seq + 1]) and not is_double(split_scramble[seq + 1]):
                        # Double + Normal = Prime (R2 R → R')
                        del split_scramble[seq]
                        split_scramble[seq] = split_scramble[seq][0] + "'"

                    elif is_prime(split_scramble[seq + 1]):
                        # Double + Prime = Normal (R2 R' → R)
                        del split_scramble[seq + 1]
                        split_scramble[seq] = split_scramble[seq][0]

                    elif is_double(split_scramble[seq + 1]):
                        # Double + Double = Cancellation (R2 R2 → [removed])
                        del split_scramble[seq], split_scramble[seq]
                
                # Step back to check for further optimizations after change
                seq -= 1
        except IndexError:
            # Reached end of sequence
            break
        seq += 1

    return " ".join(split_scramble)


def is_double(move):
    """
    Check if a move is a double turn (180°).
    
    Args:
        move (str): Move in standard notation
        
    Returns:
        bool: True if move contains '2' notation
    """
    try:
        if move[1] == "2":
            return True
        else:
            return False
    except IndexError:
        return False


def is_prime(move):
    """
    Check if a move is a prime turn (counter-clockwise).
    
    Args:
        move (str): Move in standard notation
        
    Returns:
        bool: True if move contains ' notation
    """
    try:
        if move[1] == "'":
            return True
        else:
            return False
    except IndexError:
        return False


if __name__ == "__main__":
    # Example usage and test cases
    print("Testing move sequence optimization:")
    print("Input: 'U U D D' U U2'")
    print(f"Output: {clean_moves('U U D D U U2')}")
    
    print("\nOptimizing example solution:")
    example = "B R2 B F2 L2 D D2 F2 D2 L B D U2 D2 D2 R R2 L F2 U2"
    print(f"Input:  {example}")
    print(f"Output: {clean_moves(example)}")