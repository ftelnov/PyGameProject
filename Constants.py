import pygame


# подгрузка изображений, используется только тут
def load_image(filename):
    filename = "data/png/" + filename
    return pygame.image.load(filename)


FON = load_image('fons/fon.png')  # главный фон приложения
DIE = load_image('fons/die.png')  # фон смерти
FINISH_GAME = load_image('fons/finish-game-fon.png')
FON_WITHOUT_BUTTONS = load_image('fons/fon-without-buttons.png')  # фон без кнопок для самой игры
ICON = load_image('icons/icon.png')  # иконка приложения
NAME = 'CodeRunner'  # имя приложения
CURSOR = load_image('cursor/cursor.png')  # изображение курсора
GRAVITY = 9  # гравитация
DEATH_TEXT = load_image('text/life.png')  # текст "DEATH"
HEART_IMAGE = load_image('blocks/heart.png')  # изображение сердечка
LIFE_COUNT = 3  # кол-во жизней

# размеры блоков
TILE_WIDTH = TILE_HEIGHT = 50

# изображения блоков
TILE_IMAGES = {
    'upper-block': pygame.transform.scale(load_image('blocks/block-main.png'), (TILE_WIDTH, TILE_HEIGHT)),
    'empty-block': pygame.transform.scale(load_image('blocks/block-empty.png'), (TILE_WIDTH, TILE_HEIGHT)),
    'dangerous-shadow-block': pygame.transform.scale(load_image('blocks/dangerous-shadow-block.png'),
                                                     (TILE_WIDTH, TILE_HEIGHT)),
    'dangerous-triangular-block': load_image('blocks/dangerous-triangular-block.png'),
    'jump-block': pygame.transform.scale(load_image('blocks/block-jump.png'), (TILE_WIDTH, TILE_HEIGHT)),
    'speed-up-block': pygame.transform.scale(load_image('blocks/block-speed-up.png'), (TILE_WIDTH, TILE_HEIGHT)),
    'speed-down-block': pygame.transform.scale(load_image('blocks/block-speed-down.png'), (TILE_WIDTH, TILE_HEIGHT)),
    'clone-block': pygame.transform.scale(load_image('blocks/block-clone.png'), (TILE_WIDTH, TILE_HEIGHT)),
    'finish-block': pygame.transform.scale(load_image('blocks/block-finish.png'), (TILE_WIDTH, TILE_HEIGHT))
}

# изображения игрока
PLAYER_IMAGES = {
    'stay-right': load_image('player/player-stays-right.png'),
    'stay-left': load_image('player/player-stays-left.png'),
    'go-left-1': load_image('player/player-go-left-1.png'),
    'go-left-2': load_image('player/player-go-left-2.png'),
    'go-right-1': load_image('player/player-go-right-1.png'),
    'go-right-2': load_image('player/player-go-right-2.png'),
}

# изображения кнопок
BUTTON_IMAGES = {
    'new-game': load_image('buttons/new_game_button.png'),
    'start-game': load_image('buttons/start_game_button.png'),
    'github': load_image('buttons/github-button.png'),
    'continue-game': load_image('buttons/continue_game_button.png'),
}

SONG_IMAGES = {
    True: pygame.transform.scale(load_image('blocks/song-on.png'), (35, 35)),
    False: pygame.transform.scale(load_image('blocks/song-off.png'), (35, 35))
}

# размеры поля
SIZE = WIDTH, HEIGHT = 812, 469

# коды нажатия кнопок и их соответствия
KEYS = {
    97: 'left',
    119: 'up',
    32: 'up',
    100: 'right',
}

# добавочная высота от начала поля
ADD_HEIGHT = 200

# кол-во кадров
FPS = 60
