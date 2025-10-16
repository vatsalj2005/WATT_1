import pygame
from game.game_engine import GameEngine

# ---------------------------
# Initialization
# ---------------------------
pygame.init()

# Initialize Pygame mixer for sounds
pygame.mixer.init()

# Load sounds
PADDLE_HIT_SOUND = pygame.mixer.Sound("sounds/paddle_hit.wav")
WALL_HIT_SOUND = pygame.mixer.Sound("sounds/wall_hit.wav")
SCORE_SOUND = pygame.mixer.Sound("sounds/score.wav")

# Optional: set volumes if needed
PADDLE_HIT_SOUND.set_volume(0.8)
WALL_HIT_SOUND.set_volume(0.2)
SCORE_SOUND.set_volume(1.0)

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
BLACK = (0, 0, 0)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# ---------------------------
# Initialize Game Engine with sounds
# ---------------------------
engine = GameEngine(
    WIDTH,
    HEIGHT,
    paddle_hit_sound=PADDLE_HIT_SOUND,
    wall_hit_sound=WALL_HIT_SOUND,
    score_sound=SCORE_SOUND
)

# ---------------------------
# Main Game Loop
# ---------------------------
def main():
    running = True

    while running:
        SCREEN.fill(BLACK)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Input, Update, Render
        engine.handle_input()
        engine.update()
        engine.render(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

        # Check game over
        if engine.check_game_over(SCREEN):
            # Show replay menu
            continue_game = engine.show_replay_menu(SCREEN)
            if not continue_game:
                running = False

    pygame.quit()

# ---------------------------
# Entry point
# ---------------------------
if __name__ == "__main__":
    main()