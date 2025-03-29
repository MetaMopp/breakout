# metamopp[at]gmail.com

import pygame
from pygame.locals import *
from pygame.math import Vector2
import random 
from events import Events
from breakout_sounds import Sounds  

### GAMEOBJECT: BALL ###

# define class for object ball
class Ball:
    def __init__(self, size):
        self.ball_img = pygame.image.load("assets/myball.png")
        self.ball_img.convert()
        self.rect = self.ball_img.get_frect()
        self.center_ball = size[0]//2, size[1]//2
        self.rect.center = self.center_ball
        self.normal = pygame.Vector2(0,0)
        self.velocity = pygame.Vector2(0,0)


    def draw(self, screen):
        screen.blit(self.ball_img, self.rect)


    def update(self, size, paddle, wall, events, gamestate):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.velocity.xy == (0,0):
                    Events.post_start_ball()    
                    gamestate.stopwatch.start()

        # save position for later access
        self.previous_pos = pygame.FRect(self.rect)   

        # collision detection with window boundary     
        self.rect.move_ip(self.velocity)   
        if self.rect.left < 0:
            Sounds.wall_sound.play()
            self.rect.left = 0
            self.velocity[0] *= -1
        if self.rect.right > size[0]:
            Sounds.wall_sound.play()
            self.rect.x = size[0] - self.rect.width
            self.velocity[0] *= -1
        if self.rect.top < 0:
            Sounds.wall_sound.play()
            self.rect.top = 0
            self.velocity[1] *= -1
        if (gamestate.current_level.name == "bonus_1") or (gamestate.current_level.name == "bonus_2") or (gamestate.current_level.name == "bonus_3"):
            if self.rect.bottom > size[1] + 35:
                #gamestate.clear = True
                Events.post_clear_level()
        else:
            if self.rect.bottom > size[1] + 35:
                Events.post_live_lost()            

        # collision detection with paddle
        if self.rect.colliderect(paddle):
            Sounds.touch_paddle.play()
            self.rect.bottom = paddle.rect.top + 1
            distance = (self.rect.centerx -paddle.rect.centerx) / (1.2 * self.rect.width + paddle.rect.width)
            self.normal.xy = distance, -1
            self.normal.normalize_ip()
            self.velocity.reflect_ip(self.normal)
            if abs(self.velocity.y) < 30:
                self.velocity.xy - self.velocity.xy

        ### TO DO: Collision detection with bricks ###
    
        # Returns list of all indices containing rects that collide with the Rect. If no intersecting rectangles are found: empty list
        collision_list = self.rect.collidelistall(wall.bricks) 
        if len(collision_list) >= 1:
            nearest = None 
            # calculate the collision with the shortest distance
            for i in collision_list:
                listed_brick = wall.bricks[i]
                distance = (listed_brick.rect.centerx - self.rect.centerx)**2 + (listed_brick.rect.centery - self.rect.centery)**2 
                # first iteration: set the nearest distance to the first distance that was calculated and set current indix as [0] in collision list
                if nearest == None:
                    nearest = distance
                    collision_list[0] = i
                # update: if current distance is smaller than current nearest and set current indix as [0] in collision list
                elif nearest > distance:
                    nearest = distance
                    collision_list[0] = i
                
            # set the nearest colliding brick to hit_brick
            hit_brick = wall.bricks[collision_list[0]]
            # collision on X or Y-Axis?
            intersection = self.rect.clip(hit_brick)
            hit_y = intersection[2] > intersection[3]

            # call process_hit method
            hit_brick.process_hit(hit_brick, wall, gamestate)

        # DETECT BALL'S DIRECTION AND ON WHICH AXIS IT HITS THE BRICK; CALC CONSUMED VECTOR

            # 1 diagonal: from bottomleft to topright
            if self.velocity[0] < 0 and self.velocity[1] < 0:
                self.start = self.previous_pos.topleft
                # check axis and calc actual vector consumption
                if hit_y:
                    self.consumed_vector = (hit_brick.rect.bottom - self.previous_pos.top) / self.velocity.y
                else:
                    self.consumed_vector = (hit_brick.rect.right - self.previous_pos.left) / self.velocity.x

            # 2 diagonal: from bottomright to top right
            elif self.velocity[0] > 0 and self.velocity[1] < 0:
                self.start = self.previous_pos.topright
                # check axis and calc actual vector consumption
                if hit_y:
                    self.consumed_vector = (hit_brick.rect.bottom - self.previous_pos.top) / self.velocity.y
                else:
                    self.consumed_vector = (hit_brick.rect.left - self.previous_pos.right) / self.velocity.x

            # 3 diagonal: from topright to bottomright
            elif self.velocity[0] < 0 and self.velocity[1] > 0:
                self.start = self.previous_pos.bottomleft
                # check axis and calc actual vector consumption
                if hit_y :
                    self.consumed_vector = (hit_brick.rect.top - self.previous_pos.bottom) / self.velocity.y
                else:
                    self.consumed_vector = (hit_brick.rect.right - self.previous_pos.left) / self.velocity.x

            # 4 diagonal: from topleft to bottomleft
            elif self.velocity[0] > 0 and self.velocity[1] > 0:
                self.start = self.previous_pos.bottomright
                # check axis and calc actual vector consumption
                if hit_y:
                    self.consumed_vector = (hit_brick.rect.top - self.previous_pos.bottom) / self.velocity.y
                else:
                    self.consumed_vector = (hit_brick.rect.left - self.previous_pos.right) / self.velocity.x

            # 5 vertical: from top to bottom // CAN ONLY BE Y-AXIS
            elif self.velocity[0] == 0 and self.velocity[1] > 0:
                self.start = self.previous_pos.bottom
                self.consumed_vector = (hit_brick.rect.bottom - self.previous_pos.top) / self.velocity.y
            # 6 vertical from bottom to top
            elif self.velocity[0] == 0 and self.velocity[1] < 0:
                self.start = self.previous_pos.top
                self.consumed_vector = (hit_brick.rect.top - self.previous_pos.bottom) / self.velocity.y

            # horizontal: NOT allowed // no 90° X-Axis collison possible
            elif (self.velocity[0] > 0 or self.velocity[1] < 0) and self.velocity[1] == 0:
                pass

            # Find point of reflection and set ball to reflection position
            self.reflect_pos = self.previous_pos.move(self.velocity * self.consumed_vector)
            self.rect.move_ip(self.reflect_pos[0:2])
            self.velocity.reflect_ip(self.velocity)
        