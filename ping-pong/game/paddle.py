import pygame

class Paddle:
    def __init__(self, x, y, width, height, speed=7):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed  # Movement speed

    def move(self, dy, screen_height):
        """
        Move the paddle vertically, keeping it inside the screen.
        """
        self.y += dy
        self.y = max(0, min(self.y, screen_height - self.height))

    def rect(self):
        """
        Return a pygame.Rect representing the paddle.
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def auto_track(self, ball, screen_height):
        """
        Move the paddle to follow the ball (basic AI).
        The AI tries to center the paddle on the ball.
        """
        target_y = ball.y + ball.height / 2 - self.height / 2
        if self.y < target_y:
            self.move(min(self.speed, target_y - self.y), screen_height)
        elif self.y > target_y:
            self.move(-min(self.speed, self.y - target_y), screen_height)