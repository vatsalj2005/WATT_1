import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height,
                 paddle_hit_sound=None, wall_hit_sound=None, score_sound=None):
        self.original_x = x
        self.original_y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.max_speed = 10

        # Sounds
        self.paddle_hit_sound = paddle_hit_sound
        self.wall_hit_sound = wall_hit_sound
        self.score_sound = score_sound

        self.reset()

    def move(self):
        """Update the ball's position and handle wall bounces."""
        next_y = self.y + self.vel_y

        # Top wall
        if next_y <= 0:
            self.y = -next_y
            self.vel_y *= -1
            if self.wall_hit_sound:
                self.wall_hit_sound.play(maxtime=150)

        # Bottom wall
        elif next_y + self.height >= self.screen_height:
            excess = next_y + self.height - self.screen_height
            self.y = self.screen_height - self.height - excess
            self.vel_y *= -1
            if self.wall_hit_sound:
                self.wall_hit_sound.play(maxtime=150)
        else:
            self.y = next_y

        # Update horizontal position
        self.x += self.vel_x

    def check_collision_with_paddle(self, paddle):
        """Handle collision with a paddle."""
        if self.rect().colliderect(paddle.rect()):
            if self.vel_x > 0:
                self.x = paddle.x - self.width - 1
            else:
                self.x = paddle.x + paddle.width + 1

            self.vel_x *= -1
            self.increase_speed()

            if self.paddle_hit_sound:
                self.paddle_hit_sound.play(maxtime=150)
            return True
        return False

    def increase_speed(self, increment=0.5):
        """Slightly increase ball speed after a paddle hit."""
        if abs(self.vel_x) < self.max_speed:
            self.vel_x += increment if self.vel_x > 0 else -increment
        if abs(self.vel_y) < self.max_speed:
            self.vel_y += increment if self.vel_y > 0 else -increment

    def reset(self, x=None, y=None):
        """Reset the ball to center (or custom position) with random direction."""
        self.x = x if x is not None else self.original_x
        self.y = y if y is not None else self.original_y
        self.vel_x = random.choice([-5, 5])
        self.vel_y = random.choice([-4, -3, -2, 2, 3, 4])  # never flat

    def rect(self):
        """Return the Pygame Rect of the ball."""
        return pygame.Rect(self.x, self.y, self.width, self.height)