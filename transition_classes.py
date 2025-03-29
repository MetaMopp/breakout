
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

                   

class Wall: 
    def __init__(self, width, hight, column, row, vgap, hgap, dis_left):
        self.width = width
        self.hight = hight
        self.column = column 
        self.row = row 
        self.vgap = vgap
        self.hgap = hgap
        self.dis_left = dis_left
        
        #self.dis_top = dis_top -> currently: DISTANCETOP in pattern-method
        self.bricks =[] # list of bricks
        self.hit_bricks = []

    ### WALL PATTTERNS ###
    def pattern(self, name, color, hit_type, velocity):
        DISTANCETOP = 70 # replace this later: self.dis_top
        if name == 1 or name == "bonus_1":
            for column in range(self.column):
                y = DISTANCETOP + column * (self.hight + self.vgap)
                for row in range(self.row):
                    x = self.dis_left + row * (self.width + self.hgap)
                    self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight)) #color, hit_type, velocity, x, y, width, hight
       
        elif name == 2 or name == 8:
            for column in range(self.column):
                y = DISTANCETOP + column * (self.hight + self.vgap)
                for row in range(self.row):
                    if column % 2 == 0:
                        x = (self.dis_left + 10) + row * (self.width + self.hgap)
                    else:
                        x = (self.dis_left - 10) + row * (self.width + self.hgap)
                    self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))
        
        elif (name == 3) or (name == 7) or (name == "bonus_3"):
            for column in range(self.column):
                if name == "bonus_3":
                    y = 140 + column * (self.hight + self.vgap)
                else:
                    y = DISTANCETOP + column * (self.hight + self.vgap)
                for row in range(0, self.row, +2):
                    x = self.dis_left + row * (self.width + self.hgap)
                    self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))
        
        elif name == 4:
            for column in range(self.column-4, self.column+9, +1):
                y = 20 + column * (self.hight + self.vgap)
                if column % 2 == 0:
                    for row in range(self.row):
                        x = self.dis_left + row * (self.width + (self.hgap-3))
                        self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))
                elif column % 3 == 0:
                    for row in range(self.row - 5):
                        x = (self.dis_left + 127) + row * (self.width + (self.hgap+8))
                        self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))
                else:
                    for row in range(self.row - 3):
                        x = (self.dis_left + 73) + row * (self.width + (self.hgap+2))
                        self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))
        
        elif name == 5:
            for column in range(0, self.column, +3):
                y = DISTANCETOP + column * (self.hight + self.vgap)
                for row in range(0, self.row):
                    x = self.dis_left + row * (self.width + self.hgap)
                    self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))
 
        elif name == 6:
            for column in range(self.column):
                y = DISTANCETOP + column * (self.hight + self.vgap)
                for row in range(self.row):
                    x = self.dis_left + row * (self.width + self.hgap)
                    self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))

        elif name == 9:
            for column in range(2, self.column):
                y = DISTANCETOP+30 + column * (self.hight + self.vgap)
                for row in range(self.row):
                    x = self.dis_left + row * (self.width + self.hgap)
                    self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))
   
        elif name == 10:
            for column in range(2, self.column):
                y = 70 + column * (self.hight + self.vgap+10)
                if column % 2 == 0:
                    for row in range(self.row):
                        x = self.dis_left + row * (self.width + (self.hgap))
                        self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))
                elif column % 3 == 0:
                    for row in range(self.row):
                        x = (self.dis_left + 20) + row * (self.width + (self.hgap))
                        self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))
                else:
                    for row in range(self.row):
                        x = (self.dis_left+20) + row * (self.width + (self.hgap))
                        self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))

        elif name == "bonus_2":
            for column in range(self.column-2, self.column+5, +1):
                y = 20 + column * (self.hight + self.vgap)
                if column % 2 == 0:
                    for row in range(self.row):
                        x = self.dis_left + row * (self.width + (self.hgap-3))
                        self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))
                elif column % 3 == 0:
                    for row in range(self.row - 5):
                        x = (self.dis_left + 127) + row * (self.width + (self.hgap+8))
                        self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))
                else:
                    for row in range(self.row - 3):
                        x = (self.dis_left + 73) + row * (self.width + (self.hgap+2))
                        self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))

    def build_obstacle(self, name, color, hit_type, velocity):
        DISTANCETOP = 70 

        ###  OBSTACLE PATTERNS ###
        
        if name == 3:
            for column in range(self.column):
                y = DISTANCETOP + column * (self.hight + self.vgap)
                for row in range(0, self.row, +3):
                    x = self.dis_left + row * (self.width + self.hgap)
                    self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))

        elif name == 5:
            for column in range(2, self.column+1, +3):
                y = DISTANCETOP + column * (self.hight + self.vgap)
                for row in range(self.row):
                    x = self.dis_left + row * (self.width + self.hgap)
                    self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))
        
        elif name == 8:
            for column in range(self.column):
                y = DISTANCETOP+25 + column * (self.hight + self.vgap)
                for row in range(self.row):
                    x = self.dis_left + row * (self.width + self.hgap)
                    self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))

        elif name == 10:
            for column in range(self.column):
                y = DISTANCETOP-10 + column * (self.hight + self.vgap)
                for row in range(0, self.row):
                    x = self.dis_left + row * (self.width + self.hgap)
                    self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))
                               
    # tell brick to draw itself
    def draw(self, screen):
        for brick in self.bricks:
                brick.draw(screen)

    # update wall
    def update(self, size): # detect collision with wall, remove bricks

        for brick in self.bricks:
            brick.update(size)
   
    # update bricks that are obstacles
    def update_obstacle(self, ball, size):

        for brick in self.bricks:
            brick.update(size)
        #detect collision and change ball direction
        if ball.rect.collidelist(self.bricks) >= 0:
            Sounds.spike_sound.stop() # returns -1 if there is no collision
            Sounds.obstacle_clash.play()
            hit = ball.rect.collidelist(self.bricks)
            hit_brick = self.bricks[hit]
            intersection = ball.rect.clip(hit_brick) 
            if intersection[2] > intersection[3]:
                ball.velocity[1] *= -1
                if ball.velocity[1] == 0:
                    print("is 0")
                if ball.velocity[1] != 0:
                    ball.rect[1] += ball.velocity[1] / abs(ball.velocity[1]) # push to avoid double collision
            if intersection[2] < intersection[3]:
                ball.velocity[0] *= -1
                if ball.velocity[0] == 0:
                    print("is 0")
                if ball.velocity[0] != 0:
                    ball.rect[0] += ball.velocity[0] / abs(ball.velocity[0]) # push to avoid double collision'''

