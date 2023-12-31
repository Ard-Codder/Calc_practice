import pygame
from pygame.locals import *
from pygame import mixer

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ping-Pong")

background_image = pygame.image.load("background_image.jpg").convert()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

mixer.music.load("game_music.mp3")
mixer.music.play(-1)

music_end_event = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(music_end_event)

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

platform_width = 10
platform_height = 60
platform_speed = 5

ball_width = 10
ball_x_speed = 3
ball_y_speed = 3

settings = {
    "platform_width": 10,
    "platform_height": 60,
    "platform_speed": 5,
    "ball_diameter": 10,
    "ball_x_speed": 3,
    "ball_y_speed": 3
}

sets = [platform_width, platform_height, platform_speed, ball_width, ball_x_speed, ball_y_speed]

player1_score = 0
player2_score = 0

font = pygame.font.Font(None, 36)


def create_platform(x, y, p_width, p_height):
    platform = pygame.Rect(x, y, p_width, p_height)
    return platform


def show_menu():
    intro = True
    while intro:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[K_ESCAPE]:
                pygame.quit()
                quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == music_end_event:
                mixer.music.play()

        screen.blit(background_image, (0, 0))
        title_text = font.render("Ping-Pong Game", True, white)
        start_text = font.render("1. Start Game", True, white)
        settings_text = font.render("2. Game Settings", True, white)
        quit_text = font.render("3. Quit", True, white)
        screen.blit(title_text, (screen_width / 2 - title_text.get_width() / 2, 100))
        screen.blit(start_text, (screen_width / 2 - start_text.get_width() / 2, 200))
        screen.blit(settings_text, (screen_width / 2 - settings_text.get_width() / 2, 250))
        screen.blit(quit_text, (screen_width / 2 - quit_text.get_width() / 2, 300))

        pygame.display.update()

        if keys[K_1]:
            intro = False
            start_game()
        elif keys[K_2]:
            intro = False
            show_settings()
        elif keys[K_3]:
            pygame.quit()
            quit()


def show_settings():
    while True:
        clock = pygame.time.Clock()
        screen.blit(background_image, (0, 0))
        settings_text = font.render("Game Settings", True, white)
        screen.blit(settings_text, (screen_width // 2 - settings_text.get_width() // 2, 100))
        y = 200
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[K_ESCAPE]:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start_game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == music_end_event:
                mixer.music.play()

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        for key, value in settings.items():
            label_text = font.render(f"{key}: {value}", True, white)
            decrease_arrow = font.render("<", True, white)
            increase_arrow = font.render(">", True, white)

            screen.blit(label_text, (screen_width // 2 - label_text.get_width() // 2, y))
            screen.blit(decrease_arrow, (screen_width // 2 - label_text.get_width() // 2 - 20, y))
            screen.blit(increase_arrow, (screen_width // 2 + label_text.get_width() // 2 + 5, y))

            decrease_arrow_rect = decrease_arrow.get_rect(x=screen_width // 2 - label_text.get_width() // 2 - 20, y=y)
            increase_arrow_rect = increase_arrow.get_rect(x=screen_width // 2 + label_text.get_width() // 2 + 5, y=y)

            # Уменьшение значения параметра по щелчку на стрелку влево
            if decrease_arrow_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
                if key == "platform_width" and settings[key] == 5:
                    pass
                elif key == "platform_height" and settings[key] == 10:
                    pass
                elif key == "ball_diameter" and settings[key] == 10:
                    pass
                elif (key == "ball_x_speed" or key == "ball_y_speed" or key == "platform_speed") and settings[key] == 1:
                    pass
                else:
                    settings[key] -= 1
            # Увеличение значения параметра по щелчку на стрелку вправо
            if increase_arrow_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
                if key == "platform_width" and settings[key] == 25:
                    pass
                elif key == "platform_height" and settings[key] == screen_height:
                    pass
                elif key == "ball_diameter" and settings[key] == 400:
                    pass
                elif (key == "ball_x_speed" or key == "ball_y_speed" or key == "platform_speed") and settings[
                    key] == 50:
                    pass
                else:
                    settings[key] += 1
            y += 30

        pygame.display.update()
        clock.tick(60)


def start_game():
    print(settings)
    z = [settings.get(key) for key in settings]
    for i in range(len(sets)):
        sets[i] = z[i]

    platform_width = sets[0]
    platform_height = sets[1]
    platform_speed = sets[2]
    ball_width = sets[3]
    ball_x_speed = sets[4]
    ball_y_speed = sets[5]

    player1 = create_platform(0, screen_height / 2 - platform_height / 2, platform_width, platform_height)
    player2 = create_platform(screen_width - platform_width, screen_height / 2 - platform_height / 2,
                              platform_width, platform_height)

    ball = pygame.Rect(screen_width / 2 - ball_width / 2, screen_height / 2 - ball_width / 2, ball_width, ball_width)
    ball_direction_x = -1
    ball_direction_y = -1

    player1_score = 0
    player2_score = 0

    clock = pygame.time.Clock()
    running = True

    mixer.init()
    collision_sound = mixer.Sound("collision_sound.mp3")
    hitting_the_wall = mixer.Sound("brosok-myacha.mp3")

    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[K_ESCAPE]:
                pygame.quit()
                quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == music_end_event:
                mixer.music.play()

        if keys[K_w] and player1.y - platform_speed > 0:
            player1.y -= platform_speed
        if keys[K_s] and player1.y + platform_speed < screen_height - platform_height:
            player1.y += platform_speed
        if keys[K_UP] and player2.y - platform_speed > 0:
            player2.y -= platform_speed
        if keys[K_DOWN] and player2.y + platform_speed < screen_height - platform_height:
            player2.y += platform_speed

        ball.x += ball_x_speed * ball_direction_x
        ball.y += ball_y_speed * ball_direction_y

        if ball.y <= 0 or ball.y >= screen_height - ball_width:
            ball_direction_y *= -1
            hitting_the_wall.play()

        if ball.x <= platform_width - ball_width // 2:
            ball_direction_x *= -1
            player2_score += 1
            hitting_the_wall.play()
        if ball.x >= screen_width - ball_width - platform_width + ball_width // 2:
            ball_direction_x *= -1
            player1_score += 1
            hitting_the_wall.play()

        if ball.colliderect(player1) or ball.colliderect(player2):
            ball_direction_x *= -1
            collision_sound.play()

        screen.blit(background_image, (0, 0))
        pygame.draw.rect(screen, white, player1)
        pygame.draw.rect(screen, white, player2)
        pygame.draw.rect(screen, white, ball)

        player1_text = font.render(str(player1_score), True, white)
        player2_text = font.render(str(player2_score), True, white)
        screen.blit(player1_text, (screen_width / 2 - 50, 10))
        screen.blit(player2_text, (screen_width / 2 + 30, 10))

        pygame.display.update()
        clock.tick(60)


show_menu()
