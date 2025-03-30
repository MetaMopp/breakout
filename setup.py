# metamopp[at]gmail.com

import pygame
from pygame.locals import *
import pygame.freetype
from game import Game
from events import Events

# initialize the game setup and mainloop

class Setup:
    def __init__(self):
        ### PYGAME SETUP ###
        self.title = pygame.display.set_caption("BREAKOUT") 
        self.init = pygame.init()
        self.clock = pygame.time.Clock()

        # define background; set screen size
        self.background = pygame.Color(27, 27, 27)
        self.size = 700, 800
        self.screen_width = self.size[0]
        self.screen_height = self.size[1]
        self.screen = pygame.display.set_mode((self.size))

    def run_game(self):
        self.game = Game()
        self.game.game_level(self.size)
        self.current_level_ID = self.game.gamestate.current_level.ID
        print("setup 28: initial gamestate: ", self.game.gamestate.state)
        
        ### MAINLOOP ###
        while self.game.running:
            self.screen.fill(self.background) # clear display
            # EVENTLOOP : SET NEW STATES AND LEVELS AFTER CLEARING THE CURRENT LEVEL
            events = pygame.event.get() 
            for event in events:
                if event.type == pygame.QUIT:
                    self.game.running = False
                # START BALL
                elif event.type == Events.START_BALL:
                    self.game.ball.velocity.xy = self.game.gamestate.current_level.play_velocity
                # INCREASE COIN SCORE
                elif event.type == Events.INCREASE_COIN_SCORE:
                    self.game.gamestate.increase_coin_score()
                # LIVE LOST: substracte live, enable failure mode
                elif event.type == Events.LIVE_LOST:
                    self.game.gamestate.live_lost(self.game.ball)
                # CLEAR LEVEL: stop time, count score, increase level if not last level, enable succes mode
                elif event.type == Events.CLEAR_LEVEL:
                    self.game.gamestate.level_cleared()
                # DRAW YOU-WON_SCREEN
                elif event.type == Events.YOU_WON:
                    self.game.gamestate.start_count = True
                    self.game.gamestate.state = 2 # success
                    print("should be gamestate 2: ", self.game.gamestate.state)
                # ENTER HIGHSCORE: enables user input on screen
                elif event.type == Events.ENTER_HIGHSCORE:
                    self.game.gamestate.state = 4
                    print("should be gamestate 4: ", self.game.gamestate.state)
                # HIGHSCORE-DB: save score and username in database
                elif event.type == Events.FINISHED_ENTRY:
                    self.game.hiscores.add(self.game.gamestate.score, self.game.enter_score.text_db)
                    Events.post_show_ranking()
                # SHOW RANKING: display current ranking and give choice to quit or continue game
                elif event.type == Events.SHOW_RANKING:
                    self.game.gamestate.state = 5
                    print("should be gamestate 5: ", self.game.gamestate.state)
                # CONTINUE GAME: return to gameplay mode and set to level 1
                elif event.type == Events.CONTINUE_GAME:
                    self.key_behavior = pygame.key.set_repeat(1)
                    self.game.gamestate.current_level_index = 0 
                    self.game.gamestate.current_level = self.game.gamestate.levels[self.game.gamestate.current_level_index]
                    self.game.gamestate.state = 3
                    print("should be gamestate 3: ", self.game.gamestate.state)
                # QUIT GAME
                elif event.type == Events.QUIT_GAME:
                    self.game.running = False 
                
            # detect if game level_ID has changed and if so call game_level method
            if self.current_level_ID != self.game.gamestate.current_level.ID:
                self.game.game_level(self.size)
                self.current_level_ID = self.game.gamestate.current_level.ID
                print("setup 85: self.game.gamestate.current_level.ID", self.game.gamestate.current_level.ID)
                print("setup 86: current level_ID: ", self.current_level_ID)
                print("setup 87: current level: ", self.game.gamestate.current_level.name)

            # enable visibility of level screen by setting the counter to 150 frames
            if (self.game.gamestate.state == 3 or self.game.gamestate.state == 2) and self.game.gamestate.start_count == True :
                self.game.gamestate.countdown = 150
                self.game.gamestate.start_count = False # disable to refresh the counter
                
            # set countdown for falling spikes
            if ((self.game.gamestate.current_level.name ==  7) or (self.game.gamestate.current_level.name == 8) or (self.game.gamestate.current_level.name == 10)) and self.game.gamestate.spike_start == True:
                self.game.gamestate.spike_count = 2600
                self.game.gamestate.spike_start = False        
                
            self.game.game_mode(self.size, events, self.screen)

            # DISPLAY MODE
            pygame.display.update()
            self.clock.tick(60)
            #print("end of frame")

            # COUNTER
            # countdown level screen visible in frames
            if self.game.gamestate.countdown > 0:
                self.game.gamestate.countdown = self.game.gamestate.countdown - 1
                #print(self.game.gamestate.countdown)
            else: 
                self.game.gamestate.countdown = 0
            # countdown for falling spikes
            if self.game.gamestate.spike_count > 0:
                self.game.gamestate.spike_count = self.game.gamestate.spike_count - 1
            else: 
                self.game.gamestate.spike_count = 0    

        pygame.quit()






