import pygame, constants, game
from library import load_image_scale_convert_flip
titleScreen = pygame.image.load('assets/game/gui/startscreen.png')
expoDump = pygame.image.load('assets/game/gui/expositiondump.png')
youWin = pygame.image.load('assets/game/gui/youwin.png')
pressEnter = pygame.image.load('assets/game/gui/pressenter.png')

full_health_bar = None
three_quarter_health_bar = None
half_health_bar = None
quarter_health_bar = None
score_font = None
healthbars = list()

score_img = None
points = 0
#score = '000000'
class Point(pygame.sprite.Sprite):
    def __init__(self,x,y,points):
        super().__init__()
        self.img_path = 'assets/game/points/' + str(points) + 'points.png'
        self.image = load_image_scale_convert_flip(self.img_path,scaled_factor=4,use_alpha=True)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.count = 0
    def update(self):
        self.count += 1
        if self.count >= 50:
            self.kill()

class PlayerExplosion(pygame.sprite.Sprite):
    def __init__(self,x,y, screen):
        super().__init__()
        self.img_path = 'assets/player/explosion/explosion'
        self.screen = screen
        self.flag = ''
        self.frameIndex = 0
        self.count = 0
        self.image = pygame.image.load('assets/player/explosion/explosion0.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
    def update(self):
        #self.rect = self.image.get_rect()
        if self.frameIndex == 5:
            self.flag = 'done'
            return
        self.image = load_image_scale_convert_flip(str(self.img_path + str(self.frameIndex) + '.png'),scaled_factor=4,use_alpha=True)
        #self.screen.blit(self.image,(self.x,self.y))
        self.count += 1
        if self.count % 10 == 0:
            self.frameIndex += 1

class BlinkingEnter(object):
    def __init__(self,x,y, screen):
        self.x = x
        self.y = y
        self.screen = screen
        self.flag = 0
    def update(self):
        if self.flag >= 600:
            pygame.draw.rect(self.screen,constants.GRAPHITE,(self.x,self.y,376,28))
            self.flag = -600
        elif self.flag == 0:
            self.screen.blit(pressEnter,(self.x,self.y))
        self.flag += 1


def init_gui():
    global full_health_bar,three_quarter_health_bar,half_health_bar,quarter_health_bar, score_font
    full_health_bar = load_image_scale_convert_flip('assets/game/gui/healthbarfull.png',scaled_factor=4,use_alpha=True)
    three_quarter_health_bar = load_image_scale_convert_flip('assets/game/gui/healthbarthreequarters.png',scaled_factor=4,use_alpha=True)
    half_health_bar = load_image_scale_convert_flip('assets/game/gui/healthbarhalf.png',scaled_factor=4,use_alpha=True)
    quarter_health_bar = load_image_scale_convert_flip('assets/game/gui/healthbaronequarter.png',scaled_factor=4,use_alpha=True)
    score_font = pygame.font.Font('assets/game/font/textfont.ttf', 36)

def update_health_bar(health):
    healthbars.clear()
    if health > 0:
        fCount = int(health // 10)
        for i in range(fCount):
            healthbars.append(full_health_bar)
            health -= 10
        if (health // 7.5) > 0:
            healthbars.append(three_quarter_health_bar)
        elif (health // 5) > 0:
            healthbars.append(half_health_bar)
        elif (health // 2.5) > 0:
            healthbars.append(quarter_health_bar)

class Scene(object):
    #objects is a list
    def __init__(self, bg, screen, sound, objects):
        self.objects = objects
        self.sound = sound
        self.flag = ''
        screen.blit(bg, (0,0))
    def update(self):
        for obj in self.objects:
            obj.update()
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    self.sound.play()
                    self.flag = 'done'
                if event.key==pygame.K_ESCAPE:
                    pygame.quit()
                    return

def update_score_bar():
    global score_img, score_font
    def_score = ['0','0','0','0','0','0']
    g = len(def_score)
    split_score = [str(d) for d in str(points)]
    def_score[g - len(split_score) : g] = split_score
    e= "".join(def_score)
    score_img = score_font.render(e, True, constants.WHITE)