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

    def update(self, size, paddle, all_bricks, events, gamestate, coins):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.velocity.xy == (0,0):
                    Events.post_start_ball()    
                    gamestate.stopwatch.start()

        # save position for later access
        self.previous_pos = pygame.FRect(self.rect)   
        #print("ball, 35: previous_pos: ", self.previous_pos)
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
                Events.post_clear_level()
        else:
            if self.rect.bottom > size[1] + 35:
                Events.post_live_lost()

        if len(coins) > 0:
            coin = coins[0]
            if self.rect.collidelist(coin.coins) >= 0: # returns -1 if there is no collision    
                hit_index = self.rect.collidelist(coin.coins) # gives index interger
                # call process_hit to tell coin that it was hit 
                coin.process_hit(hit_index)
            
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
        collision_list = self.rect.collidelistall(all_bricks) 
        if len(collision_list) >= 1:
            nearest = None 
            # calculate the collision with the shortest distance
            for i in collision_list:
                listed_brick = all_bricks[i]
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
            hit_brick = all_bricks[collision_list[0]]
            # collision on X or Y-Axis? 
            intersection = self.rect.clip(hit_brick)
            hit_y = intersection[2] > intersection[3]

            # call process_hit method
            hit_brick.process_hit(hit_brick, all_bricks, gamestate)

                # DETECT BALL'S DIRECTION AND ON WHICH AXIS IT HITS THE BRICK; CALC CONSUMED VECTOR
            if self.velocity.xy == (0, 0):
                pass
            else:
                # 1 diagonal: from bottomright to topleft
                if self.velocity[0] < 0 and self.velocity[1] < 0:
                    self.start = self.previous_pos.topleft
                    print("scenario #1")
                    print(self.start)
                    # check axis and calc actual vector consumption
                    if hit_y:
                        self.consumed_vector = (hit_brick.rect.bottom - self.previous_pos.top) / self.velocity.y 
                        self.normal.xy = 0, -1
                        #self.normal.normalize_ip()
                    else:
                        self.consumed_vector = (hit_brick.rect.right - self.previous_pos.left) / self.velocity.x 
                        self.normal.xy = 1, 0
                        #self.normal.normalize_ip()

                # 2 diagonal: from bottomleft to top right
                elif self.velocity[0] > 0 and self.velocity[1] < 0:
                    self.start = self.previous_pos.topright
                    print("scenario #2")
                    print(self.start)
                    # check axis and calc actual vector consumption
                    if hit_y:
                        self.consumed_vector = (hit_brick.rect.bottom - self.previous_pos.top) / self.velocity.y 
                        self.normal.xy = 0, -1
                        #self.normal.normalize_ip()
                    else:
                        self.consumed_vector = (hit_brick.rect.left - self.previous_pos.right) / self.velocity.x 
                        self.normal.xy = -1, 0
                        #self.normal.normalize_ip()

                # 3 diagonal: from topleft to bottomright
                elif self.velocity[0] < 0 and self.velocity[1] > 0:
                    self.start = self.previous_pos.bottomleft
                    print("scenario #3")
                    print(self.start)
                    # check axis and calc actual vector consumption
                    if hit_y :
                        self.consumed_vector = (hit_brick.rect.top - self.previous_pos.bottom) / self.velocity.y 
                        self.normal.xy = 0, 1
                    else:
                        self.consumed_vector = (hit_brick.rect.right - self.previous_pos.left) / self.velocity.x 
                        self.normal.xy = 1, 0

                # 4 diagonal: from topright to bottomleft
                elif self.velocity[0] > 0 and self.velocity[1] > 0:
                    self.start = self.previous_pos.bottomright
                    print("scenario #4")
                    print(self.start)
                    # check axis and calc actual vector consumption
                    if hit_y:
                        self.consumed_vector = (hit_brick.rect.top - self.previous_pos.bottom) / self.velocity.y 
                        self.normal.xy = 0, 1
                    else:
                        self.consumed_vector = (hit_brick.rect.left - self.previous_pos.right) / self.velocity.x
                        self.normal.xy = -1, 0

                # 5 vertical: from top to bottom // CAN ONLY BE Y-AXIS
                elif self.velocity[0] == 0 and self.velocity[1] > 0:
                    self.start = self.previous_pos.bottom
                    print("scenario #5")
                    print(self.start)
                    self.consumed_vector = (hit_brick.rect.top - self.previous_pos.buttom) / self.velocity.y 
                    self.normal.xy = 0, 1
                # 6 vertical from bottom to top
                elif self.velocity[0] == 0 and self.velocity[1] < 0:
                    self.start = self.previous_pos.top
                    print("scenario #6")
                    print(self.start)
                    self.consumed_vector = (hit_brick.rect.bottom - self.previous_pos.top) / self.velocity.y
                    self.normal.xy = 0, -1

                # horizontal: NOT allowed // no 90° X-Axis collison possible
                elif (self.velocity[0] > 0 or self.velocity[1] < 0) and self.velocity[1] == 0:
                    print("scenario #7")
                    print(self.start)
                    pass
                
                # Find point of reflection and set ball to reflection position
                self.reflect_pos = self.previous_pos.move(self.velocity * self.consumed_vector)
                self.rect.topleft = self.reflect_pos[0:2]
                #if self.consumed_vector < 1:
                print("topleft 194 : ", self.rect.topleft)
                print("ball, 195: consumed vector: ",self.consumed_vector)
                self.velocity.reflect_ip(self.normal)
                print("ball 197: self.normal " ,self.normal)
                print("ball, 198: self velocity: ", self.velocity)
                self.unused_vector = (1 - self.consumed_vector)
                print("ball, 200, unused vector: ", self.unused_vector)
                self.available_velocity = self.velocity * self.unused_vector
                print("ball, 202: available_velocity: ", self.available_velocity)
                self.test = self.velocity - self.available_velocity
                print("ball, 204: self.test: ", self.test)
                self.end_pos = self.rect.topleft + self.available_velocity # ball would end here when it could have used his full velocity
                print("ball, 206 end pos?: ", self.end_pos)
                #self.update(size, paddle, all_bricks, events, gamestate, coins)
        