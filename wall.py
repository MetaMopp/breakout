# metamopp[at]gmail.com

from pygame.locals import *
from brick import Brick

# define a class wall, consisting of bricks
class Wall: 
    def __init__(self, width, hight, column, row, vgap, hgap, dis_left):
        self.width = width
        self.hight = hight
        self.column = column 
        self.row = row 
        self.vgap = vgap
        self.hgap = hgap
        self.dis_left = dis_left
        self.bricks =[] # list of bricks
       
    ### WALL PATTTERNS ###
    def build_destructibles(self, name, color, hit_type, velocity):
        DISTANCETOP = 70 # replace this later: self.dis_top
        if name == 1 or name == "bonus_1":
            for column in range(self.column):
                y = DISTANCETOP + column * (self.hight + self.vgap)
                for row in range(self.row):
                    x = self.dis_left + row * (self.width + self.hgap)
                    self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight)) #color, hit_type, velocity, x, y, width, hight
       
        elif name == 2 or name == 8:
            for column in range(self.column):
                y = DISTANCETOP + column * (self.hight + self.vgap)
                for row in range(self.row):
                    if column % 2 == 0:
                        x = (self.dis_left + 10) + row * (self.width + self.hgap)
                    else:
                        x = (self.dis_left - 10) + row * (self.width + self.hgap)
                    self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))
        
        elif (name == 3) or (name == 7) or (name == "bonus_3"):
            for column in range(self.column):
                if name == "bonus_3":
                    y = 140 + column * (self.hight + self.vgap)
                else:
                    y = DISTANCETOP + column * (self.hight + self.vgap)
                for row in range(0, self.row, +2):
                    x = self.dis_left + row * (self.width + self.hgap)
                    self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))
        
        elif name == 4:
            for column in range(self.column-4, self.column+9, +1):
                y = 20 + column * (self.hight + self.vgap)
                if column % 2 == 0:
                    for row in range(self.row):
                        x = self.dis_left + row * (self.width + (self.hgap-3))
                        self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))
                elif column % 3 == 0:
                    for row in range(self.row - 5):
                        x = (self.dis_left + 127) + row * (self.width + (self.hgap+8))
                        self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))
                else:
                    for row in range(self.row - 3):
                        x = (self.dis_left + 73) + row * (self.width + (self.hgap+2))
                        self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))
        
        elif name == 5:
            for column in range(0, self.column, +3):
                y = DISTANCETOP + column * (self.hight + self.vgap)
                for row in range(0, self.row):
                    x = self.dis_left + row * (self.width + self.hgap)
                    self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))
 
        elif name == 6:
            for column in range(self.column):
                y = DISTANCETOP + column * (self.hight + self.vgap)
                for row in range(self.row):
                    x = self.dis_left + row * (self.width + self.hgap)
                    self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))

        elif name == 9:
            for column in range(2, self.column):
                y = DISTANCETOP+30 + column * (self.hight + self.vgap)
                for row in range(self.row):
                    x = self.dis_left + row * (self.width + self.hgap)
                    self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))
   
        elif name == 10:
            for column in range(2, self.column):
                y = 70 + column * (self.hight + self.vgap+10)
                if column % 2 == 0:
                    for row in range(self.row):
                        x = self.dis_left + row * (self.width + (self.hgap))
                        self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))
                elif column % 3 == 0:
                    for row in range(self.row):
                        x = (self.dis_left + 20) + row * (self.width + (self.hgap))
                        self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))
                else:
                    for row in range(self.row):
                        x = (self.dis_left+20) + row * (self.width + (self.hgap))
                        self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))

        elif name == "bonus_2":
            for column in range(self.column-2, self.column+5, +1):
                y = 20 + column * (self.hight + self.vgap)
                if column % 2 == 0:
                    for row in range(self.row):
                        x = self.dis_left + row * (self.width + (self.hgap-3))
                        self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))
                elif column % 3 == 0:
                    for row in range(self.row - 5):
                        x = (self.dis_left + 127) + row * (self.width + (self.hgap+8))
                        self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))
                else:
                    for row in range(self.row - 3):
                        x = (self.dis_left + 73) + row * (self.width + (self.hgap+2))
                        self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))

    ### OBSTACLE PATTERNS ###
    def build_obstacles(self, name, color, hit_type, velocity):
        DISTANCETOP = 70 
        
        if name == 3:
            for column in range(self.column):
                y = DISTANCETOP + column * (self.hight + self.vgap)
                for row in range(0, self.row, +3):
                    x = self.dis_left + row * (self.width + self.hgap)
                    self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))

        elif name == 5:
            for column in range(2, self.column+1, +3):
                y = DISTANCETOP + column * (self.hight + self.vgap)
                for row in range(self.row):
                    x = self.dis_left + row * (self.width + self.hgap)
                    self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))
        
        elif name == 8:
            for column in range(self.column):
                y = DISTANCETOP+25 + column * (self.hight + self.vgap)
                for row in range(self.row):
                    x = self.dis_left + row * (self.width + self.hgap)
                    self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))

        elif name == 10:
            for column in range(self.column):
                y = DISTANCETOP-10 + column * (self.hight + self.vgap)
                for row in range(0, self.row):
                    x = self.dis_left + row * (self.width + self.hgap)
                    self.bricks.append(Brick(color, hit_type, velocity, x, y, self.width, self.hight))
                               