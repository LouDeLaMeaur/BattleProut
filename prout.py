import pygame

class Prout:
    def __init__(self, x, y):
        self.pos = (x, y)

    def draw(self, screen):
        pygame.draw.circle(screen, 'brown', self.pos, 5, width=2)