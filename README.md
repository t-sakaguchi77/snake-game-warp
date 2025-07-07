# Terminal Snake Game

A classic Snake game that runs in your terminal, built with Python and the curses library.

## Features

- **Smooth gameplay** with adjustable speed
- **Colorful graphics** using terminal colors
- **Multiple control schemes** (Arrow keys or WASD)
- **Score tracking** with speed increase as you progress
- **Game over detection** with restart option
- **Responsive design** that adapts to terminal size

## How to Play

1. Run the game:
   ```bash
   python3 snake_game.py
   ```
   or
   ```bash
   ./snake_game.py
   ```

2. **Controls:**
   - Use **Arrow keys** or **WASD** to move the snake
   - Press **'q'** to quit the game
   - After game over, press **'r'** to restart or **'q'** to quit

3. **Objective:**
   - Eat the red food (`*`) to grow your snake and increase your score
   - Avoid hitting the walls or your own body
   - The game gets faster as your score increases

## Game Elements

- **Snake Head:** `@` (green, bold)
- **Snake Body:** `#` (green)
- **Food:** `*` (red, bold)
- **Score:** Displayed at the top left
- **Border:** White frame around the game area

## Requirements

- Python 3.x
- Terminal with at least 40x10 character size
- curses library (included with Python on macOS/Linux)

## Tips

- The snake starts moving to the right
- You cannot move directly into your own body (reverse direction)
- Food appears randomly in empty spaces
- Your score increases by 10 points for each food eaten
- Game speed increases every 50 points

Enjoy the game!
