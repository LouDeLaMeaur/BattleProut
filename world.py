import pygame
from typing import Tuple

class World:
    def __init__(self):
        # self.scene = Scene()
        self.player = Player()
        # self.effects = Effects()

    def draw(self, screen):
        self.player.draw(screen)

class Player:
    def __init__(self):
        self.pos = [0, 0]
        self.rect = pygame.Rect(self.pos, (20, 20))
        
    def draw(self, screen):
        pygame.draw.rect(screen, 'red', self.rect)

    def move(self, delta: Tuple):
        self.pos[0] += delta[0]
        self.pos[1] += delta[1]
        self.rect = self.rect.move(delta[0], delta[1])
        print(self.rect)

class Scene:
    def __init__(self):
        pass