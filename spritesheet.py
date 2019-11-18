import pygame as pg
from settings import *

class Spritesheet:
    # utility  class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritsheet = pg.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height, scale=1):
        # grab on image  out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritsheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width * scale, height * scale))
        return image