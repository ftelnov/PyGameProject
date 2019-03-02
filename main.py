import pygame
import sys
from Constants import *
from MainFunctions import *

pygame.init()

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
running = True
screen = pygame.display.set_mode(SIZE)
pygame.display.flip()
clock = pygame.time.Clock()
level = generate_level(load_level('level.txt'), player_group, tiles_group, all_sprites)
mainPlayer = level[0]
mainPlayer.set_field_geometry(SIZE)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(FON, (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
events = []
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            events.append(event)
    screen.blit(FON, (0, 0))
    player_group.update(events)
    all_sprites.draw(screen)
    tiles_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
