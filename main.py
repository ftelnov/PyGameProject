import sys
from MainFunctions import *
from Classes import *

pygame.init()  # инициализация

# все группы спрайтов(глобальные)
all_sprites = pygame.sprite.Group()  # все спрайты
tiles_group = pygame.sprite.Group()  # препятсвия
player_group = pygame.sprite.Group()  # группа игрока
clone_group = pygame.sprite.Group()  # группа клон-блоков

screen = pygame.display.set_mode(SIZE)  # главный surface
pygame.display.set_icon(ICON)
pygame.display.set_caption(NAME)
pygame.display.flip()  # отображаем начальный экран
clock = pygame.time.Clock()  # контроль времени в pygame
level = generate_level(load_level('level.txt'), player_group, tiles_group, all_sprites,
                       clone_group)  # генерируем уровень
mainPlayer = level[0]  # получаем персонажа
mainPlayer.set_field_geometry(SIZE)  # устанавливаем игроку размеры поля(нужно для корректной работы спрайта игрока)
start_position = mainPlayer.get_rect()  # стартовая позиция игрока


#  функция выхода из приложения
def terminate():
    pygame.quit()
    sys.exit()


#  начальная заставка
def start_screen():
    fon = pygame.transform.scale(FON, (WIDTH, HEIGHT))  # фон заставки
    buttons_group = pygame.sprite.Group()
    start_game_button = Button(buttons_group, 200, 250, BUTTON_IMAGES['start-game'])
    screen.blit(fon, (0, 0))  # грузим фон
    start_running = True  # флаг заставки
    while start_running:  # основной цикл заставки
        for event in pygame.event.get():  # чекаем события
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_game_button.rect.collidepoint(event.pos):
                    start_running = False
        buttons_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    main_game()


#  основной цикл игры
def main_game():
    camera = Camera()  # инициализируем объект камеры
    events = []  # заводим список событий
    mainPlayer.reincarnation()  # восстанавливаем данные главного игрока

    for sprite in tiles_group:  # восстанавливаем все спрайты
        sprite.reincarnation()

    for sprite in all_sprites:
        if sprite.type == 'player-clone':
            sprite.kill()

    main_running = True
    while main_running:  # основной цикл
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                events.append(event)
        screen.blit(FON_WITHOUT_BUTTONS, (0, 0))

        # обновляем положение камеры и всех спрайтов
        camera.update(mainPlayer)
        for sprite in all_sprites:
            camera.apply(sprite)

        # подгружаем игроку все события
        player_group.update(events)

        # обновляем группу клон-блоков
        clone_group.update(mainPlayer, all_sprites)

        # отрисовываем спрайты
        all_sprites.draw(screen)
        # если персонаж умер, заканчиваем игру
        if not mainPlayer.alive:
            main_running = False

        # очищаем список событий
        events.clear()
        pygame.display.flip()
        clock.tick(FPS)
    die_screen()


# заставка смерти, аналогично предидущим
def die_screen():
    fon = pygame.transform.scale(DIE, (WIDTH, HEIGHT))
    buttons_group = pygame.sprite.Group()
    new_game_button = Button(buttons_group, 200, 250, BUTTON_IMAGES['new-game'])
    screen.blit(fon, (0, 0))
    die_running = True
    while die_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if new_game_button.rect.collidepoint(event.pos):
                    die_running = False
        buttons_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    main_game()


start_screen()
