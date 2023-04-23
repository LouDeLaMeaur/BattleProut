import pygame
from world import World
import math
from configparser import ConfigParser
# from tcpclient import TCPClient

class Game:
    def __init__(self):
        self.running = False
        self.parser = None
        self.screen = None
        self.clock = None
        self.world = World()
        # self.client = TCPClient()

    def setup(self):
        pygame.init()
        self._setup_config()
        self._setup_screen()
        self.clock = pygame.time.Clock()
        self.running = True

    def _setup_config(self):
        self.parser = ConfigParser()
        self.parser.read("options")

    def _setup_screen(self):
        window_width = int(self.parser.get('screen', 'window_width'))
        window_height = int(self.parser.get('screen', 'window_height'))
        self.screen = pygame.display.set_mode((window_width, window_height))

    def on_envent(self):
        # Quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        # Key pressed Event
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            if not self.world.level.is_wall(math.floor(self.world.player.pos[0]/40), math.floor((self.world.player.pos[1]-20)/40)):
                self.world.player.move((0, -10))
        if keys[pygame.K_q]:
            if not self.world.level.is_wall(math.floor((self.world.player.pos[0]-20)/40), math.floor((self.world.player.pos[1])/40)):
                self.world.player.move((-10, 0))
        if keys[pygame.K_s]:
            if not self.world.level.is_wall(math.floor((self.world.player.pos[0])/40), math.floor((self.world.player.pos[1]+10)/40)):
                self.world.player.move((0, 10))
        if keys[pygame.K_d]:
            if not self.world.level.is_wall(math.floor((self.world.player.pos[0]+10)/40), math.floor((self.world.player.pos[1])/40)):
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
        fps = int(self.parser.get('screen', 'FPS'))
        self.clock.tick(fps)  # limits FPS to 60

    def mainLoop(self):
        self.setup()
        while self.running:
            self.on_envent()
            self.on_loop()
            self.on_render()
        self.teardown()

    def teardown(self):
        pygame.quit()