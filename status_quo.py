# metamopp[at]gmail.com

import pygame
from pygame.locals import *
import pygame.freetype

# Draw heads up dislplay: elapsed time, score, lives

class StatusQuo:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.freetype.Font('assets/DigitalJots.ttf', 45)
        self.font.antialiased = False
        self.font.kerning = False
        self.font.pad = True

    def update(self, lives, stopwatch, brick_score):
        self.your_lives = self.font.render("Lives: " + str(lives), pygame.Color(250, 200, 100), pygame.Color(27, 27, 27))
        self.rounded = round(stopwatch.elapsed)
        self.time_elapsed = self.font.render("Time: " + str(self.rounded), pygame.Color(250, 200, 100), pygame.Color(27, 27, 27))
        self.current_score = self.font.render("Score: " + str(brick_score), pygame.Color(250, 200, 100), pygame.Color(27, 27, 27))

    def draw(self, screen):
        screen.blit(self.your_lives[0], (490, 10))
        screen.blit(self.time_elapsed[0], (80, 10))
        screen.blit(self.current_score[0], (270, 10))

