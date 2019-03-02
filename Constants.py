import pygame

FON = pygame.image.load('data/fon.png')


player_image = pygame.image.load('data/player.png')

tile_width = tile_height = 50

tile_images = {
    'upper-block': pygame.transform.scale(pygame.image.load('data/block-main.png'), (tile_width, tile_height)),
    'empty-block': pygame.transform.scale(pygame.image.load('data/block-empty.png'), (tile_width, tile_height)),
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
