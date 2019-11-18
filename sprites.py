import pygame as pg
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.jumping = False
        self.walking = False
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


    def animated(self):
        now = pg.time.get_ticks()

        # parado
        if not self.jumping and not self.walking:
            if now - self.last_update > 250:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.frame_parado)
                self.image = self.frame_parado[self.current_frame]

        # mask
        self.mask = pg.mask.from_surface(self.image)

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED

        if keys[pg.K_SPACE]:
            self.jump()

        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071 + self.game.dt
            self.vy *= 0.7071 + self.game.dt

    def collide_with_walls(self, dir):
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
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
                self.vx = 0
                self.rect.x = self.x




    def jump(self):
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        self.rect.y -= 1
        if hits:
            self.vel.y = -JUMP

    def update(self):
        self.animated()
        self.get_keys()
        self.acc = vec(0, PLAYER_GRAVITY)

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION

        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.5:
            self.vel.x = 0

        if self.vel.y > 10:
            self.vel.y = 10

        self.pos += self.vel + 0.5 * self.acc


        self.x += self.vx * self.game.dt
        self.y += self.vy + self.game.dt

        if self.pos.y > 640:
            self.pos.y = 0

        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')



