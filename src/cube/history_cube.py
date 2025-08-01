"""
Rubik's Cube with Move History Tracking

This module extends the basic Cube class to include move history tracking
capabilities. The HistoryCube is essential for solution generation as it
maintains a complete record of all moves executed, allowing for solution
reconstruction and analysis.

The history tracking is used primarily by:
- The solving algorithm to build complete solutions
- Step-by-step solving mode for navigation
- Move optimization and analysis
- Solution verification and testing

This class provides the same cube functionality as the base Cube class
while transparently recording all move operations.
"""

from typing import List, Dict, Union

from .cube import Cube
from .pieces import Corner, Edge, EDGE_TO_UF, CORNER_TO_UFR
from .move import Move
from .colour import Colour
from ..scramble import parser


class HistoryCube(Cube):
    """
    Cube implementation with comprehensive move history tracking.
    
    Extends the base Cube class to maintain a complete history of all
    moves executed. This enables solution generation, move analysis,
    and step-by-step solving functionality.
    
    Attributes:
        _history (List[Move]): Complete sequence of moves executed
        
    All cube operations are identical to the base Cube class, with
    the addition of automatic move history recording.
    """
    
    def __init__(self, size: int, faces: Dict[str, List[List[Colour]]]=None):
        """
        Initialize a HistoryCube with optional predefined face configuration.
        
        Args:
            size (int): Cube dimension (typically 3 for standard cube)
            faces (Dict, optional): Predefined face configuration,
                                   defaults to solved state if None
        """
        super().__init__(size)
        
        # Use provided faces or default to solved state
        self.faces = faces if faces else self.faces
        
        # Initialize empty move history
        self._history = []

    def get_move_history(self) -> List[Move]:
        """
        Retrieve the complete move history.
        
        Returns:
            List[Move]: Chronological sequence of all moves executed
        """
        return self._history

    def get_edge(self, piece: str) -> Edge:
        """
        Get edge piece information without affecting move history.
        
        Overrides parent method to temporarily disable history tracking
        during piece analysis operations.
        
        Args:
            piece (str): Edge piece identifier
            
        Returns:
            Edge: Edge piece information with colors
        """
        moves = parser.scramble_to_moves(EDGE_TO_UF[piece])

        # Execute setup moves without recording to history
        self.do_moves(moves, False)
        info = Edge({
            piece[0]: Colour(self.faces["U"][-1][1]),
            piece[1]: Colour(self.faces["F"][0][1])
        })
        # Undo setup moves without recording to history
        self.do_moves(parser.invert_moves(moves), False)

        return info

    def get_corner(self, piece: str) -> Corner:
        """
        Get corner piece information without affecting move history.
        
        Overrides parent method to temporarily disable history tracking
        during piece analysis operations.
        
        Args:
            piece (str): Corner piece identifier
            
        Returns:
            Corner: Corner piece information with colors
        """
        moves = parser.scramble_to_moves(CORNER_TO_UFR[piece])

        # Execute setup moves without recording to history
        self.do_moves(moves, False)
        info = Corner({
            piece[0]: Colour(self.faces["U"][-1][-1]), 
            piece[1]: Colour(self.faces["F"][0][-1]),
            piece[2]: Colour(self.faces["R"][0][0])
        })
        # Undo setup moves without recording to history
        self.do_moves(parser.invert_moves(moves), False)

        return info

    def do_moves(self, moves: Union[str, List[Move]], save_history: bool=True):
        """
        Execute moves with optional history tracking.
        
        Extends the parent do_moves method to include history recording.
        Allows temporary disabling of history tracking for internal operations.
        
        Args:
            moves: Move sequence to execute (string or Move list)
            save_history (bool): Whether to record moves in history
                                (default: True)
        """
        # Execute the moves using parent implementation
        super().do_moves(moves)

        # Convert string notation to Move objects if needed
        if isinstance(moves, str):
            moves = parser.scramble_to_moves(moves)

        # Record moves to history if requested
        if save_history:
            for move in moves:
                self._history.append(move)
