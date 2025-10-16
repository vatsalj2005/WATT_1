import pygame
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GameEngine:
    def __init__(self, width, height, paddle_hit_sound=None, wall_hit_sound=None, score_sound=None):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        # Initialize paddles
        self.player = Paddle(10, height // 2 - self.paddle_height // 2,
                             self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - self.paddle_height // 2,
                         self.paddle_width, self.paddle_height)

        # Initialize ball with sound effects
        self.ball = Ball(width // 2, height // 2, 15, 15, width, height,
                         paddle_hit_sound=paddle_hit_sound,
                         wall_hit_sound=wall_hit_sound,
                         score_sound=score_sound)

        # Scores
        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

        # Default winning score
        self.winning_score = 5

    # -------------------
    # Handle player input
    # -------------------
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    # -------------------
    # Update game logic
    # -------------------
    def update(self):
        self.ball.move()

        # Paddle collisions
        self.ball.check_collision_with_paddle(self.player)
        self.ball.check_collision_with_paddle(self.ai)

        # Scoring
        if self.ball.x <= 0:
            self.ai_score += 1
            if self.ball.score_sound:
                self.ball.score_sound.play(maxtime=150)
            self.ball.reset(self.width // 2, self.height // 2)

        elif self.ball.x + self.ball.width >= self.width:
            self.player_score += 1
            if self.ball.score_sound:
                self.ball.score_sound.play(maxtime=150)
            self.ball.reset(self.width // 2, self.height // 2)

        # AI movement (only track after serve)
        if abs(self.ball.vel_x) > 0:
            self.ai.auto_track(self.ball, self.height)

    # -------------------
    # Render game objects
    # -------------------
    def render(self, screen):
        screen.fill(BLACK)

        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())

        # Center dividing line
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        # Draw scores
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

    # -------------------
    # Check for game over
    # -------------------
    def check_game_over(self, screen):
        winner_text = ""
        if self.player_score >= self.winning_score:
            winner_text = "Player Wins!"
        elif self.ai_score >= self.winning_score:
            winner_text = "AI Wins!"

        if winner_text:
            screen.fill(BLACK)
            font = pygame.font.SysFont("Arial", 60)
            text_surface = font.render(winner_text, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
            screen.blit(text_surface, text_rect)
            pygame.display.flip()

            pygame.time.delay(2000)
            screen.fill(BLACK)
            pygame.display.flip()
            pygame.time.delay(500)
            return True
        return False

    # -------------------
    # Replay menu
    # -------------------
    def show_replay_menu(self, screen):
        menu_font = pygame.font.SysFont("Arial", 40)
        instructions = [
            "Select Game Mode:",
            "3 - Best of 3",
            "5 - Best of 5",
            "7 - Best of 7",
            "ESC - Exit"
        ]

        waiting = True
        while waiting:
            screen.fill(BLACK)
            for i, line in enumerate(instructions):
                text_surface = menu_font.render(line, True, WHITE)
                text_rect = text_surface.get_rect(center=(self.width // 2, 150 + i * 60))
                screen.blit(text_surface, text_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        self.winning_score = 3
                        waiting = False
                    elif event.key == pygame.K_5:
                        self.winning_score = 5
                        waiting = False
                    elif event.key == pygame.K_7:
                        self.winning_score = 7
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        return False

        # Reset scores and ball for a new game
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset(self.width // 2, self.height // 2)
        return True