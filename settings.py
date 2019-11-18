# game options/settings
TITLE = "Meu primeiro game!"
WIDTH = 640  # 16 * 64 OR 32 * 32 OR  64 * 16
HEIGHT = 360  # 16 * 48 OR 32 * 24 OR 64 * 12
FPS = 60

#grids para o mapa
TILESIZE = 16
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

#Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.8
JUMP = 14

HERO_SHEET = "adventurer_v15.png"
HERO_W = 50
HERO_H = 37

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
LIGHTGREY = (100, 100, 100)
DARKGREY = (40, 40, 40)
BGCOLOR = DARKGREY


# Player settings
PLAYER_SPEED = 300
PLAT_SPEED = 100