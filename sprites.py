import pygame as pg
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.jumping = False
        self.abaixar = False
        self.air = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.frame_parado[0]
        self.rect = self.image.get_rect()

        self.vx, self.vy = 0, 0
        self.x = x
        self.y = y

        self.acc = vec(0, 0)
        self.pos = vec(x, y)
        self.vel = vec(0, 0)

    def load_images(self):
        col = 7
        lin = 16
        total = col * lin

        self.all_hero_image = []
        for frame in range(total):
            self.all_hero_image.append(
                self.game.spritesheet.get_image(
                    frame % col * HERO_W, frame // col * HERO_H, HERO_W, HERO_H))

        # frames parado
        self.frame_parado = []
        for frame in self.all_hero_image[0:4]:
            self.frame_parado.append(frame)

        # frames abaixar
        self.frame_abaixar = []
        for frame in self.all_hero_image[4:8]:
            self.frame_abaixar.append(frame)

        # frames correr
        self.frame_correr_d = []
        for frame in self.all_hero_image[8:14]:
            self.frame_correr_d.append(frame)

        self.frame_correr_e = []
        for frame in self.all_hero_image[8:14]:
            self.frame_correr_e.append(pg.transform.flip(frame, True, False))

        # frames pular
        self.frame_pular = []
        for frame in self.all_hero_image[14:22]:
            self.frame_pular.append(frame)

        # frames caindo
        self.frame_cair = []
        for frame in self.all_hero_image[22:24]:
            self.frame_cair.append(frame)

    def animated_frames(self, now, time, list, loop=True, count = 0):
        # para auxiliar na animacao de frames para animacao
       if now - self.last_update > time:
            self.last_update = now
            if loop:
                self.current_frame = (self.current_frame + 1) % len(list)
                self.image = list[self.current_frame]
            elif self.current_frame < count:
                self.current_frame = (self.current_frame + 1) % len(list)
                self.image = list[self.current_frame]
            elif self.current_frame > count:
                self.current_frame = count



    def animated(self):
        now = pg.time.get_ticks()

        # parado
        if not self.jumping and not self.abaixar:
            self.animated_frames(now, 250, self.frame_parado)

        # abaixar
        if self.abaixar and not self.jumping:
            self.animated_frames(now, 250, self.frame_abaixar)

        # correr_d
        if self.vx > 0 and not self.jumping and not self.air:
            self.animated_frames(now, 150, self.frame_correr_d)

        # correr_e
        if self.vx < 0 and not self.jumping and not self.air:
            self.animated_frames(now, 150, self.frame_correr_e)

        # pular
        if self.jumping:
            self.animated_frames(now, 50, self.frame_pular, False, 7)
            if self.current_frame == 7:
                self.jumping = False

        #cair
        if self.vel.y > 5:
            self.air = True
        if self.air:
            self.animated_frames(now, 20, self.frame_cair)

        # mask
        self.mask = pg.mask.from_surface(self.image)

    def get_press_events_up(self, event):
        if event.key == pg.K_s or event.key == pg.K_DOWN:
            self.abaixar = False

    def get_press_events_down(self, event):
        if event.key == pg.K_s or event.key == pg.K_DOWN:
            self.abaixar = True

    def get_keys(self):
        self.vx, self.vy = 0, 0

        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_ACC
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_ACC

        if keys[pg.K_SPACE]:
            self.jump()

        if self.vx != 0 and self.vy != 0:
            #self.vx *= 0.7071 + self.game.dt
            self.vy *= 0.7071 + self.game.dt

    def collide_with_walls(self, dir):
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                 self.air = False

                 if self.vel.y > 0:
                   self.pos.y = hits[0].rect.top - self.rect.height
                   self.vel.y = 0
                 if self.vel.y < 0:
                   self.pos.y = hits[0].rect.bottom
                   self.vel.y = 0

                 self.vel.y = 0
                 self.rect.y = self.pos.y

        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                #self.vx = 0
                self.rect.x = self.x




    def jump(self):
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        self.rect.y -= 1
        if hits:
            self.vel.y = -JUMP

        self.jumping = True

    def update(self):
        self.animated()
        self.get_keys()
        self.acc = vec(0, PLAYER_GRAVITY)

        # apply friction
        self.acc.x += self.vx * PLAYER_FRICTION

        # equations of motion
        self.vel += self.acc
        self.vx += self.acc.x
        if abs(self.vx) < 0.5:
            self.vx = 0

        if self.vel.y > 10:
            self.vel.y = 10

        self.pos += self.vel + 0.5 * self.acc


        self.x += self.vx + 0.5 * self.acc.x
        self.y += self.vy + self.game.dt

        if self.pos.y > 640:
            self.pos.y = 0

        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')



