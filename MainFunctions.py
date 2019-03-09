from Classes import Tile, Player, DangerousTile, ShadowTile, CloneTile
from Constants import *


# подгружаем уровень в игру
def load_level(filename):
    filename = "data/levels/" + filename  # конечный путь к уровню
    with open(filename, 'r') as mapFile:
        level_map = [line.replace(' ', '.') for line in mapFile]
    max_width = max(map(len, level_map))  # максимальная ширина уровня
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))  # добавляем пустых клеток к правому краю


# функция генерирования уровня
def generate_level(level, player_group, tiles_group, all_sprites, clone_tiles):
    new_player, x, y = None, None, None  # заводим переменные для игрока, а также для его координат
    maximum_height = 0  # максимальная высота уровня
    for y in range(len(level)):
        for x in range(len(level[y])):
            # пустой блок
            if level[y][x] == '.':
                Tile(tiles_group, all_sprites, 'empty-block', x, y)
            # простой блок, на котором можно спокойно постоять
            elif level[y][x] == '#':
                Tile(tiles_group, all_sprites, 'upper-block', x, y)
            # заводим персонажа
            elif level[y][x] == '@':
                Tile(tiles_group, all_sprites, 'empty-block', x, y)
                new_player = Player(player_group, all_sprites, x, y)
            # заводим опасные блоки
            elif level[y][x] == '!':
                DangerousTile(tiles_group, all_sprites, 'dangerous-triangular-block', x, y)
            # заводим блоки, через которые можно провалиться
            elif level[y][x] == 'S':
                ShadowTile(tiles_group, all_sprites, 'dangerous-shadow-block', x, y)
            # заводим блоки, на которых можно подпрыгнуть высоко
            elif level[y][x] == 'J':
                Tile(tiles_group, all_sprites, 'jump-block', x, y)
            # заводим блоки, которые увеличивают скорость
            elif level[y][x] == '+':
                Tile(tiles_group, all_sprites, 'speed-up-block', x, y)
            # заводим блоки, которые уменьшают скорость
            elif level[y][x] == '-':
                Tile(tiles_group, all_sprites, 'speed-down-block', x, y)
            # клонирующие персонажа блока
            elif level[y][x] == 'C':
                CloneTile(clone_tiles, tiles_group, all_sprites, 'clone-block', x, y)
            # финиширующий уровень блок
            elif level[y][x] == 'F':
                Tile(tiles_group, all_sprites, 'finish-block', x, y)
            # вычисляем максимальную высоту на каждой итерации
            if TILE_HEIGHT * y - ADD_HEIGHT > maximum_height:
                maximum_height = TILE_HEIGHT * y - ADD_HEIGHT
    # вернем игрока, а также размер поля в клетках
    new_player.set_maximum_height(maximum_height)

    # установим строго фрагментированные группы препятствий для игрока
    new_player.set_warning_group(tiles_group)
    new_player.set_dangerous_group(tiles_group)
    new_player.set_jump_group(tiles_group)
    new_player.set_speed_up_group(tiles_group)
    new_player.set_speed_down_group(tiles_group)

    # возвращаем персонажа, его координаты, максимальную высоту
    return new_player, x, y, maximum_height
