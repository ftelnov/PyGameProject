import pygame


def load_image(filename):
    filename = "data/png/" + filename
    return pygame.image.load(filename)


FON = load_image('fon.png')

tile_width = tile_height = 50

tile_images = {
    'upper-block': pygame.transform.scale(load_image('block-main.png'), (tile_width, tile_height)),
    'empty-block': pygame.transform.scale(load_image('block-empty.png'), (tile_width, tile_height)),
}

player_images = {
    'stay-right': load_image('player-stays-right.png'),
    'stay-left': load_image('player-stays-left.png'),
    'go-left-1': load_image('player-go-left-1.png'),
    'go-left-2': load_image('player-go-left-2.png'),
    'go-right-1': load_image('player-go-right-1.png'),
    'go-right-2': load_image('player-go-right-2.png'),
}
SIZE = WIDTH, HEIGHT = 812, 469

KEYS = {
    97: 'left',
    119: 'up',
    32: 'up',
    100: 'right',
}

ADDHEIGHT = 200

FPS = 60
