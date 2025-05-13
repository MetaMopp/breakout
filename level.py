# metamopp[at]gmail.com

import pygame
from pygame.locals import *
from wall import Wall
from brick import Brick
from paddle import Paddle
#from gameobject import Paddle
#from gameobject import Spike
from spike import Spike
from coin import Coin
#from gameobject import Coin 

class Level:
    # create a list with all game levels
    def get_levels():
        levels = [Level(
            42,                                                  # ID
            1,                                                   # name
            [0, 4.5],                                            # play_velocity
            [                                                    # brick parameter
                [(100, 0, 220), 1, (0,0), 50, 20, 6, 5, 12, 60, 100, 1],   # [0](color), [1]type, [2]velocity, w, h, c, r, vgap, hgap, dis_left, name
                [(250, 90, 150), 2, (0,0), 30, 20, 4, 4, 33, 81, 162, 1]
            ],
            [],                                                  # obstacle parameter
            [],                                                  # spikes parameter
            [],                                                  # coins parameter
            [1.05, 120, 10]                                      # paddle parameter

        ),
        Level(
            43,                                                  # ID
            2,                                                   # name
            [0, 5],                                              # play_velocity
            [                                                    # brick parameter
                [(0, 120, 220), 1, (0,0.02), 50, 20, 8, 8, 20, 12, 100, 2]      # (color), type, velocity, w, h, c, r, vgap, hgap, dis_left, name
            ],
            [],                                                  # obstacle parameter
            [],                                                  # spikes parameter
            [],                                                  # coins parameter
            [1.05, 120, 10]                                      # paddle parameter
         ),
         Level(
            44,                                                  # ID
            3,                                                   # name
            [0, 5.5],                                            # play_velocity
            [                                                    # brick parameter
                [(200, 0, 150), 1, (0,0), 60, 20, 7, 7, 10, 20, 80, 3]     # (color), type, velocity, w, h, c, r, vgap, hgap, dis_left, name
            ],
            [                                                    # obstacle parameter
                [(50, 70, 50), 0, (0,0), 40, 20, 10, 7, 6, 13, 168, 3]
            ],                                                
            [],                                                  # spikes parameter
            [],                                                  # coins parameter
            [1.05, 100, 10] # paddle parameter
         ),
         Level(
            45,                                                           # ID
            "bonus_1",                                                    # name
            [0, 10],                                                      # play_velocity
            [                                                             # brick parameter
                [(135, 206, 250), 1, (0,0), 50, 50, 4, 8, 20, 12, 108, "bonus_1"]   # (color), type, velocity, w, h, c, r, vgap, hgap, dis_left, name
            ],
            [],                                                           # obstacle parameter
            [],                                                           # spikes parameter
            [                                                             # coins parameter
                [(), 4, 8, 38, 31, 106, "bonus_1"]
            ],                                                
            [1.05, 200, 10]                                               # paddle parameter
         ),
         Level(
            46,                                                  # ID
            4,                                                   # name
            [0, 6],                                              # play_velocity
            [                                                    # brick parameter
                [(0, 200, 150), 1, (0,0.035), 50, 20, 6, 9, 10, 10, 95, 4]    # (color), type, velocity, w, h, c, r, vgap, hgap, dis_left, name
            ],
            [],                                                  # obstacle parameter
            [],                                                  # spikes parameter
            [],                                                  # coins parameter
            [1.05, 95, 10]                                       # paddle parameter
         ),
         Level(
            47,                                                  # ID
            5,                                                   # name
            [0, 6],                                              # play_velocity
            [                                                    # brick parameter
                [(255, 140, 0), 1, (0,0), 40, 20, 10, 10, 5, 15, 82, 5]    # (color), type, velocity, w, h, c, r, vgap, hgap, dis_left, name
            ],
            [                                                    # obstacle parameter
                [(180, 180, 180), 0, (0,0), 50, 15, 8, 9, 10, 8, 92, 5]
            ],                                                
            [],                                                  # spikes parameter
            [],                                                  # coins parameter
            [1.05, 85, 10]                                       # paddle parameter

        ),
        Level(
            48,                                                  # ID
            6,                                                   # name
            [0, 6.5],                                            # play_velocity
            [                                                    # brick parameter
                [(180, 255, 30), 1, (0,0), 55, 20, 6, 4, 20, 68, 133, 6],  # (color), type, velocity, w, h, c, r, vgap, hgap, dis_left, name
                [(50, 100, 250), 2, (0,0), 40, 20, 5, 5, 30, 82, 83, 6]
            ],
            [],                                                  # obstacle parameter
            [],                                                  # spikes parameter
            [],                                                  # coins parameter
            [1.05, 90, 10]                                       # paddle parameter

        ),
        Level(
            49,                                                        # ID
            "bonus_2",                                                 # name
            [0, 10],                                                   # play_velocity
            [                                                          # brick parameter
                [(125, 7, 50), 1, (0,0), 50, 50, 4, 8, 20, 12, 117,  "bonus_2"]  # (color), type, velocity, w, h, c, r, vgap, hgap, dis_left, name
            ],
            [],                                                        # obstacle parameter
            [],                                                        # spikes parameter
            [                                                          # coins parameter
                [(), 4, 8, 40, 31, 106, "bonus_2"]
            ],                                                
            [1.05, 200, 10]                                            # paddle parameter
         ),
         Level(
            50,                                                  # ID
            7,                                                   # name
            [0, 7],                                              # play_velocity
            [                                                    # brick parameter
                [(130, 100, 230), 1, (0,0), 55, 20, 6, 9, 20, 8, 72, 7]    # (color), type, velocity, w, h, c, r, vgap, hgap, dis_left, name
            ],
            [],                                                  # obstacle parameter
            [                                                    # spikes parameter
                [(190, 190, 0), [[147, 70], [177, 70], [162, 100]]],
                [(190, 190, 0), [[274, 70], [304, 70], [289, 100]]],
                [(190, 190, 0), [[401, 70], [431, 70], [416, 100]]],
                [(190, 190, 0), [[528, 70], [558, 70], [543, 100]]]
            ],                                                
            [],                                                  # coins parameter
            [1.05, 85, 10]                                       # paddle parameter
         ),
         Level(
            51,                                                  # ID
            8,                                                   # name
            [0, 7.5],                                            # play_velocity
            [                                                    # brick parameter
                [(0, 200, 70), 1, (0,0), 40, 20, 7, 6, 25, 20, 180, 8]     # (color), type, velocity, w, h, c, r, vgap, hgap, dis_left, name
            ],
            [                                                    # obstacle parameter
                [(230, 200, 5), 0, (0,0), 30, 25, 8, 2, 6, 400, 120, 8]
            ],                                                
            [                                                    # spikes parameter
                [(128, 0, 128), [[60, 70], [100, 70], [80, 100]]],
                [(128, 0, 128), [[610, 70], [650, 70], [630, 100]]],
                [(128, 0, 128), [[60, 70], [100, 70], [80, 100]]],
                [(128, 0, 128), [[610, 70], [650, 70], [630, 100]]]
            ],                                                
            [],                                                  # coins parameter
            [1.05, 90, 10]                                       # paddle parameter
         ),
         Level(
            52,                                                  # ID
            9,                                                   # name
            [0, 7.5],                                            # play_velocity
            [                                                    # brick parameter
                [(0, 200, 200), 1, (0,0.06), 55, 20, 6, 4, 20, 68, 133, 9] ,  # (color), type, velocity, w, h, c, r, vgap, hgap, dis_left, name
                [(255, 255, 100), 2, (0,0), 40, 20, 6, 5, 25, 82, 83, 9]
            ],
            [],                                                  # obstacle parameter
            [],                                                  # spikes parameter
            [],                                                  # coins parameter
            [1.05, 90, 10]                                       # paddle parameter

        ),
        Level(
            53,                                                        # ID
            "bonus_3",                                                 # name
            [0, 11],                                                   # play_velocity
            [                                                          # brick parameter
                [(250, 0, 100), 1, (0,0.05), 50, 50, 4, 8, 22, 17, 125, "bonus_3"]  # (color), type, velocity, w, h, c, r, vgap, hgap, dis_left, name
            ],
            [],                                                        # obstacle parameter
            [],                                                        # spikes parameter
            [                                                          # coins parameter
                [(), 6, 7, 42, 38, 121, "bonus_3"]
            ],                                                
            [1.05, 200, 10]                                            # paddle parameter
         ),
         Level(
            54,                                                  # ID
            10,                                                  # name
            [0, 8.5],                                            # play_velocity
            [                                                    # brick parameter
                [(250, 50, 150), 2, (0,0.05), 50, 20, 7, 5, 9, 55, 130, 10],  # (color), type, velocity, w, h, c, r, vgap, hgap, dis_left, name
                [(70, 130, 180), 1, (0,0.03), 45, 20, 7, 5, 9, 60, 80, 10]
            ],
            [                                                    # obstacle parameter
                [(190, 190, 190), 0, (0,0.01), 40, 15, 1, 10, 4, 8, 110, 10]
            ],                                                
            [                                                    # spikes parameter
                [(255, 191, 0), [[113, 90], [143, 90], [128, 120]]],
                [(255, 191, 0), [[259, 90], [289, 90], [274, 120]]],
                [(255, 191, 0), [[403, 90], [432, 90], [417, 120]]],
                [(255, 191, 0), [[547, 90], [577, 90], [562, 120]]]
            ],                                                
            [],                                                  # coins parameter
            [1.05, 90, 10]                                       # paddle parameter
         )

        ]
        return levels


    def __init__(self, ID, name, play_velocity, wall_p, obstacles_p, spikes_p, coins_p, paddle_p):
        self.ID =  ID # level 1 = 42, level 10: 54
        self.name = name
        self.play_velocity = play_velocity
        self.wall_p = wall_p
        self.obstacles_p = obstacles_p
        self.spikes_p = spikes_p
        self.coins_p = coins_p
        self.paddle_p = paddle_p
        
    # iterate over the paramters and return the object
    def get_walls(self):     
        walls = []
        for p in self.wall_p:
            wall = Wall(p[3], p[4], p[5], p[6], p[7], p[8], p[9])
            #brick = Brick(p[0], p[1], p[2], p[3])
            wall.pattern(p[10], p[0], p[1], p[2]) #p[0]=color, p[1]=type, p[2]= velocity
            #brick.build_wall(p[4], p[5], p[6], p[7], p[8], p[9])
            walls.append(wall)
        return walls
    
    def get_obstacles(self):
        obstacles = []
        n_bricks = 0
        for p in self.obstacles_p:
            obstacle = Wall(p[3], p[4], p[5], p[6], p[7], p[8], p[9])
            #obstacle = Brick(p[0], p[1], p[2], p[3])
            obstacle.build_obstacle(p[10], p[0], p[1], p[2])
            obstacles.append(obstacle)
            n_bricks += len(obstacle.bricks)
        return obstacles, n_bricks
    
    def get_spikes(self):
        spikes = []
        for p in self.spikes_p:
            spike = Spike(p[0], p[1])
            spikes.append(spike)
        return spikes

    def get_coins(self):
        coins = []
        for p in self.coins_p:
            coin = Coin()
            coin.pattern(p[1], p[2], p[3], p[4], p[5], p[6])
            coins.append(coin)
        return coins
        
    def get_paddle(self, size):
        p = self.paddle_p
        return Paddle(size[0] // 2 - (p[1]/2), size[1] // p[0], p[1], p[2])
         

                   

    
        
       

            
           
           