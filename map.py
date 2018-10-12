import numpy as np
import pygame
import random
from constantes import *
from snake import *


class Map:
    """Map class"""

    def __init__(self, snake):
        self.structure = MAP
        self.snake = snake
        self.food = True
        self.add_food(random.randint(SPRITE_NUMBER/2-2, SPRITE_NUMBER/2+2),
                      random.randint(SPRITE_NUMBER/2-2, SPRITE_NUMBER/2+2))

    def update(self):
        snake_head_x, snake_head_y = self.snake.head
        if self.structure[snake_head_y][snake_head_x] == FOOD:
            self.snake.grow()
            self.structure[snake_head_y][snake_head_x] = NOTHING
            self.food = False
        elif self.structure[snake_head_y][snake_head_x] == WALL:
            self.snake.alive = False
        if not self.food:
            self.add_food(random.randint(1, SPRITE_NUMBER - 2),
                          random.randint(1, SPRITE_NUMBER - 2))

    def add_food(self, block_x, block_y):
        self.structure[block_x][block_y] = FOOD
        self.food = True

    def render(self, window):
        background = pygame.image.load(IMAGE_BACKGROUND).convert()
        wall = pygame.image.load(IMAGE_WALL).convert()
        food = pygame.image.load(IMAGE_FOOD).convert_alpha()

        window.blit(background, (0, 0))
        num_line = 0
        for line in self.structure:
            num_case = 0
            for sprite in line:
                x = num_case * SPRITE_SIZE
                y = num_line * SPRITE_SIZE
                if sprite == 1:
                    window.blit(wall, (x, y))
                if sprite == 3:
                    window.blit(food, (x, y))
                num_case += 1
            num_line += 1
        self.snake.render(window)