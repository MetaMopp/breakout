import pygame
from pygame.locals import *
import time
from stopwatch import Stopwatch 
from events import Events
from level import Level
from breakout_sounds import Sounds 
from status_quo import StatusQuo
from draw_display import YouWon, GameOver, LevelDisplay

### GAMESTATE ###

class Gamestate:
    def __init__(self):
        # set initial states
        self.key_behavior = pygame.key.set_repeat(1)
        self.state = 3 # initial state should be 3 = level screen 
        self.lives = 7 # should be 3
        self.start_count = True # should be true
        self.countdown = 0
        self.stopwatch = Stopwatch()
        #self.rounded_time = None # not needed anymore!/?
        self.brick_score = 0 
        self.score = 0
        self.spike_start = True # should be true
        self.spike_count = 0  
        self.coin_score = 0 
        self.levels = Level.get_levels()
        '''index level list: ID, name = 
        Level 42, 1    # 0    Level 43, 2          # 1
        Level 44, 3    # 2    Level 45, "bonus_1"  # 3
        Level 46, 4    # 4    Level 47, 5          # 5
        Level 48, 6    # 6    Level 49, "bonus_2"  # 7
        Level 50, 7    # 8    Level 51, 8          # 9
        Level 52, 9    # 10   Level 53, "bonus_3"  # 11
        Level 54, 10   # 12'''
        self.current_level_index = 10
        self.current_level = self.levels[self.current_level_index]        
        self.status_quo = StatusQuo() 
        self.you_won = YouWon() 
        self.game_over = GameOver()  
        self.level_display = LevelDisplay()


    # GAMESTATE METHODS
    # if level is cleared: count score switch to next level, set counter
    def level_cleared(self):
        self.stopwatch.stop()
        self.rounded_time = round(self.stopwatch.elapsed)
        self.score = self.brick_score - (self.rounded_time // 30)
        if self.score < 0:
            self.score = 0
        if self.current_level_index < len(self.levels)-1:
            self.current_level_index += 1
            self.current_level = self.levels[self.current_level_index]
            self.state = 3  
            self.spike_start = True
            self.start_count = True # enable to re-enter countdown-loop in setupclass
            print("78, game: level.name: ", self.current_level.name, "game: gamestate: ", self.state)
                    
        elif self.state != 2:
            Events.post_you_won()

    def increase_coin_score(self):
        self.coin_score += 1
        if self.coin_score == 30:
            Sounds.gain_sound.play()
            self.lives += 1
            self.coin_score = 0
   
    # if live is lost: subtract live, play sound, recenter ball, enable failure mode
    def live_lost(self, ball):
        self.lives = self.lives - 1 
        Sounds.live_lost_sound.play()
        time.sleep(.6)
        ball.rect.center = ball.center_ball
        ball.velocity.xy = 0,0
        if self.lives == 0:
            self.stopwatch.stop()
            time.sleep(.5)
            Sounds.game_over_sound.play()
            self.state = 1 # failure mode, game over screen

    # set the initial state after pressing "continue: Y" to restart from level 1
    def set_initial_state(self):
        self.key_behavior = pygame.key.set_repeat(1)
        self.brick_score = 0
        self.stopwatch = Stopwatch()
        self.lives = 3
        self.current_level_index = 0 
        self.current_level = self.levels[self.current_level_index]
        self.state = 3