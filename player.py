import pygame, game, bullet, copy, constants, powerup, gui, enemy
from library import load_image_scale_convert_flip

#import __main__

class PlayerClass(pygame.sprite.Sprite):

    BULLET_SIZE = (48, 60)


    NORMAL_SPEED = 8 / constants.FRAME_RATE_MULTIPLIER
    FAST_SPEED = 10 / constants.FRAME_RATE_MULTIPLIER

    NORMAL_FRAME_DELAY = 4 * constants.FRAME_RATE_MULTIPLIER
    BACKUP_FRAME_DELAY = 10 * constants.FRAME_RATE_MULTIPLIER
    LOOP_FRAME_DELAY = 6 * constants.FRAME_RATE_MULTIPLIER

    TURNING_RADIUS = 8 / constants.FRAME_RATE_MULTIPLIER

    #rate of fire

    DEEP_TURN_COUNT = 20 * constants.FRAME_RATE_MULTIPLIER

    VERTICLE_GUN_OFFSET = 20

    FIRING_SOUND = None
    POWERUP_SOUND = None
    PLAYER_HIT_SOUND = None
    PLAYER_LOOP_SOUND = None

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        #animation sets 
        self.FORWARD = [load_image_scale_convert_flip('assets/player/forward/planeforward.png', scaled_factor=4, use_alpha=True),
                        load_image_scale_convert_flip('assets/player/forward/planeforward2.png', scaled_factor=4, use_alpha=True)]

        self.LEFT_DEEP_TURN = [load_image_scale_convert_flip('assets/player/deepturn/planedeepturn.png', scaled_factor=4, use_alpha=True),
                               load_image_scale_convert_flip('assets/player/deepturn/planedeepturn2.png', scaled_factor=4, use_alpha=True)]
        self.LEFT_MILD_TURN = [load_image_scale_convert_flip('assets/player/mildturn/planemildturn.png', scaled_factor=4, use_alpha=True),
                               load_image_scale_convert_flip('assets/player/mildturn/planemildturn2.png', scaled_factor=4, use_alpha=True)]
        self.LEFT = [self.LEFT_MILD_TURN,self.LEFT_DEEP_TURN]

        self.RIGHT_DEEP_TURN = [load_image_scale_convert_flip('assets/player/deepturn/planedeepturn.png', scaled_factor=4, flip=True, use_alpha=True),
                                load_image_scale_convert_flip('assets/player/deepturn/planedeepturn2.png', scaled_factor=4, flip=True, use_alpha=True)]
        self.RIGHT_MILD_TURN = [load_image_scale_convert_flip('assets/player/mildturn/planemildturn.png', scaled_factor=4, flip=True, use_alpha=True), 
                                load_image_scale_convert_flip('assets/player/mildturn/planemildturn2.png', scaled_factor=4, flip=True, use_alpha=True)]
        self.RIGHT = [self.RIGHT_MILD_TURN, self.RIGHT_DEEP_TURN]

        self.TURN = [self.RIGHT_DEEP_TURN, self.LEFT_DEEP_TURN,self.RIGHT_MILD_TURN,self.LEFT_MILD_TURN]

        # This one does not have images for the rotating propeller. Need to flip the images horizontally to get those.
        self.LOOP = [load_image_scale_convert_flip('assets/player/loop/planeloop0.png', scaled_factor=4, use_alpha=True), 
                     load_image_scale_convert_flip('assets/player/loop/planeloop0.png', scaled_factor=4, use_alpha=True, flip=True),
                     load_image_scale_convert_flip('assets/player/loop/planeloop1.png', scaled_factor=4, use_alpha=True), 
                     load_image_scale_convert_flip('assets/player/loop/planeloop1.png', scaled_factor=4, use_alpha=True, flip=True),
                     load_image_scale_convert_flip('assets/player/loop/planeloop2.png', scaled_factor=4, use_alpha=True), 
                     load_image_scale_convert_flip('assets/player/loop/planeloop2.png', scaled_factor=4, use_alpha=True, flip=True),
                     load_image_scale_convert_flip('assets/player/loop/planeloop3.png', scaled_factor=4, use_alpha=True), 
                     load_image_scale_convert_flip('assets/player/loop/planeloop3.png', scaled_factor=4, use_alpha=True, flip=True),
                     load_image_scale_convert_flip('assets/player/loop/planeloop4.png', scaled_factor=4, use_alpha=True), 
                     load_image_scale_convert_flip('assets/player/loop/planeloop4.png', scaled_factor=4, use_alpha=True, flip=True),
                     load_image_scale_convert_flip('assets/player/loop/planeloop5.png', scaled_factor=4, use_alpha=True), 
                     load_image_scale_convert_flip('assets/player/loop/planeloop5.png', scaled_factor=4, use_alpha=True, flip=True),
                    ]
        self.LOOP_MOVEMENTS = [-self.TURNING_RADIUS,-self.TURNING_RADIUS,0,0,0,self.TURNING_RADIUS,self.TURNING_RADIUS,self.TURNING_RADIUS,0,0,-self.TURNING_RADIUS,-self.TURNING_RADIUS]
        self.image = self.FORWARD[0]
        self.mask = pygame.mask.from_surface(self.image)
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width/2, (screen_height/4 * 3))
        
        self.finishedCycle = False
        self.frameCount = 0
        self.planeFrameIndex = 0
        self.turnCounter = 0
        self.bulletTimeCounter = 0
        self.bulletSpriteList = pygame.sprite.Group()
        self.frames = self.FORWARD
        self.speed = self.NORMAL_SPEED
        self.frame_delay = self.NORMAL_FRAME_DELAY
        self.orientation = ''
        self.bullet_image_modifier = ''
        self.max_health = 30
        self.health = self.max_health
        self.iFrameCount = 30
        #default bullet stats
        self.bullet_damage = 4 #increments: 4, 6, 8, 10, 12
        self.bullet_speed = 12 #increments: 12, 16, 20, 24, 28
        self.bullet_delay = 15   #increments: 15, 13, 11, 9, 7
        self.bullet_count = 1 #increments: 1, 2, 3
        self.bullet_image = load_image_scale_convert_flip('assets/player/bullet/bullet.png', scaled_size=self.BULLET_SIZE, use_alpha=True)

        #load audio sound effects
        if not self.FIRING_SOUND:
            self.load_firing_sound()
        if not self.POWERUP_SOUND:
            self.load_powerup_sound()
        if not self.PLAYER_HIT_SOUND:
            self.load_player_hit_sound()
        if not self.PLAYER_LOOP_SOUND:
            self.load_player_loop_sound()
            
        pygame.mixer.music.load('assets/sound/planeflyingforward.wav')
        pygame.mixer.music.play(-1)
        #for future; stop playing sound when player dies.
       # pygame.mixer.music.load('assets/sound/planeflyingforward.wav')
       # pygame.mixer.music.play(-1)

    def update(self):
        if self.bulletTimeCounter < (self.bullet_delay * constants.FRAME_RATE_MULTIPLIER):
            self.bulletTimeCounter += 1
        if self.iFrameCount < 30:
            self.iFrameCount += 1
        self.bulletSpriteList.update()
        self.cycle_animation()
        self.playerAction()

    def cycle_animation(self):
        self.frameCount += 1

        if self.frameCount >= self.frame_delay:
            self.frameCount = 0
            if self.planeFrameIndex < (len(self.frames)-1):
                self.planeFrameIndex += 1
                self.finishedCycle = False
            else:
                self.finishedCycle = True
                self.planeFrameIndex = 0


            self.image = self.frames[self.planeFrameIndex]
            self.mask = pygame.mask.from_surface(self.image)
    def check_collision(self, objGroup):
        for obj in objGroup:
            if pygame.sprite.collide_mask(self, obj) and self.frames != self.LOOP:
                if type(obj) == powerup.PowerupClass:
                    #powerups
                    if obj.powerup_type == 'health':
                        self.max_health += 10
                        self.health = self.max_health
                        gui.update_health_bar(self.health)
                    if obj.powerup_type == 'bulletspeed':
                        if self.bullet_speed < 28:
                            self.bullet_speed += 4

                    elif obj.powerup_type == 'bulletdelay':
                        if self.bullet_delay > 7:
                            self.bullet_delay -= 2

                    elif obj.powerup_type == 'bulletdamage':
                        if self.bullet_damage < 12:
                            self.bullet_damage += 2
                            #updates image for bullet
                            self.bullet_image_modifier = str(int((self.bullet_damage/2))-1)
                            self.bullet_image = load_image_scale_convert_flip(str('assets/player/bullet/bullet' + self.bullet_image_modifier + '.png'),
                             scaled_size=self.BULLET_SIZE, use_alpha=True)

                    elif obj.powerup_type == 'bulletcount':
                        if self.bullet_count < 3:
                            self.bullet_count += 1

                    self.POWERUP_SOUND.play()
                    obj.kill()
                elif type(obj) == bullet.Bullet and \
                    obj.owner_class != type(self):
                    #enemy bullet
                    self.health -= obj.bullet_damage
                    if gui.points > int(obj.bullet_damage):
                        gui.points -= int(obj.bullet_damage)
                    gui.update_score_bar()
                    self.PLAYER_HIT_SOUND.play()
                    gui.update_health_bar(self.health)
                    obj.kill()
                elif type(obj) == enemy.Enemy and self.iFrameCount >= 30:
                        self.health -= 2.5
                        self.PLAYER_HIT_SOUND.play()
                        gui.update_health_bar(self.health)
                        self.iFrameCount = 0

                    
    def loadNormalState(self):
        self.frames = self.FORWARD
        self.frame_delay = self.NORMAL_FRAME_DELAY
        self.speed = self.NORMAL_SPEED
        self.orientation = ''
    def playerAction(self):
        keys = pygame.key.get_pressed()
        self.xspeed = 0
        self.yspeed = 0
        #--- MOVEMENT ---
        
        screen_width, screen_height = pygame.display.get_surface().get_size()
        if self.frames == self.LOOP:
            if self.finishedCycle:
                #sound effect stopped, as it is *slightly* longer than the animation
                self.PLAYER_LOOP_SOUND.stop()
                self.load_player_loop_sound()
                self.loadNormalState()
            else:
                self.yspeed += self.LOOP_MOVEMENTS[self.planeFrameIndex]
        else:
            if keys[pygame.K_q] and self.rect.top > self.TURNING_RADIUS and \
                    self.rect.top < (screen_height - (self.rect.height + self.TURNING_RADIUS)):
                self.PLAYER_LOOP_SOUND.play()
                self.frames = self.LOOP
                self.frame_delay = self.LOOP_FRAME_DELAY
            else:
                if self.orientation == 'transition' and self.finishedCycle:
                    self.loadNormalState()
                else:
                    #-- HORIZONTAL MOVEMENT --
                    if keys[pygame.K_LEFT]:
                        self.orientation = 'left'
                        #is player not already turning left?
                        if self.frames not in self.LEFT:
                            self.frames = self.LEFT_MILD_TURN
                            self.turnCounter = 0
                        else:
                            self.turnCounter += 1
                            if self.turnCounter >= self.DEEP_TURN_COUNT:
                                self.frames = self.LEFT_DEEP_TURN
                                self.speed = self.FAST_SPEED

                        if self.rect.centerx <= 0:
                            self.rect.centerx = screen_width
                        self.xspeed -= self.speed

                    elif keys[pygame.K_RIGHT]:
                        self.orientation = 'right'
                        if self.frames not in self.RIGHT:
                            self.frames = self.RIGHT_MILD_TURN
                            self.turnCounter = 0
                        else:
                            self.turnCounter += 1
                            if self.turnCounter >= self.DEEP_TURN_COUNT:
                                self.frames = self.RIGHT_DEEP_TURN
                                self.speed = self.FAST_SPEED
                        if self.rect.centerx >= screen_width:
                            self.rect.centerx = 0
                        self.xspeed += self.speed

                    #is player resuming neutral state?
                    elif self.frames in self.TURN and self.orientation != 'transition':
                        self.frameCount = 0
                        self.orientation = 'transition'
                        if self.orientation == 'left':
                            self.frames = self.LEFT_MILD_TURN
                        else:
                            self.frames = self.RIGHT_MILD_TURN
                        
                    #-- VERTICAL MOVEMENT --
                    if keys[pygame.K_UP]:
                        if self.rect.top - self.speed >= 0:
                            self.yspeed -= self.speed 
                    elif keys[pygame.K_DOWN]:
                        if self.rect.bottom + self.speed <= screen_height:
                            self.yspeed += self.speed


                    #--- SHOOTING ---
                    if keys[pygame.K_SPACE]:
                        if self.bulletTimeCounter >= (self.bullet_delay * constants.FRAME_RATE_MULTIPLIER):

                            #note: bullet damage is equal to 4, 6, 8, 10, 12. If these values are changed, the following code will have to be changed.
                            #changes file for image depending on bullet damage.

                            self.FIRING_SOUND.play()
                            self.bulletTimeCounter = 0
                            self.firing_position_x = self.rect.centerx
                            self.firing_position_y = self.rect.top + self.VERTICLE_GUN_OFFSET
                            #adding multiple bullets
                            if self.bullet_count == 1 or self.bullet_count == 3:
                                self.bulletSpriteList.add(bullet.Bullet((self.firing_position_x,self.firing_position_y),type(self), 0, self.bullet_image, self.bullet_damage, self.bullet_speed))
                            if self.bullet_count == 3:
                                self.bulletSpriteList.add(bullet.Bullet((self.firing_position_x-72,self.firing_position_y),type(self),345, self.bullet_image,self.bullet_damage, self.bullet_speed))
                                self.bulletSpriteList.add(bullet.Bullet((self.firing_position_x+72,self.firing_position_y),type(self),15, self.bullet_image,self.bullet_damage, self.bullet_speed))
                            elif self.bullet_count == 2:
                                self.bulletSpriteList.add(bullet.Bullet((self.firing_position_x-36,self.firing_position_y),type(self),355, self.bullet_image,self.bullet_damage, self.bullet_speed))
                                self.bulletSpriteList.add(bullet.Bullet((self.firing_position_x+36,self.firing_position_y),type(self),5, self.bullet_image,self.bullet_damage, self.bullet_speed))

        self.rect.centerx += self.xspeed
        self.rect.centery += self.yspeed

    @classmethod
    def load_firing_sound(cls):
        cls.FIRING_SOUND = pygame.mixer.Sound('assets/sound/bulletshot.wav')
    @classmethod
    def load_powerup_sound(cls):
        cls.POWERUP_SOUND = pygame.mixer.Sound('assets/sound/powerupget.wav')
    @classmethod
    def load_player_hit_sound(cls):
        cls.PLAYER_HIT_SOUND = pygame.mixer.Sound('assets/sound/playerhit.wav')
    @classmethod
    def load_player_loop_sound(cls):
        cls.PLAYER_LOOP_SOUND = pygame.mixer.Sound('assets/sound/playerloop.wav')

