"""
Rubik's Cube Solver - Web Interface
A Flask web application that provides a complete Rubik's Cube solving experience.

This module serves as the main web interface for the Rubik's Cube solver,
offering features including:
- Interactive 3D cube visualization
- Cube scrambling with random algorithms
- Cube solving functionality
- Step-by-step solution walkthrough
- Manual cube manipulation

The application uses Flask to provide RESTful API endpoints for cube operations
and serves a responsive web interface for user interaction.
"""

from flask import Flask, render_template, request, jsonify
import sys
import os

# Import cube-related modules for core functionality
from .cube.cube import Cube
from .cube.solver import generate_solution
from .scramble.generator import gen_scramble
from .scramble.parser import moves_to_scramble

# Configure Flask application with frontend templates and static files
app = Flask(__name__, template_folder='frontend', static_folder='frontend', static_url_path='')

# Global cube instance for maintaining state across requests
cube = None

# Step-by-step solving mode data structure
step_mode_data = {
    'active': False,
    'solution_moves': [],
    'current_step': 0,
    'step_cube_states': []
}

@app.route('/')
def index():
    """
    Serve the main cube interface page.
    
    Returns:
        str: Rendered HTML template for the main application interface
    """
    return render_template('index.html')

@app.route('/api/new_cube', methods=['POST'])
def new_cube():
    """
    Initialize a new solved Rubik's cube.
    
    Creates a fresh 3x3 cube in the solved state and returns its current state.
    
    Returns:
        dict: JSON response containing success status, message, and cube state
    """
    global cube
    cube = Cube(3)
    return jsonify({
        'status': 'success',
        'message': 'New cube created',
        'cube_state': get_cube_state()
    })

@app.route('/api/scramble', methods=['POST'])
def scramble_cube():
    """
    Apply a random scramble sequence to the cube.
    
    Generates a random scrambling algorithm and applies it to the current cube.
    If no cube exists, creates a new one first.
    
    Returns:
        dict: JSON response with scramble sequence applied and resulting cube state
        
    Raises:
        Exception: If scramble generation or application fails
    """
    global cube
    if cube is None:
        cube = Cube(3)
    
    try:
        scramble = gen_scramble()
        cube.do_moves(scramble)
        return jsonify({
            'status': 'success',
            'scramble': scramble,
            'cube_state': get_cube_state()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/api/move', methods=['POST'])
def make_move():
    """
    Execute a single move or sequence of moves on the cube.
    
    Accepts move notation (e.g., R, U', F2) and applies it to the current cube state.
    
    Args:
        JSON body should contain:
        - move (str): Move notation string to execute
    
    Returns:
        dict: JSON response with move applied and resulting cube state
        
    Raises:
        Exception: If move notation is invalid or cube is uninitialized
    """
    global cube
    if cube is None:
        return jsonify({
            'status': 'error',
            'message': 'No cube initialized'
        })
    
    data = request.get_json()
    move = data.get('move', '')
    
    try:
        cube.do_moves(move)
        return jsonify({
            'status': 'success',
            'move': move,
            'cube_state': get_cube_state()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/api/solve', methods=['POST'])
def solve_cube():
    """
    Generate a complete solution for the current cube.
    
    Analyzes the current cube state and generates a sequence of moves to solve it.
    
    Returns:
        dict: JSON response containing:
        - solution: String of moves to solve the cube
        - move_count: Number of moves in the solution
        - cube_state: Current state of the cube
        
    Raises:
        Exception: If cube is uninitialized or solving algorithm fails
    """
    global cube
    if cube is None:
        return jsonify({
            'status': 'error',
            'message': 'No cube initialized'
        })
    
    try:
        solution_moves = generate_solution(cube)
        solution = moves_to_scramble(solution_moves)
        return jsonify({
            'status': 'success',
            'solution': solution,
            'move_count': len(solution_moves),
            'cube_state': get_cube_state()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/api/reset', methods=['POST'])
def reset_cube():
    """
    Reset the cube to its solved state.
    
    Creates a new cube instance in the solved configuration, discarding
    any previous state or step-by-step solving progress.
    
    Returns:
        dict: JSON response confirming reset and providing solved cube state
    """
    global cube
    cube = Cube(3)  # Create a new solved cube
    
    return jsonify({
        'status': 'success',
        'message': 'Cube reset to solved state',
        'cube_state': get_cube_state()
    })

@app.route('/api/state', methods=['GET'])
def get_state():
    """
    Retrieve the current state of the cube.
    
    Returns the complete state representation of all six faces of the cube.
    If no cube exists, creates a new solved cube.
    
    Returns:
        dict: JSON response containing the current cube state representation
    """
    global cube
    if cube is None:
        cube = Cube(3)
    
    return jsonify({
        'status': 'success',
        'cube_state': get_cube_state()
    })

@app.route('/api/apply_scramble', methods=['POST'])
def apply_scramble():
    """
    Apply a custom scramble sequence to the cube.
    
    Resets the cube to solved state and then applies the provided scramble sequence.
    Useful for setting up specific cube configurations for practice or testing.
    
    Args:
        JSON body should contain:
        - scramble (str): Space-separated move sequence to apply
    
    Returns:
        dict: JSON response with applied scramble and resulting cube state
        
    Raises:
        Exception: If scramble sequence contains invalid moves
    """
    global cube
    data = request.get_json()
    scramble = data.get('scramble', '').strip()
    
    if not scramble:
        return jsonify({
            'status': 'error',
            'message': 'No scramble provided'
        })
    
    try:
        cube = Cube(3)  # Reset to solved state first
        cube.do_moves(scramble)
        return jsonify({
            'status': 'success',
            'scramble': scramble,
            'cube_state': get_cube_state()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/api/step_solve/start', methods=['POST'])
def start_step_solve():
    """
    Initialize step-by-step solving mode.
    
    Generates a complete solution for the current cube and prepares for
    step-by-step walkthrough. Pre-calculates all intermediate cube states
    to enable forward and backward navigation through the solution.
    
    Returns:
        dict: JSON response containing:
        - total_steps: Number of moves in the solution
        - current_step: Current position (0 = start)
        - current_move: Next move to be executed
        - cube_state: Current state of the cube
        
    Raises:
        Exception: If cube is uninitialized or solution generation fails
    """
    global cube, step_mode_data
    if cube is None:
        return jsonify({
            'status': 'error',
            'message': 'No cube initialized'
        })
    
    try:
        # Generate solution
        solution_moves = generate_solution(cube)
        solution = moves_to_scramble(solution_moves)
        solution_list = solution.split()
        
        # Store initial cube state and generate all intermediate states
        step_cube_states = []
        temp_cube = Cube(3)
        temp_cube.faces = {face: [row[:] for row in cube.faces[face]] for face in cube.faces}
        step_cube_states.append({face: [row[:] for row in temp_cube.faces[face]] for face in temp_cube.faces})
        
        # Generate all intermediate states
        for move in solution_list:
            temp_cube.do_moves(move)
            step_cube_states.append({face: [row[:] for row in temp_cube.faces[face]] for face in temp_cube.faces})
        
        # Set up step mode
        step_mode_data = {
            'active': True,
            'solution_moves': solution_list,
            'current_step': 0,
            'step_cube_states': step_cube_states
        }
        
        # Show the first move to be taken
        first_move = solution_list[0] if solution_list else 'SOLVED'
        
        return jsonify({
            'status': 'success',
            'total_steps': len(solution_list),
            'current_step': 0,
            'current_move': first_move,
            'cube_state': get_cube_state()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/api/step_solve/next', methods=['POST'])
def next_step():
    """
    Advance to the next step in the step-by-step solution.
    
    Moves forward one step in the pre-calculated solution sequence,
    updating the cube state to reflect the next move's result.
    
    Returns:
        dict: JSON response with updated step information and cube state
        
    Raises:
        Exception: If step mode is not active or already at final step
    """
    global cube, step_mode_data
    
    if not step_mode_data['active']:
        return jsonify({
            'status': 'error',
            'message': 'Step-by-step mode not active'
        })
    
    if step_mode_data['current_step'] >= len(step_mode_data['solution_moves']):
        return jsonify({
            'status': 'error',
            'message': 'Already at final step'
        })
    
    step_mode_data['current_step'] += 1
    cube.faces = {face: [row[:] for row in step_mode_data['step_cube_states'][step_mode_data['current_step']][face]] 
                  for face in step_mode_data['step_cube_states'][step_mode_data['current_step']]}
    
    # Show the next move to be taken, not the current move
    if step_mode_data['current_step'] < len(step_mode_data['solution_moves']):
        next_move = step_mode_data['solution_moves'][step_mode_data['current_step']]
    else:
        next_move = 'SOLVED'
    
    return jsonify({
        'status': 'success',
        'current_step': step_mode_data['current_step'],
        'total_steps': len(step_mode_data['solution_moves']),
        'current_move': next_move,
        'cube_state': get_cube_state()
    })

@app.route('/api/step_solve/prev', methods=['POST'])
def prev_step():
    """
    Go back to the previous step in the step-by-step solution.
    
    Moves backward one step in the pre-calculated solution sequence,
    reverting the cube state to the previous step's configuration.
    
    Returns:
        dict: JSON response with updated step information and cube state
        
    Raises:
        Exception: If step mode is not active or already at first step
    """
    global cube, step_mode_data
    
    if not step_mode_data['active']:
        return jsonify({
            'status': 'error',
            'message': 'Step-by-step mode not active'
        })
    
    if step_mode_data['current_step'] <= 0:
        return jsonify({
            'status': 'error',
            'message': 'Already at first step'
        })
    
    step_mode_data['current_step'] -= 1
    cube.faces = {face: [row[:] for row in step_mode_data['step_cube_states'][step_mode_data['current_step']][face]] 
                  for face in step_mode_data['step_cube_states'][step_mode_data['current_step']]}
    
    # Show the next move to be taken, not the current move
    if step_mode_data['current_step'] < len(step_mode_data['solution_moves']):
        next_move = step_mode_data['solution_moves'][step_mode_data['current_step']]
    else:
        next_move = 'SOLVED'
    
    return jsonify({
        'status': 'success',
        'current_step': step_mode_data['current_step'],
        'total_steps': len(step_mode_data['solution_moves']),
        'current_move': next_move,
        'cube_state': get_cube_state()
    })

@app.route('/api/step_solve/stop', methods=['POST'])
def stop_step_solve():
    """
    Exit step-by-step solving mode.
    
    Deactivates the step-by-step mode and clears all related state data.
    The cube remains in its current state.
    
    Returns:
        dict: JSON response confirming step mode has been stopped
    """
    global step_mode_data
    
    step_mode_data = {
        'active': False,
        'solution_moves': [],
        'current_step': 0,
        'step_cube_states': []
    }
    
    return jsonify({
        'status': 'success',
        'message': 'Step-by-step mode stopped'
    })

@app.route('/api/step_solve/status', methods=['GET'])
def step_solve_status():
    """
    Get the current status of step-by-step solving mode.
    
    Provides information about whether step mode is active and,
    if so, the current progress through the solution.
    
    Returns:
        dict: JSON response containing step mode status and progress information
    """
    if step_mode_data['active']:
        # Show the next move to be taken, not the current move
        if step_mode_data['current_step'] < len(step_mode_data['solution_moves']):
            next_move = step_mode_data['solution_moves'][step_mode_data['current_step']]
        else:
            next_move = 'SOLVED'
            
        return jsonify({
            'status': 'success',
            'active': True,
            'current_step': step_mode_data['current_step'],
            'total_steps': len(step_mode_data['solution_moves']),
            'current_move': next_move
        })
    else:
        return jsonify({
            'status': 'success',
            'active': False
        })

def get_cube_state():
    """
    Convert the internal cube representation to a web-friendly format.
    
    Transforms the cube's 3D face arrays with RGB color tuples into
    a flat dictionary structure with single-letter color codes suitable
    for JSON serialization and frontend consumption.
    
    Returns:
        dict: Cube state with color-coded faces or None if no cube exists
        
    The returned dictionary contains:
    - Six face arrays (front, back, left, right, up, down)
    - Each face contains 9 color letters (W, Y, R, O, B, G)
    - Boolean flag indicating if cube is solved
    """
    if cube is None:
        return None
    
    try:
        # Convert color tuples to single letter representation
        def color_to_letter(color_tuple):
            color_map = {
                (255, 255, 255): 'W',  # White
                (255, 255, 0): 'Y',    # Yellow
                (255, 0, 0): 'R',      # Red
                (255, 165, 0): 'O',    # Orange
                (0, 0, 255): 'B',      # Blue
                (0, 255, 0): 'G'       # Green
            }
            return color_map.get(color_tuple, 'W')
        
        # Convert 3x3 face array to flat list of color letters
        def face_to_colors(face):
            colors = []
            for row in face:
                for color_tuple in row:
                    colors.append(color_to_letter(color_tuple))
            return colors
        
        return {
            'front': face_to_colors(cube.faces['F']),
            'back': face_to_colors(cube.faces['B']),
            'left': face_to_colors(cube.faces['L']),
            'right': face_to_colors(cube.faces['R']),
            'up': face_to_colors(cube.faces['U']),
            'down': face_to_colors(cube.faces['D']),
            'is_solved': cube.is_solved()
        }
    except Exception as e:
        print(f"Error getting cube state: {e}")
        # Fallback - return a default solved state
        default_colors = ['W'] * 9
        return {
            'front': ['G'] * 9,
            'back': ['B'] * 9, 
            'left': ['O'] * 9,
            'right': ['R'] * 9,
            'up': ['W'] * 9,
            'down': ['Y'] * 9,
            'is_solved': True
        }

if __name__ == '__main__':
    # Initialize the application with a new solved cube
    cube = Cube(3)
    
    # Start the Flask development server with debug mode enabled
    # Server is accessible from any network interface on port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
