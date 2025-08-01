"""
Rubik's Cube Core Implementation

This module contains the main Cube class that represents a 3D Rubik's cube
and provides all fundamental operations for cube manipulation, state checking,
and move execution.

The Cube class supports:
- Standard Rubik's cube notation (F, R, U, L, B, D moves)
- Cube rotations and transformations
- State validation and solved checking
- Individual piece access (corners and edges)
- Move sequence execution from string notation

This is the core data structure used throughout the Rubik's cube solver.
"""

from typing import List, TypeVar, Union
from itertools import permutations

from .move import Move
from .colour import Colour, INITIAL_FACE_COLOUR_MAPPING
from .pieces import Corner, Edge, CORNER_TO_UFR, EDGE_TO_UF
from ..scramble import parser


class Cube:
    """
    Represents a 3D Rubik's cube with complete state and manipulation capabilities.
    
    The cube maintains the state of all six faces and provides methods for
    executing moves, checking solved state, and accessing individual pieces.
    
    Attributes:
        size (int): Dimension of the cube (typically 3 for standard Rubik's cube)
        faces (dict): Dictionary mapping face names to 2D color arrays
    """
    
    def __init__(self, size: int):
        """
        Initialize a new Rubik's cube in solved state.
        
        Args:
            size (int): The dimension of the cube (3 for standard cube)
        """
        self.size = size
        self.faces = {face: self._generate_face(colour, size) 
                      for face, colour in INITIAL_FACE_COLOUR_MAPPING}

    def get_sticker(self, sticker: str) -> Colour:
        """
        Get the color of a specific sticker on the cube.
        
        Args:
            sticker (str): Sticker identifier in standard notation
            
        Returns:
            Colour: The color of the specified sticker
            
        Raises:
            ValueError: If the sticker identifier is invalid
        """
        for perm in permutations(sticker):
            if "".join(perm) in EDGE_TO_UF:
                return self.get_edge("".join(perm))[sticker[0]]
            elif "".join(perm) in CORNER_TO_UFR:
                return self.get_corner("".join(perm))[sticker[0]]

        raise ValueError(f"Not a valid sticker: {sticker}")

    def get_edge(self, piece: str) -> Edge:
        """
        Get information about a specific edge piece.
        
        Args:
            piece (str): Edge piece identifier
            
        Returns:
            Edge: Edge piece object with color information
        """
        moves = parser.scramble_to_moves(EDGE_TO_UF[piece])

        self.do_moves(moves)
        info = Edge({
            piece[0]: Colour(self.faces["U"][-1][1]),
            piece[1]: Colour(self.faces["F"][0][1])
        })
        parser.invert_moves(moves)

        return info

    def get_corner(self, piece: str) -> Corner:
        """
        Get information about a specific corner piece.
        
        Args:
            piece (str): Corner piece identifier
            
        Returns:
            Corner: Corner piece object with color information
        """
        moves = parser.scramble_to_moves(CORNER_TO_UFR[piece])

        self.do_moves(moves)
        info = Corner({
            piece[0]: Colour(self.faces["U"][-1][-1]), 
            piece[1]: Colour(self.faces["F"][0][-1]),
            piece[2]: Colour(self.faces["R"][0][0])
        })
        parser.invert_moves(moves)

        return info

    def do_moves(self, moves: Union[str, List[Move]]):
        """
        Execute a sequence of moves on the cube.
        
        Args:
            moves: Either a string in standard notation (e.g., "R U R'") 
                  or a list of Move objects
        """
        if isinstance(moves, str):
            moves = parser.scramble_to_moves(moves)

        for move in moves:
            if move.face == "y":
                self._y_rotate()
            else:
                self._rotate(move)

    def is_solved(self) -> bool:
        """
        Check if the cube is in a solved state.
        
        Returns:
            bool: True if all faces have uniform colors, False otherwise
        """
        for face in self.faces.values():
            for row in face:
                if any(piece_colour != face[0][0] for piece_colour in row):
                    return False

        return True

    def _generate_face(self, colour: Colour, size: int):
        """
        Generate a face with uniform color for cube initialization.
        
        Args:
            colour (Colour): The color to fill the face with
            size (int): The dimension of the face (size x size)
            
        Returns:
            List[List[Colour]]: 2D array representing the face
        """
        return [[colour for _ in range(size)] for _ in range(size)]

    def _face_rotate(self, face: str):
        """
        Rotate a single face 90 degrees clockwise.
        
        Args:
            face (str): Face identifier (F, R, U, L, B, D)
        """
        self.faces[face] = [list(row) for row in zip(*self.faces[face][::-1])]

    def _adjacent_face_swap(self, face: str):
        """
        Swap adjacent face stickers when rotating a face.
        
        This method handles the complex logic of moving stickers between
        adjacent faces when a face rotation occurs.
        
        Args:
            face (str): The face being rotated (F, R, U, L, B, D)
        """
        if face == "U":
            l = [self.faces[face][0] for face in ["F", "L", "B", "R"]]

            self.faces["F"][0], self.faces["L"][0], \
                self.faces["B"][0], self.faces["R"][0] = l[-1:] + l[:-1]

        elif face == "D":
            l = [self.faces[face][-1] for face in ["F", "L", "B", "R"]]

            self.faces["F"][-1], self.faces["L"][-1], \
                self.faces["B"][-1], self.faces["R"][-1] = l[1:] + l[:1]

        elif face == "F":
            l = [self.faces["U"], _transpose(self.faces["R"]),
                 self.faces["D"], _transpose(self.faces["L"])]
            r = [l[0][-1], l[1][0][::-1], l[2][0], l[3][-1][::-1]]

            l[0][-1], l[1][0], l[2][0], l[3][-1] = r[-1:] + r[:-1]

            self.faces["U"][-1] = l[0][-1]
            self.faces["R"] = _transpose(l[1])
            self.faces["D"][0] = l[2][0]
            self.faces["L"] = _transpose(l[3])

        elif face == "R":
            self._y_rotate()
            self._adjacent_face_swap("F")
            self._y_rotate(inverse=True)

        elif face == "L":
            self._y_rotate(inverse=True)
            self._adjacent_face_swap("F")
            self._y_rotate()

        elif face == "B":
            self._y_rotate(double=True)
            self._adjacent_face_swap("F")
            self._y_rotate(double=True)
            
    def _rotate(self, move: Move):
        """
        Execute a single move on the cube.
        
        Args:
            move (Move): The move to execute (handles normal, double, inverse)
        """
        for _ in range(2 if move.double else 3 if move.invert else 1):
            self._face_rotate(move.face)
            self._adjacent_face_swap(move.face)

    def _y_rotate(self, double=False, inverse=False):
        """
        Perform a cube rotation around the Y-axis.
        
        This rotates the entire cube, changing which faces are front/back/left/right.
        
        Args:
            double (bool): If True, rotate 180 degrees
            inverse (bool): If True, rotate counter-clockwise
        """
        for i in range(2 if double else 3 if inverse else 1):
            l = [self.faces[face] for face in ["F", "L", "B", "R"]]
            self.faces["F"], self.faces["L"], self.faces["B"], self.faces["R"] = l[-1:] + l[:-1]

            self._face_rotate("U")
            for _ in range(3):
                self._face_rotate("D")
    

T = TypeVar("T")
def _transpose(l: List[List[T]]) -> List[List[T]]:
    """
    Transpose a 2D matrix (swap rows and columns).
    
    Args:
        l: 2D list to transpose
        
    Returns:
        List[List[T]]: Transposed matrix
    """
    return [list(i) for i in zip(*l)]
