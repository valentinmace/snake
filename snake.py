# Valentin Macé
# valentin.mace@kedgebs.com
# Developed for fun
# Feel free to use this code as you wish as long as you quote me as author

"""
snake.py
~~~~~~~~~~

This module is for building the snake itself in the snake game

The snake:
- Is on the form of a list, each element for a body block (containing its coordinates)
- Has a head pointing on the first block, a direction and also a neural network (brain)
- Has vision given by the map (Map.scan method)
- Is in charge of moving its blocks, aging, growing by adding a block to the right place
  and makes decision with neural net
- Gives its fitness based on self age and length

"""

from neural_network import *


class Snake:
    """Snake Class"""

    def __init__(self, neural_net=None):
        """
        :param neural_net: NeuralNet given to the snake in charge of decisions (AI)
        """
        self.body = [[10, 10], [9, 10], [9, 11], [9, 12]]       # the snake is in fact a list of coordinates
        self.head = self.body[0][:]                             # first body block
        self.old_tail = self.head[:]                            # useful to grow
        self.direction = RIGHT
        self.age = 0
        self.starve = 500                                       # useful to avoid looping AI snakes
        self.alive = True
        self.neural_net = neural_net
        self.vision = []                                        # holds the map.scan() and is used by the neural net

    def update(self):
        """
        Actualize the snake through time, making it older and more hungryat each game iteration,
        sorry snek
        """
        self.age += 1
        self.starve -= 1
        if self.starve < 1:
            self.alive = False
        self.move()

    def grow(self):
        """
        Makes snake grow one block longer
        Called by map.update() when snake's head is in collision with food
        """
        self.starve = 500                   # useful to avoid looping AI snakes (they die younger -> bad fitness)
        self.body.append(self.old_tail)     # that's why I keep old_tail

    def move(self):
        """
        Makes the snake move, head moves in current direction and each blocks replace its predecessor
        """
        self.old_tail = self.body[-1][:]        # save old position of last block
        self.head[0] += self.direction[0]       # moves head
        self.head[1] += self.direction[1]
        if self.head in self.body[1:]:          # if snakes hits himself
            self.alive = False
        self.body.insert(0, self.body.pop())    # each block is replace by predecessor
        self.body[0] = self.head[:]             # first block is head

    def turn_right(self):
        """
        Makes the snake direction to the right of the current direction
        Current direction = [x,y], turn_right gives [-y,x]

        Example:
        If [0,1] (down) is current direction, [-1,0] (right) is new direction
        """
        temp = self.direction[0]
        self.direction[0] = -self.direction[1]
        self.direction[1] = temp

    def turn_left(self):
        """
        Makes the snake direction to the right of the current direction
        Current direction = [x,y], turn_right gives [y,-x]
        """
        temp = self.direction[0]
        self.direction[0] = self.direction[1]
        self.direction[1] = -temp

    def AI(self):
        """
        Makes decision for the snake direction according to its current vision
        Vision is given to the NeuralNetwork and most activated output neuron is considered as decision
        """
        decision = np.argmax(self.neural_net.feed_forward(self.vision))
        if decision == 1:
            self.turn_right()
        elif decision == 2:
            self.turn_left()

    def fitness(self):
        """
        Measures how well the snake is doing as a function of its length and age

        Note:
        - You can be creative with the formula and find a better solution
        - It has a big impact on the genetic algorithm

        :return: integer representing how good the snake is performing
        """
        return (len(self.body)**2) * self.age

    def render(self, window):
        """
        Renders the map (background, walls and food) on the window surface and calls render() of snake
        Very very very unoptimized since render does not affect the genetic algorithm

        :param window: surface window
        """
        body = pygame.image.load(IMAGE_SNAKE).convert_alpha()                   # loading image
        for block in self.body:
            window.blit(body, (block[0]*SPRITE_SIZE, block[1]*SPRITE_SIZE))     # painting a beautiful snek
        if self.neural_net:                                                     # calls for neural net rendering
            self.neural_net.render(window, self.vision)
