import pygame
from pygame.locals import *
from pygame.math import Vector2
from events import Events
from breakout_sounds import Sounds  

# define class for object bricks
class Brick:
    def __init__(self, color, hit_type, velocity, x, y, width, hight):
        self.color = color
        self.hit_type = hit_type
        self.velocity = pygame.Vector2(velocity)
        self.rect = pygame.FRect(x, y, width, hight)
        self.hit_count = 0

    def process_hit(self, hit_brick, wall, gamestate):
        # hit brick?
        self.hit = hit_brick
        if self.hit_type == 0:
            Sounds.spike_sound.stop() # returns -1 if there is no collision
            Sounds.obstacle_clash.play()
            pass
        else:
            self.hit_count += 1
            if self.hit_type <= self.hit_count:
                Sounds.spike_sound.stop()
                Sounds.destroy_brick.play()
                wall.bricks.remove(self.hit)
                gamestate.brick_score += 1  
            else:
                Sounds.spike_sound.stop()
                Sounds.touch_brick.play()
                wall.hit_bricks.append(self.hit)
        
    def draw(self, screen):
         pygame.draw.rect(screen, self.color, self.rect, border_radius=5)

    def update(self, size):
        self.rect[0] += self.velocity.x
        self.rect[1] += self.velocity.y

        if self.rect.bottom > size[1]:
            Events.post_live_lost()  
