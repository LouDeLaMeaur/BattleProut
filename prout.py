import pygame
from threading import Thread
import time

class Prout(Thread):
    def __init__(self, x, y):
        super().__init__()
        self.pos = (x, y)
        self.status = True
        self.start()
        
    def run(self):
        time.sleep(2)
        self.status = False

    def draw(self, screen, prout_list):
        if self.status:
            pygame.draw.circle(screen, 'brown', self.pos, 5, width=2)
        else:
            prout_list.remove(self)