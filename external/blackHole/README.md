# Black Hole 3D Simulation

A realistic 3D visualization of a black hole with accretion disk, relativistic jets, and orbiting particles.

## Features

- **Event Horizon**: Black sphere representing the point of no return
- **Accretion Disk**: Hot, rotating disk of matter spiraling into the black hole
- **Relativistic Jets**: High-energy particle streams ejected from the poles
- **Orbiting Particles**: Objects in stable orbits around the black hole
- **Gravitational Lensing**: Visual effects showing spacetime distortion
- **Temperature Visualization**: Color-coded particles based on distance/temperature

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python black_hole_simulation.py
```

The simulation will open an interactive 3D plot window where you can:
- Rotate the view by clicking and dragging
- Zoom in/out with the mouse wheel
- Watch the animated accretion disk and orbiting particles

## Physics Features

- Accretion disk particles rotate faster closer to the black hole (Kepler's laws)
- Temperature gradient: hotter (bluer) particles closer to the black hole
- Relativistic jets emanating from the poles
- Multiple orbital inclinations for orbiting particles
- Event horizon at 2× the Schwarzschild radius