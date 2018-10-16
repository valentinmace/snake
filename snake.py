import pygame
from constantes import *
from neural_network import *


class Snake:
    """Snake class"""

    def __init__(self, neural_net=None):
        self.body = [[15, 15]]
        self.head = self.body[0][:]
        self.old_tail = self.head[:]
        self.direction = RIGHT
        self.age = 0
        self.alive = True
        self.neural_net = neural_net
        self.vision = []

    def update(self):
        self.age += 1
        self.move()

    def grow(self):
        self.body.append(self.old_tail)

    def move(self):
        self.old_tail = self.body[-1][:]
        self.head[0] += self.direction[0]
        self.head[1] += self.direction[1]
        if self.head in self.body[1:]:
            self.alive = False
        self.body.insert(0, self.body.pop())
        self.body[0] = self.head[:]

    def AI(self):
        decision = DIRECTIONS[np.argmax(self.neural_net.feed_forward(self.vision))]
        # if self.direction[0] != decision[0] and self.direction[1] != decision[1]:
        #     self.direction = decision

    def fitness(self):
      return (len(self.body)**2) * self.age**2

    def render(self, window):
        body = pygame.image.load(IMAGE_SNAKE).convert_alpha()
        for block in self.body:
            window.blit(body, (block[0]*SPRITE_SIZE, block[1]*SPRITE_SIZE))
