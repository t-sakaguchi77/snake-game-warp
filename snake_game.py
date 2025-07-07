#!/usr/bin/env python3
"""
Terminal Snake Game
A classic Snake game implementation using Python's curses library.
Controls: Arrow keys or WASD to move, 'q' to quit.
"""

import curses
import random
import time
from enum import Enum
from collections import deque

class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

class SnakeGame:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.setup_screen()
        self.reset_game()
    
    def setup_screen(self):
        """Initialize the game screen and colors."""
        curses.curs_set(0)  # Hide cursor
        self.stdscr.nodelay(1)  # Non-blocking input
        self.stdscr.timeout(100)  # Game speed (milliseconds)
        
        # Initialize colors
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Snake
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Food
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Score
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Border
        
        # Get screen dimensions
        self.height, self.width = self.stdscr.getmaxyx()
        
        # Create game area (leave space for borders and score)
        self.game_height = self.height - 4
        self.game_width = self.width - 2
        
        # Create game window
        self.game_win = curses.newwin(self.game_height, self.game_width, 2, 1)
        
    def reset_game(self):
        """Reset the game state."""
        # Snake starts in the middle of the screen
        start_y = self.game_height // 2
        start_x = self.game_width // 2
        
        # Snake body (head at the front)
        self.snake = deque([(start_y, start_x), (start_y, start_x - 1), (start_y, start_x - 2)])
        
        # Initial direction
        self.direction = Direction.RIGHT
        
        # Score
        self.score = 0
        
        # Food position
        self.spawn_food()
        
        # Game state
        self.game_over = False
        
    def spawn_food(self):
        """Spawn food at a random location not occupied by the snake."""
        while True:
            food_y = random.randint(0, self.game_height - 1)
            food_x = random.randint(0, self.game_width - 1)
            
            if (food_y, food_x) not in self.snake:
                self.food = (food_y, food_x)
                break
    
    def handle_input(self):
        """Handle user input for controlling the snake."""
        key = self.stdscr.getch()
        
        # Quit game
        if key == ord('q') or key == ord('Q'):
            return False
        
        # Direction controls
        new_direction = None
        
        if key == curses.KEY_UP or key == ord('w') or key == ord('W'):
            new_direction = Direction.UP
        elif key == curses.KEY_DOWN or key == ord('s') or key == ord('S'):
            new_direction = Direction.DOWN
        elif key == curses.KEY_LEFT or key == ord('a') or key == ord('A'):
            new_direction = Direction.LEFT
        elif key == curses.KEY_RIGHT or key == ord('d') or key == ord('D'):
            new_direction = Direction.RIGHT
        
        # Prevent the snake from moving into itself
        if new_direction:
            opposite_directions = {
                Direction.UP: Direction.DOWN,
                Direction.DOWN: Direction.UP,
                Direction.LEFT: Direction.RIGHT,
                Direction.RIGHT: Direction.LEFT
            }
            
            if new_direction != opposite_directions.get(self.direction):
                self.direction = new_direction
        
        return True
    
    def update_snake(self):
        """Update snake position and check for collisions."""
        if self.game_over:
            return
        
        # Get current head position
        head_y, head_x = self.snake[0]
        
        # Calculate new head position
        dy, dx = self.direction.value
        new_head_y = head_y + dy
        new_head_x = head_x + dx
        
        # Check wall collision
        if (new_head_y < 0 or new_head_y >= self.game_height or
            new_head_x < 0 or new_head_x >= self.game_width):
            self.game_over = True
            return
        
        # Check self collision
        if (new_head_y, new_head_x) in self.snake:
            self.game_over = True
            return
        
        # Add new head
        self.snake.appendleft((new_head_y, new_head_x))
        
        # Check if food is eaten
        if (new_head_y, new_head_x) == self.food:
            self.score += 10
            self.spawn_food()
            # Increase game speed slightly
            self.stdscr.timeout(max(50, 100 - self.score // 50))
        else:
            # Remove tail if no food eaten
            self.snake.pop()
    
    def draw(self):
        """Draw the game state on the screen."""
        # Clear screen
        self.stdscr.clear()
        self.game_win.clear()
        
        # Draw border
        self.stdscr.attron(curses.color_pair(4))
        self.stdscr.border()
        self.stdscr.attroff(curses.color_pair(4))
        
        # Draw title
        title = "SNAKE GAME"
        self.stdscr.addstr(0, (self.width - len(title)) // 2, title, curses.color_pair(3) | curses.A_BOLD)
        
        # Draw score
        score_text = f"Score: {self.score}"
        self.stdscr.addstr(1, 2, score_text, curses.color_pair(3))
        
        # Draw controls
        controls = "Controls: Arrow keys/WASD to move, 'q' to quit"
        if len(controls) < self.width - 4:
            self.stdscr.addstr(1, self.width - len(controls) - 2, controls, curses.color_pair(4))
        
        # Draw snake
        for i, (y, x) in enumerate(self.snake):
            if i == 0:  # Head
                self.game_win.addch(y, x, '@', curses.color_pair(1) | curses.A_BOLD)
            else:  # Body
                self.game_win.addch(y, x, '#', curses.color_pair(1))
        
        # Draw food
        food_y, food_x = self.food
        self.game_win.addch(food_y, food_x, '*', curses.color_pair(2) | curses.A_BOLD)
        
        # Draw game over message
        if self.game_over:
            game_over_text = "GAME OVER! Press 'r' to restart or 'q' to quit"
            game_over_y = self.height - 2
            game_over_x = (self.width - len(game_over_text)) // 2
            self.stdscr.addstr(game_over_y, game_over_x, game_over_text, 
                              curses.color_pair(2) | curses.A_BOLD | curses.A_BLINK)
        
        # Refresh windows
        self.stdscr.refresh()
        self.game_win.refresh()
    
    def handle_game_over(self):
        """Handle game over state."""
        self.stdscr.nodelay(0)  # Blocking input
        
        while True:
            key = self.stdscr.getch()
            
            if key == ord('q') or key == ord('Q'):
                return False
            elif key == ord('r') or key == ord('R'):
                self.reset_game()
                self.stdscr.nodelay(1)  # Non-blocking input
                self.stdscr.timeout(100)  # Reset game speed
                return True
    
    def run(self):
        """Main game loop."""
        while True:
            # Handle input
            if not self.handle_input():
                break
            
            # Update game state
            if not self.game_over:
                self.update_snake()
            
            # Draw everything
            self.draw()
            
            # Handle game over
            if self.game_over:
                if not self.handle_game_over():
                    break

def main():
    """Main function to start the game."""
    try:
        # Check terminal size
        stdscr = curses.initscr()
        height, width = stdscr.getmaxyx()
        
        if height < 10 or width < 40:
            curses.endwin()
            print("Terminal too small! Please resize to at least 40x10 characters.")
            return
        
        # Start the game
        game = SnakeGame(stdscr)
        game.run()
        
    except KeyboardInterrupt:
        pass
    finally:
        # Clean up
        curses.endwin()

if __name__ == "__main__":
    main()
