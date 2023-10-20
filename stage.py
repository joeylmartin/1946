import pygame, random, game, constants, library

#GAMEPLAY HAS THREE LAYERS:
#BACKGROUND(ex. water, desert, etc.)
#MIDGROUND(ex. clouds, trees, etc.); this travels at twice the speed of background.
# -- note; midlayer will have its objects randomly placed. 
#GAMEPLAY(y'know, where you move around) 
CLOUD_OPACITY = 150
SCROLLING = True
class Cloud():

    def __init__(self, position, size, image):
        self.rect = pygame.Rect(position, size)
        self.image = image
        self.shadow_offset_x = -15
        self.shadow_offset_y = 15

class Stage(object):
    BACKGROUND_SPEED = 3 / constants.FRAME_RATE_MULTIPLIER
    MID_SPEED = 2 * BACKGROUND_SPEED

    def __init__(self, background_image):
        self.background_image = background_image
        
        screen_height = pygame.display.get_surface().get_height()
        self.mg = pygame.image.load('assets/game/stage/cloud.png').convert_alpha()
        self.background_y_offset = 0
        self.done = False
        mg_size= self.mg.get_size()
        self.cloud_list = [Cloud([70, -screen_height], mg_size, self.mg),
                           Cloud([20, -(screen_height*1.5)], mg_size, self.mg),
                           Cloud([40, -(screen_height/2)], mg_size, self.mg),
                           Cloud([90, 0], mg_size, self.mg)
                          ]

    def display_stage(self, display):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        
        # Background scrolling
        # Background need to be drawn twice since as it scrolls the image needs to be
        # drawn over the top part of the background and the second over the bottom part 
        if SCROLLING is True: 
            self.background_y_offset += self.BACKGROUND_SPEED
            if self.background_y_offset >= screen_height:
                # must subtract in case scroll amount is not evenly divisible into image height or will jump
                self.background_y_offset -= screen_height
        
        #draw the panes that make up the background
        display.blit(self.background_image, (0, self.background_y_offset - screen_height))
        display.blit(self.background_image, (0, self.background_y_offset))
        

        #midground scrolling + randomization
        for cloud in self.cloud_list:
            if SCROLLING is True:
                cloud.rect.top += self.MID_SPEED
            if cloud.rect.top <= screen_height and cloud.rect.bottom >= 0:
                #if cloud is on screen, move shadow downwards slightly
                if SCROLLING is True:
                    cloud.shadow_offset_y -= (self.MID_SPEED * 0.01)
            if cloud.rect.top >= screen_height:
                cloud.rect.top = -screen_height
                cloud.shadow_offset_y = 15
                mg_width, mg_height = self.mg.get_size()
                #randomized scale of object, between 1/4 and full width of screen

                cloud.rect.width = random.randint(int(mg_width/2), int(screen_width*1/2))
                cloud.rect.height = int((cloud.rect.width/mg_width) * mg_height)
                
                #randomizes x coord, between 0 and the width of screen - width of object
                cloud.rect.left = random.randint(int(-cloud.rect.width/4), int(screen_width - cloud.rect.width*3/4))
                cloud.image = pygame.transform.scale(self.mg, cloud.rect.size)
            else:
                #blit shadow, cloud.
                display.blit(library.make_shadow(cloud.image, CLOUD_OPACITY), (cloud.rect.left+cloud.shadow_offset_x,cloud.rect.top+cloud.shadow_offset_y))
                display.blit(cloud.image, cloud.rect.topleft)
                


