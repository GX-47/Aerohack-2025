"""
Rubik's Cube Layer-by-Layer (LBL) Solver

This module implements a complete Layer-by-Layer solving algorithm for the
Rubik's cube. The LBL method is one of the most intuitive and widely taught
solving methods, breaking down the solution into these sequential steps:

1. Cross: Form a plus/cross pattern on the bottom layer
2. First Layer Corners: Complete the first layer (bottom)
3. Middle Layer Edges: Position all middle layer edge pieces
4. EOLL (Edge Orientation Last Layer): Orient last layer edges
5. OCLL (Orientation Corners Last Layer): Orient last layer corners
6. CPLL (Corner Permutation Last Layer): Position last layer corners
7. EPLL (Edge Permutation Last Layer): Position last layer edges

The solver provides detailed step-by-step output and returns a complete
move sequence that can be executed to solve any valid cube configuration.
"""

from typing import List
from copy import deepcopy

from .cube import Cube
from .move import Move
from .colour import WHITE, YELLOW, GREEN, BLUE, ORANGE, RED
from .history_cube import HistoryCube
from ..scramble.cleaner import clean_moves
from ..scramble.parser import scramble_to_moves, moves_to_scramble


def generate_solution(cube: Cube) -> List[Move]:
    """
    Generate a complete LBL solution for the given cube state.
    
    This function implements the Layer-by-Layer method to solve a Rubik's cube,
    providing detailed progress tracking and move counting for each step.
    
    Args:
        cube (Cube): The cube state to solve
        
    Returns:
        List[Move]: Sequence of moves that will solve the cube
        
    The function prints detailed progress information including:
    - Move count for each solving step
    - Individual step solutions
    - Total move count and breakdown
    """
    print("\n=== Layer-by-Layer (LBL) Solution Generation ===")
    cube_copy = HistoryCube(cube.size, deepcopy(cube.faces))

    print("Step 1: Solving Cross (White Cross on Bottom)...")
    initial_moves = len(cube_copy.get_move_history())
    solve_cross(cube_copy)
    cross_moves = len(cube_copy.get_move_history()) - initial_moves
    print(f"Cross solved in {cross_moves} moves")
    if cross_moves > 0:
        cross_solution = cube_copy.get_move_history()[initial_moves:]
        print(f"Cross moves: {moves_to_scramble(cross_solution)}")
    
    print("\nStep 2: Solving First Layer Corners...")
    corners_start = len(cube_copy.get_move_history())
    solve_corners(cube_copy)
    corners_moves = len(cube_copy.get_move_history()) - corners_start
    print(f"First layer corners solved in {corners_moves} moves")
    if corners_moves > 0:
        corners_solution = cube_copy.get_move_history()[corners_start:]
        print(f"Corners moves: {moves_to_scramble(corners_solution)}")
    
    print("\nStep 3: Solving Middle Layer Edges...")
    middle_start = len(cube_copy.get_move_history())
    solve_middle_edges(cube_copy)
    middle_moves = len(cube_copy.get_move_history()) - middle_start
    print(f"Middle layer solved in {middle_moves} moves")
    if middle_moves > 0:
        middle_solution = cube_copy.get_move_history()[middle_start:]
        print(f"Middle layer moves: {moves_to_scramble(middle_solution)}")
    
    print("\nStep 4: Solving EOLL (Edge Orientation of Last Layer)...")
    eoll_start = len(cube_copy.get_move_history())
    solve_eoll(cube_copy)
    eoll_moves = len(cube_copy.get_move_history()) - eoll_start
    print(f"EOLL solved in {eoll_moves} moves")
    if eoll_moves > 0:
        eoll_solution = cube_copy.get_move_history()[eoll_start:]
        print(f"EOLL moves: {moves_to_scramble(eoll_solution)}")
    
    print("\nStep 5: Solving OCLL (Orientation of Corners of Last Layer)...")
    ocll_start = len(cube_copy.get_move_history())
    solve_ocll(cube_copy)
    ocll_moves = len(cube_copy.get_move_history()) - ocll_start
    print(f"OCLL solved in {ocll_moves} moves")
    if ocll_moves > 0:
        ocll_solution = cube_copy.get_move_history()[ocll_start:]
        print(f"OCLL moves: {moves_to_scramble(ocll_solution)}")
    
    print("\nStep 6: Solving CPLL (Corner Permutation of Last Layer)...")
    cpll_start = len(cube_copy.get_move_history())
    solve_cpll(cube_copy)
    cpll_moves = len(cube_copy.get_move_history()) - cpll_start
    print(f"CPLL solved in {cpll_moves} moves")
    if cpll_moves > 0:
        cpll_solution = cube_copy.get_move_history()[cpll_start:]
        print(f"CPLL moves: {moves_to_scramble(cpll_solution)}")
    
    print("\nStep 7: Solving EPLL (Edge Permutation of Last Layer)...")
    epll_start = len(cube_copy.get_move_history())
    solve_epll(cube_copy)
    epll_moves = len(cube_copy.get_move_history()) - epll_start
    print(f"EPLL solved in {epll_moves} moves")
    if epll_moves > 0:
        epll_solution = cube_copy.get_move_history()[epll_start:]
        print(f"EPLL moves: {moves_to_scramble(epll_solution)}")
    
    total_moves = len(cube_copy.get_move_history())
    print(f"\n=== LBL Solution Complete! ===")
    print(f"Total moves: {total_moves}")
    print(f"Breakdown: Cross({cross_moves}) + Corners({corners_moves}) + Middle({middle_moves}) + EOLL({eoll_moves}) + OCLL({ocll_moves}) + CPLL({cpll_moves}) + EPLL({epll_moves})")
    print(f"Full solution: {moves_to_scramble(cube_copy.get_move_history())}")
    print("=" * 50)

    return scramble_to_moves(clean_moves(moves_to_scramble(cube_copy.get_move_history())))


def solve_cross(cube: HistoryCube):
    """
    Solve the cross (plus pattern) on the bottom layer.
    
    This is the first step of LBL solving, creating a cross pattern on the
    bottom face with matching edge pieces on adjacent faces.
    
    Args:
        cube (HistoryCube): The cube to solve (modified in place)
    """
    # Edge position mapping for cross solving
    EDGES = {
        "UF": "",           # Already in correct position
        "UL": "U'",         # Move from Up-Left to Down-Front
        "UR": "U",          # Move from Up-Right to Down-Front
        "UB": "U2",         # Move from Up-Back to Down-Front
        "LB": "L U' L'",    # Extract from Left-Back
        "LD": "L2 U'",      # Extract from Left-Down
        "LF": "L' U' L",    # Extract from Left-Front
        "RB": "R' U R",     # Extract from Right-Back
        "RD": "R2 U",       # Extract from Right-Down
        "RF": "R U R'",
        "DB": "B2 U2",
        "DF": "F2"
    }

    for colour in [BLUE, ORANGE, GREEN, RED]:
        for edge in EDGES:
            cur_edge = tuple(cube.get_edge(edge).values())

            if cur_edge in [(colour, YELLOW), (YELLOW, colour)]:
                cube.do_moves(EDGES[edge])

                if cube.get_edge("UF")["U"] == YELLOW:
                    cube.do_moves("F2")
                else:
                    cube.do_moves("R U' R' F")

                cube.do_moves("D'")
                
                break

    cube.do_moves("D2")


def solve_corners(cube: Cube):
    CORNERS = {
        "UFR": "U2 U2",
        "DFR": "R U R' U'",
        "DBR": "R' U R U",
        "URB": "U",
        "ULF": "U'",
        "UBL": "U2",
        "DFL": "L' U' L",
        "DBL": "L U L' U" 
    }

    for colour1, colour2 in [(GREEN, RED), (BLUE, RED), 
                             (BLUE, ORANGE), (GREEN, ORANGE)]:
        for corner in CORNERS:
            cur_corner = cube.get_corner(corner).values()

            if colour1 in cur_corner and colour2 in cur_corner and YELLOW in cur_corner:
                cube.do_moves(CORNERS[corner])

                if cube.get_sticker("UFR") == YELLOW:
                    moves = "U R U2 R' U R U' R'"
                elif cube.get_sticker("FUR") == YELLOW:
                    moves = "U R U' R'"
                else:
                    moves = "R U R'"
                
                cube.do_moves(moves)
                cube.do_moves("D'")

                break
    

def solve_middle_edges(cube: Cube):
    EDGES = {
        "UF": "U2 U2",
        "UR": "U",
        "UL": "U'",
        "UB": "U2",
        "RF": "R' F R F' R U R' U'",
        "LF": "L F' L' F L' U' L U",
        "RB": "R' U R B' R B R'",
        "LB": "L U' L' B L' B' L"
    }

    for colour1, colour2 in [(GREEN, RED), (RED, BLUE), (BLUE, ORANGE), (ORANGE, GREEN)]:
        for edge in EDGES:
            cur_edge = tuple(cube.get_edge(edge).values())

            if cur_edge == (colour1, colour2) or cur_edge == (colour2, colour1):
                cube.do_moves(EDGES[edge])

                if cube.get_sticker("FU") == colour1:
                    moves = "U R U' R' F R' F' R"
                else:
                    moves = "U2 R' F R F' R U R'"
                cube.do_moves(moves)
                cube.do_moves("y")

                break


def solve_eoll(cube: Cube):
    for _ in range(4):
        top_layer = [cube.get_sticker("UB"), cube.get_sticker("UR"),
                     cube.get_sticker("UF"), cube.get_sticker("UL")]
        eo_state = [face == WHITE for face in top_layer]

        if eo_state == [False, False, False, False]:
            cube.do_moves("R U2 R2 F R F' U2 R' F R F'")
            break
        elif eo_state == [False, False, True, True]:
            cube.do_moves("U F U R U' R' F''")
            break
        elif eo_state == [False, True, False, True]:
            cube.do_moves("F R U R' U' F'")
            break
        else:
            cube.do_moves("U")


def solve_ocll(cube: Cube):
    OCLLS = {
        "S": "R U R' U R U2 R' U",
        "AS": "U R' U' R U' R' U2 R",
        "H": "F R U R' U' R U R' U' R U R' U' F'",
        "Headlights": "R2 D' R U2 R' D R U2 R",
        "Sidebars": "U' L F R' F' L' F R F'",
        "Fish": "R' U2 R' D' R U2 R' D R2",
        "Pi": "U R U2 R2 U' R2 U' R2 U2 R"
    }

    def get_top_layer_corners(cube: Cube):
        return [cube.get_sticker("UBL"), cube.get_sticker("UBR"),
                cube.get_sticker("UFR"), cube.get_sticker("UFL")]

    def get_co_state(top_layer):
        return [face == WHITE for face in top_layer]

    for _ in range(4):
        co_state = get_co_state(get_top_layer_corners(cube))

        if co_state == [False, False, False, False]:
            while cube.get_sticker("FUR") != WHITE or cube.get_sticker("FUL") != WHITE:
                cube.do_moves("U")

            if cube.get_corner("UFR")["F"] == cube.get_corner("UBL")["B"]: 
                cube.do_moves(OCLLS["H"])
            else:
                cube.do_moves(OCLLS["Pi"])
            break
        elif co_state == [False, False, False, True]:
            if cube.get_sticker("FUR") == WHITE:
                cube.do_moves(OCLLS["S"])
            else:
                cube.do_moves(OCLLS["AS"])
            break
        elif co_state == [False, False, True, True]:
            if cube.get_sticker("BRU") == WHITE:
                cube.do_moves(OCLLS["Headlights"])
            else:
                cube.do_moves(OCLLS["Sidebars"])
            break
        elif co_state == [False, True, False, True]:
            if cube.get_sticker("RUF") != WHITE:
                cube.do_moves("U2")
            cube.do_moves(OCLLS["Fish"])
            break
        else:
            cube.do_moves("U")


def solve_cpll(cube: Cube):
    alg = "R' U L' U2 R U' R' U2 R L "

    for _ in range(4):
        if cube.get_sticker("FUR") == cube.get_sticker("FUL") and cube.get_sticker("BLU") == cube.get_sticker("BRU"):
            break

        if cube.get_sticker("FRU") == cube.get_sticker("FLU"):
            cube.do_moves(alg)
            break
        cube.do_moves("U")
    else:
        cube.do_moves(alg + " U " + alg)


def solve_epll(cube: Cube):
    solved_edges = 0

    for _ in range(4):
        if cube.get_sticker("FU") == cube.get_sticker("FUR"):
            solved_edges += 1
        cube.do_moves("U")

    if solved_edges != 4:
        if solved_edges == 0:
            cube.do_moves("R U' R U R U R U' R' U' R2")

        while cube.get_sticker("FU") != cube.get_sticker("FUR"):
            cube.do_moves("U")

        cube.do_moves("U2")

        while cube.get_sticker("FU") != cube.get_sticker("FUR"):
            cube.do_moves("R U' R U R U R U' R' U' R2")

    while cube.get_sticker("FU") != cube.get_sticker("FR"):
        cube.do_moves("U") 