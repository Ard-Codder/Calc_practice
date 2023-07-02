import pygame
from pygame.locals import *
from pygame import mixer

pygame.init()

screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("pong")

black = pygame.color.Color(0, 0, 0)
white = pygame.color.Color(255, 255, 255)

platform_width = 10
platform_height = 60
platform_speed = 5

ball_width = 10
ball_height = 10
ball_x_speed = 3
ball_y_speed = 3

player1_score = 0
player2_score = 0

font = pygame.font.Font(None, 36)


def create_platform(x, y):
    platform = pygame.Rect(x, y, platform_width, platform_height)
    return platform


player1 = create_platform(10, screen_height / 2 - platform_height / 2)
player2 = create_platform(screen_width - platform_width - 10, screen_height / 2 - platform_height / 2)

ball = pygame.Rect(screen_width / 2 - ball_width / 2, screen_height / 2 - ball_height / 2, ball_width, ball_height)
ball_direction_x = -1
ball_direction_y = -1

clock = pygame.time.Clock()
running = True

mixer.init()
collision_sound = mixer.Sound("collision_sound.mp3")

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    keys = pygame.key.get_pressed()

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

    if ball.y <= 0 or ball.y >= screen_height - ball_height:
        ball_direction_y *= -1

    if ball.x <= 0:
        ball_direction_x *= -1
        player2_score += 1
    if ball.x >= screen_width - ball_width:
        ball_direction_x *= -1
        player1_score += 1

    if ball.colliderect(player1) or ball.colliderect(player2):
        ball_direction_x *= -1
        collision_sound.play()

    screen.fill(black)
    pygame.draw.rect(screen, white, player1)
    pygame.draw.rect(screen, white, player2)
    pygame.draw.rect(screen, white, ball)

    player1_text = font.render(str(player1_score), True, white)
    player2_text = font.render(str(player2_score), True, white)
    screen.blit(player1_text, (screen_width / 2 - 50, 10))
    screen.blit(player2_text, (screen_width / 2 + 30, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
