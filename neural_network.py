# Valentin Macé
# valentin.mace@kedgebs.com
# Developed for fun
# Feel free to use this code as you wish as long as you quote me as author

"""
neural_network.py
~~~~~~~~~~

This module is for building a classic dense neural network

Weights and biases are initialized randomly according to a normal distribution
A network can be saved and loaded for later use
The class is build for the snake project so:
- The rendering method is not very modular and is specifi for this project, I'll improve it later
- No backpropagation since we don't need it for the genetic algorithm
"""

from numba import jit
import numpy as np
import pygame
from constants import *
from pygame import gfxdraw


class NeuralNetwork:
    """Neural Network class"""

    def __init__(self, shape=None):
        """
        :param shape: list of int, describes how many layers and neurons by layer the network has
        """
        self.shape = shape
        self.biases = []
        self.weights = []
        self.score = 0        # to remember how well it performed
        if shape:
            for y in shape[1:]:                             # biases random initialization
                self.biases.append(np.random.randn(y, 1))
            for x, y in zip(shape[:-1], shape[1:]):         # weights random initialization
                self.weights.append(np.random.randn(y, x))

    def feed_forward(self, a):
        """
        Main function, takes an input vector and calculate the output by propagation through the network

        :param a: column of integers, inputs for the network (snake's vision)
        :return: column of integers, output neurons activation
        """
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a)+b)
        return a

    def save(self, name=None):
        """
        Saves network weights and biases into 2 separated files in current folder

        :param name: str, in case you want to name it
        :return: creates two files
        """
        if not name:
            np.save('saved_weights_'+str(self.score), self.weights)
            np.save('saved_biases_'+str(self.score), self.biases)
        else:
            np.save(name + '_weights', self.weights)
            np.save(name + '_biases', self.biases)

    def load(self, filename_weights, filename_biases):
        """
        Loads saved network weights and biases from 2 files into the actual network object

        :param filename_weights: file containing saved weights
        :param filename_biases: file containing saved biases
        """
        self.weights = np.load(filename_weights)
        self.biases = np.load(filename_biases)

    def render(self, window, vision):
        """
        Display the network at the current state in the right part of game window

        The function supports any network shape but is not very flexible
        I plan to work on it for later projects

        :param window: surface, game window
        :param vision: column of int, snake vision needed to show inputs
        """
        network = [np.array(vision)]            # will contain all neuron activation from each layer
        for i in range(len(self.biases)):
            activation = sigmoid(np.dot(self.weights[i], network[i]) + self.biases[i])  # compute neurons activations
            network.append(activation)                                                  # append it

        screen_division = WINDOW_SIZE / (len(network) * 2)     # compute distance between layers knowing window's size
        step = 1
        for i in range(len(network)):                                           # for each layer
            for j in range(len(network[i])):                                    # for each neuron in current layer
                y = int(WINDOW_SIZE/2 + (j*24) - (len(network[i])-1)/2 * 24)    # neuron position
                x = int(WINDOW_SIZE + screen_division * step)
                intensity = int(network[i][j][0] * 255)                         # neuron intensity

                if i < len(network)-1:
                    for k in range(len(network[i+1])):                                          # connections
                        y2 = int(WINDOW_SIZE/2 + (k * 24) - (len(network[i+1]) - 1) / 2 * 24)   # connections target position
                        x2 = int(WINDOW_SIZE + screen_division * (step+2))
                        pygame.gfxdraw.line(window, x, y, x2, y2,                               # draw connection
                                            (intensity/2+30, intensity/2+30, intensity/2+30, intensity/2+30))

                pygame.gfxdraw.filled_circle(window, x, y, 9, (intensity, intensity, intensity))    # draw neuron
                pygame.gfxdraw.aacircle(window, x, y, 9, (205, 205, 205))
            step += 2

@jit(nopython=True)
def sigmoid(z):
    """
    The sigmoid function, classic neural net activation function
    @jit is used to speed up computation
    """
    return 1.0 / (1.0 + np.exp(-z))
