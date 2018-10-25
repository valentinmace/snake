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
        self.food = [random.randint(8, 12), random.randint(8, 12)]

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

    # def scan(self):
    #
    #     def scan_obstacle(direction_x, direction_y, direction_range):
    #         res = 0
    #         for i in range(1, 10):
    #             step_x = head_x + i * direction_x
    #             step_y = head_y + i * direction_y
    #
    #             if i < direction_range:
    #                 if structure[step_y][step_x] == WALL:
    #                     res = max(res, 1 / distance((head_x, head_y), (step_x, step_y)))
    #                 elif [step_x, step_y] in snake_body:
    #                     res = max(res, 1 / distance((head_x, head_y), (step_x, step_y)))
    #         return res
    #
    #     def scan_food(direction_x, direction_y, direction_range):
    #         res = 0
    #         for i in range(1, direction_range):
    #             if food_x == (head_x + i * direction_x) and food_y == (head_y + i * direction_y):
    #                 res = 1
    #         return res
    #
    #     scan = [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]]
    #     structure = self.structure
    #     snake_body = self.snake.body
    #     head_x = self.snake.head[0]
    #     head_y = self.snake.head[1]
    #     food_x = self.food[0]
    #     food_y = self.food[1]
    #
    #     forward_x = self.snake.direction[0]
    #     forward_y = self.snake.direction[1]
    #     right_x = -forward_y
    #     right_y = forward_x
    #     left_x = forward_y
    #     left_y = -forward_x
    #     forward_right_x = forward_x + right_x
    #     forward_right_y = forward_y + right_y
    #     forward_left_x = forward_x + left_x
    #     forward_left_y = forward_y + left_y
    #     backward_right_x = -forward_left_x
    #     backward_right_y = -forward_left_y
    #     backward_left_x = -forward_right_x
    #     backward_left_y = -forward_right_y
    #
    #     forward_range = (20 - (forward_x * head_x + forward_y * head_y) - 1) % 19 + 1
    #     backward_range = 21 - forward_range
    #     right_range = (20 - (right_x * head_x + right_y * head_y) - 1) % 19 + 1
    #     left_range = 21 - right_range
    #
    #     scan[0][0] = scan_obstacle(forward_x, forward_y, forward_range)
    #     scan[1][0] = scan_obstacle(right_x, right_y, right_range)
    #     scan[2][0] = scan_obstacle(left_x, left_y, left_range)
    #     scan[3][0] = scan_obstacle(forward_right_x, forward_right_y, min(forward_range, right_range))
    #     scan[4][0] = scan_obstacle(forward_left_x, forward_left_y, min(forward_range, left_range))
    #     scan[5][0] = scan_obstacle(backward_right_x, backward_right_y, min(backward_range, right_range))
    #     scan[6][0] = scan_obstacle(backward_left_x, backward_left_y, min(backward_range, left_range))
    #
    #     scan[7][0] = scan_food(forward_x, forward_y, forward_range)
    #     scan[8][0] = scan_food(right_x, right_y, right_range)
    #     scan[9][0] = scan_food(left_x, left_y, left_range)
    #     scan[10][0] = scan_food(forward_right_x, forward_right_y, min(forward_range, right_range))
    #     scan[11][0] = scan_food(forward_left_x, forward_left_y, min(forward_range, left_range))
    #     scan[12][0] = scan_food(backward_right_x, backward_right_y, min(backward_range, right_range))
    #     scan[13][0] = scan_food(backward_left_x, backward_left_y, min(backward_range, left_range))
    #     self.snake.vision = scan

    def render(self, window):
        background = pygame.image.load(IMAGE_BACKGROUND).convert()
        wall = pygame.image.load(IMAGE_WALL).convert()
        food = pygame.image.load(IMAGE_FOOD).convert_alpha()

        # window.blit(background, (0, 0))
        window.fill([0,0,0])
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



    def scan(self):

        def scan_obstacle(direction_x, direction_y, direction_range):
            res = 0
            for i in range(1, 10):
                step_x = head_x + i * direction_x
                step_y = head_y + i * direction_y

                if i < direction_range:
                    if structure[step_y][step_x] == WALL:
                        res = 1 / distance((head_x, head_y), (step_x, step_y))
            return res

        def scan_self(direction_x, direction_y, direction_range):
            res = 0
            for i in range(1, 10):
                step_x = head_x + i * direction_x
                step_y = head_y + i * direction_y

                if i < direction_range:
                    if [step_x, step_y] in snake_body:
                        res = max(res, 1 / distance((head_x, head_y), (step_x, step_y)))
            return res

        def scan_food(direction_x, direction_y, direction_range):
            res = 0
            for i in range(1, direction_range):
                if food_x == (head_x + i * direction_x) and food_y == (head_y + i * direction_y):
                    res = 1
            return res

        scan = [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]]
        structure = self.structure
        snake_body = self.snake.body
        head_x = self.snake.head[0]
        head_y = self.snake.head[1]
        food_x = self.food[0]
        food_y = self.food[1]

        forward_x = self.snake.direction[0]
        forward_y = self.snake.direction[1]
        right_x = -forward_y
        right_y = forward_x
        left_x = forward_y
        left_y = -forward_x
        forward_right_x = forward_x + right_x
        forward_right_y = forward_y + right_y
        forward_left_x = forward_x + left_x
        forward_left_y = forward_y + left_y
        backward_right_x = -forward_left_x
        backward_right_y = -forward_left_y
        backward_left_x = -forward_right_x
        backward_left_y = -forward_right_y

        forward_range = (20 - (forward_x * head_x + forward_y * head_y) - 1) % 19 + 1
        backward_range = 21 - forward_range
        right_range = (20 - (right_x * head_x + right_y * head_y) - 1) % 19 + 1
        left_range = 21 - right_range
        forward_right_range = min(forward_range, right_range)
        forward_left_range = min(forward_range, left_range)
        backward_right_range = min(backward_range, right_range)
        backward_left_range = min(backward_range, left_range)

        scan[0][0] = scan_obstacle(forward_x, forward_y, forward_range)
        scan[1][0] = scan_obstacle(right_x, right_y, right_range)
        scan[2][0] = scan_obstacle(left_x, left_y, left_range)
        scan[3][0] = scan_obstacle(forward_right_x, forward_right_y, forward_right_range)
        scan[4][0] = scan_obstacle(forward_left_x, forward_left_y, forward_left_range)
        scan[5][0] = scan_obstacle(backward_right_x, backward_right_y, backward_right_range)
        scan[6][0] = scan_obstacle(backward_left_x, backward_left_y, backward_left_range)

        scan[7][0] = scan_food(forward_x, forward_y, forward_range)
        scan[8][0] = scan_food(right_x, right_y, right_range)
        scan[9][0] = scan_food(left_x, left_y, left_range)
        scan[10][0] = scan_food(forward_right_x, forward_right_y, forward_right_range)
        scan[11][0] = scan_food(forward_left_x, forward_left_y, forward_left_range)
        scan[12][0] = scan_food(backward_right_x, backward_right_y, backward_right_range)
        scan[13][0] = scan_food(backward_left_x, backward_left_y, backward_left_range)

        scan[14][0] = scan_self(forward_x, forward_y, forward_range)
        scan[15][0] = scan_self(right_x, right_y, right_range)
        scan[16][0] = scan_self(left_x, left_y, left_range)
        scan[17][0] = scan_self(forward_right_x, forward_right_y, forward_right_range)
        scan[18][0] = scan_self(forward_left_x, forward_left_y, forward_left_range)
        scan[19][0] = scan_self(backward_right_x, backward_right_y, backward_right_range)
        scan[20][0] = scan_self(backward_left_x, backward_left_y, backward_left_range)
        # return scan[14:21]
        self.snake.vision = scan



@jit(nopython=True)
def distance(p1=None, p2=None):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


