# Valentin Macé
# valentin.mace@kedgebs.com
# Developed for fun
# Feel free to use this code as you wish as long as you quote me as author

"""
map.py
~~~~~~~~~~

This module is for building map for the snake game

The map:
- Contains its structure in a matrix form (see MAP in constants.py)
- Contains a instance of a snake and an instance of a food
- Is in charge of managing collisions, creation of food and giving vision to the snake

Notes:
- Some choices might seems weird in term of conception but I built it with priority for performance
      since the GA is greedy
"""

import math
import random
from snake import *


class Map:
    """Map class"""

    def __init__(self, snake):
        self.structure = MAP                                            # matrix of 0 and 1 representing the map
        self.snake = snake                                              # snake evolving in the map
        self.food = [random.randint(8, 12), random.randint(8, 12)]      # food (list of 2 coordinates)

    def update(self):
        """
        Checks for collision between snake's head and walls or food
        Takes the right action in case of collision
        """
        snake_head_x, snake_head_y = self.snake.head
        snake_pos = self.structure[snake_head_y][snake_head_x]
        if [snake_head_x, snake_head_y] == self.food:                   # if snake's head is on food
            self.snake.grow()                                           # snake grows and new food is created
            self.add_food(random.randint(1, SPRITE_NUMBER - 2),
                          random.randint(1, SPRITE_NUMBER - 2))
        elif snake_pos == WALL:                                         # if snake's head is on wall, snek is ded
            self.snake.alive = False

    def add_food(self, block_x, block_y):
        """
        Adds food on (block_x, block_y) position
        """
        self.food = [block_x, block_y]

    def render(self, window):
        """
        Renders the map (background, walls and food) on the game window and calls render() of snake
        Very very very unoptimized since render does not affect the genetic algorithm

        :param window: surface window
        """
        wall = pygame.image.load(IMAGE_WALL).convert()          # loading images
        food = pygame.image.load(IMAGE_FOOD).convert_alpha()

        window.fill([0,0,0])                # painting background
        num_line = 0
        for line in self.structure:         # running through the map structure
            num_case = 0
            for sprite in line:
                x = num_case * SPRITE_SIZE
                y = num_line * SPRITE_SIZE
                if sprite == 1:                         # displaying wall
                    window.blit(wall, (x, y))
                if self.food == [num_case, num_line]:   # displaying food
                    window.blit(food, (x, y))
                num_case += 1
            num_line += 1
        self.snake.render(window)         # snake will be rendered on above the map



    def scan(self):
        """
        Scans the snake's environment into the 'scan' variable (list of lists) and gives it to snake's vision

        Notes:
        - 7 first inputs are for walls, 7 next for food, 7 last for itself (its body)
        - Food is seen across all the map, walls and body are seen in range of 10 blocks max
        - This method is long and I do not factorise much for performance issues,
          the structure is easily understandable anyway

        :return: nothing but gives vision to the snake
        """
        def scan_wall(direction_x, direction_y, direction_range):
            """
            Looks for a wall in the direction given in parameters for 10 steps max

            I decided to use inner methods for a compromise between performance and factorisation

            :param direction_x: direction in x axis, can be 1, 0 or -1 for "right", "stay" and "left" respectively
            :param direction_y: direction in y axis, can be 1, 0 or -1 for "down", "stay" and "up" respectively
            :param direction_range: maximum range to scan
            :return: number with 0 value if nothing or 1/distance to wall if wall's detected
            """
            res = 0
            for i in range(1, 10):                      # looking up to 10 blocks max
                step_x = head_x + i * direction_x       # coordinates of next block to check
                step_y = head_y + i * direction_y

                if i < direction_range:
                    if structure[step_y][step_x] == WALL:                       # if wall is detected in current block
                        res = 1 / distance((head_x, head_y), (step_x, step_y))  # returns 1/distance to the block
            return res

        def scan_self(direction_x, direction_y, direction_range):
            """
            Looks for a snake's body block in the direction given in parameters for 10 steps max

            :params see "scan_wall", same params
            :return: number with 0 value if nothing or 1/distance to body if a body block is detected
            """
            res = 0
            for i in range(1, 10):
                step_x = head_x + i * direction_x
                step_y = head_y + i * direction_y

                if i < direction_range:
                    if [step_x, step_y] in snake_body:
                        res = max(res, 1 / distance((head_x, head_y), (step_x, step_y)))
            return res

        def scan_food(direction_x, direction_y, direction_range):
            """
            Looks for food in the direction given in parameters until range is reached

            :params see "scan_wall", same params
            :return: number with 0 value if nothing or 1/distance to body if a body block is detected
            """
            res = 0
            for i in range(1, direction_range):
                if food_x == (head_x + i * direction_x) and food_y == (head_y + i * direction_y):
                    res = 1
            return res

        scan = [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]]    # default value
        structure = self.structure
        snake_body = self.snake.body                # making local variables for readability and performance
        head_x = self.snake.head[0]
        head_y = self.snake.head[1]
        food_x = self.food[0]
        food_y = self.food[1]

        forward_x = self.snake.direction[0]         # calculating each coordinate for each 7 directions
        forward_y = self.snake.direction[1]         # since the snake sees in FIRST PERSON
        right_x = -forward_y
        right_y = forward_x
        left_x = forward_y                          # for example, if snake's looking in [1,0] direction (down)
        left_y = -forward_x                         # its left is [1,0] (right for us because we look from above)
        forward_right_x = forward_x + right_x
        forward_right_y = forward_y + right_y
        forward_left_x = forward_x + left_x
        forward_left_y = forward_y + left_y         # see snake.py class for better explanations
        backward_right_x = -forward_left_x
        backward_right_y = -forward_left_y
        backward_left_x = -forward_right_x
        backward_left_y = -forward_right_y

        forward_range = (20 - (forward_x * head_x + forward_y * head_y) - 1) % 19 + 1   # computing max range
        backward_range = 21 - forward_range                                             # for each direction
        right_range = (20 - (right_x * head_x + right_y * head_y) - 1) % 19 + 1
        left_range = 21 - right_range
        forward_right_range = min(forward_range, right_range)           # values are hard encoded
        forward_left_range = min(forward_range, left_range)             # since I'm not planning on making it modifiable
        backward_right_range = min(backward_range, right_range)
        backward_left_range = min(backward_range, left_range)

        scan[0][0] = scan_wall(forward_x, forward_y, forward_range)                 # scanning walls in all directions
        scan[1][0] = scan_wall(right_x, right_y, right_range)
        scan[2][0] = scan_wall(left_x, left_y, left_range)
        scan[3][0] = scan_wall(forward_right_x, forward_right_y, forward_right_range)
        scan[4][0] = scan_wall(forward_left_x, forward_left_y, forward_left_range)
        scan[5][0] = scan_wall(backward_right_x, backward_right_y, backward_right_range)
        scan[6][0] = scan_wall(backward_left_x, backward_left_y, backward_left_range)

        scan[7][0] = scan_food(forward_x, forward_y, forward_range)                 # scanning food in all directions
        scan[8][0] = scan_food(right_x, right_y, right_range)
        scan[9][0] = scan_food(left_x, left_y, left_range)
        scan[10][0] = scan_food(forward_right_x, forward_right_y, forward_right_range)
        scan[11][0] = scan_food(forward_left_x, forward_left_y, forward_left_range)
        scan[12][0] = scan_food(backward_right_x, backward_right_y, backward_right_range)
        scan[13][0] = scan_food(backward_left_x, backward_left_y, backward_left_range)

        scan[14][0] = scan_self(forward_x, forward_y, forward_range)                # scanning body in all directions
        scan[15][0] = scan_self(right_x, right_y, right_range)
        scan[16][0] = scan_self(left_x, left_y, left_range)
        scan[17][0] = scan_self(forward_right_x, forward_right_y, forward_right_range)
        scan[18][0] = scan_self(forward_left_x, forward_left_y, forward_left_range)
        scan[19][0] = scan_self(backward_right_x, backward_right_y, backward_right_range)
        scan[20][0] = scan_self(backward_left_x, backward_left_y, backward_left_range)

        self.snake.vision = scan    # gives snake vision


@jit(nopython=True)
def distance(p1=None, p2=None):
    """
    Gives euclidian distance between two points
    @jit is used to speed up computation

    :param p1: origin point
    :param p2: end point
    :return: distance
    """
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


