/* User Controls and Event Handling - Fixed State Management */

function handleKeyPress(event) {
    // Don't handle keys if user is typing in an input field or textarea
    if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
        // Allow all normal input operations (typing, paste, etc.)
        return;
    }
    
    // Allow Ctrl+V (paste) to focus the input field if nothing is focused
    if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'v') {
        const scrambleInput = document.getElementById('scramble-input');
        if (document.activeElement !== scrambleInput) {
            event.preventDefault();
            scrambleInput.focus();
            return;
        }
    }
    
    // Step mode navigation
    if (stepModeActive) {
        if (event.key === 'ArrowRight') {
            event.preventDefault();
            nextStep();
        } else if (event.key === 'ArrowLeft') {
            event.preventDefault();
            prevStep();
        } else if (event.key === 'Escape') {
            event.preventDefault();
            stopStepSolve();
        }
        return; // Don't process other keys in step mode
    }
    
    // Regular keyboard controls
    const key = event.key.toLowerCase();
    const isShift = event.shiftKey;
    
    // Cube moves
    if (['u', 'r', 'l', 'b', 'd', 'f'].includes(key)) {
        event.preventDefault();
        const move = key.toUpperCase() + (isShift ? "'" : '');
        applyMove(move);
    }
    // Other shortcuts
    else if (key === 's') {
        event.preventDefault();
        scrambleCube();
    } else if (key === ' ') {
        event.preventDefault();
        solveCube();
    } else if (key === 'c') {
        event.preventDefault();
        document.getElementById('scramble-input').focus();
    }
}

function handleScrambleInput(event) {
    if (event.key === 'Enter') {
        applyCustomScramble();
    }
}

function handleScramblePaste(event) {
    // Allow paste operation and clean up the input after a short delay
    setTimeout(() => {
        const input = event.target;
        // Clean up the pasted text to ensure it contains only valid cube notation
        input.value = input.value.trim();
    }, 10);
}

// Fixed solve function with reliable state restoration
function solveCube() {
    // Check if cube is scrambled before allowing solve
    if (!isScrambled) {
        showStatus('Please scramble the cube first before solving!', 'error');
        return;
    }
    
    if (stepModeActive) {
        stopStepSolve();
    }
    
    // Always restore to scrambled state and wait for confirmation
    const restorePromise = scrambledState ? 
        restoreScrambledStateAndVerify() : 
        Promise.resolve();
    
    restorePromise.then(() => {
        needsScrambledRestore = false;
        console.log('Starting auto-solve from verified scrambled state');
        
        // Start step-by-step mode for auto-solving
        fetch('/api/step_solve/start', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    updateStepInfo();
                    updateCubeDisplay();
                    document.getElementById('solution-container').style.display = 'none';
                    
                    // Start auto-solve animation
                    startAutoSolve();
                } else {
                    showStatus(data.message, 'error');
                }
            })
            .catch(error => {
                console.error('Error starting auto-solve:', error);
                showStatus('Error starting auto-solve', 'error');
            });
    }).catch(error => {
        console.error('Error restoring scrambled state:', error);
        showStatus('Error restoring scrambled state: ' + error.message, 'error');
    });
}

function setAutoSolveSpeed() {
    const speedSelect = document.getElementById('speed-control');
    autoSolveSpeed = parseInt(speedSelect.value);
}

function startAutoSolve() {
    autoSolveActive = true;
    document.getElementById('step-button').disabled = true;
    
    // Disable manual step controls during auto-solve
    document.getElementById('prev-button').disabled = true;
    document.getElementById('next-button').disabled = true;
    document.getElementById('step-help-text').textContent = 'Auto-solving in progress... Click "Exit Step Mode" to stop.';
    
    // Start the auto-solve timer (use selected speed)
    autoSolveTimer = setTimeout(autoSolveNextStep, autoSolveSpeed);
}

function autoSolveNextStep() {
    if (!autoSolveActive || !stepModeActive) {
        stopAutoSolve();
        return;
    }
    
    // Check if we're at the end
    fetch('/api/step_solve/status')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success' && data.active) {
                if (data.current_move === 'SOLVED') {
                    // Cube is solved, stop auto-solving
                    stopAutoSolve();
                    showStatus('Auto-solve completed!', 'success');
                    return;
                }
                
                // Apply next step
                fetch('/api/step_solve/next', { method: 'POST' })
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'success') {
                            updateStepInfo();
                            updateCubeDisplay();
                            
                            // Schedule next step
                            if (autoSolveActive) {
                                autoSolveTimer = setTimeout(autoSolveNextStep, autoSolveSpeed);
                            }
                        } else {
                            stopAutoSolve();
                            showStatus('Auto-solve error: ' + data.message, 'error');
                        }
                    })
                    .catch(error => {
                        stopAutoSolve();
                        showStatus('Auto-solve error', 'error');
                    });
            } else {
                stopAutoSolve();
            }
        })
        .catch(error => {
            stopAutoSolve();
            showStatus('Auto-solve error', 'error');
        });
}

function stopAutoSolve() {
    autoSolveActive = false;
    if (autoSolveTimer) {
        clearTimeout(autoSolveTimer);
        autoSolveTimer = null;
    }
    document.getElementById('step-button').disabled = false;
    
    // Set flag to restore scrambled state on next solve attempt
    if (scrambledState) {
        needsScrambledRestore = true;
    }
    
    // Re-enable manual step controls
    document.getElementById('prev-button').disabled = false;
    document.getElementById('next-button').disabled = false;
    document.getElementById('step-help-text').textContent = 'Click "Next →" to apply the move shown above';
}

function toggleStepSolve() {
    if (autoSolveActive) {
        stopAutoSolve();
        return;
    }
    
    if (stepModeActive) {
        stopStepSolve();
    } else {
        startStepSolve();
    }
}

// Fixed step solve function with reliable state restoration
function startStepSolve() {
    // Check if cube is scrambled before allowing solve
    if (!isScrambled) {
        showStatus('Please scramble the cube first before solving!', 'error');
        return;
    }
    
    // Always restore to scrambled state and wait for confirmation
    const restorePromise = scrambledState ? 
        restoreScrambledStateAndVerify() : 
        Promise.resolve();
    
    restorePromise.then(() => {
        needsScrambledRestore = false;
        console.log('Starting step-by-step solve from verified scrambled state');
        
        // Wait a bit more to ensure the backend has processed the state change
        setTimeout(() => {
            fetch('/api/step_solve/start', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        showStatus('Step-by-step mode started', 'success');
                        updateStepInfo();
                        updateCubeDisplay();
                        document.getElementById('solution-container').style.display = 'none';
                    } else {
                        showStatus(data.message, 'error');
                    }
                })
                .catch(error => {
                    console.error('Error starting step solve:', error);
                    showStatus('Error starting step solve', 'error');
                });
        }, 200); // Additional delay to ensure backend processes the state
        
    }).catch(error => {
        console.error('Error restoring scrambled state:', error);
        showStatus('Error restoring scrambled state: ' + error.message, 'error');
    });
}

// New function to restore state and verify it was applied
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

function nextStep() {
    if (autoSolveActive) {
        showStatus('Cannot manually navigate during auto-solve', 'error');
        return;
    }
    
    fetch('/api/step_solve/next', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                updateStepInfo();
                updateCubeDisplay();
            } else {
                showStatus(data.message, 'error');
            }
        })
        .catch(error => {
            showStatus('Error moving to next step', 'error');
        });
}

function prevStep() {
    if (autoSolveActive) {
        showStatus('Cannot manually navigate during auto-solve', 'error');
        return;
    }
    
    fetch('/api/step_solve/prev', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                updateStepInfo();
                updateCubeDisplay();
            } else {
                showStatus(data.message, 'error');
            }
        })
        .catch(error => {
            showStatus('Error moving to previous step', 'error');
        });
}

function stopStepSolve() {
    // Stop auto-solve if it's running
    stopAutoSolve();
    
    // Set flag to restore scrambled state on next solve attempt
    if (scrambledState) {
        needsScrambledRestore = true;
    }
    
    fetch('/api/step_solve/stop', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                showStatus('Step-by-step mode stopped', 'success');
                updateStepInfo();
            } else {
                showStatus(data.message, 'error');
            }
        })
        .catch(error => {
            showStatus('Error stopping step solve', 'error');
        });
}

// Initialize the application when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, checking Three.js...');
    
    // Check if Three.js loaded
    if (typeof THREE === 'undefined') {
        console.error('Three.js failed to load');
        document.getElementById('cube-canvas').innerHTML = 
            '<div style="padding: 20px; text-align: center; color: #ff0000;">Failed to load 3D library. Please refresh the page.</div>';
        return;
    }
    
    console.log('Three.js loaded successfully');
    
    // Wait a bit for everything to settle
    setTimeout(() => {
        try {
            init3DCube();
            updateCubeDisplay();
        } catch (error) {
            console.error('Error during initialization:', error);
        }
    }, 200);
    
    // Set up keyboard event listeners
    document.addEventListener('keydown', handleKeyPress);
    
    // Handle input field events
    const scrambleInput = document.getElementById('scramble-input');
    scrambleInput.addEventListener('keypress', handleScrambleInput);
    scrambleInput.addEventListener('paste', handleScramblePaste);
    
    // Ensure context menu (right-click) works for paste operations
    scrambleInput.addEventListener('contextmenu', function(event) {
        // Allow the default context menu for copy/paste operations
        event.stopPropagation();
    });
    
    // Handle window resize
    window.addEventListener('resize', onWindowResize, false);
});