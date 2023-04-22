import pygame
from world import World
from config import *

class Game:
    def __init__(self):
        self.running = False
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        self.world = World()

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
            self.world.player.move((0, -10))
        if keys[pygame.K_q]:
            self.world.player.move((-10, 0))
        if keys[pygame.K_s]:
            self.world.player.move((0, 10))
        if keys[pygame.K_d]:
            self.world.player.move((10, 0))
    
    def on_loop(self):
        pass

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