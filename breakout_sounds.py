# metamopp[at]gmail.com

import pygame

### FREE SOUNDS FROM MIXKIT.CO ### 

class Sounds:
    
    pygame.mixer.init()

    destroy_brick = pygame.mixer.Sound("assets/mixkit-brick-2.wav") 
    level_sound = pygame.mixer.Sound("assets/mixkit-level.wav")
    game_over_sound = pygame.mixer.Sound("assets/mixkit-game-over.wav")
    obstacle_clash = pygame.mixer.Sound("assets/mixkit-obstacle-2.wav")
    spike_sound = pygame.mixer.Sound("assets/mixkit-spike-2.wav")
    touch_brick = pygame.mixer.Sound("assets/mixkit-2-hit-brick.wav")
    touch_paddle = pygame.mixer.Sound("assets/mixkit-paddle.wav")
    wall_sound = pygame.mixer.Sound("assets/mixkit-wall.wav")
    live_lost_sound = pygame.mixer.Sound("assets/mixkit-losing.wav")
    gain_sound = pygame.mixer.Sound("assets/mixkit-gain.wav")
    coin_sound = pygame.mixer.Sound("assets/mixkit-coin.wav")

    destroy_brick.set_volume(0.3)
    spike_sound.set_volume(0.4)
    level_sound.set_volume(0.4)
    game_over_sound.set_volume(1)
    touch_brick.set_volume(0.3)
    touch_paddle.set_volume(0.2)
    wall_sound.set_volume(0.1)
    live_lost_sound.set_volume(0.3)
    gain_sound.set_volume(0.4)
    coin_sound.set_volume(0.3)