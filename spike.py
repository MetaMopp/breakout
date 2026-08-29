# metamopp[at]gmail.com

import pygame
from pygame.locals import *
import random 
from events import Events
from breakout_sounds import Sounds  

### GAMEOBJECT: SPIKE  ###

# define class for object spike
class Spike:
    def __init__(self, color, points):
        self.points = points
        self.color = pygame.Color(color)
        self.velocity = pygame.Vector2(0,0)
        self.ran_num = random.randint(0, 1300)
        self.clip_list = []
                     
    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.points)
        
    def update(self, paddle, gamestate):
        self.velocity.xy = 0, 3
        if gamestate.spike_count < self.ran_num:
            Sounds.spike_sound.play()
            for i in range(3): 
                self.points[i][0] += self.velocity.x
                self.points[i][1] += self.velocity.y
        if gamestate.spike_count == 0:
            Sounds.spike_sound.stop()            
        
        # test ALL THREE edges of the spike triangle against the paddle.
        self.clipped = (paddle.rect.clipline((self.points[0], self.points[1]))
                        or paddle.rect.clipline((self.points[1], self.points[2]))
                        or paddle.rect.clipline((self.points[2], self.points[0])))
        if self.clipped:
            a = self.clipped[0]
            (first, second) = a # unpack tuple 
            self.clip_list.append(first)
            if len(self.clip_list) > 2:
                Sounds.spike_sound.stop()
                Events.post_live_lost()