import pygame
from Constants import *


# Класс камеры
class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


# Класс препятствия
class Tile(pygame.sprite.Sprite):
    def __init__(self, tiles_group, all_sprites, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]  # Изображение препятствия
        self.type = tile_type  # Тип препятствия
        self.rect = self.image.get_rect().move(tile_width * pos_x, ADDHEIGHT + tile_height * pos_y)
        # форма, ограничивающая блок препятствия


# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, player_group, all_sprites, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image  # изображение игрока
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 3, ADDHEIGHT + tile_height * pos_y + tile_height // 5)
        self.tile_width = tile_width  # ширина всех припятсвия
        self.tile_height = tile_height  # высота всех препятсвий
        self.warning_group = 0  # блоки, через которые нельзя пройти
        self.speed = 10  # Константная скорость
        self.movement = {
            'left': False,
            'right': False,
            'down': False,
            'up': False
        }  # индикатор движения

    def update(self, events):
        for event in events:
            try:
                direction = KEYS[event.key]
            except KeyError:
                continue
            self.movement[direction] = not self.movement[direction]
        if self.movement['up']:
            self.rect.y -= self.speed
            for tile in self.warning_group:
                if pygame.sprite.collide_rect(self, tile):
                    self.rect.y += self.speed
                    break
        if self.movement['left']:
            self.rect.x -= self.speed
            for tile in self.warning_group:
                if pygame.sprite.collide_rect(self, tile):
                    self.rect.x += self.speed
                    break
        if self.movement['right']:
            self.rect.x += self.speed
            for tile in self.warning_group:
                if pygame.sprite.collide_rect(self, tile):
                    self.rect.x -= self.speed
                    break
        if self.movement['down']:
            self.rect.y += self.speed
            for tile in self.warning_group:
                if pygame.sprite.collide_rect(self, tile):
                    self.rect.y -= self.speed
                    break
        if self.rect.y < 0:
            self.rect.y = self.fieldGeometry[1] - 15
        if self.rect.y > self.fieldGeometry[1]:
            self.rect.y = 15
        if self.rect.x > self.fieldGeometry[0] - 15:
            self.rect.x = 15
        if self.rect.x < 0:
            self.rect.x = self.fieldGeometry[0] - 15
        events.clear()

    def set_field_geometry(self, geometry):
        self.fieldGeometry = geometry

    def set_warning_group(self, tiles_group):
        self.warning_group = pygame.sprite.Group(*filter(lambda till: till.type == 'upper-block', tiles_group))
