import os
import json
import datetime
import random
import pygame, bullet, game, constants, flightpaths, library, cache, powerup, gui

ENEMY_ASSETS_DIR = os.path.join('assets', 'enemy')


def launch_enemy_formation(country, plane_type, path_side=None):
    plane_info = Enemy.info_cache.fetch((country, plane_type))
    formation_groups = plane_info['formation_groups']
    formation_grp = formation_groups[random.randrange(len(formation_groups))]
    grp_offset = formation_grp['offsets']
    grp_spawn_area = formation_grp['spawn_area']

    if path_side == None:
        path_side = random.randint(0, 1)

    path_choice = random.randrange(len(plane_info['path_sets']))
    
    screen_width, screen_height = pygame.display.get_surface().get_size()
    if grp_spawn_area['width']:
        formation_grp_offset_x = (grp_spawn_area['left']*screen_width + 
                                  random.randrange(grp_spawn_area['width']*screen_width))
    else:
        formation_grp_offset_x = grp_spawn_area['left']*screen_width

    if grp_spawn_area['height']:
        formation_grp_offset_y = (grp_spawn_area['top']*screen_width + 
                                  random.randrange(grp_spawn_area['height']*screen_width))
    else:
        formation_grp_offset_y = grp_spawn_area['top']*screen_width

    
    formation = []
    for formation_offset in grp_offset:

        plane_offset = [formation_offset['x'] + formation_grp_offset_x,
                        formation_offset['y'] + formation_grp_offset_y]
        if path_side:
            plane_offset[0] = -plane_offset[0]
        enemyInstance = Enemy(country, plane_type, plane_offset=plane_offset, 
                              ms_time_delay=formation_offset['t'], path_choice=path_choice, 
                              path_side=path_side)
        formation.append(enemyInstance)
    return formation


def load_plane_info(country, plane_type):
    asset_path = os.path.join(ENEMY_ASSETS_DIR, country, plane_type)
    plane_info_path = os.path.join(asset_path, 'plane_info.json')
    with open(plane_info_path, "r") as infile:
        plane_info = json.load(infile)

    #Add items to cache to do one time loads and transformations. 
    plane_info['bullet_image'] = library.load_image_scale_convert_flip(plane_info['bullet_image'],
                                                                scaled_factor=plane_info['bullet_scale_factor'], 
                                                                use_alpha=True)
    plane_info['path_sets'] = flightpaths.make_flight_paths(plane_info, asset_path)

    return plane_info


class Enemy(pygame.sprite.Sprite):

    # FIX mod this later to cache all enemy country types 
    #update for german support.
    
    info_cache =  cache.Cache(load_plane_info)
    bulletSpriteList = pygame.sprite.Group()
        
        
    #XXX time_offset, but leave for later
    def __init__(self, country, plane_type, plane_offset=(0,0), ms_time_delay=0, path_choice=0, path_side=0):
        super().__init__()
        
        plane_info = self.info_cache.fetch((country, plane_type))
        
        self.frame_delay = plane_info['frame_delay'] * constants.FRAME_RATE_MULTIPLIER
        self.speed = plane_info['speed'] / constants.FRAME_RATE_MULTIPLIER
        self.health = plane_info['health']
        self.bullet_damage = plane_info['bullet_damage']
        self.bullet_speed = plane_info['bullet_speed']
        self.firing_position = plane_info['firing_position']
        self.bullet_image = plane_info['bullet_image']
        self.path_sets = plane_info['path_sets']
        self.point_count = plane_info['point_count']

            
        self.path = self.path_sets[path_choice][path_side]
        self.path_segment_index = 0
        self.path_segment_offset = 0
        #This is an x, y offset for this plane from the main path
        self.plane_offset = plane_offset
        self.start_time = datetime.datetime.now() + datetime.timedelta(milliseconds=ms_time_delay)
        
        self.frame_count = 0
        self.frame_index = 0

        
        self.frames = self.path[self.path_segment_index].frame_set

        self.image = self.frames[self.frame_index]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = self.plane_position()

 


    def cycle_animation(self):
        self.frame_count += 1
        if self.frame_count >= self.frame_delay:
            self.frame_count = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames) 


    def plane_position(self):
        path_segment = self.path[self.path_segment_index]
        x = path_segment.start_point[0] \
            + (self.path_segment_offset/path_segment.length*path_segment.w) \
            + self.plane_offset[0]
        y = path_segment.start_point[1] \
            + (self.path_segment_offset/path_segment.length*path_segment.h) \
            + self.plane_offset[1]

        return (x, y)
    

    def update(self):
        if self.health <= 0:
            pygame.mixer.Sound('assets/sound/enemydown.wav').play()
            if random.randint(0,constants.POWERUP_RARITY) == 1 and len(powerup.powerups) > 0:
                self.bulletSpriteList.add(powerup.spawn_powerup(self.rect.centerx,self.rect.centery))
            gui.points += self.point_count
            #game.gameInstance.score = gui.update_score_bar(game.gameInstance.points)
            gui.update_score_bar()
            point = gui.Point(self.rect.centerx,self.rect.centery, self.point_count)
            self.bulletSpriteList.add(point)
            self.kill()
            return

        if datetime.datetime.now() < self.start_time:
            return
        if not self.move_plane():
            return

        self.cycle_animation()
        self.frames = self.path[self.path_segment_index].frame_set
        self.masks = self.path[self.path_segment_index].mask_set
        self.image = self.frames[self.frame_index]
        self.mask = self.masks[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = self.plane_position()
        

    def move_plane(self):
        path_segment = self.path[self.path_segment_index]

        self.path_segment_offset += self.speed
        
        while self.path_segment_offset >= path_segment.length:
            self.path_segment_offset -= path_segment.length
            if path_segment.bullet_angle != None:
                for position in self.firing_position:
                    self.bulletSpriteList.add(bullet.Bullet((self.rect.centerx + position,self.rect.centery),type(self), path_segment.bullet_angle, self.bullet_image, self.bullet_damage, self.bullet_speed))

            self.path_segment_index += 1
            if self.path_segment_index >= len(self.path):
                if not path_segment.endless:
                    self.kill()
                    return False
                else:
                    self.path_segment_index += path_segment.endless + 1

            path_segment = self.path[self.path_segment_index]

        return True

