# metamopp[at]gmail.com

import pygame
from pygame.locals import *
from events import Events

class Brick:
    def __init__(self, color, hit_type, velocity, x, y, width, hight):
        self.color = color
        self.hit_type = hit_type
        self.velocity = velocity
        self.rect = pygame.FRect(x, y, width, hight)

    def draw(self, screen):
         pygame.draw.rect(screen, self.color, self.rect, border_radius=5)

    def update(self, size):
        self.rect[0] += self.velocity.x
        self.rect[1] += self.velocity.y

        if self.rect.bottom > size[1]:
            Events.post_live_lost()  
        

class Wall: 
    def __init(self, width, hight, column, row, vgap, hgap, dis_left, dis_top):
        self.width = width
        self.hight = hight
        self.column = column 
        self.row = row 
        self.vgap = vgap
        self.hgap = hgap
        self.dis_left = dis_left
        self.dis_top = dis_top
        self.bricks =[]

    def pattern(self):
        for column in range(self.column):
            y = self.dis_top + self.column * (self.hight + self.vgap)
            for row in range(self.row):
                x = self.dis_left + row * (self.width + self.hgap)
                self.bricks.append(Brick())
        
    def draw(self, screen, brick):
        for brick in self.bricks:
                brick.draw(screen)

    def update(self, brick, size):
        for brick in self.bricks:
            brick.update(size)
                

    