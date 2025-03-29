# metamopp[at]gmail.com

import pygame
from pygame.locals import *
import pygame.freetype

# Draw the display "you won", "game over" and the name of the current level on the screen

class YouWon:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.freetype.Font('assets/DigitalJots.ttf', 70)
        self.font.antialiased = False
        self.font.kerning = False
        self.font.pad = True

    def draw(self, screen, rounded_time):
        won = self.font.render("You won!", pygame.Color(255, 0 , 0))
        screen.blit(won[0], (250, 250))
        your_time = self.font.render("Time: " + str(rounded_time) + " sec", pygame.Color(255, 0, 0))
        screen.blit(your_time[0], (180, 320))
        

class GameOver:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.freetype.Font('assets/DigitalJots.ttf', 100)
        self.font.antialiased = False
        self.font.kerning = False
        self.font.pad = True

    def draw(self, screen):
        game_over = self.font.render("game over", pygame.Color(255, 0, 0))
        screen.blit(game_over[0], (200, 250))


class LevelDisplay():
    def __init__(self):
        pygame.font.init()
        self.font = pygame.freetype.Font('assets/DigitalJots.ttf', 100)
        self.font.antialiased = False
        self.font.kerning = False
        self.font.pad = True

    def draw(self, screen, name, ID):
        if (ID == 45) or (ID == 49) or (ID == 53):
            self.level_title = 'BONUS'
            blit_x = 250
        else:
            self.level_title = f"Level {name}"
            blit_x = 220
        
        self.title_image = self.font.render(self.level_title, pygame.Color(230, 165, 15))
        screen.blit(self.title_image[0], (blit_x, 250))
        




        
