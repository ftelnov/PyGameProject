from Constants import *
import pygame


# функция проверяет, принадлежит ли блок тому, на котором можно стоять, или "warning block group"
def check_warning_group(tile):
    # записываю каждый кондитионал в отдельной строке, дабы не загромождать код
    first = tile.type == 'upper-block'
    second = tile.type == 'jump-block'
    speed = tile.type == 'speed-up-block' or tile.type == 'speed-down-block'
    clone = tile.type == 'clone-block'
    if first or second or speed or clone:
        return True
    return False


# Класс камеры
class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # привязка камеры к какому-либо объекту
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # изменяем положение объекта относительно камеры
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


# Класс препятствия
class Tile(pygame.sprite.Sprite):
    def __init__(self, tiles_group, all_sprites, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = TILE_IMAGES[tile_type]  # Изображение препятствия
        self.type = tile_type  # Тип препятствия
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, ADD_HEIGHT + TILE_HEIGHT * pos_y)
        self.safeForm = self.rect.x, self.rect.y
        # форма, ограничивающая блок препятствия

    def reincarnation(self):
        self.rect.x = self.safeForm[0]
        self.rect.y = self.safeForm[1]


# Класс убивающего блока
class DangerousTile(Tile):
    def __init__(self, tiles_group, all_sprites, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites, tile_type, pos_x, pos_y)
        self.rect.y += 20
        self.rect.x += 5
        self.safeForm = self.rect.x, self.rect.y


# Класс блоков, через которые проваливаешься
class ShadowTile(Tile):
    def __init__(self, tiles_group, all_sprites, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites, tile_type, pos_x, pos_y)
        self.image = TILE_IMAGES['dangerous-shadow-block']


# Класс блоков для клона персонажа(Java)
class CloneTile(Tile):
    def __init__(self, clone_tiles, tiles_group, all_sprites, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites, tile_type, pos_x, pos_y)
        self.add(clone_tiles)
        self.flag = 0  # наступали на этот блок или нет

    def update(self, main_player, all_sprites):
        if self.flag:
            return
        main_player.rect.y += 1
        if pygame.sprite.collide_rect(self, main_player):
            self.flag = 1
            # создаем клона персонажа
            PlayerCloneUnused(all_sprites, main_player.rect.x, main_player.rect.y - 1, main_player.image)
        main_player.rect.y -= 1

    # возраждаем персонажа
    def reincarnation(self):
        super().reincarnation()
        self.flag = 0


# Класс кнопок для меню
class Button(pygame.sprite.Sprite):
    def __init__(self, group, x, y, image):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect().move(x, y)


# Клон персонажа
class PlayerCloneUnused(pygame.sprite.Sprite):
    def __init__(self, group, x, y, image):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect().move(x, y)
        self.type = 'player-clone'


# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, player_group, all_sprites, pos_x, pos_y, maximum_height=-1):
        super().__init__(player_group, all_sprites)
        self.image = PLAYER_IMAGES['stay-right']  # изображение игрока
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x + 3, ADD_HEIGHT + TILE_HEIGHT * pos_y + TILE_HEIGHT // 6 - 1)
        self.type = 'player'
        # перемещаем объект как нужно
        self.start_position = self.rect.x, self.rect.y
        self.tile_width = TILE_WIDTH  # ширина всех припятсвия
        self.tile_height = TILE_HEIGHT  # высота всех препятсвий
        self.fieldGeometry = 0  # разметка поля

        self.warning_group = 0  # блоки, через которые нельзя пройти
        self.dangerous_group = 0  # "убийственные блоки"
        self.jump_group = 0  # блоки, на которых можно высоко прыгнуть
        self.speed_up_group = 0  # блоки, увеличивающие скорость
        self.speed_down_group = 0  # блоки, уменьшающие скорость
        self.finish_level_group = 0  # блоки, завершающие уровень

        self.speed = 5  # Константная скорость перемещения(влево/вправо)

        self.jumpSpeed = 18  # Высота прыжка
        self.fallSpeed = 9  # Скорость паденя
        self.stateOfJump = 0  # Фазы прыжка
        self.stateOfWalkLeft = 0  # Фазы хотьбы влево
        self.stateOfWalkRight = 0  # Фазы хотьбы вправо
        self.lastMove = 'right'  # сторона, в которую игрок в последний раз шагал

        self.alive = True  # флаг, жив ли персонаж
        self.finish_game = False  # флан, завершена ли игра
        self.onEarth = True  # Флаг, определяющий, находится Ваш персонаж на земле, или в воздухе
        self.movement = {
            'left': False,
            'right': False,
        }  # индикатор движения

        self.maximumHeight = maximum_height  # максимальная высота, до которой может опуститься персонаж
        self.safeMaximumHeight = maximum_height  # сейв максимальной высоты, для реинкарнации

    #  восстанавливаем персонажа, чтобы не пересоздавать
    def reincarnation(self):
        self.stateOfJump = 0
        self.stateOfWalkLeft = 0
        self.stateOfWalkRight = 0
        self.lastMove = 'right'

        self.alive = True
        self.onEarth = True
        self.movement['left'] = False
        self.movement['right'] = False

        self.rect.x = self.start_position[0]
        self.rect.y = self.start_position[1]

        self.maximumHeight = self.safeMaximumHeight

    # возвращаем местоположение персонажа
    def get_rect(self):
        return self.rect.y, self.rect.x

    def update(self, events):
        #  Проверяем, завершена ли игра
        if pygame.sprite.spritecollide(self, self.finish_level_group, False):
            self.finish_game = True
            return
        self.onEarth = False
        #  Моделька находится в постоянном падении
        self.rect.y += self.fallSpeed
        self.maximumHeight -= self.fallSpeed
        #  если стоим на статичном блоке
        if pygame.sprite.spritecollide(self, self.warning_group, False):
            self.rect.y -= self.fallSpeed  # если мы стоим на блоке, возвращаемся в исходное положение
            self.maximumHeight += self.fallSpeed  # также приводим в обратное положение максимальную высоту
            self.onEarth = True
        #  если пересекаемся с опасным блоком
        if pygame.sprite.spritecollide(self, self.dangerous_group, False):
            self.alive = False  # убиваем персонажа
            Player.play_die_song()  # отыгрываем мелодию смерти

        # Проверяем, на земле ли персонаж
        if self.onEarth:
            #  стандартно проверяем блоки, на которых стоим
            self.rect.y += self.fallSpeed
            self.stateOfJump = 0
            if pygame.sprite.spritecollide(self, self.jump_group, False):
                self.jumpSpeed = 36
            else:
                self.jumpSpeed = 18

            flag = 0  # Проверяем, стоим мы на каком-либо скоростном блоке

            if pygame.sprite.spritecollide(self, self.speed_up_group, False):
                self.speed = 10
                flag = 1

            if pygame.sprite.spritecollide(self, self.speed_down_group, False):
                self.speed = 2
                flag = 1

            #  Если нет, то сносим скорость к стандартной
            if not flag:
                self.speed = 5

            self.rect.y -= self.fallSpeed  # вовзращаемся в исходное положение
        else:
            #  логика прыжка
            if 0 < self.stateOfJump <= 12:
                self.rect.y -= self.jumpSpeed
                self.maximumHeight += self.jumpSpeed
                if pygame.sprite.spritecollide(self, self.warning_group, False):
                    self.rect.y += self.jumpSpeed
                    self.maximumHeight -= self.jumpSpeed
                self.stateOfJump += 1

        # проходимся по событиям
        for event in events:
            try:
                direction = KEYS[event.key]
            except KeyError:
                continue
            if direction == 'up':
                if event.type != pygame.KEYUP and self.onEarth:
                    self.rect.y -= self.jumpSpeed
                    self.maximumHeight += self.jumpSpeed
                    self.stateOfJump = 1
                    if pygame.sprite.spritecollide(self, self.warning_group, False):
                        self.rect.y += self.jumpSpeed
                        self.maximumHeight -= self.jumpSpeed
            else:
                if event.type == pygame.KEYUP:
                    self.movement[direction] = False
                elif event.type == pygame.KEYDOWN:
                    self.movement[direction] = True
        #  логика движения влево
        if self.movement['left']:
            #  свитчим по стадии хотьбы
            if self.stateOfWalkLeft <= 4:
                self.image = PLAYER_IMAGES['go-left-1']
            elif 4 <= self.stateOfWalkLeft <= 8:
                self.image = PLAYER_IMAGES['go-left-2']
            else:
                self.stateOfWalkLeft = 0
            self.rect.x -= self.speed
            self.lastMove = 'left'  # в последний раз двигались влево
            if pygame.sprite.spritecollide(self, self.warning_group, False):
                self.rect.x += self.speed
            self.stateOfWalkLeft += 1
        #  логика движения вправо
        if self.movement['right']:
            #  свитчим по стадии хотьбы
            if self.stateOfWalkRight <= 4:
                self.image = PLAYER_IMAGES['go-right-1']
            elif 4 <= self.stateOfWalkRight <= 8:
                self.image = PLAYER_IMAGES['go-right-2']
            else:
                self.stateOfWalkRight = 0
            self.rect.x += self.speed
            self.lastMove = 'right'  # в последний раз двигались вправо
            if pygame.sprite.spritecollide(self, self.warning_group, False):
                self.rect.x -= self.speed
            self.stateOfWalkRight += 1
        if not self.movement['right'] and not self.movement['left']:
            if self.lastMove == 'right':
                self.image = PLAYER_IMAGES['stay-right']
            else:
                self.image = PLAYER_IMAGES['stay-left']
        if self.maximumHeight < 0:
            self.alive = 0
            Player.play_die_song()
        events.clear()

    #  узнаем конечную ширину и высоту поля
    def set_field_geometry(self, geometry):
        self.fieldGeometry = geometry

    #  устанавливаем группу препятствий(нужна для правильной хотьбы)
    def set_warning_group(self, tiles_group):
        self.warning_group = pygame.sprite.Group(
            *filter(check_warning_group, tiles_group))

    #  устанавливаем группу, которая убивает игрока
    def set_dangerous_group(self, tiles_group):
        self.dangerous_group = pygame.sprite.Group(
            *filter(lambda till: till.type == 'dangerous-triangular-block', tiles_group))

    #  устанавливаем максимальную высоту, которая является смертельной для игрока
    def set_maximum_height(self, height):
        self.maximumHeight = height
        self.safeMaximumHeight = height

    #  устанавливаем группу блоков, на которых можно высоко выпрыгнуть
    def set_jump_group(self, tiles_group):
        self.jump_group = pygame.sprite.Group(*filter(lambda x: x.type == 'jump-block', tiles_group))

    #  устанавливаем группу блоков, на которых можно ускориться
    def set_speed_up_group(self, tiles_group):
        self.speed_up_group = pygame.sprite.Group(
            *filter(lambda x: x.type == 'speed-up-block', tiles_group))

    #  устанавливаем группу блоков, на которых можно замедлиться
    def set_speed_down_group(self, tiles_group):
        self.speed_down_group = pygame.sprite.Group(
            *filter(lambda x: x.type == 'speed-down-block', tiles_group))

    #  устанавливаем группу блоков, которые завершают игру
    def set_finish_group(self, tiles_group):
        self.finish_level_group = pygame.sprite.Group(*filter(lambda x: x.type == 'finish-block', tiles_group))

    # мелодия смерти
    @staticmethod
    def play_die_song():
        pygame.mixer.music.load("data/music/damage.wav")
        pygame.mixer.music.play()
