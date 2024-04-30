import pygame
import math

screen_width = 800
screen_height = 600

class Bomb:

    def __init__(self, x, y, size, speed, direction):
        self.image = pygame.transform.scale(pygame.image.load("bomb.png"), (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.size = size
        self.speed = speed
        self.direction = direction

    def move(self):
        angle_radians = math.radians(self.direction)
        dx = self.speed * math.cos(angle_radians)
        dy = self.speed * math.sin(angle_radians)
        self.rect.x += dx
        self.rect.y += dy
        if self.rect.left > screen_width:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = screen_width
        if self.rect.top > screen_height:
            self.rect.bottom = 0
        elif self.rect.bottom < 0:
            self.rect.top = screen_height

    def render(self, surface):
        surface.blit(self.image, self.rect)
