"""Main file"""

# import math
# import random
import numpy as np
#import pygame
# from pygame.locals import *
# from constantes import *
# from block import *
# from network import *
from genetic_algorithm import *
import cProfile
from snake import *
from game import*
import time

# map = Map()
# map.generate()
# print(map.structure)
# print(np.where(map.structure==FOOD))

# game = Game()
# game.start_visible(playable=True)
# cProfile.run('game.start_invisible()')

net = Network(shape=[16,16,4])
t1 = time.time()
game = Game()
for i in range(10000):
    game.start_invisible(neural_net=net)
t2 = time.time()
print("temps", t2 - t1)

# total = []
# t2 = 0
# for i in range(1):
#   t1 = time.time()
#   gen = Genetic(networks_number=8000, crossover_method='neuron', mutation_method='weight')
#   gen.start()
#   t2 = time.time()
#   total.append(t2 - t1)
#   print(i)
#
# print(total)
# print(np.mean(total))
