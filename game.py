import pygame
from world import World
from config import *
import math
# from tcpclient import TCPClient

class Game:
    def __init__(self):
        self.running = False
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        self.world = World()
        # self.client = TCPClient()

    def setup(self):
        pygame.init()
        self.running = True

    def on_envent(self):
        # Quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        # Key pressed Event
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            if not self.world.level.is_wall(math.floor(self.world.player.pos[0]/40), math.floor((self.world.player.pos[1]-10)/40)):
                self.world.player.move((0, -10))
        if keys[pygame.K_q]:
            if not self.world.level.is_wall(math.floor((self.world.player.pos[0]-10)/40), math.floor((self.world.player.pos[1])/40)):
                self.world.player.move((-10, 0))
        if keys[pygame.K_s]:
            if not self.world.level.is_wall(math.floor((self.world.player.pos[0])/40), math.floor((self.world.player.pos[1]+20)/40)):
                self.world.player.move((0, 10))
        if keys[pygame.K_d]:
            if not self.world.level.is_wall(math.floor((self.world.player.pos[0]+20)/40), math.floor((self.world.player.pos[1])/40)):
                self.world.player.move((10, 0))
        if keys[pygame.K_SPACE]:
            self.world.player.prout()

    
    def on_loop(self):
        self.world.player.curs_pos = pygame.mouse.get_pos()
        self.world.player.find_vision()

    def on_render(self):
        self.screen.fill('black')
        self.world.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(FPS)  # limits FPS to 60

    def mainLoop(self):
        self.setup()
        while self.running:
            self.on_envent()
            self.on_loop()
            self.on_render()
        self.teardown()

    def teardown(self):
        pygame.quit()