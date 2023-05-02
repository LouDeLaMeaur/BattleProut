import pygame
from typing import Tuple
import numpy as np
from configparser import ConfigParser
import math
from prout import Prout

class World:
    def __init__(self):
        self.level = Level()
        self.player = Player(self)
        self.effects = Effects()

    def draw(self, screen):
        self.level.draw(screen)
        self.player.draw(screen)
        self.effects.draw(screen)

class Player:
    def __init__(self, world):
        self.world = world
        self.pos = [500, 300]
        self.vitesse = 5
        self.color = 'red'
        self.curs_pos = ()
        self.vision = None
        self.prout_pos = None
        
    def draw(self, screen):
        self._draw_character(screen)
        self._draw_vision(screen)
        self._draw_prout_pos(screen)
    
    def _draw_character(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, 10)
        pygame.draw.circle(screen, "blue",self.pos , 100, width=1)

    def _draw_vision(self, screen):
        pygame.draw.line(screen, 'gray', self.pos, (self.vision))

    def _draw_prout_pos(self, screen):
        pygame.draw.circle(screen, "white", self.prout_pos, 2)

    def refresh(self, keys): 
        # get key events and decide if players doing something or not
        self.refresh_position(keys)
        self.refresh_action(keys)

    def refresh_position(self, keys):
        if keys[pygame.K_z]:
            if not self.world.level.is_wall(math.floor(self.pos[0]/40), math.floor((self.pos[1]-20)/40)):
                self.move((0, -self.vitesse))
        if keys[pygame.K_q]:
            if not self.world.level.is_wall(math.floor((self.pos[0]-20)/40), math.floor((self.pos[1])/40)):
                self.move((-self.vitesse, 0))
        if keys[pygame.K_s]:
            if not self.world.level.is_wall(math.floor((self.pos[0])/40), math.floor((self.pos[1]+10)/40)):
                self.move((0, self.vitesse))
        if keys[pygame.K_d]:
            if not self.world.level.is_wall(math.floor((self.pos[0]+10)/40), math.floor((self.pos[1])/40)):
                self.move((self.vitesse, 0))

    def refresh_action(self, keys):
        if keys[pygame.K_SPACE]:
            self.world.player.prout(self.world.effects)
        if keys[pygame.K_x]:
            self.world.effects.remove_all_prouts()

    def move(self, delta: Tuple):
        self.pos[0] += delta[0]
        self.pos[1] += delta[1]

    def find_vision(self):
        oppose = self.pos[1] - self.curs_pos[1]
        adja = self.pos[0] - self.curs_pos[0]
        try:
            alpha = math.atan(oppose / adja)
        except ZeroDivisionError:
            alpha = 1
        
        dx = math.cos(alpha) * 100
        dy = math.sin(alpha) * 100
        if adja > 0:
            dx *= -1
            dy *= -1
        self.vision = (self.pos[0]+dx, self.pos[1]+dy) 
        self.prout_pos = (self.pos[0]-dx, self.pos[1]-dy)

    def prout(self, effet):
        effet.prouts.append(Prout(self.prout_pos[0], self.prout_pos[1]))

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

class Effects:
    def __init__(self):
        self.prouts = []

    def draw(self, screen):
        for prout in self.prouts:
            prout.draw(screen, self.prouts)

    def remove_all_prouts(self):
        self.prouts = []