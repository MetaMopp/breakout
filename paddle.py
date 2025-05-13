# metamopp[at]gmail.com

import pygame
from pygame.locals import *

### GAMEOBJECT: PADDLE ###
              
# define class for object paddle
class Paddle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.FRect(x, y, width, height)
        self.color = pygame.Color(0, 255, 0)
        self.dir = {K_LEFT: (-1, 0), K_RIGHT: (1, 0)}

    # after live lost
    def center(self, size):
        self.rect = pygame.FRect((size[0] // 2 - (self.rect.width/2)), (size[1] // 1.05), self.rect.width, self.rect.height)
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 4, border_radius=3)

    def update(self, screen_width, events):  
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in self.dir:
                    self.velocity = self.dir[event.key]  
                    self.rect.move_ip(self.velocity)
                    if self.rect.left < 0:
                        self.rect[0] = 0
                    elif self.rect.right > screen_width:
                        self.rect[0] = screen_width - self.rect[2]
