import pygame
from constantes import *
from map import *
from pygame.locals import *
from snake import *


class Game:
    """Game class"""

    def __init__(self):
        self.game_score = 0
        self.game_time = 0

    def start_invisible(self):
        snake = Snake()
        map = Map(snake)
        cont = True
        while cont:
            self.game_time += 1
            snake.AI()
            snake.update()
            map.update()
            if snake.alive == False:
                cont = False
                self.game_time = 0

    def start_visible(self, playable=False):
        pygame.init()
        gameWindow = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))  # Opening game window
        pygame.display.set_caption(WINDOW_TITLE)                          # Title
        snake = Snake()
        map = Map(snake)
        update = 0
        cont = True
        while cont:
            pygame.time.Clock().tick(30)
            self.render(gameWindow, map)
            for event in pygame.event.get():
                if event.type == QUIT:
                    cont = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        cont = False
                    if event.key == K_RIGHT:
                        snake.direction = RIGHT
                        snake.update()
                        map.update()
                    elif event.key == K_LEFT:
                        snake.direction = LEFT
                        snake.update()
                        map.update()
                    elif event.key == K_UP:
                        snake.direction = UP
                        snake.update()
                        map.update()
                    elif event.key == K_DOWN:
                        snake.direction = DOWN
                        snake.update()
                        map.update()

            # update += 1
            # if update > 0:
            #     update = 0
            #     if not playable:
            #         self.map.snake.AI()
            #     self.map.snake.update()
            #     self.map.update()
            if not snake.alive:
                cont = False

    def render(self, window, map):
        map.render(window)
        pygame.display.flip()