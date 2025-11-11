# NeuroVerse

A simple neural network-powered game where an AI character navigates a grid world, learning to avoid fire and seek food through reinforcement learning principles.

## Features

- **Neural Network AI**: The character uses a basic neural network to make decisions based on sensory input
- **Grid-Based World**: 10x10 grid with randomly placed fire (red) and food (green) tiles
- **Manual Control**: Players can manually control the character using arrow keys or WASD
- **Real-time Gameplay**: Built with Pygame for smooth, interactive gameplay
- **Health System**: Character has hunger/health that decreases over time and can be restored by eating food

## Installation

1. Ensure you have Python 3.7+ installed
2. Clone or download this repository
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

Run the game with:
```bash
python src/main.py
```

## Gameplay

- **Objective**: Survive as long as possible by avoiding fire and eating food
- **Controls**:
  - Arrow keys or WASD: Manual movement
  - R: Restart the game
- **Elements**:
  - Blue circle: You (the character)
  - Red squares: Fire - avoid these, they damage health
  - Green squares: Food - eat these to restore health and gain points
- **AI Behavior**: The neural network learns to:
  - Run away from nearby fire
  - Move toward nearby food when hungry
  - Balance survival instincts with food-seeking behavior

## Neural Network Architecture

The AI uses a simple feedforward neural network with:
- **Input neurons**: 9 total (8 directional sensors for fire/food + 1 hunger sensor)
- **Hidden neurons**: None (direct connections)
- **Output neurons**: 4 movement directions (left, right, up, down)
- **Activation**: Linear (no activation function, allowing negative weights)
- **Learning**: Pre-wired connections simulating basic instincts

## Requirements

- Python 3.7+
- Pygame

## License

This project is open source and available under the MIT License.
