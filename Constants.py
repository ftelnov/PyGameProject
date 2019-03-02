import pygame

FON = pygame.image.load('data/fon.png')

tile_images = {
    'upper-block': pygame.image.load('data/block-main.png'),
    'empty-block': pygame.image.load('data/block-empty.png'),
}

player_image = pygame.image.load('data/player.png')

tile_width = tile_height = 50

SIZE = WIDTH, HEIGHT = 812, 469

KEYS = {
    97: 'left',
    119: 'up',
    32: 'up',
    100: 'right',
}

ADDHEIGHT = 250

FPS = 60
