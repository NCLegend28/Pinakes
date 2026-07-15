# Black Hole Simulation - C++ OpenGL Version

A high-performance 3D black hole simulation using C++ and OpenGL for real-time rendering.

## Features

- **Real-time 3D Graphics**: 60+ FPS rendering using OpenGL
- **Event Horizon**: Physically accurate black hole with gravitational effects
- **Dynamic Accretion Disk**: 2000+ particles with realistic orbital mechanics
- **Relativistic Jets**: High-energy particle streams from magnetic field lines
- **Interactive Camera**: Full 3D navigation with mouse and keyboard
- **Physically Based**: Kepler's laws, temperature gradients, and orbital decay

## Dependencies

### macOS (using Homebrew)
```bash
brew install cmake glfw glew glm
```

### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install cmake libglfw3-dev libglew-dev libglm-dev
```

### Windows (using vcpkg)
```bash
vcpkg install glfw3 glew glm
```

## Building

```bash
mkdir build
cd build
cmake ..
make -j4
```

## Running

```bash
./BlackHoleSimulation
```

## Controls

- **WASD**: Move camera forward/back/left/right
- **Mouse**: Look around (camera rotation)
- **Mouse Wheel**: Zoom in/out
- **ESC**: Exit simulation

## Technical Details

### Rendering Pipeline
- **Vertex Shaders**: Transform 3D coordinates and handle particle positioning
- **Fragment Shaders**: Calculate realistic lighting, temperature colors, and gravitational effects
- **Particle System**: Dynamic point sprites with soft falloff and glow effects

### Physics Simulation
- **Orbital Mechanics**: Particles follow Kepler's laws with √(GM/r) velocity
- **Temperature Gradient**: Blackbody radiation colors based on distance from black hole
- **Gravitational Spiraling**: Accretion disk particles gradually spiral inward
- **Relativistic Jets**: Bipolar outflows with realistic expansion and turbulence

### Performance
- **Optimized Rendering**: Uses vertex buffer objects and instanced rendering
- **Level of Detail**: Particle density adapts based on distance
- **Efficient Updates**: Physics calculations optimized for real-time performance

## File Structure

```
blackHole/
├── CMakeLists.txt          # Build configuration
├── include/                # Header files
│   ├── BlackHole.h
│   ├── ParticleSystem.h
│   └── Camera.h
├── src/                    # Source files
│   ├── main.cpp
│   ├── BlackHole.cpp
│   ├── ParticleSystem.cpp
│   └── Camera.cpp
└── shaders/                # GLSL shaders
    ├── blackhole.vert
    ├── blackhole.frag
    ├── particle.vert
    └── particle.frag
```

## Customization

Edit these parameters in the source code:
- `eventHorizon`: Size of the black hole
- `accretionDiskInner/Outer`: Disk boundaries
- Number of particles in each system
- Orbital speeds and decay rates
- Color schemes and visual effects