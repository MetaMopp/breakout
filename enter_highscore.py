# metamopp[at]gmail.com

import pygame
from pygame.locals import *
import pygame.freetype
from events import Events

# enter name for highscore list on screen

class EnterScore:
    def __init__(self):
          self.valid_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890-_'
          self.user_input = ''
          self.min_length = 1
          self.max_length = 16
          self.text_db = ''   
          pygame.font.init()
          self.font = pygame.freetype.Font('assets/DigitalJots.ttf', 50)
          self.font.antialiased = False
          self.font.kerning = False
          self.font.pad = True       

    def update_string(self, events, screen, score):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # check for keystrokes (unicode) and add to string as user input
                if len(event.unicode) == 1 and event.unicode in self.valid_chars:
                    self.user_input = self.user_input + event.unicode
                    if len(self.user_input) == self.max_length:
                        self.user_input = self.user_input[:-1]
                # delete last char in string if backspace was pushed   
                elif event.key == pygame.K_BACKSPACE:
                    self.user_input = self.user_input[:-1]
                # save user_input in self.text_db and post event that the entry has been finished
                elif (len(self.user_input) >= self.min_length) and (event.key == pygame.K_RETURN):
                    self.text_db = self.user_input
                    Events.post_finished_entry(self.text_db)
        
        self.text_score = self.font.render("New Highscore: " + str(score), pygame.Color(255, 0, 0))
        screen.blit(self.text_score[0], (55, 210))

        self.text_display = self.font.render("Enter your name: " + str(self.user_input), pygame.Color(255, 0, 0))
        screen.blit(self.text_display[0], (55, 250))
                







# internal methods

def main():
    events = pygame.event.get() 
    text = get_text()
    print(text)

def get_text(events):
    test = EnterScore()
    test.update_string(events)
    return test.user_input


if __name__ == "__main__":
    main()

