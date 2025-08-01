/* 3D Cube Rendering with Three.js */

// 3D Cube variables
let scene, camera, renderer, controls;
let cubeGroup, cubies = [];
const CUBE_SIZE = 3;
const CUBIE_SIZE = 2.5;
const CUBIE_GAP = 0.05;

// Color mapping for cube faces
const colorMap = {
    'W': 0xffffff, // White
    'Y': 0xffff00, // Yellow
    'R': 0xff0000, // Red
    'O': 0xff8000, // Orange
    'B': 0x0000ff, // Blue
    'G': 0x00ff00  // Green
};

function init3DCube() {
    console.log('Initializing 3D cube...');
    
    const container = document.getElementById('cube-canvas');
    if (!container) {
        console.error('Cube canvas container not found!');
        return;
    }
    
    try {
        // Clear the loading message
        container.innerHTML = '';
        
        // Create scene
        scene = new THREE.Scene();
        scene.background = new THREE.Color(0xd3d3d3);
        
        // Create camera with proper aspect ratio
        const width = container.clientWidth || 800;
        const height = container.clientHeight || 500;
        camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
        camera.position.set(7, 7, 7);
        camera.lookAt(0, 0, 0);
        
        // Create renderer
        renderer = new THREE.WebGLRenderer({ 
            antialias: true,
            alpha: true
        });
        renderer.setSize(width, height);
        renderer.setClearColor(0xd3d3d3, 1);
        
        // Add renderer to container
        container.appendChild(renderer.domElement);
        
        // Add simple mouse controls
        addMouseControls();
        
        // Add lighting
        const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
        scene.add(ambientLight);
        
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(10, 10, 5);
        scene.add(directionalLight);
        
        // Create cube group
        cubeGroup = new THREE.Group();
        scene.add(cubeGroup);
        
        // Create initial test cube to verify rendering
        createTestCube();
        
        // Start animation loop
        animate();
        
        console.log('3D cube initialized successfully!');
        
        // After a short delay, create the actual cubies
        setTimeout(() => {
            createCubies();
            console.log('Cubies created');
            // Update the cube display to show proper colors
            updateCubeDisplay();
        }, 100);
        
    } catch (error) {
        console.error('Error initializing 3D cube:', error);
        container.innerHTML = '<div style="padding: 20px; text-align: center; color: #ff0000;">3D visualization error: ' + error.message + '</div>';
    }
}

function createTestCube() {
    // Create a simple test cube first to verify everything works
    const geometry = new THREE.BoxGeometry(2, 2, 2);
    const material = new THREE.MeshLambertMaterial({ color: 0xff0000 });
    const testCube = new THREE.Mesh(geometry, material);
    testCube.position.set(0, 0, 0);
    cubeGroup.add(testCube);
    
    // Remove test cube after 1 second
    setTimeout(() => {
        cubeGroup.remove(testCube);
    }, 1000);
}

function addMouseControls() {
    let isMouseDown = false;
    let mouseX = 0, mouseY = 0;
    
    renderer.domElement.addEventListener('mousedown', function(event) {
        isMouseDown = true;
        mouseX = event.clientX;
        mouseY = event.clientY;
        event.preventDefault();
    });
    
    document.addEventListener('mouseup', function() {
        isMouseDown = false;
    });
    
    document.addEventListener('mousemove', function(event) {
        if (!isMouseDown || !cubeGroup) return;
        
        const deltaX = event.clientX - mouseX;
        const deltaY = event.clientY - mouseY;
        
        cubeGroup.rotation.y += deltaX * 0.01;
        cubeGroup.rotation.x += deltaY * 0.01;
        
        mouseX = event.clientX;
        mouseY = event.clientY;
        event.preventDefault();
    });
    
    renderer.domElement.addEventListener('wheel', function(event) {
        event.preventDefault();
        const scale = event.deltaY > 0 ? 1.1 : 0.9;
        camera.position.multiplyScalar(scale);
    });
}

function createCubies() {
    console.log('Creating cubies...');
    cubies = [];
    
    // Clear existing cubies
    if (cubeGroup) {
        while(cubeGroup.children.length > 0) {
            cubeGroup.remove(cubeGroup.children[0]);
        }
    }
    
    for (let x = 0; x < CUBE_SIZE; x++) {
        cubies[x] = [];
        for (let y = 0; y < CUBE_SIZE; y++) {
            cubies[x][y] = [];
            for (let z = 0; z < CUBE_SIZE; z++) {
                const cubie = createCubie(x, y, z);
                cubies[x][y][z] = cubie;
                cubeGroup.add(cubie);
            }
        }
    }
    console.log('Cubies created:', cubies.length * cubies[0].length * cubies[0][0].length);
}

function createCubie(x, y, z) {
    const geometry = new THREE.BoxGeometry(CUBIE_SIZE, CUBIE_SIZE, CUBIE_SIZE);
    
    // Create materials for each face - will be updated by updateCubie
    // Let's test the Three.js face ordering by creating a recognizable pattern
    const materials = [
        new THREE.MeshLambertMaterial({ color: 0x000000 }), // Face 0
        new THREE.MeshLambertMaterial({ color: 0x000000 }), // Face 1
        new THREE.MeshLambertMaterial({ color: 0x000000 }), // Face 2
        new THREE.MeshLambertMaterial({ color: 0x000000 }), // Face 3
        new THREE.MeshLambertMaterial({ color: 0x000000 }), // Face 4
        new THREE.MeshLambertMaterial({ color: 0x000000 })  // Face 5
    ];
    
    const cubie = new THREE.Mesh(geometry, materials);
    
    // Position cubie
    const offset = (CUBE_SIZE - 1) / 2;
    cubie.position.set(
        (x - offset) * (CUBIE_SIZE + CUBIE_GAP),
        (y - offset) * (CUBIE_SIZE + CUBIE_GAP),
        (z - offset) * (CUBIE_SIZE + CUBIE_GAP)
    );
    
    cubie.castShadow = true;
    cubie.receiveShadow = true;
    
    // Store position for reference
    cubie.userData = { x, y, z };
    
    return cubie;
}

function animate() {
    requestAnimationFrame(animate);
    if (renderer && scene && camera) {
        renderer.render(scene, camera);
    }
}

function onWindowResize() {
    const container = document.getElementById('cube-canvas');
    if (container && camera && renderer) {
        const containerRect = container.getBoundingClientRect();
        camera.aspect = containerRect.width / containerRect.height;
        camera.updateProjectionMatrix();
        renderer.setSize(containerRect.width, containerRect.height);
    }
}

function update3DCube(cubeState) {
    if (!cubeState || !cubies.length) return;
    
    // Update cubie colors based on cube state
    try {
        // Clear all faces first
        for (let x = 0; x < CUBE_SIZE; x++) {
            for (let y = 0; y < CUBE_SIZE; y++) {
                for (let z = 0; z < CUBE_SIZE; z++) {
                    const cubie = cubies[x][y][z];
                    if (cubie && cubie.material) {
                        // Set all internal faces to black
                        for (let i = 0; i < 6; i++) {
                            cubie.material[i].color.setHex(0x000000);
                        }
                    }
                }
            }
        }
        
        // Map faces to cubie positions correctly with fixed orientation
        updateCubieFace('front', cubeState.front);   // Front face (Z = 2) - Green
        updateCubieFace('back', cubeState.back);     // Back face (Z = 0) - Blue
        updateCubieFace('right', cubeState.right);   // Right face (X = 2) - Red
        updateCubieFace('left', cubeState.left);     // Left face (X = 0) - Orange
        updateCubieFace('up', cubeState.up);         // Top face (Y = 2) - White
        updateCubieFace('down', cubeState.down);     // Bottom face (Y = 0) - Yellow
    } catch (error) {
        console.warn('Error updating 3D cube:', error);
    }
}

function updateCubieFace(faceName, faceColors) {
    if (!faceColors || !Array.isArray(faceColors)) return;
    
    // Convert face colors array to 3x3 grid and update cubie materials
    for (let i = 0; i < 9; i++) {
        const row = Math.floor(i / 3);
        const col = i % 3;
        const color = colorMap[faceColors[i]] || 0x000000;
        
        let x, y, z, faceIndex;
        
        switch (faceName) {
            case 'front': // Green face - front of cube (positive Z)
                x = col; 
                y = 2 - row; // Flip Y to match standard cube orientation
                z = 2; // Front is highest Z
                faceIndex = 4; // Three.js +Z face
                break;
                
            case 'back': // Blue face - back of cube (negative Z)
                x = 2 - col; // Flip X when viewing from back
                y = 2 - row; // Flip Y to match standard cube orientation
                z = 0; // Back is lowest Z
                faceIndex = 5; // Three.js -Z face
                break;
                
            case 'right': // Red face - right side (positive X)
                x = 2; // Right is highest X
                y = 2 - row; // Flip Y to match standard cube orientation
                z = 2 - col; // Z decreases as col increases (right-to-left on face)
                faceIndex = 0; // Three.js +X face
                break;
                
            case 'left': // Orange face - left side (negative X)
                x = 0; // Left is lowest X
                y = 2 - row; // Flip Y to match standard cube orientation
                z = col; // Z increases as col increases (left-to-right on face)
                faceIndex = 1; // Three.js -X face
                break;
                
            case 'up': // White face - top (positive Y)
                x = col; 
                y = 2; // Up is highest Y
                z = row; // Z increases as row increases (top-to-bottom on face)
                faceIndex = 2; // Three.js +Y face
                break;
                
            case 'down': // Yellow face - bottom (negative Y)
                x = col; 
                y = 0; // Down is lowest Y
                z = 2 - row; // Z decreases as row increases (bottom-to-top on face)
                faceIndex = 3; // Three.js -Y face
                break;
                
            default:
                return;
        }
        
        // Update the cubie material
        if (cubies[x] && cubies[x][y] && cubies[x][y][z]) {
            const cubie = cubies[x][y][z];
            if (cubie.material[faceIndex]) {
                cubie.material[faceIndex].color.setHex(color);
            }
        }
    }
}

function getFaceIndex(faceName) {
    // Three.js box geometry face order: [+X, -X, +Y, -Y, +Z, -Z]
    const faceMap = {
        'right': 0,  // +X 
        'left': 1,   // -X   
        'up': 2,     // +Y 
        'down': 3,   // -Y 
        'front': 4,  // +Z 
        'back': 5    // -Z 
    };
    return faceMap[faceName] || -1;
}