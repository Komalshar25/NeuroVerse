# Source Code Documentation

This directory contains the core source code for NeuroVerse.

## Files Overview

### `main.py`
The main entry point and game loop. Contains:
- `Neuron` class: Basic neuron implementation with weighted connections
- `Brain` class: Neural network container and execution logic
- `World` class: Grid-based environment with fire and food spawning
- `Character` class: Player/AI entity with health and scoring
- `build_brain()`: Function to construct the neural network architecture
- `main()`: Pygame-based game loop handling input, rendering, and AI updates

### `neurons.py`
Detailed neuron and brain implementations (if separated from main.py).

### `world.py`
World environment logic, including grid management and sensory functions.

### `character.py`
Character behavior, movement, and interaction with the world.

### `__init__.py`
Package initialization file.

## Architecture Notes

- The neural network is pre-wired with instincts rather than trained
- Sensory input includes directional detection of fire and food
- Movement decisions are made every 8 game ticks when no manual input is detected
- Health decreases gradually and can be restored by consuming food
