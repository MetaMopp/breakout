# metamopp[at]gmail.com

import pygame
from pygame.locals import *
from events import Events
from breakout_sounds import Sounds  

### GAMEOBJECT: BRICK ###

# define class for object bricks
class Brick:
    def __init__(self, color, hit_type, velocity, x, y, width, hight):
        self.color = color
        self.hit_type = hit_type
        self.velocity = pygame.Vector2(velocity)
        self.rect = pygame.FRect(x, y, width, hight)
        self.hit_count = 0

    def process_hit(self, hit_brick, all_bricks, gamestate):
        # function is called in Ball.update when a brick was hit
        self.hit = hit_brick
        if self.hit_type == 0: # obstacle-type -> do not remove
            Sounds.spike_sound.stop() 
            Sounds.obstacle_clash.play()
            pass
        else:
            self.hit_count += 1 
            if self.hit_type <= self.hit_count: # if type is 1 -> remove from list
                Sounds.spike_sound.stop()
                Sounds.destroy_brick.play()
                all_bricks.remove(self.hit)
                gamestate.brick_score += 1  
            else:
                Sounds.spike_sound.stop()
                Sounds.touch_brick.play()
        
    def draw(self, screen):
         pygame.draw.rect(screen, self.color, self.rect, border_radius=5)

    def update(self, size):
        self.rect[0] += self.velocity.x # move bricks down
        self.rect[1] += self.velocity.y

        if self.rect.bottom > size[1]: # paddle did not hit the ball
            Events.post_live_lost()  
