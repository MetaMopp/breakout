# metamopp[at]gmail.com

import pygame
from pygame.locals import *
from pygame.math import Vector2
import random 
from events import Events
from breakout_sounds import Sounds  

### GAMEOBJECTS: PADDLE, SPIKE, COIN ###
              
# define class for object paddle
class Paddle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.FRect(x, y, width, height)
        self.color = pygame.Color(0, 255, 0)
        self.dir = {K_LEFT: (-1, 0), K_RIGHT: (1, 0)}
       

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 4, border_radius=3)


    def update(self, screen_width, events):  
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in self.dir:
                    p_velocity = self.dir[event.key]  
                    self.rect.move_ip(p_velocity)
                    if self.rect.left < 0:
                        self.rect[0] = 0
                    elif self.rect.right > screen_width:
                        self.rect[0] = screen_width - self.rect[2]


#define class for object spike
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
        
        self.clipped = paddle.rect.clipline((self.points[0], self.points[1]) or paddle.rect.clipline((self.points[1], self.points[2])) or paddle.rect.clipline((self.points[2], self.points[0])))
        if self.clipped:
            a = self.clipped[0]
            (first, second) = a # unpack tuple 
            self.clip_list.append(first)
            if len(self.clip_list) > 2:
                Sounds.spike_sound.stop()
                Events.post_live_lost()


# define class for coins in bonus level            
class Coin:
    def __init__(self):
        self.color = pygame.Color((212, 175, 55))
        self.velocity = pygame.Vector2(0,0)
        self.width = 30 
        self.hight = 30 
        self.coins = []

    def distribute(self, column, row, vgap, hgap, dis_left, name):
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


    def draw(self, screen):
        for self.coin_rect in self.coins:
            pygame.draw.circle(screen, self.color, (self.coin_rect.centerx+10, self.coin_rect.centery+10), 10)


    def update(self, ball, gamestate):
        if ball.rect.collidelist(self.coins) >= 0: # returns -1 if there is no collision    
            hit = ball.rect.collidelist(self.coins)
            Sounds.coin_sound.play()
            self.coins.remove(self.coins[hit])
            Events.post_increase_coin_score()
            

        if gamestate.current_level.name == "bonus_2" or gamestate.current_level.name == "bonus_3":
            if gamestate.current_level.name == "bonus_2":
                self.velocity.y = 0.03
            elif gamestate.current_level.name == "bonus_3":
                self.velocity.y = 0.05
                for self.coin_rect in self.coins:
                    self.coin_rect[0] += self.velocity.x
                    self.coin_rect[1] += self.velocity.y

               


# internal methods   
    
def main():
    size = 700, 500
    screen_width, screen_hight = size
    screen = pygame.display.set_mode((size))
    ball = get_ball(size)
    print("ball: ", ball)
    print("ball velocity: ", ball.velocity)
    paddle = get_paddle()
    print("paddle: ", paddle.rect, paddle.dir) 
    brick = get_brick()
    print("brick: ", brick)
   

def get_ball(size):
    ball = Ball(size)
    return ball 

def get_brick():
    brick = Brick((100, 50, 150), 50, 20)
    return brick 

def get_paddle():
    screen_width = 700
    screen_height = 500
    paddle_width = 120
    paddle_height = 10
    paddle = Paddle(screen_width // 2 - (paddle_width/2), screen_height // 1.1, paddle_width, paddle_height)
    return paddle   
    


if __name__ == '__main__':
    main()

