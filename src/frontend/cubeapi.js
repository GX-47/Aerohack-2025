/* API Communication Functions - Improved State Management */

// Global state
let stepModeActive = false;
let autoSolveActive = false;
let autoSolveTimer = null;
let autoSolveSpeed = 1000; // milliseconds between moves
let scrambledState = null; // Stores the scrambled cube state
let needsScrambledRestore = false; // Flag to restore to scrambled state before solving
let isScrambled = false; // Flag to track if cube has been scrambled since last reset

function showStatus(message, type = 'success') {
    const status = document.getElementById('status');
    status.textContent = message;
    status.className = `status ${type}`;
    status.style.display = 'block';
    
    setTimeout(() => {
        status.style.display = 'none';
    }, 5000);
}

function updateCubeDisplay() {
    fetch('/api/state')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success' && data.cube_state) {
                renderCube(data.cube_state);
                update3DCube(data.cube_state);
            } else {
                renderDefaultCube();
            }
        })
        .catch(error => {
            console.error('Error updating cube display:', error);
            renderDefaultCube();
        });
}

function updateStepInfo() {
    fetch('/api/step_solve/status')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success' && data.active) {
                stepModeActive = true;
                document.getElementById('step-controls').style.display = 'block';
                document.getElementById('step-button').classList.add('active');
                
                // Show "Next move" to make it clear this is what to do next
                if (data.current_move === 'SOLVED') {
                    document.getElementById('step-info').textContent = 
                        `Step ${data.current_step}/${data.total_steps}: Solved!`;
                } else {
                    document.getElementById('step-info').textContent = 
                        `Step ${data.current_step}/${data.total_steps} - Next move: ${data.current_move}`;
                }
            } else {
                stepModeActive = false;
                document.getElementById('step-controls').style.display = 'none';
                document.getElementById('step-button').classList.remove('active');
                document.getElementById('step-info').textContent = 'Step mode not active';
            }
        })
        .catch(error => {
            console.error('Error updating step info:', error);
        });
}

function renderCube(cubeState) {
    const faces = ['U', 'L', 'F', 'R', 'B', 'D'];
    
    faces.forEach(face => {
        const faceElement = document.getElementById(`face-${face}`);
        if (cubeState[face.toLowerCase()]) {
            faceElement.innerHTML = renderFace(cubeState[face.toLowerCase()]);
        } else {
            faceElement.innerHTML = renderDefaultFace();
        }
    });
}

function renderDefaultCube() {
    const faces = ['U', 'L', 'F', 'R', 'B', 'D'];
    faces.forEach(face => {
        const faceElement = document.getElementById(`face-${face}`);
        faceElement.innerHTML = renderDefaultFace();
    });
}

function renderFace(colors) {
    let html = '';
    for (let i = 0; i < 3; i++) {
        html += '<div class="cube-row">';
        for (let j = 0; j < 3; j++) {
            const colorClass = getColorClass(colors[i * 3 + j]);
            html += `<div class="cube-cell ${colorClass}"></div>`;
        }
        html += '</div>';
    }
    return html;
}

function renderDefaultFace() {
    let html = '';
    for (let i = 0; i < 3; i++) {
        html += '<div class="cube-row">';
        for (let j = 0; j < 3; j++) {
            html += '<div class="cube-cell color-white"></div>';
        }
        html += '</div>';
    }
    return html;
}

function getColorClass(color) {
    const colorMap = {
        'W': 'color-white',
        'Y': 'color-yellow',
        'R': 'color-red',
        'O': 'color-orange',
        'B': 'color-blue',
        'G': 'color-green'
    };
    return colorMap[color] || 'color-white';
}

function newCube() {
    fetch('/api/new_cube', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            showStatus(data.message, data.status === 'success' ? 'success' : 'error');
            updateCubeDisplay();
            document.getElementById('solution-container').style.display = 'none';
            // Clear scrambled state on new cube
            scrambledState = null;
            needsScrambledRestore = false;
            isScrambled = false;
        })
        .catch(error => {
            showStatus('Error creating new cube', 'error');
        });
}

function scrambleCube() {
    if (autoSolveActive) {
        showStatus('Cannot scramble during auto-solve', 'error');
        return;
    }
    
    if (stepModeActive) {
        stopStepSolve();
    }
    
    fetch('/api/scramble', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                showStatus(`Scrambled with: ${data.scramble}`, 'success');
                updateCubeDisplay();
                // Save the scrambled state after a short delay to ensure state is updated
                setTimeout(() => {
                    saveScrambledState();
                }, 150); // Increased delay slightly for reliability
                needsScrambledRestore = false;
                isScrambled = true; // Mark as scrambled
            } else {
                showStatus(data.message, 'error');
                updateCubeDisplay();
            }
            document.getElementById('solution-container').style.display = 'none';
        })
        .catch(error => {
            showStatus('Error scrambling cube', 'error');
        });
}

function resetCube() {
    if (autoSolveActive) {
        showStatus('Cannot reset during auto-solve', 'error');
        return;
    }
    
    if (stepModeActive) {
        stopStepSolve();
    }
    
    fetch('/api/reset', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            showStatus(data.message, data.status === 'success' ? 'success' : 'error');
            updateCubeDisplay();
            document.getElementById('solution-container').style.display = 'none';
            // Clear the saved scrambled state when reset is clicked
            scrambledState = null;
            needsScrambledRestore = false;
            isScrambled = false; // Mark as not scrambled (solved state)
        })
        .catch(error => {
            showStatus('Error resetting cube', 'error');
        });
}

// Improved function with better error handling and verification
function saveScrambledState() {
    // Save current cube state as the scrambled state
    fetch('/api/get_state', { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success' && data.state) {
                scrambledState = data.state;
                console.log('Scrambled state saved successfully');
            } else {
                console.warn('Failed to save scrambled state:', data.message);
            }
        })
        .catch(error => {
            console.error('Error saving scrambled state:', error);
        });
}

// Improved function with better verification
function restoreScrambledState() {
    if (!scrambledState) {
        console.warn('No scrambled state to restore');
        return Promise.resolve();
    }
    
    console.log('Restoring to scrambled state...');
    return fetch('/api/set_state', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ state: scrambledState })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('Successfully restored to scrambled state');
            // Update display to show restored state
            setTimeout(() => updateCubeDisplay(), 50);
            return true;
        } else {
            throw new Error(data.message || 'Failed to restore scrambled state');
        }
    });
}

// New function to restore state and verify it was applied (used by controls.js)
function restoreScrambledStateAndVerify() {
    if (!scrambledState) {
        console.warn('No scrambled state to restore');
        return Promise.resolve();
    }
    
    console.log('Restoring to scrambled state and verifying...');
    showStatus('Restoring to scrambled state...', 'info');
    
    return fetch('/api/set_state', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ state: scrambledState })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('State restoration API call successful');
            
            // Wait and then verify the state was actually applied
            return new Promise((resolve, reject) => {
                setTimeout(() => {
                    fetch('/api/get_state', { method: 'GET' })
                        .then(response => response.json())
                        .then(verifyData => {
                            if (verifyData.status === 'success') {
                                // Compare states to ensure restoration worked
                                const statesMatch = JSON.stringify(verifyData.state) === JSON.stringify(scrambledState);
                                if (statesMatch) {
                                    console.log('State restoration verified successfully');
                                    updateCubeDisplay(); // Update display to show restored state
                                    showStatus('Restored to scrambled state', 'success');
                                    resolve(true);
                                } else {
                                    console.error('State restoration failed - states do not match');
                                    console.log('Expected:', scrambledState);
                                    console.log('Actual:', verifyData.state);
                                    reject(new Error('State verification failed'));
                                }
                            } else {
                                reject(new Error('Failed to verify state restoration'));
                            }
                        })
                        .catch(reject);
                }, 300); // Wait for backend to process the state change
            });
        } else {
            throw new Error(data.message || 'Failed to restore scrambled state');
        }
    });
}

function applyCustomScramble() {
    const scramble = document.getElementById('scramble-input').value.trim();
    if (!scramble) {
        showStatus('Please enter a scramble sequence', 'error');
        return;
    }
    
    if (stepModeActive) {
        stopStepSolve();
    }
    
    fetch('/api/apply_scramble', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scramble: scramble })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                showStatus(`Applied scramble: ${data.scramble}`, 'success');
                document.getElementById('scramble-input').value = '';
                document.getElementById('solution-container').style.display = 'none';
                // Save the scrambled state and reset the restore flag
                setTimeout(() => {
                    saveScrambledState();
                }, 150); // Increased delay for reliability
                needsScrambledRestore = false;
                isScrambled = true; // Mark as scrambled
            } else {
                showStatus(data.message, 'error');
            }
            updateCubeDisplay();
        })
        .catch(error => {
            showStatus('Error applying scramble', 'error');
        });
}

function applyMove(move) {
    if (autoSolveActive) {
        showStatus('Cannot apply moves during auto-solve', 'error');
        return;
    }
    
    if (stepModeActive) {
        showStatus('Cannot apply moves in step-by-step mode', 'error');
        return;
    }
    
    // Set the restore flag since manual moves change the cube state
    if (scrambledState && isScrambled) {
        needsScrambledRestore = true;
    }
    
    // Swap F and B moves to fix visualization
    let actualMove = move;
    if (move === 'F') {
        actualMove = 'B';
    } else if (move === "F'") {
        actualMove = "B'";
    } else if (move === 'F2') {
        actualMove = 'B2';
    } else if (move === 'B') {
        actualMove = 'F';
    } else if (move === "B'") {
        actualMove = "F'";
    } else if (move === 'B2') {
        actualMove = 'F2';
    }
    
    fetch('/api/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ move: actualMove })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                showStatus(`Applied move: ${move}`, 'success'); // Show original move to user
            } else {
                showStatus(data.message, 'error');
            }
            updateCubeDisplay();
        })
        .catch(error => {
            console.error('Error applying move:', error);
            showStatus('Error applying move', 'error');
        });
}