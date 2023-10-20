import pygame, random
from library import load_image_scale_convert_flip\

def_powerups = ['health','health','health','bulletcount','bulletcount',
'bulletdelay','bulletdelay','bulletdelay','bulletdelay',
'bulletspeed','bulletspeed','bulletspeed','bulletspeed',
'bulletdamage','bulletdamage','bulletdamage','bulletdamage']
powerups = list()
class PowerupClass(pygame.sprite.Sprite):

    def __init__(self, powerup_type):
        super().__init__()
        #power up types are: bulletcount, bulletdamage, bulletdelay, bulletspeed
        self.powerup_type = powerup_type
        self.imagePath = 'assets/powerup/' + self.powerup_type + '.png'
        self.image = load_image_scale_convert_flip(self.imagePath,scaled_factor=4,use_alpha=True)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
def spawn_powerup(x,y):
    if len(powerups) > 0:
        pup_type = random.choice(powerups)
        powerups.remove(pup_type)
        p_up = PowerupClass(pup_type)
        p_up.rect.centerx = x
        p_up.rect.centery = y
        return p_up