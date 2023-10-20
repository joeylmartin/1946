#!/usr/bin/env python

import pygame, player, stage, constants, enemy, powerup, gui, traceback
import library
import collections

MSEC_PER_FRAME = 1000 / constants.FRAME_RATE
MIN_MSEC_PER_FRAME = 1

excess_msec = None
#gameInstance = None
last_tick = None
score_font = None

#elements

waterBackground = pygame.image.load('assets/game/stage/waterbackground.png')
desertBackground = pygame.image.load('assets/game/stage/desertbackground.png')
grassBackground = pygame.image.load('assets/game/stage/grassbackground.png')


def main():
    global screen, clock, excess_msec, gameplay_loop, score_font
    #init the sound mixer BEFORE the pygame.init() to get rid of sound lag.
    pygame.mixer.pre_init(44100, -16, 2)
    pygame.init()
    try:
        #Background size (810, 1080)
        size = waterBackground.get_size()
        screen = pygame.display.set_mode(size)
        excess_msec = 0
        pygame.display.set_caption("1946")
        pygame.display.set_icon(pygame.image.load('assets/game/gui/logo.png').convert())
        pygame.mouse.set_visible(False)
        done = False
        clock = pygame.time.Clock()
        stages = [
            #stage bg : number of ticks for end
            stage.Stage(waterBackground.convert()),
            stage.Stage(grassBackground.convert()),
            stage.Stage(waterBackground.convert()),
            stage.Stage(desertBackground.convert()),
            stage.Stage(desertBackground.convert()),
            stage.Stage(grassBackground.convert()),
        ]
        #gui stuff
        
        title_screen = gui.Scene(gui.titleScreen,screen,pygame.mixer.Sound('assets/sound/startgame.wav'),
        [gui.BlinkingEnter(203,700,screen)])
        while title_screen.flag == '':
            title_screen.update()
            pygame.display.flip()
        expo_dump = gui.Scene(gui.expoDump,screen,pygame.mixer.Sound('assets/sound/missionstart.wav'),
        [gui.BlinkingEnter(203,1000,screen)])
        while expo_dump.flag == '':
            expo_dump.update()
            pygame.display.flip()
        

        def gameplay_loop():
            global gameInstance, last_tick
            gameInstance = GameClass()
            gui.points = 0
            gui.score = '000000'
            gui.update_score_bar()
            levelIndex = 0
            last_tick = pygame.time.get_ticks()
            for level in stages:
                #init stage
                gameInstance.stage = level
                gameInstance.init_level(levelIndex)
                #stage overview
                mission_start_img_path = 'assets/game/mission/mission' + str((levelIndex + 1)) + 'startup.png'
                mission_start = gui.Scene(pygame.image.load(mission_start_img_path),screen,pygame.mixer.Sound('assets/sound/missionstart.wav'),[gui.BlinkingEnter(203, 700, screen)])
                pygame.mixer.music.pause()
                while mission_start.flag == '':
                    mission_start.update()
                    pygame.display.flip()
                pygame.mixer.music.unpause()
                #start gameplay
                pygame.mixer.music.load('assets/sound/planeflyingforward.wav')
                pygame.mixer.music.play(-1)
                gameInstance.level_start_time = pygame.time.get_ticks()
                while True:
                    last_tick = pygame.time.get_ticks()
                    gameInstance.spawn_check()
                    done = gameInstance.process_events()
                    if len(gameInstance.enemy_queue) <= 0:
                        if len(gameInstance.all_sprites_list.sprites()) <= 1:
                            break
                    pass_ticks_draw_display()
                levelIndex += 1
                gameInstance.all_sprites_list.empty()
                gameInstance.all_sprites_list.add(gameInstance.playerInstance)
            pygame.mixer.music.stop()
            you_win = gui.Scene(gui.youWin,screen,pygame.mixer.Sound('assets/sound/missionstart.wav'),[gui.BlinkingEnter(203, 1000, screen)])
            while you_win.flag == '':
                you_win.update()
                screen.blit(gui.score_img,(302,700))
                pygame.display.flip()
            return gameplay_loop()
        gameplay_loop()

    except Exception as ex:
        print(traceback.format_exc())
        raise
    finally:
        # Close window and exit
        pygame.quit()


class GameClass(object):
    
    enemies_list = [
                    [
                     {'country': 'japan', 'plane_type': 'small', 'time_delay': 0, 'path_side': None},
                     {'country': 'japan', 'plane_type': 'small', 'time_delay': 10000, 'path_side': None},
                     {'country': 'japan', 'plane_type': 'medium', 'time_delay': 20000, 'path_side': 1},
                     {'country': 'japan', 'plane_type': 'small', 'time_delay': 20000, 'path_side': 0},
                     {'country': 'japan', 'plane_type': 'small', 'time_delay': 30000, 'path_side': 0},
                     {'country': 'japan', 'plane_type': 'small', 'time_delay': 30000, 'path_side': 1},
                     {'country': 'japan', 'plane_type': 'medium', 'time_delay': 35000, 'path_side': 0},
                     {'country': 'japan', 'plane_type': 'small', 'time_delay': 40000, 'path_side': 0},
                     {'country': 'japan', 'plane_type': 'medium', 'time_delay': 45000, 'path_side': 0},
                     {'country': 'japan', 'plane_type': 'medium', 'time_delay': 45000, 'path_side': 1}
                    ], 
                    [
                     {'country': 'germany', 'plane_type': 'small', 'time_delay': 0, 'path_side': None},
                     {'country': 'germany', 'plane_type': 'small', 'time_delay': 10000, 'path_side': None},
                     {'country': 'germany', 'plane_type': 'medium', 'time_delay': 20000, 'path_side': 1},
                     {'country': 'germany', 'plane_type': 'small', 'time_delay': 20000, 'path_side': 0},
                     {'country': 'germany', 'plane_type': 'small', 'time_delay': 30000, 'path_side': 0},
                     {'country': 'germany', 'plane_type': 'small', 'time_delay': 30000, 'path_side': 1},
                     {'country': 'germany', 'plane_type': 'medium', 'time_delay': 35000, 'path_side': 0},
                     {'country': 'germany', 'plane_type': 'small', 'time_delay': 40000, 'path_side': 0},
                     {'country': 'germany', 'plane_type': 'medium', 'time_delay': 45000, 'path_side': 0},
                     {'country': 'germany', 'plane_type': 'medium', 'time_delay': 45000, 'path_side': 1}
                    ],
                    [
                     {'country': 'japan', 'plane_type': 'big', 'time_delay': 0, 'path_side': 0}
                    ],
                    [
                     {'country': 'japan', 'plane_type': 'small', 'time_delay': 0, 'path_side': 0},
                     {'country': 'germany', 'plane_type': 'small', 'time_delay': 0, 'path_side': 1},
                     {'country': 'japan', 'plane_type': 'medium', 'time_delay': 10000, 'path_side': None},
                     {'country': 'japan', 'plane_type': 'medium', 'time_delay': 10000, 'path_side': None},
                     {'country': 'germany', 'plane_type': 'medium', 'time_delay': 15000, 'path_side': None},
                     {'country': 'japan', 'plane_type': 'small', 'time_delay': 20000, 'path_side': None},
                     {'country': 'germany', 'plane_type': 'small', 'time_delay': 30000, 'path_side': None},
                     {'country': 'germany', 'plane_type': 'medium', 'time_delay': 40000, 'path_side': None},
                     {'country': 'germany', 'plane_type': 'medium', 'time_delay': 40000, 'path_side': None},
                     {'country': 'germany', 'plane_type': 'medium', 'time_delay': 40000, 'path_side': None},
                     {'country': 'germany', 'plane_type': 'medium', 'time_delay': 50000, 'path_side': None},
                    ],
                    [
                     {'country': 'japan', 'plane_type': 'small', 'time_delay': 0, 'path_side': 0},
                     {'country': 'germany', 'plane_type': 'small', 'time_delay': 0, 'path_side': 1},
                     {'country': 'japan', 'plane_type': 'medium', 'time_delay': 10000, 'path_side': None},
                     {'country': 'japan', 'plane_type': 'medium', 'time_delay': 10000, 'path_side': None},
                     {'country': 'germany', 'plane_type': 'medium', 'time_delay': 15000, 'path_side': None},
                     {'country': 'japan', 'plane_type': 'small', 'time_delay': 20000, 'path_side': None},
                     {'country': 'japan', 'plane_type': 'medium', 'time_delay': 25000, 'path_side': None},
                     {'country': 'germany', 'plane_type': 'small', 'time_delay': 30000, 'path_side': None},
                     {'country': 'germany', 'plane_type': 'medium', 'time_delay': 35000, 'path_side': None},
                     {'country': 'japan', 'plane_type': 'medium', 'time_delay': 40000, 'path_side': None},
                     {'country': 'germany', 'plane_type': 'medium', 'time_delay': 40000, 'path_side': None},
                     {'country': 'germany', 'plane_type': 'medium', 'time_delay': 50000, 'path_side': None}
                    ],
                    [
                     {'country': 'japan', 'plane_type': 'big', 'time_delay': 0, 'path_side': 0}
                    ]
                   ]
    #This class serves as an instance for the game. All we have to do is make a new instance
    #of this class to reset it  
    def __init__(self):
        #constructor
        super().__init__()
        font = pygame.font.Font(None, 30)
        self.all_sprites_list = pygame.sprite.Group()
        self.playerInstance = player.PlayerClass()
        self.all_sprites_list.add(self.playerInstance)
        powerup.powerups = powerup.def_powerups
        gui.init_gui()
        gui.update_health_bar(self.playerInstance.health)
        gui.update_score_bar()
        stage.SCROLLING = True

        self.level_start_time = None
        self.enemy_queue = None
        self.stage = None
        
    def process_events(self):
        #this method serves to handle the pygame-specific events, and global events, like collision detection.

        if self.playerInstance.health <= 0:
            #player death
            pygame.mixer.music.stop()
            pygame.mixer.Sound('assets/sound/playerdown.wav').play()
            stage.SCROLLING = False
            playerExplosion = gui.PlayerExplosion(0,0, screen)
            playerExplosion.rect.center = self.playerInstance.rect.center
            #self.playerInstance.kill()
            self.all_sprites_list.empty()
            self.all_sprites_list.add(playerExplosion)
            while playerExplosion.flag == '':
                playerExplosion.update()
                pass_ticks_draw_display()
            if int(repr(last_tick)[-1]) == 3:
                #easter egg ;)
                gameover_img = pygame.image.load('assets/game/gui/gameoverspecial.png')
            else:
                gameover_img = pygame.image.load('assets/game/gui/gameover.png')
            game_over = gui.Scene(gameover_img,screen,pygame.mixer.Sound('assets/sound/missionstart.wav'),[gui.BlinkingEnter(203,1000,screen)])
            while game_over.flag == '':
                game_over.update()
                pygame.display.flip()
            return gameplay_loop()

        for bullet in self.playerInstance.bulletSpriteList:
            bullet.checkCollision(self.all_sprites_list)
        self.playerInstance.check_collision(self.all_sprites_list)
        self.playerInstance.check_collision(enemy.Enemy.bulletSpriteList)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True
        return False

    def draw_gui(self, display, hBar):
        i = 0
        for health in hBar:
            display.blit(health, ((46 * i) +48, 1000))
            i += 1
        display.blit(gui.score_img,(302,20))

    def build_shadows(self, display):
        for obj in self.all_sprites_list:
            shadow_obj = library.make_shadow(obj.image, constants.OBJECT_OPACITY)
            display.blit(shadow_obj, (obj.rect.left+constants.SHADOW_OFFSET_X, obj.rect.top+constants.SHADOW_OFFSET_Y))

    def display_frame(self, screen):
        self.all_sprites_list.update()
        enemy.Enemy.bulletSpriteList.update()
        self.stage.display_stage(screen)
        self.build_shadows(screen)
        self.all_sprites_list.draw(screen)
        enemy.Enemy.bulletSpriteList.draw(screen)
        self.playerInstance.bulletSpriteList.draw(screen)
        self.draw_gui(screen,gui.healthbars)
        pygame.display.flip()

    def spawn_check(self):
        if not self.enemy_queue:
            return
        if self.enemy_queue[0]['time_delay'] >= (pygame.time.get_ticks() - self.level_start_time):
            return
        formation_spec = self.enemy_queue.popleft()
        enemy_formation = enemy.launch_enemy_formation(formation_spec['country'], formation_spec['plane_type'],
                                                       path_side=formation_spec['path_side'])    
        self.all_sprites_list.add(enemy_formation)

    def spawn_queue_empty(self):
        return not self.enemy_queue


    def init_level(self, level):
        self.playerInstance.health = self.playerInstance.max_health
        gui.update_health_bar(self.playerInstance.health)
        self.playerInstance.rect.center = (405, 810)
        self.level = level
        self.enemy_queue = collections.deque(self.enemies_list[level])

        


def pass_ticks_draw_display():
    global excess_msec
    gameInstance.display_frame(screen)
    # Was the calculation for this frame too long? 
    # Keep track of excess msecs and gradually use them up over the next frames until back to nor
    ticks_passed = pygame.time.get_ticks() - last_tick
    if ticks_passed > MSEC_PER_FRAME:
        excess_msec += ticks_passed - MSEC_PER_FRAME

    adjusted_msec_per_frame = MSEC_PER_FRAME - excess_msec
    # Can't go under minimum amount so save it till next round
    if adjusted_msec_per_frame < MIN_MSEC_PER_FRAME:
        adjusted_msec_per_frame = MIN_MSEC_PER_FRAME
        excess_msec -= MSEC_PER_FRAME - MIN_MSEC_PER_FRAME
    else:
        excess_msec = 0

    clock.tick(1000/adjusted_msec_per_frame)


if __name__ == "__main__":
    main()