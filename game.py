import pygame
import random
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *

# Game settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 50
OBSTACLE_SIZE = 50
SPEED = 5
FALL_SPEED = 4

# Player position
player_x = 0
player_y = -0.8  # Near bottom of screen

# Obstacles list
obstacles = []
score = 0
game_over = False

def draw_square(x, y, size, color):
    """Draw a square at (x, y) with a given size and color."""
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x - size, y - size)  # Bottom left
    glVertex2f(x + size, y - size)  # Bottom right
    glVertex2f(x + size, y + size)  # Top right
    glVertex2f(x - size, y + size)  # Top left
    glEnd()

def spawn_obstacle():
    """Spawn a new obstacle at a random position."""
    x_pos = random.uniform(-0.9, 0.9)
    obstacles.append([x_pos, 1.0])  # Start from the top

def move_obstacles():
    """Move obstacles down and check for collision."""
    global game_over, score
    new_obstacles = []
    for obs in obstacles:
        obs[1] -= FALL_SPEED / 100  # Move down
        if obs[1] > -1:  # Still visible
            new_obstacles.append(obs)
        
        # Collision check
        if abs(obs[0] - player_x) < 0.1 and abs(obs[1] - player_y) < 0.1:
            game_over = True

    obstacles[:] = new_obstacles
    score += 1  # Increase score

def game_loop():
    """Main game loop."""
    global player_x, game_over

    clock = pygame.time.Clock()
    spawn_timer = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_LEFT and player_x > -0.9:
                    player_x -= 0.1
                elif event.key == K_RIGHT and player_x < 0.9:
                    player_x += 0.1

        # Spawn obstacles
        spawn_timer += 1
        if spawn_timer % 30 == 0:  # Adjust frequency
            spawn_obstacle()

        move_obstacles()

        # Clear screen
        glClear(GL_COLOR_BUFFER_BIT)

        # Draw player
        draw_square(player_x, player_y, 0.05, (0, 1, 0))  # Green

        # Draw obstacles
        for obs in obstacles:
            draw_square(obs[0], obs[1], 0.05, (1, 0, 0))  # Red

        pygame.display.flip()
        clock.tick(30)  # 30 FPS

    print(f"Game Over! Final Score: {score}")
    pygame.quit()

def main():
    """Initialize OpenGL and start the game."""
    pygame.init()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF | OPENGL)

    # Set up the 2D view
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -1, 1)  # 2D projection
    glMatrixMode(GL_MODELVIEW)
    
    game_loop()

if __name__ == "__main__":
    main()
