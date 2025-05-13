# metamopp[at]gmail.com

import pygame
from pygame.locals import *
from stopwatch import Stopwatch 
from events import Events
from ball import Ball
from gamestate import Gamestate
from breakout_sounds import Sounds 
from hiscores import HiScores
from enter_highscore import EnterScore
from display_ranking import DisplayRanking

### GAME: OBJECTS, MODES & LEVEL ###

class Game:
    def __init__(self):
        self.running = True
        self.gamestate = Gamestate()
        self.hiscores = HiScores("assets/highscore.csv")
        self.enter_score = EnterScore()
        self.display_ranking = DisplayRanking()
        
    # set game levels    
    def game_level(self, size):
        self.walls = self.gamestate.current_level.get_walls()
        self.obstacles, self.n_bricks = self.gamestate.current_level.get_obstacles()
        # loop through all lists and create single list with all bricks
        self.wall = []
        self.obstacle = []
        self.all_bricks= []
        for wall in self.walls:
            self.wall.append(wall)
            for brick in wall.bricks:
                self.all_bricks.append(brick)
        for obstacle in self.obstacles:
            self.obstacle.append(obstacle)
            for brick in obstacle.bricks:
                self.all_bricks.append(brick)
        
        self.spikes = self.gamestate.current_level.get_spikes()
        self.coins = self.gamestate.current_level.get_coins()
        self.paddle = self.gamestate.current_level.get_paddle(size)
        self.ball = Ball(size)
                   
    
    # GAME MODES: 0 = play, 1 = failure, 2 = success, 3 = level display               
    def game_mode(self, size, events, screen):
        
        # PLAY 
        if self.gamestate.state == 0: # game play mode    
            # UPDATE GAMEOBJECTS 
            self.gamestate.status_quo.update(self.gamestate.lives, self.gamestate.stopwatch, self.gamestate.brick_score)
            self.paddle.update(size[0], events)
            self.ball.update(size, self.paddle, self.all_bricks, events, self.gamestate, self.coins, 1) 

            # clear complete list of bricks  and post CLEAR LEVEL event
            for brick in self.all_bricks:
                brick.update(size)
                #print("n_bricks: ", self.n_bricks)
                #print("game 141: len all_bricks: ", len(self.all_bricks))
            if (len(self.all_bricks) == self.n_bricks) and (self.coins == []):
                print(len(self.all_bricks))
                if len(self.spikes) != 0:
                    self.spikes.clear()
                Events.post_clear_level()

            # update spikes
            for spike in self.spikes:
                spike.update(self.paddle, self.gamestate)

            # update coins and clear list of coins       
            clear_coins = 0
            for coin in self.coins:
                coin.update(self.gamestate)
                if coin.coins == []:
                    clear_coins += 1
                    self.coins.clear()                                                              
        
            # DRAW GAMEOBJECTS
            self.gamestate.status_quo.draw(screen)
            self.ball.draw(screen)
            self.paddle.draw(screen)

            for coin in self.coins:
                coin.draw(screen)

            for brick in self.all_bricks:
                brick.draw(screen)

            for spike in self.spikes:
                spike.draw(screen)

                
        # GAME OVER:
        elif self.gamestate.state == 1: # failure mode
            self.gamestate.game_over.draw(screen)
               
        # YOU WON
        elif self.gamestate.state == 2: # success mode
            self.gamestate.you_won.draw(screen, self.gamestate.rounded_time)
        
            if self.gamestate.countdown == 0:
                #compare current to listed highscores, post if current highscore > listed highscore
                length_list = self.hiscores.len()
                if length_list < 5:
                    Events.post_enter_highscore()
                else:
                    for rank in range(5):   
                        self.list_score, self.list_name = (self.hiscores.get_entry_at(rank))
                        self.list_rank = rank + 1
                        if self.gamestate.score > self.list_score:
                            Events.post_enter_highscore()
                        else:
                            Events.post_show_ranking()
    
        # DRAW LEVEL DISPLAY ON SCREEN, PLAY SOUND, RESET STATE
        elif self.gamestate.state == 3: # level display mode
            self.gamestate.level_display.draw(screen, self.gamestate.current_level.name, self.gamestate.current_level.ID) #self.gamestate.level, self.gamestate.level_ID,
            Sounds.level_sound.play()
            if self.gamestate.countdown == 0:
                    self.gamestate.state = 0
            
        
        # ENTER USER INPUT ON SCREEN
        elif self.gamestate.state == 4:
            self.gamestate.key_behavior = pygame.key.set_repeat(0)
            # method call to enter name on screen
            self.enter_score.update_string(events, screen, self.gamestate.score)

 
        # SHOW THE TOP 5 HIGHSCORES AND QUIT OR CONTINUE TO PLAY
        elif self.gamestate.state == 5: 
            self.display_ranking.show_ranking(screen, self.hiscores)  
            self.display_ranking.quit_or_continue(screen, events)
            
            


       

# internal methods; no need to call these methods from outside this class

def main():
    game = get_game() # 1
    print(f"running: {game.running}", "rounded_time: ", {game.gamestate.rounded_time})

def get_game(): # 1
    game = Game()
    game.running = True
    game.gamestate.state = 0
    game.gamestate.level = 1
    game.gamestate.lives = 2
    game.gamestate.brick_score = 0
    game.gamestate.score = 0
    game.gamestate.rounded_time = None 
    return game 

if __name__ == "__main__":
    main()
