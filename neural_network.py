from numba import jit
import numpy as np


class Network:
    """Neural Network class"""

    def __init__(self, shape=[14,16,3]):
        self.num_layers = len(shape)
        self.shape = shape
        self.biases = []
        self.weights = []
        self.score = 0

        for y in shape[1:]:
          self.biases.append(np.random.randn(y, 1))

        for x, y in zip(shape[:-1], shape[1:]):
          self.weights.append(np.random.randn(y, x))

    def feed_forward(self, a):
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a)+b)
        return a

    def save(self):
        np.save('saved_weights_'+str(self.score), self.weights)
        np.save('saved_biases_'+str(self.score), self.biases)

    def load(self, filename_weights, filename_biases):
        self.weights = np.load(filename_weights)
        self.biases = np.load(filename_biases)

@jit(nopython=True)
def sigmoid(z):
    """The sigmoid function."""
    return 1.0 / (1.0 + np.exp(-z))
