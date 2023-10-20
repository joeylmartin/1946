import os
import pygame, math, library

#def make_flight_paths(path_points_path, flightpath_filepaths, image_scale_factor):
def make_flight_paths(plane_info, asset_path):
    screen_width = pygame.display.get_surface().get_width()
    
    image_scale_factor = plane_info['scale_factor']

    
    frame_set = []
    for path in plane_info['images']:
        file_path = os.path.join(asset_path, path)
        frame_set.append(library.load_image_scale_convert_flip(file_path, scaled_factor=image_scale_factor, use_alpha=True))

    path_points_sets = plane_info['paths']

    path_sets = []
    for path_points in path_points_sets:
        if len(path_points[-1]) == 1:
            endless = path_points[-1][0]
        else:
            endless = None
        
        start_point = path_points[0]
        path_list = []
        mirror_path_list = []

        for point_set in path_points[1:]:
            point = point_set[:2]
            if len(point_set) == 3:
                path_segment = PathSegment(start_point, point, frame_set, bullet_angle=point_set[2], no_rotation=endless)

            elif len(point_set) == 2:
                path_segment = PathSegment(start_point, point, frame_set, no_rotation=endless)

            if len(point_set) == 1:
                point = path_points[point_set[0]]
                path_segment = PathSegment(start_point, point, frame_set, endless=endless, no_rotation=endless)

            path_list.append(path_segment)
            mirror_start_point = (screen_width - start_point[0], start_point[1])
            mirror_point = (screen_width - point[0], point[1])
            
            if len(point_set) == 3:
                mirror_path_segment = PathSegment(mirror_start_point, mirror_point, frame_set, bullet_angle=(360-point_set[2]), no_rotation=endless)

            else:
                mirror_path_segment = PathSegment(mirror_start_point, mirror_point, frame_set, no_rotation=endless)

            mirror_path_list.append(mirror_path_segment)

            start_point = point

        path_sets.append((path_list, mirror_path_list))
    
    return path_sets

def calc_angle(x, y):
    #x and y are reversed on purpose because we want the bearing angle.
    return 90 + (math.atan2(y, x) * 180 / math.pi)

class PathSegment():
    def __init__(self, start_point, end_point, frame_set, bullet_angle=None, endless=None, no_rotation=False):

        self.start_point = start_point
        self.w = end_point[0] - start_point[0]
        self.h = end_point[1] - start_point[1]
        self.length = math.hypot(self.w, self.h)
        self.bullet_angle = bullet_angle
        self.endless = endless
        self.bearing = calc_angle(self.w, self.h)
        self.frame_set = []
        self.mask_set = []
        #This is for optimisation we will add in support for on/off screen later so it does not blit while offscreen
        self.on_screen = None

        for frame in frame_set:
            if no_rotation:
                temp = frame
            else:
                temp = pygame.transform.rotate(frame, -self.bearing)
            self.frame_set.append(temp)
            self.mask_set.append(pygame.mask.from_surface(temp))