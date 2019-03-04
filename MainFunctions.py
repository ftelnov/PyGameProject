from Classes import Tile, Player, DangerousTile
import pygame
from Constants import *


def load_level(filename):
    filename = "data/levels/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level, player_group, tiles_group, all_sprites):
    new_player, x, y = None, None, None
    maximum_height = 0
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile(tiles_group, all_sprites, 'empty-block', x, y)
            elif level[y][x] == '#':
                Tile(tiles_group, all_sprites, 'upper-block', x, y)
            elif level[y][x] == '@':
                Tile(tiles_group, all_sprites, 'empty-block', x, y)
                new_player = Player(player_group, all_sprites, x, y)
            elif level[y][x] == '!':
                DangerousTile(tiles_group, all_sprites, 'dangerous-triangular-block', x, y)
            if ADDHEIGHT + tile_height * y > maximum_height:
                maximum_height = ADDHEIGHT + tile_height * y
    # вернем игрока, а также размер поля в клетках
    new_player.set_warning_group(tiles_group)
    new_player.set_maximum_height(maximum_height)
    new_player.set_dangerous_group(tiles_group)
    return new_player, x, y, maximum_height
