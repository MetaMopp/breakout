# metamopp[at]gmail.com

import pygame
from pygame.locals import *
import pygame.freetype
import time
from stopwatch import Stopwatch 
from events import Events
from ball import Ball
#from gameobject import Ball
from level import Level
from breakout_sounds import Sounds 
from status_quo import StatusQuo
from draw_display import YouWon, GameOver, LevelDisplay
from hiscores import HiScores
from enter_highscore import EnterScore
from display_ranking import DisplayRanking

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
        self.rounded_time = None
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
        self.current_level_index = 2
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
        print("all bricks: ",len(self.all_bricks))

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
            self.ball.update(size, self.paddle, self.all_bricks, events, self.gamestate) 

            # clear bricks
            for brick in self.all_bricks:
                brick.update(size)
                print("len all_bricks: ", len(self.all_bricks))
                if (len(self.all_bricks) == self.n_bricks) and (self.coins == []):
                    if len(self.spikes) != 0:
                        self.spikes.clear()
                    Events.post_clear_level()

            # clear bricks/walls and post CLEAR LEVEl event
            '''clear_walls = 0
            for wall in self.walls:
                wall.update(size) 
                if wall.bricks == []:
                    clear_walls += 1
                if ((clear_walls > 0 and clear_walls == len(self.walls))) and (self.coins == []):
                    if len(self.spikes) != 0:
                        self.spikes.clear()
                    Events.post_clear_level()

            # update obstacle wall
            for obstacle in self.obstacles:
                obstacle.update_obstacle(self.ball, size)'''

            # update spikes
            for spike in self.spikes:
                spike.update(self.paddle, self.gamestate)

            # update coins and clear list of coins       
            clear_coins = 0
            for coin in self.coins:
                coin.update(self.ball, self.gamestate)
                if coin.coins == []:
                    clear_coins += 1
                    self.coins.clear()                                                              
        
            # DRAW GAMEOBJECTS
            self.gamestate.status_quo.draw(screen)
            self.ball.draw(screen)
            self.paddle.draw(screen)

            for coin in self.coins:
                coin.draw(screen)

            for wall in self.walls:
                wall.draw(screen)

            for obstacle in self.obstacles:
                obstacle.draw(screen)

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
    game = get_game() #1
    print(f"running: {game.running}", "rounded_time: ", {game.gamestate.rounded_time})

    gamestate = get_game_state() #2
    print(f"state {gamestate.state}, brick_score {gamestate.brick_score}, score {gamestate.score}, lives {gamestate.lives}")

    game_state, game_lives, game_level = get_game_level() #3
    print(f"game_state: {game_state}, game_lives: {game_lives}, game_level: {game_level}")
 

def get_game(): #1
    game = Game()
    game.running = True
    game.gamestate.state = 0
    game.gamestate.level = 1
    game.gamestate.lives = 2
    game.gamestate.brick_score = 0
    game.gamestate.score = 0
    game.gamestate.rounded_time = None 
    return game 

def get_game_state(): #2
    gamestate = Gamestate()
    gamestate.state = 3
    gamestate.brick_score = 78
    gamestate.score = 100
    gamestate.lives = 2
    gamestate.rounded_time = 50
    return gamestate

def get_game_level(): #3
    gamestate = Gamestate()
    gamestate.state = 0
    gamestate.lives = 5
    gamestate.level = 1
    gamestate.brick_score = 78
    gamestate.score = 0
    gamestate.rounded_time = None
    return gamestate.state, gamestate.lives, gamestate.level 


if __name__ == "__main__":
    main()
