import pygame
from Constants import *


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


class Tile(pygame.sprite.Sprite):
    def __init__(self, tiles_group, all_sprites, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.type = tile_type
        self.rect = self.image.get_rect().move(tile_width * pos_x,  200 + tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, player_group, tiles_group, all_sprites, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, 200 + tile_height * pos_y)
        self.tile_width = tile_width
        self.tiles_group = tiles_group
        self.tile_height = tile_height
        self.flag = 0
        self.warning_group = 0

    def update(self, events, tiles_group):
        if not self.flag:
            self.flag = 1
            self.warning_group = pygame.sprite.Group(*filter(lambda till: till.type == 'wall', tiles_group))
        for event in events:
            if event.key == 273:
                self.rect.y -= self.tile_height
                for tile in self.warning_group:
                    if pygame.sprite.collide_rect(self, tile):
                        self.rect.y += self.tile_height
                        break
            elif event.key == 276:
                self.rect.x -= self.tile_width
                for tile in self.warning_group:
                    if pygame.sprite.collide_rect(self, tile):
                        self.rect.x += self.tile_width
                        break
            elif event.key == 275:
                self.rect.x += self.tile_width
                for tile in self.warning_group:
                    if pygame.sprite.collide_rect(self, tile):
                        self.rect.x -= self.tile_width
                        break
            elif event.key == 274:
                self.rect.y += self.tile_height
                for tile in self.warning_group:
                    if pygame.sprite.collide_rect(self, tile):
                        self.rect.y -= self.tile_height
                        break
            if self.rect.y < 0:
                self.rect.y = self.fieldGeometry[1] - 15
            if self.rect.y > self.fieldGeometry[1]:
                self.rect.y = 15
            if self.rect.x > self.fieldGeometry[0] - 15:
                self.rect.x = 15
            if self.rect.x < 0:
                self.rect.x = self.fieldGeometry - 15
        events.clear()

    def setFieldGeometry(self, geometry):
        self.fieldGeometry = geometry
