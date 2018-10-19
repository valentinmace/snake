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

# net = Network(shape=[16,16,4])
# t1 = time.time()
# game = Game()
# for i in range(5000):
#     game.start_invisible(neural_net=net)
# t2 = time.time()
# print("temps", t2 - t1)

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
#
# gen = Genetic(networks_number=12000, crossover_method='neuron', mutation_method='weight')
# gen.start()

net = Network()
net.load(filename_weights='saved_weights_15855175.npy', filename_biases='saved_biases_15855175.npy')
game = Game()
# print(game.start_invisible(neural_net=net))
print(game.start_visible(neural_net=net))
print(game.start_visible(neural_net=net))
print(game.start_visible(neural_net=net))
print(game.start_visible(neural_net=net))
print(game.start_visible(neural_net=net))





# Modifier la manière du snake avec à sa gauche droite etc, changer la notion de distance (pour les diagonales), la
# queue en mur et enfin (plus tard) la food tu la scannes avec deux inputs (x-xpomme et y-ypomme)
