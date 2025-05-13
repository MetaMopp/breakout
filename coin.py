# metamopp[at]gmail.com

import pygame
from pygame.locals import *
from events import Events
from breakout_sounds import Sounds  

### GAMEOBJECT: COIN  ###

# define class for coins in bonus level            
class Coin:
    def __init__(self):
        self.color = pygame.Color((212, 175, 55))
        self.velocity = pygame.Vector2(0,0)
        self.width = 30 
        self.hight = 30 
        self.coins = []

    def build(self, column, row, vgap, hgap, dis_left, name):
        self.coin_column = column
        self.coin_row = row
        self.coins = []
       
        # distances and gaps between bricks / window
        self.vgap = vgap 
        self.hgap = hgap 
        self.dis_left = dis_left 
        DISTANCETOP = 71 

        ### COIN PATTERNS ###
        if name == "bonus_1":
            for column in range(self.coin_column):
                y = DISTANCETOP + column * (self.hight + self.vgap)
                for row in range(self.coin_row):
                    x = self.dis_left + row * (self.width + self.hgap)
                    self.coin_rect = pygame.FRect(x, y, self.width, self.hight)
                    self.coins.append(self.coin_rect)

        elif name == "bonus_2":
            for column in range(self.coin_column-3, self.coin_column+6, +1):
                y = 20 + column * (self.hight + self.vgap)
                if column % 2 == 0:
                    for row in range(self.coin_row):
                        x = self.dis_left + row * (self.width + (self.hgap))
                        self.coin_rect = pygame.FRect(x, y, self.width, self.hight)
                        self.coins.append(self.coin_rect)
                elif column % 3 == 0:
                    for row in range(self.coin_row - 5):
                        x = (self.dis_left + 138) + row * (self.width + (self.hgap+13))
                        self.coin_rect = pygame.FRect(x, y, self.width, self.hight)
                        self.coins.append(self.coin_rect)
                else:
                    for row in range(self.coin_row - 3):
                        x = (self.dis_left + 77) + row * (self.width + (self.hgap+6))
                        self.coin_rect = pygame.FRect(x, y, self.width, self.hight)
                        self.coins.append(self.coin_rect) 
    
        elif name == "bonus_3":
            for column in range(self.coin_column):
                y = DISTANCETOP-3 + column * (self.hight + self.vgap)
                for row in range(0, self.coin_row):
                    x = self.dis_left + row * (self.width + self.hgap)
                    self.coin_rect = pygame.FRect(x, y, self.width, self.hight)
                    self.coins.append(self.coin_rect) 
    
    def process_hit(self, hit_index):
        Sounds.coin_sound.play()
        self.hit = hit_index
        self.coins.remove(self.coins[self.hit])
        Events.post_increase_coin_score()

    def draw(self, screen):
        for self.coin_rect in self.coins:
            pygame.draw.circle(screen, self.color, (self.coin_rect.centerx+10, self.coin_rect.centery+10), 10)

    def update(self, gamestate):            
        if gamestate.current_level.name == "bonus_2" or gamestate.current_level.name == "bonus_3":
            if gamestate.current_level.name == "bonus_2":
                self.velocity.y = 0.03
            elif gamestate.current_level.name == "bonus_3":
                self.velocity.y = 0.05
                for self.coin_rect in self.coins:
                    self.coin_rect[0] += self.velocity.x
                    self.coin_rect[1] += self.velocity.y
