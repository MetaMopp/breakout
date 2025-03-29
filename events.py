# metamopp[at]gmail.com

import pygame
from pygame.locals import *

### COSTUM EVENTS ###

class Events:
    START_BALL = pygame.event.custom_type()
    def post_start_ball():
        pygame.event.post(pygame.event.Event(Events.START_BALL))
                          
    CLEAR_LEVEL = pygame.event.custom_type()
    def post_clear_level():
        pygame.event.post(pygame.event.Event(Events.CLEAR_LEVEL))

    INCREASE_COIN_SCORE = pygame.event.custom_type()
    def post_increase_coin_score():
        pygame.event.post(pygame.event.Event(Events.INCREASE_COIN_SCORE))

    LIVE_LOST = pygame.event.custom_type()
    def post_live_lost():
        pygame.event.post(pygame.event.Event(Events.LIVE_LOST))

    YOU_WON = pygame.event.custom_type()
    def post_you_won():
        pygame.event.post(pygame.event.Event(Events.YOU_WON))
    
    ENTER_HIGHSCORE = pygame.event.custom_type()
    def post_enter_highscore():
        pygame.event.post(pygame.event.Event(Events.ENTER_HIGHSCORE))

    FINISHED_ENTRY = pygame.event.custom_type()
    def post_finished_entry(text_db):
        pygame.event.post(pygame.event.Event(Events.FINISHED_ENTRY))

    SHOW_RANKING = pygame.event.custom_type()
    def post_show_ranking():
        pygame.event.post(pygame.event.Event(Events.SHOW_RANKING))

    CONTINUE_GAME = pygame.event.custom_type()
    def post_continue_game():
        pygame.event.post(pygame.event.Event(Events.CONTINUE_GAME))

    QUIT_GAME = pygame.event.custom_type()
    def post_quit_game():
        pygame.event.post(pygame.event.Event(Events.QUIT_GAME))