# metamopp[at]gmail.com

import pygame
from pygame.locals import *
import pygame.freetype
from events import Events

# show the current ranking on screen

class DisplayRanking:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.freetype.Font('assets/DigitalJots.ttf', 50)
        self.font.antialiased = False
        self.font.kerning = False
        self.font.pad = True
        self.hi_string = ' '

    def show_ranking(self, screen, hiscores):
        # iterate over the ranking in database and store rank 1-5 in a string
        for rank in range(5):    
            self.score, self.name = (hiscores.get_entry_at(rank))
            self.rank = rank + 1
            self.hi_string = f"{self.rank}. {self.name} - {self.score}"
            
            # draw highscore list on screen
            self.text_highscore = self.font.render("Score:",pygame.Color(255, 0, 0))
            screen.blit(self.text_highscore[0], (90, 60))
            if self.rank == 1:
                self.highscore_list = self.font.render(self.hi_string, pygame.Color(126, 87, 194))
                screen.blit(self.highscore_list[0], (90, 100))
            elif self.rank == 2:
                self.highscore_list = self.font.render(self.hi_string, pygame.Color(25, 118, 210))
                screen.blit(self.highscore_list[0], (90, 130))
            elif self.rank == 3:
                self.highscore_list = self.font.render(self.hi_string, pygame.Color(0, 200, 83))
                screen.blit(self.highscore_list[0], (90, 160))
            elif self.rank == 4:
                self.highscore_list = self.font.render(self.hi_string, pygame.Color(251, 192, 45))
                screen.blit(self.highscore_list[0], (90, 190))
            elif self.rank == 5:
                self.highscore_list = self.font.render(self.hi_string, pygame.Color(255, 111, 0))
                screen.blit(self.highscore_list[0], (90, 220))

    # user can choose to continue and restart in level 1 or quit the game with key "y" and "n"
    def quit_or_continue(self, screen, events):
        self.quit_or_con = self.font.render("Do you want to continue? y/n", pygame.Color(255, 0, 0))
        screen.blit(self.quit_or_con[0], (90, 310))
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    Events.post_continue_game()
                elif event.key == pygame.K_n:
                    Events.post_quit_game()