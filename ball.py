# metamopp[at]gmail.com

import pygame
from pygame.locals import *
from pygame.math import Vector2
from events import Events
from breakout_sounds import Sounds  

### GAMEOBJECT: BALL ###

# define class for object ball
class Ball:
    def __init__(self, size):
        self.ball_img = pygame.image.load("assets/myball.png")
        self.ball_img.convert()
        self.rect = self.ball_img.get_frect()
        self.center_ball = size[0]//2, size[1]//2
        self.rect.center = self.center_ball
        self.normal = pygame.Vector2(0,0)
        self.velocity = pygame.Vector2(0,0)

    def draw(self, screen):
        screen.blit(self.ball_img, self.rect)

    # how far into this step the ball first touches that brick:
    # 0 = right at the start, 1 = at the very end of the step.
    # Used to pick which of several overlapping bricks was hit FIRST.
    def time_of_impact(self, hit_brick):
        infinite = float('inf')
        # when the ball does not move on an axis it never 'enters' on that axis,
        # so that axis puts no limit on when the contact happens
        if self.velocity[0] > 0:
            entry_x = (hit_brick.rect.left - self.previous_pos.right) / self.velocity[0]
        elif self.velocity[0] < 0:
            entry_x = (hit_brick.rect.right - self.previous_pos.left) / self.velocity[0]
        else:
            entry_x = -infinite # ball is not moving on x-axis
        if self.velocity[1] > 0:
            entry_y = (hit_brick.rect.top - self.previous_pos.bottom) / self.velocity[1]
        elif self.velocity[1] < 0:
            entry_y = (hit_brick.rect.bottom - self.previous_pos.top) / self.velocity[1]
        else:
            entry_y = -infinite # ball is notmoving on x-axis
        # the ball is only really touching once BOTH axes overlap -> the later one wins
        return max(entry_x, entry_y)


    # this method is needed and called in the update-method to find the hit_brick's side of collision
    def find_horizontal_hit(self, hit_brick):
        # using Minkowsi sum:
        # Grow the brick by the ball's size, then trace the ball's CENTER through it.
        # Tracing one corner fails whenever the ball overhangs the brick
        grown = pygame.FRect(
            hit_brick.rect.x - self.rect.width / 2,
            hit_brick.rect.y - self.rect.height / 2,
            hit_brick.rect.width + self.rect.width,
            hit_brick.rect.height + self.rect.height,
        )
        start = self.previous_pos.center
        clipped_line = list(grown.clipline(start + self.rect.center))
        if clipped_line == []:
            # No crossing found. Fall back to the dominant axis instead of silently
            # reporting a side hit - that fallthrough was the teleport bug.
            return abs(self.velocity.y) >= abs(self.velocity.x)
        point_1 = clipped_line[0]
        point_2 = clipped_line[1]
        dis_point_1 = (point_1[0] - start[0])**2 + (point_1[1] - start[1])**2
        dis_point_2 = (point_2[0] - start[0])**2 + (point_2[1] - start[1])**2
        # smallest distance from clipped_line start-/endpoint = (first) intersection
        if dis_point_1 < dis_point_2:
            intersection = point_1
        else:
            intersection = point_2
        # entered through the grown rect's top/bottom edge = hit a horizontal face
        return intersection[1] == grown.top or intersection[1] == grown.bottom


    def update(self, size, paddle, all_bricks, events, gamestate, coins, unused_vector):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.velocity.xy == (0,0):
                    Events.post_start_ball()    
                    gamestate.stopwatch.start()

        # save position for later access
        self.previous_pos = pygame.FRect(self.rect)   

        # collision detection with window boundary     
        self.rect.move_ip(self.velocity * unused_vector)   
        if self.rect.left < 0:
            Sounds.wall_sound.play()
            self.rect.left = 0
            self.velocity[0] *= -1
        if self.rect.right > size[0]:
            Sounds.wall_sound.play()
            self.rect.x = size[0] - self.rect.width
            self.velocity[0] *= -1
        if self.rect.top < 0:
            Sounds.wall_sound.play()
            self.rect.top = 0
            self.velocity[1] *= -1
        if (gamestate.current_level.name == "bonus_1") or (gamestate.current_level.name == "bonus_2") or (gamestate.current_level.name == "bonus_3"):
            if self.rect.bottom > size[1] + 35:
                Events.post_clear_level()
        else:
            if self.rect.bottom > size[1] + 35:
                Events.post_live_lost()

        if len(coins) > 0:
            coin = coins[0]
            if self.rect.collidelist(coin.coins) >= 0: # returns -1 if there is no collision    
                hit_index = self.rect.collidelist(coin.coins) # gives index interger
                # call process_hit to tell coin that it was hit 
                coin.process_hit(hit_index)
            
        # collision detection with paddle
        if self.rect.colliderect(paddle):
            Sounds.touch_paddle.play()
            self.rect.bottom = paddle.rect.top + 1
            distance = (self.rect.centerx -paddle.rect.centerx) / (1.2 * self.rect.width + paddle.rect.width)
            self.normal.xy = distance, -1
            self.normal.normalize_ip()
            self.velocity.reflect_ip(self.normal)
            if abs(self.velocity.y) < (0.25 * self.velocity.length()):
                self.velocity.xy = self.velocity.xy

        # collision detection with bricks 
        # Returns list of all indices containing rects that collide with the Rect. If no intersecting rectangles are found: empty list
        collision_list = self.rect.collidelistall(all_bricks) 
        if len(collision_list) >= 1:
            nearest = None 
            # pick the brick that is reached FIRST in time, not the one whose centre
            # happens to be closest: the ball (35px) is tall enough to overlap two
            # rows at once, and then the nearest centre can be the wrong brick.
            for i in collision_list:
                listed_brick = all_bricks[i]
                distance = self.time_of_impact(listed_brick)
                # first iteration: set the nearest distance to the first distance that was calculated and set current indix as [0] in collision list
                if nearest == None:
                    nearest = distance
                    collision_list[0] = i
                # update: if current distance is smaller than current nearest and set current indix as [0] in collision list
                elif nearest > distance:
                    nearest = distance
                    collision_list[0] = i
                
            # set the nearest colliding brick to hit_brick
            hit_brick = all_bricks[collision_list[0]]
            # call process_hit method
            hit_brick.process_hit(hit_brick, all_bricks, gamestate)

            # DETECT BALL'S DIRECTION AND ON WHICH AXIS IT HITS THE BRICK; CALC CONSUMED VECTOR
            if self.velocity.xy == (0, 0):
                pass
            else:
                # 1 diagonal: from bottomright to topleft
                if self.velocity[0] < 0 and self.velocity[1] < 0:
                    self.start = self.previous_pos.topleft
                    self.end = self.rect.topleft
                    hit_horizontal = self.find_horizontal_hit(hit_brick)
                    # check axis and calc actual vector consumption
                    if hit_horizontal:
                        self.consumed_vector = (hit_brick.rect.bottom - self.previous_pos.top) / self.velocity.y 
                        self.normal.xy = 0, 1   
                    else:
                        self.consumed_vector = (hit_brick.rect.right - self.previous_pos.left) / self.velocity.x 
                        self.normal.xy = -1, 0

                # 2 diagonal: from bottomleft to top right
                elif self.velocity[0] > 0 and self.velocity[1] < 0:
                    self.start = self.previous_pos.topright
                    self.end = self.rect.topright
                    hit_horizontal = self.find_horizontal_hit(hit_brick)
                    # check axis and calc actual vector consumption
                    if hit_horizontal:
                        self.consumed_vector = (hit_brick.rect.bottom - self.previous_pos.top) / self.velocity.y 
                        self.normal.xy = 0, 1
                    else:
                        self.consumed_vector = (hit_brick.rect.left - self.previous_pos.right) / self.velocity.x 
                        self.normal.xy = -1, 0

                # 3 diagonal: from topleft to bottomright
                elif self.velocity[0] < 0 and self.velocity[1] > 0:
                    self.start = self.previous_pos.bottomleft
                    self.end = self.rect.bottomleft
                    hit_horizontal = self.find_horizontal_hit(hit_brick)
                    # check axis and calc actual vector consumption
                    if hit_horizontal :
                        self.consumed_vector = (hit_brick.rect.top - self.previous_pos.bottom) / self.velocity.y 
                        self.normal.xy = 0, -1
                    else:
                        self.consumed_vector = (hit_brick.rect.right - self.previous_pos.left) / self.velocity.x 
                        self.normal.xy = 1, 0

                # 4 diagonal: from topright to bottomleft
                elif self.velocity[0] > 0 and self.velocity[1] > 0:
                    self.start = self.previous_pos.bottomright
                    self.end = self.rect.bottomright
                    hit_horizontal = self.find_horizontal_hit(hit_brick)
                    # check axis and calc actual vector consumption
                    if hit_horizontal:
                        self.consumed_vector = (hit_brick.rect.top - self.previous_pos.bottom) / self.velocity.y 
                        self.normal.xy = 0, -1
                    else:
                        self.consumed_vector = (hit_brick.rect.left - self.previous_pos.right) / self.velocity.x
                        self.normal.xy = -1, 0

                # 5 ball moves vertical: from top to bottom // CAN ONLY BE BOTTOM/TOP HIT ON BRICK
                elif self.velocity[0] == 0 and self.velocity[1] > 0:
                    self.start = self.previous_pos.bottom
                    self.consumed_vector = (hit_brick.rect.top - self.previous_pos.bottom) / self.velocity.y 
                    self.normal.xy = 0, -1    

                # 6 ball moves vertical from bottom to top
                elif self.velocity[0] == 0 and self.velocity[1] < 0:
                    self.start = self.previous_pos.top
                    self.consumed_vector = (hit_brick.rect.bottom - self.previous_pos.top) / self.velocity.y
                    self.normal.xy = 0, 1

                # 7 ball moves horizontal // CAN ONLY BE LEFT/RIGHT HIT ON BRICK
                # velocity is never (0,0) here, so velocity[0] cannot be 0 as well
                elif self.velocity[1] == 0:
                    if self.velocity[0] > 0:   # moving right -> hits the brick's left face
                        self.consumed_vector = (hit_brick.rect.left - self.previous_pos.right) / self.velocity[0]
                    else:                      # moving left  -> hits the brick's right face
                        self.consumed_vector = (hit_brick.rect.right - self.previous_pos.left) / self.velocity[0]
                    self.normal.xy = -1, 0
                
                # Find point of reflection and set ball to reflection position
                # SAFETY NET: consumed_vector is a FRACTION of this step, so it has to
                # stay inside 0..unused_vector. Without this one bad classification
                # can fling the ball hundreds of pixels in a single frame.
                self.consumed_vector = max(0.0, min(self.consumed_vector, unused_vector))

                self.reflect_pos = self.previous_pos.move(self.velocity * self.consumed_vector)
                self.rect.topleft = self.reflect_pos[0:2]
                self.velocity.reflect_ip(self.normal)
                unused_vector -= self.consumed_vector
                self.available_velocity = self.velocity * unused_vector
                self.end_pos = self.rect.topleft + self.available_velocity # ball would end here when it could have used his full velocity
                # require real progress, else a zero-length step could recurse forever
                if unused_vector > 0.01 and self.consumed_vector > 0.0001:
                    self.update(size, paddle, all_bricks, events, gamestate, coins, unused_vector)

                