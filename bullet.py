import pygame, player, game, stage, constants, powerup, math

from library import load_image_scale_convert_flip


class Bullet(pygame.sprite.Sprite):
    
    HIT_SOUND = None
    
    def __init__(self, firing_position, owner_class, bearing_angle, image, bullet_damage, bullet_speed):
        # Call the parent class (Sprite) constructor 
        
        super().__init__()
        #SCREEN_HEIGHT = 
        #SCREEN_WIDTH = 
        self.bullet_damage = bullet_damage
        self.bullet_speed = bullet_speed / constants.FRAME_RATE_MULTIPLIER
        self.bearing_angle = bearing_angle
        self.image = image
        self.image = pygame.transform.rotate(self.image,-bearing_angle)
        self.rect = self.image.get_rect()
        self.rect.midbottom = firing_position
        self.mask = pygame.mask.from_surface(self.image)
        self.reference_rect = list(self.rect.center)
        self.owner_class = owner_class

        if not self.HIT_SOUND:
            self.load_hit_sound()
        
    
    #this function takes in two args: self(duh) and a sprite group.
    def checkCollision(self, objGroup):
        for obj in objGroup:
            #if bullet is colliding with player or powerup, ignore
            if type(obj) == self.owner_class or type(obj) == powerup.PowerupClass:
                continue
            #if (singular) sprite and bullet are colliding, subtract that sprite's health by the bullet's damage
            if pygame.sprite.collide_mask(self, obj):
                obj.health -= self.bullet_damage
                #destroy the bullet
                self.HIT_SOUND.play()
                self.kill()
                


    def update(self):
        #note: bearing angle is in deg.
        self.std_angle = 90 - self.bearing_angle
        if self.std_angle < 0:
            self.std_angle += 360
        if self.std_angle > 360:
            self.std_angle -= 360 
        self.xspeed = math.cos(math.radians(self.std_angle)) * self.bullet_speed
        self.yspeed = math.sin(math.radians(self.std_angle)) * self.bullet_speed
        #reference rect is created to imitate float-like accuracy for position
        self.reference_rect[0] += self.xspeed
        self.reference_rect[1] -= self.yspeed
        self.rect.centerx = int(self.reference_rect[0])
        self.rect.centery = int(self.reference_rect[1])
        
        #if offscreen, die
        if self.rect.bottom <= 0 or self.rect.top >= pygame.display.get_surface().get_height() or \
         self.rect.right <= 0 or self.rect.left >= pygame.display.get_surface().get_width():
            self.kill()



    @classmethod
    def load_hit_sound(cls):
        cls.HIT_SOUND = pygame.mixer.Sound('assets/sound/enemyhit.wav')