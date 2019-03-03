import pygame


def load_image(filename):
    filename = "data/png/" + filename
    return pygame.image.load(filename)


FON = load_image('fons/fon.png')
DIE = load_image('fons/die.png')


BUTTON_NEW_GAME = load_image('buttons/new_game_button.png')
DIE.blit(BUTTON_NEW_GAME, (200, 250))

tile_width = tile_height = 50

tile_images = {
    'upper-block': pygame.transform.scale(load_image('blocks/block-main.png'), (tile_width, tile_height)),
    'empty-block': pygame.transform.scale(load_image('blocks/block-empty.png'), (tile_width, tile_height)),
    'dangerous-triangular-block': load_image('blocks/dangerous-triangular-block.png')
}

player_images = {
    'stay-right': load_image('player/player-stays-right.png'),
    'stay-left': load_image('player/player-stays-left.png'),
    'go-left-1': load_image('player/player-go-left-1.png'),
    'go-left-2': load_image('player/player-go-left-2.png'),
    'go-right-1': load_image('player/player-go-right-1.png'),
    'go-right-2': load_image('player/player-go-right-2.png'),
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
