# Project setup

import pygame as pg
import sys
from settings import *
from sprites import *
from titemap import *
from spritesheet import *
from os import path
from bg_platform import *

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.load_data()

    def load_data(self):
        # folder
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        map_dir = path.join(self.dir, 'map')

        # load map tmx
        self.map = TileMap(path.join(map_dir, 'level2.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        # load spritesheet image
        self.spritesheet = Spritesheet(path.join(img_dir, HERO_SHEET))



    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()

        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'wall':
                self.obstaculo = Obstaculos(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)


        self.camera = Camera(self.map.width, self.map.height)


    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        self.camera.update(self.player)


    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            # event KEYDOWN
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()


    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw_font(self, surf, text, size, x, y):
        self.font_name = pg.font.match_font('arial')
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, BLACK)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    def draw(self):
        # Game Loop - draw
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))

        self.draw_font(self.screen, str("{:.2f}".format(self.player.vel.y)), 18, WIDTH/2, 4*16)

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.run()
    g.show_go_screen()

pg.quit()