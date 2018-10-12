"""Main file"""

# import math
# import random
import numpy as np
#import pygame
# from pygame.locals import *
# from constantes import *
# from block import *
# from network import *
import cProfile
from snake import *
from game import*
# map = Map()
# map.generate()
# print(map.structure)
# print(np.where(map.structure==FOOD))

game = Game()
game.start_visible()
# cProfile.run('game.start_invisible()')


# t1 = time.time()
# game = Game()
# for i in range(10000):
#     game.start_invisible()
# t2 = time.time()
# print("temps", t2 - t1)



# a = [[0 for i in range(30)] for j in range(30)]
# t1 = time.time()
# for i in range(1000000):
#     a[10][10] = 1
# t2 = time.time()
# print("temps", t2 - t1)
#
# b = np.zeros((30, 30), dtype=int)
# t1 = time.time()
# for i in range(1000000):
#     b[10,10] = 1
# t2 = time.time()
# print("temps", t2 - t1)
