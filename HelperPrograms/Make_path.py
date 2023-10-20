#!/usr/bin/env python

import pygame, traceback
import collections
import json
import os
import datetime

FRAME_RATE = 10

#elements

waterBackground = pygame.image.load('../assets/game/stage/waterbackground.png')
desertBackground = pygame.image.load('../assets/game/stage/desertbackground.png')
grassBackground = pygame.image.load('../assets/game/stage/grassbackground.png')
 
def main():
    pygame.init()
    
    try:
        #Background size (810, 1080)
        size = waterBackground.get_size()
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("1946 Path Maker")
        #pygame.mouse.set_visible(True)
        #set startGame to 'game'to skip the title screen/exposition for debug purposes.
        clock = pygame.time.Clock()

        #Main game loop
        screen.blit(waterBackground, (0, 0))
        position_list = []
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
            if pygame.mouse.get_focused():
                position = pygame.mouse.get_pos()
                print(position)
                position_list.append(position)
            elif position_list:
                break

            pygame.display.flip()

            clock.tick(FRAME_RATE)
        date_time = datetime.datetime.now().strftime("%Y.%m.%d_%H.%M.%S")
        filename = 'path_' + date_time + '.json'
        filepath = os.path.join("Paths", filename)
        with open(filepath, 'w') as outfile:
            json.dump(position_list, outfile)

    except Exception as ex:
        print(traceback.format_exc())
        raise
    finally:
        # Close window and exit
        pygame.quit()

if __name__ == "__main__":
    main()