import sys
from MainFunctions import *
from Classes import *
import webbrowser

pygame.init()  # инициализация

# все группы спрайтов(глобальные)
all_sprites = pygame.sprite.Group()  # все спрайты
tiles_group = pygame.sprite.Group()  # препятсвия
player_group = pygame.sprite.Group()  # группа игрока
clone_group = pygame.sprite.Group()  # группа клон-блоков
cursor_group = pygame.sprite.Group()  # группа курсора

screen = pygame.display.set_mode(SIZE)  # главный surface
pygame.display.set_icon(ICON)  # устанавливаем иконку
pygame.display.set_caption(NAME)  # устанавливаем имя
pygame.display.flip()  # отображаем начальный экран
cursor = pygame.sprite.Sprite()  # изменяем курсор
cursor.image = CURSOR  # устанавливаем ему изображение
cursor.rect = cursor.image.get_rect()  # подгоняем размер
cursor_group.add(cursor)  # добавляем в группу всех спрайтов

#  грузим фоновую музыку
pygame.mixer.music.load("data/music/background.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1, 0.0)

#  кол-во жизней
life = LIFE_COUNT

#  флаг проигрывания музыки
song = True

clock = pygame.time.Clock()  # контроль времени в pygame
levels = get_levels()  # получили все уровни
level_index = 0  # переменная, показывающая, на каком уровне мы сейчас находимся


# функция выхода из приложения
def terminate():
    pygame.quit()
    sys.exit()


# начальная заставка
def start_screen():
    global level_index, song
    level_index = 0  # текущий уровень
    fon = pygame.transform.scale(FON, (WIDTH, HEIGHT))  # фон заставки
    buttons_group = pygame.sprite.Group()
    start_game_button = Button(buttons_group, 200, 250, BUTTON_IMAGES['start-game'])

    song_button = SONG_IMAGES[song]

    start_running = True  # флаг заставки

    while start_running:  # основной цикл заставки
        for event in pygame.event.get():  # чекаем события
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_game_button.rect.collidepoint(event.pos):
                    start_running = False
                if song_button.get_rect().collidepoint(event.pos):
                    song = not song
                    if song:
                        pygame.mixer.music.play(-1, 0.0)
                    else:
                        pygame.mixer.music.stop()

            elif event.type == pygame.MOUSEMOTION:
                cursor.rect.x = event.pos[0]
                cursor.rect.y = event.pos[1]

        song_button = SONG_IMAGES[song]
        screen.blit(fon, (0, 0))  # грузим фон
        screen.blit(song_button, (0, 0))
        buttons_group.draw(screen)
        if pygame.mouse.get_focused():
            cursor_group.draw(screen)
            pygame.mouse.set_visible(0)
        pygame.display.flip()
        clock.tick(FPS)

    global life
    life = 3
    level = levels[level_index]  # получаем уровень из списка уровней
    main_game(level)


#  основной цикл игры
def main_game(level_name):
    global level_index
    for sprite in all_sprites:
        sprite.kill()
    camera = Camera()  # инициализируем объект камеры
    events = []  # заводим список событий
    level = generate_level(load_level(level_name), player_group, tiles_group, all_sprites, clone_group)
    main_player = level[0]  # получаем персонажа
    state = 0  # показывает, завершена ли игра, или персонаж умер
    # устанавливаем игроку размеры поля(нужно для корректной работы спрайта игрока)
    main_player.set_field_geometry(SIZE)
    main_player.reincarnation()  # восстанавливаем данные главного игрока

    # Устанавливаем группу сердец
    heart_group = pygame.sprite.Group()
    for pos in range(800 - 45 * life, 800, 45):
        Life(heart_group, pos, 10)

    for sprite in tiles_group:  # восстанавливаем все спрайты
        sprite.reincarnation()

    for sprite in all_sprites:
        if sprite.type == 'player-clone':
            sprite.kill()
    while True:  # основной цикл
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key == 27:
                    terminate()
                events.append(event)

            elif event.type == pygame.MOUSEMOTION:
                cursor.rect.x = event.pos[0]
                cursor.rect.y = event.pos[1]

        screen.blit(FON_WITHOUT_BUTTONS, (0, 0))

        # обновляем положение камеры и всех спрайтов
        camera.update(main_player)
        for sprite in all_sprites:
            camera.apply(sprite)

        # подгружаем игроку все события
        player_group.update(events)

        # обновляем группу клон-блоков
        clone_group.update(main_player, all_sprites)

        # отрисовываем спрайты
        all_sprites.draw(screen)

        # если игра завершена, грузим другой уровень:
        if main_player.finish_game:
            level_index += 1
            state = 1
            break
        # если персонаж умер, заканчиваем игру
        if not main_player.alive:
            state = 0
            break

        # очищаем список событий
        events.clear()

        # убираем стандартный курсор
        if pygame.mouse.get_focused():
            pygame.mouse.set_visible(0)

        heart_group.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
    if level_index > len(levels) - 1:
        finish_game_screen()
        return
    die_screen(level_name) if not state else main_game(levels[level_index])


# заставка смерти, аналогично предидущим
def die_screen(level):
    global life
    state = 0  # какая кнопка была нажата
    fon = pygame.transform.scale(DIE, (WIDTH, HEIGHT))
    buttons_group = pygame.sprite.Group()  # группа кнопок
    new_game_button = Button(buttons_group, 200, 350, BUTTON_IMAGES['new-game'])  # кнопка начала игры
    if life >= 1:
        continue_game_button = Button(buttons_group, 200, 250,
                                      BUTTON_IMAGES['continue-game'])  # кнопка продолжения игры
    else:
        new_game_button.rect.y = 250

    # Устанавливаем группу сердец
    heart_group = pygame.sprite.Group()
    for pos in range(670, 670 + 45 * life, 45):
        Life(heart_group, pos, 10)

    die_running = True
    while die_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if new_game_button.rect.collidepoint(event.pos):
                    die_running = False
                    state = 1
                if life >= 1 and continue_game_button.rect.collidepoint(event.pos):
                    die_running = False
                    state = 0
                    life -= 1

            elif event.type == pygame.MOUSEMOTION:
                cursor.rect.x = event.pos[0]
                cursor.rect.y = event.pos[1]

            elif event.type == pygame.KEYDOWN and event.key == 27:
                terminate()

        screen.blit(fon, (0, 0))

        buttons_group.draw(screen)  # отрисовываем кнопки

        # убираем стандартный курсор
        if pygame.mouse.get_focused():
            cursor_group.draw(screen)
            pygame.mouse.set_visible(0)

        heart_group.draw(screen)  # отрисовываем группу сердец

        pygame.display.flip()
        clock.tick(FPS)
    if not state:
        main_game(level)
    else:
        start_screen()


# завершающий экран(если прошел игру)
def finish_game_screen():
    fon = pygame.transform.scale(FINISH_GAME, (WIDTH, HEIGHT))  # грузим фон
    buttons_group = pygame.sprite.Group()  # все кнопки
    github_button = Button(buttons_group, 415, 395, BUTTON_IMAGES['github'])  # гитхаб кнопка
    finish_game = True  # флаг текущего фона
    while finish_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if github_button.rect.collidepoint(event.pos):
                    webbrowser.open('https://github.com/ftelnov/PyGameProject')  # открываем репозиторий с проектом
            elif event.type == pygame.KEYDOWN and event.key == 27:
                finish_game = False
                terminate()

            elif event.type == pygame.MOUSEMOTION:
                cursor.rect.x = event.pos[0]
                cursor.rect.y = event.pos[1]
        screen.blit(fon, (0, 0))

        buttons_group.draw(screen)

        # убираем стандартный курсор
        if pygame.mouse.get_focused():
            cursor_group.draw(screen)
            pygame.mouse.set_visible(0)

        pygame.display.flip()
        clock.tick(FPS)
    start_screen()


start_screen()
