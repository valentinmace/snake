import math
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
        self.food = [random.randint(13, 17), random.randint(13, 17)]

    def update(self):
        snake_head_x, snake_head_y = self.snake.head
        snake_pos = self.structure[snake_head_y][snake_head_x]
        if [snake_head_x, snake_head_y] == self.food:
            self.snake.grow()
            self.add_food(random.randint(1, SPRITE_NUMBER - 2),
                          random.randint(1, SPRITE_NUMBER - 2))
        elif snake_pos == WALL:
            self.snake.alive = False

    def add_food(self, block_x, block_y):
        self.food = [block_x, block_y]

    def scan(self):
        scan = [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]]
        snake_body = self.snake.body
        snake_direction = self.snake.direction
        food_x = self.food[0]
        food_y = self.food[1]
        structure = self.structure
        head_x = self.snake.head[0]
        head_y = self.snake.head[1]
        up_range = head_y + 1
        down_range = 30 - head_y
        left_range = head_x + 1
        right_range = 30 - head_x

        for i in range(1, 8):

            if i < up_range:                                                                # Scanning UP
                if structure[head_y - i][head_x] == WALL:
                    scan[0][0] = 1/distance((head_x, head_y), (head_x, head_y - i))
                elif [head_x, head_y - i] in snake_body:
                    scan[16][0] = max(scan[16][0], 1/distance((head_x, head_y), (head_x, head_y - i)))
                if i < left_range:                                                          # Scanning UP-LEFT
                    if structure[head_y - i][head_x - i] == WALL:
                        scan[4][0] = 1/distance((head_x, head_y), (head_x - i, head_y - i))
                    elif [head_x - i, head_y - i] in snake_body:
                        scan[20][0] = max(scan[20][0], 1/distance((head_x, head_y), (head_x - i, head_y - i)))

            if i < down_range:                                                              # Scanning DOWN
                if structure[head_y + i][head_x] == WALL:
                    scan[1][0] = 1/distance((head_x, head_y), (head_x, head_y + i))
                elif [head_x, head_y + i] in snake_body:
                    scan[17][0] = max(scan[17][0], 1/distance((head_x, head_y), (head_x, head_y - i)))
                if i < right_range:                                                         # Scanning DOWN-RIGHT
                    if structure[head_y + i][head_x + i] == WALL:
                        scan[5][0] = 1/distance((head_x, head_y), (head_x + i, head_y + i))
                    elif [head_x + i, head_y + i] in snake_body:
                        scan[21][0] = max(scan[21][0], 1/distance((head_x, head_y), (head_x + i, head_y + i)))

            if i < left_range:                                                              # Scanning LEFT
                if structure[head_y][head_x - i] == WALL:
                    scan[2][0] = 1/distance((head_x, head_y), (head_x - i, head_y))
                elif [head_x - i, head_y] in snake_body:
                    scan[18][0] = max(scan[18][0], 1/distance((head_x, head_y), (head_x - i, head_y)))
                if i < down_range:                                                          # Scanning DOWN-LEFT
                    if structure[head_y + i][head_x - i] == WALL:
                        scan[6][0] = 1/distance((head_x, head_y), (head_x - i, head_y + i))
                    elif [head_x - i, head_y + i] in snake_body:
                        scan[22][0] = max(scan[22][0], 1/distance((head_x, head_y), (head_x - i, head_y + i)))

            if i < right_range:                                                             # Scanning RIGHT
                if structure[head_y][head_x + i] == WALL:
                    scan[3][0] = 1/distance((head_x, head_y), (head_x + i, head_y))
                elif [head_x + i, head_y] in snake_body:
                    scan[19][0] = max(scan[19][0], 1/distance((head_x, head_y), (head_x + i, head_y)))
                if i < up_range:                                                            # Scanning UP-RIGHT
                    if structure[head_y - i][head_x + i] == WALL:
                        scan[7][0] = 1/distance((head_x, head_y), (head_x + i, head_y - i))
                    elif [head_x + i, head_y - i] in snake_body:
                        scan[23][0] = max(scan[23][0], 1/distance((head_x, head_y), (head_x + i, head_y - i)))

        for i in range(1, up_range):
            if food_x == head_x and food_y == (head_y - i):
                scan[8][0] = 1
            if i < left_range:
                if food_x == (head_x - i) and food_y == (head_y - i):
                    scan[12][0] = 1

        for i in range(1, down_range):
            if food_x == head_x and food_y == (head_y + i):
                scan[9][0] = 1
            if i < right_range:
                if food_x == (head_x + i) and food_y == (head_y + i):
                    scan[13][0] = 1

        for i in range(1, left_range):
            if food_x == head_x - i and food_y == head_y:
                scan[10][0] = 1
            if i < down_range:
                if food_x == (head_x - i) and food_y == (head_y + i):
                    scan[14][0] = 1

        for i in range(1, right_range):
            if food_x == head_x + i and food_y == head_y:
                scan[11][0] = 1
            if i < up_range:
                if food_x == (head_x + i) and food_y == (head_y - i):
                    scan[15][0] = 1

        if snake_direction == UP:
            scan[17][0] = 0
        elif snake_direction == DOWN:
            scan[16][0] = 0
        elif snake_direction == LEFT:
            scan[19][0] = 0
        elif snake_direction == RIGHT:
            scan[18][0] = 0
        self.snake.vision = scan

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
                if self.food == [num_case, num_line]:
                    window.blit(food, (x, y))
                num_case += 1
            num_line += 1
        self.snake.render(window)

@jit(nopython=True)
def distance(p1=None, p2=None):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
