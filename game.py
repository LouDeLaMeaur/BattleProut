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
        self.fps = None
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
        self.fps = int(self.parser.get('screen', 'FPS'))
        pygame.display.set_caption(self.parser.get('screen', 'window_title'))

    def on_envent(self):
        # Quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        # Key pressed Event
        keys = pygame.key.get_pressed()
        self.world.player.refresh(keys)

    
    def on_loop(self):
        self.world.player.curs_pos = pygame.mouse.get_pos()
        self.world.player.find_vision()

    def on_render(self):
        self.screen.fill('black')
        self.world.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(self.fps)  # limits FPS to 60

    def mainLoop(self):
        self.setup()
        while self.running:
            self.on_envent()
            self.on_loop()
            self.on_render()
        self.teardown()

    def teardown(self):
        pygame.quit()