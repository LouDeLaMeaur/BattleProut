import pygame
from typing import Tuple
import numpy as np
from configparser import ConfigParser

class World:
    def __init__(self):
        self.level = Level()
        self.player = Player()
        # self.effects = Effects()

    def draw(self, screen):
        self.level.draw(screen)
        self.player.draw(screen)

class Player:
    def __init__(self):
        self.pos = [500, 300]
        self.rect = pygame.Rect(self.pos, (20, 20))
        self.color = 'red'
        self.curs_pos = pygame.mouse.get_pos()
        
    def draw(self, screen):
        self._draw_character(screen)
        self._draw_vision(screen)
    
    def _draw_character(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def _draw_vision(self, screen):
        pygame.draw.line(screen, 'gray', (self.pos[0]+10, self.pos[1]+10), (self.curs_pos))

    def move(self, delta: Tuple):
        self.pos[0] += delta[0]
        self.pos[1] += delta[1]
        self.rect = self.rect.move(delta[0], delta[1])
        print(self.rect)

    def prout(self):
        self.color = 'brown'

class Level:
    def __init__(self):
        self.key = {}
        parser = ConfigParser()
        parser.read('levels/level1.map')
        self.tileset = parser.get('level', 'tileset')
        print(parser.get('level', 'level_map'))
        self.map = np.array([[map_row] for map_row in parser.get('level', 'level_map').split('\n')])
        print(self.map)
        for section in parser.sections():
            # section value is the name of the section, if 1 it's a car description
            if len(section) == 1:
                desc = dict(parser.items(section))
                self.key[section] = desc
        self.width = len(self.map[0][0])
        self.height = len(self.map)
        print(self.width, self.height)

    def get_tile(self, x, y):
        try:
            char = self.map[y][0][x]
        except IndexError:
            return {}
        try:
            return self.key[char]
        except KeyError:
            return {}

    def get_bool(self, x, y, name):
        value = self.get_tile(x, y).get(name)
        return value

    def is_wall(self, x, y):
        return self.get_bool(x, y, 'wall')
    
    def draw(self, screen):
        for row_index in range(self.height):
            for block_index in range(self.width):
                if self.is_wall(block_index, row_index):
                    rect_ext = pygame.Rect((block_index*40, row_index*40), (40, 40))
                    rect_int = pygame.Rect((block_index*40+5, row_index*40+5), (30, 30))
                    pygame.draw.rect(screen, 'blue', rect_ext)
                    pygame.draw.rect(screen, 'black', rect_int)