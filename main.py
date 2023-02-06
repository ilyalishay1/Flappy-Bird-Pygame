import pygame as pg
import sys
from random import randint
from time import sleep


pg.init()

COVER = pg.image.load('FlappyBirdCover.jpg.webp')
BACKGROUND = pg.image.load('flappy-background.png')
FLAPPY_BIRD_IMAGE = pg.image.load('FlappyBirdImage.jpeg')
BOTTOM_PIPE_IMAGE = pg.image.load('BottomPipe.jpeg')
TOP_PIPE_IMAGE = pg.image.load('TopPipe.jpeg')

WHITE = (255, 255, 255)
SPRING_GREEN = (0, 255, 127)
RED = (255, 0, 0)
WINDOW_HEIGHT = 500
WINDOW_WIDTH = 1000
FLAPPY_BIRD_IMAGE.set_colorkey((255, 255, 255))

score = 0
end_game_font = pg.font.SysFont('Arial', 98, True)
render_end_game = end_game_font.render('GAME OVER', True, RED)
score_font = pg.font.SysFont('Arial', 28, True)
speed = 3
fps = 60
clock = pg.time.Clock()
y_pos_bird = WINDOW_HEIGHT // 2
pipes = []
pipes_scores = []
pipe_pos = WINDOW_HEIGHT // 2
pipe_size = 200

window = pg.display.set_caption('Flappy Bird')
window = pg.display.set_icon(COVER)
window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


while True:
    clock.tick(fps)
    # window.fill(WHITE)
    window.blit(BACKGROUND, (0, 0))
    y_pos_bird += 2

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                y_pos_bird -= 75

    speed = 3 + score // 100

    for i in range(len(pipes) - 1, -1, -1):
        pipe = pipes[i]
        pipe.x -= speed

        if pipe.right < 0:
            pipes.remove(pipe)

    if len(pipes) == 0 or pipes[len(pipes) - 1].x < WINDOW_WIDTH - 200:
        pipes.append(pg.Rect((WINDOW_WIDTH, 0, 50, pipe_pos - pipe_size // 2)))
        pipes.append(pg.Rect((WINDOW_WIDTH, pipe_pos + pipe_size // 2, 50, WINDOW_HEIGHT - pipe_pos + pipe_size // 2)))

        pipe_pos += randint(-100, 100)
        if pipe_pos < pipe_size:
            pipe_pos = pipe_size

        elif pipe_pos > WINDOW_HEIGHT - pipe_size:
            pipe_pos = WINDOW_HEIGHT - pipe_size

    for pipe in pipes:
        pg.draw.rect(window, SPRING_GREEN, pipe)
        if pipe.y == 0:
            rect = BOTTOM_PIPE_IMAGE.get_rect(bottomleft=pipe.bottomleft)
            window.blit(BOTTOM_PIPE_IMAGE, rect)
        else:
            rect = TOP_PIPE_IMAGE.get_rect(topleft=pipe.topleft)
            window.blit(TOP_PIPE_IMAGE, rect)

    flappy_bird_player = pg.draw.rect(window, WHITE, (50, y_pos_bird, 44, 30))
    window.blit(FLAPPY_BIRD_IMAGE, flappy_bird_player)

    for pipe in pipes:
        if flappy_bird_player.colliderect(pipe):
            window.blit(render_end_game, (200, 200))
            sleep(3)
            pg.quit()
            sys.exit()

        if pipe.right < flappy_bird_player.left and pipe not in pipes_scores:
            pipes_scores.append(pipe)
            score += 5

    if y_pos_bird > 500 or y_pos_bird < 0:
        window.blit(render_end_game, (200, 200))
        sleep(3)
        pg.quit()
        sys.exit()

    render_score = score_font.render(f'Score: {score}', True, WHITE)
    window.blit(render_score, (50, 10))
    pg.display.update()
