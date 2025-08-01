# Rubik's Cube Solver - Aerohack '25 Submission

**Author:** Akash Anand  
**Competition:** Aerohack '25  
**Challenge:** Rubik's Cube Solving Algorithm Implementation

## 🎯 Overview

This project implements a complete Rubik's Cube solving system that can solve any scrambled 3x3 cube through a sequence of valid moves. The solution combines algorithmic problem-solving with an interactive web interface, providing both computational efficiency and visual appeal.

## 🚀 Getting Started

### Prerequisites
Install dependencies with:
```bash
pip install -r requirements.txt
```

### Running the Application
```bash
python -m src.app
```

### Access Points
- **Web Interface**: http://localhost:5000
- **API Endpoints**: RESTful cube manipulation
- **3D Visualization**: Automatic Three.js integration

## 🧠 Problem-Solving Approach

### Algorithmic Strategy: Layer-by-Layer (LBL) Method
The solver implements the widely-used Layer-by-Layer approach, breaking down the complex 3D puzzle into manageable sequential steps:

1. **Cross Formation** - Create a white cross on the bottom layer
2. **First Layer Corners** - Complete the bottom layer with white corners
3. **Middle Layer Edges** - Position all middle layer edge pieces
4. **Last Layer Edge Orientation (EOLL)** - Orient top layer edges
5. **Last Layer Corner Orientation (OCLL)** - Orient top layer corners  
6. **Last Layer Corner Permutation (CPLL)** - Position top layer corners
7. **Last Layer Edge Permutation (EPLL)** - Position top layer edges

### Problem Decomposition
- **State Representation**: 6 faces × 9 stickers with RGB color tuples
- **Move Engine**: Standard notation (F, R, U, L, B, D) with prime and double variants
- **Solution Generation**: Step-by-step algorithmic approach with move optimization

## 🏗️ Data Structures & Architecture

### Core Data Structures

#### 1. **Cube Class** (`src/cube/cube.py`)
```python
class Cube:
    faces: Dict[str, List[List[Colour]]]  # 6 faces with 3x3 color grids
    size: int                            # Cube dimension (3 for standard)
```
- **Internal Representation**: Dictionary mapping face names to 2D color arrays
- **State Tracking**: RGB color tuples for precise color representation
- **Move Execution**: Direct face rotation and adjacent sticker swapping

#### 2. **HistoryCube Class** (`src/cube/history_cube.py`)
```python
class HistoryCube(Cube):
    _history: List[Move]  # Complete move sequence tracking
```
- **Solution Generation**: Records all moves for complete solution reconstruction
- **Step Navigation**: Enables forward/backward step-by-step solving

#### 3. **Move Representation** (`src/cube/move.py`)
```python
@dataclass
class Move:
    face: str      # F, R, U, L, B, D
    invert: bool   # Prime notation (')
    double: bool   # Double rotation (2)
```

#### 4. **Piece Mapping** (`src/cube/pieces.py`)
- **Edge Pieces**: 12 edges mapped to standardized UF position
- **Corner Pieces**: 8 corners mapped to standardized UFR position
- **Efficient Access**: O(1) piece retrieval and analysis

## 🔄 State Prediction & Move Engine

### State Transition System
The move engine accurately simulates cube rotations through:

#### 1. **Face Rotation Logic**
```python
def _face_rotate(self, face: str):
    """90° clockwise face rotation using matrix transpose"""
    self.faces[face] = [list(row) for row in zip(*self.faces[face][::-1])]
```

#### 2. **Adjacent Face Updates**
```python
def _adjacent_face_swap(self, face: str):
    """Complex sticker movement between adjacent faces"""
    # Handles all 6 face rotation patterns with precise sticker tracking
```

#### 3. **Cube Rotations**
- **Y-Rotations**: Entire cube rotation for algorithm simplification
- **State Preservation**: Accurate tracking through complex move sequences

### Predictive Capabilities
- **Move Validation**: All moves follow standard WCA notation
- **State Verification**: Real-time solved state checking
- **Sequence Optimization**: Move cleaning and redundancy removal

## ⚡ Algorithm Efficiency

### Performance Characteristics

#### **Time Complexity**
- **Move Execution**: O(1) per move (constant face operations)
- **Solution Generation**: O(n) where n is solution length
- **State Checking**: O(1) solved state verification

#### **Space Complexity**
- **Cube State**: O(1) - Fixed 54 stickers
- **Move History**: O(n) - Linear with solution length
- **Piece Mapping**: O(1) - Static lookup tables

### Optimization Features

#### 1. **Move Sequence Cleaning** (`src/scramble/cleaner.py`)
```python
# Examples of optimization:
"R R" → "R2"        # Combine consecutive moves
"R R'" → ""         # Cancel opposing moves  
"R2 R2" → ""        # Cancel double moves
```

#### 2. **Efficient Piece Access**
- Pre-computed move sequences for piece positioning
- O(1) piece retrieval without cube manipulation
- Standardized piece analysis positions

#### 3. **Solution Statistics**
```
Step-by-step move counting:
├── Cross: ~20-25 moves average
├── First Layer: ~25-30 moves average  
├── Middle Layer: ~30-35 moves average
└── Last Layer: ~35-40 moves average (EOLL + OCLL + CPLL + EPLL)
Total: ~110-130 moves average
```

## 🎨 Creative Design Features

### 1. **Interactive 3D Visualization** (`src/frontend/cube3d.js`)
- **Three.js Integration**: Real-time 3D cube rendering
- **Mouse Controls**: Intuitive rotation and zoom
- **Live Updates**: Immediate visual feedback for moves

### 2. **Step-by-Step Solving Mode**
- **Forward/Backward Navigation**: Move through solution steps
- **Visual Move Indication**: Shows next move to execute  
- **Educational Value**: Learn solving algorithms interactively

### 3. **Multiple Interface Options**
- **Web API**: RESTful endpoints for programmatic access
- **Interactive Controls**: Point-and-click and keyboard shortcuts
- **Custom Scrambles**: Apply specific cube configurations

### 4. **Comprehensive Move Parser** (`src/scramble/parser.py`)
```python
# Bidirectional conversion between notation and Move objects
"R U R' D2" ↔ [Move('R'), Move('U'), Move('R', invert=True), Move('D', double=True)]
```

## 🌟 Bonus Features Implemented

### ✅ **Visual Simulation & Cube UI**
- Complete 3D visualization with Three.js
- Real-time move animation and state updates
- Responsive design for various screen sizes
- Interactive controls (mouse, keyboard, touch)

### ✅ **Scalability Foundation**
The architecture supports extensibility for different cube sizes:

```python
class Cube:
    def __init__(self, size: int):  # Parameterized cube dimension
        self.size = size
        self.faces = {face: self._generate_face(colour, size) 
                      for face, colour in INITIAL_FACE_COLOUR_MAPPING}
```

**Current Implementation**: Optimized for 3x3 cubes  
**Future Extension**: Framework ready for 2x2, 4x4+ variants

### ✅ **Additional Creative Elements**
- **Scramble Generation**: WCA-standard 40-move scrambles
- **Move History Tracking**: Complete solution reconstruction
- **Solution Optimization**: Automatic move sequence cleaning
- **Multiple Input Methods**: String notation, interactive controls
- **Educational Mode**: Step-by-step learning interface


### Interactive Controls
- **Keyboard**: U, R, L, B, D, F (Shift for prime moves)
- **Mouse**: Click and drag for 3D rotation
- **Shortcuts**: S for scramble, Space for solve

## 📊 Technical Specifications

### Project Structure
```
src/
├── app.py                 # Flask web application
├── cube/
│   ├── cube.py           # Core cube implementation
│   ├── solver.py         # LBL solving algorithm
│   ├── history_cube.py   # Move tracking extension
│   ├── move.py           # Move representation
│   ├── pieces.py         # Piece mapping system
│   └── colour.py         # Color definitions
├── scramble/
│   ├── generator.py      # Random scramble generation
│   ├── parser.py         # Move notation conversion
│   └── cleaner.py        # Move optimization
└── frontend/
    ├── index.html        # Main interface
    ├── cube3d.js         # 3D visualization
    ├── cubeapi.js        # API communication
    ├── controls.js       # User interaction
    └── styles.css        # Visual styling
```

### Dependencies
- **Backend**: Flask (Python web framework)
- **Frontend**: Three.js (3D graphics), Vanilla JavaScript
- **Core**: Pure Python implementation (no external cube libraries)

---

**Aerohack '25 Submission by Akash Anand**  
*Github Link: https://github.com/GX-47/Aerohack-2025.git*
