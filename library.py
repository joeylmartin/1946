import pygame


def load_image_scale_convert_flip(image_path, scaled_factor=None, scaled_size=None,
                                  flip=False, use_alpha=False):
    '''
    Loads the image from image_path 
    Scales image if requested. 
        scaled_size is a tuple of desired (width, height)
        scaled_factor is a multiplier from current size 
    flips it if requested.
    Does the convert() for performance.
        Uses aplha if the user says image has transparency
    '''
    image = pygame.image.load(image_path)
    
    if flip:
        image = pygame.transform.flip(image, True, False)

    if scaled_factor:
        w = image.get_width() * scaled_factor
        h = image.get_height() * scaled_factor
        image = pygame.transform.scale(image, (w, h))
    elif scaled_size:
        image = pygame.transform.scale(image, scaled_size)

    if use_alpha:
        return image.convert_alpha()
    return image.convert()

def make_shadow(image,opacity):
    maskObject = pygame.mask.from_surface(image)
    return maskObject.to_surface(setcolor=(0,0,0,opacity), unsetcolor=None)