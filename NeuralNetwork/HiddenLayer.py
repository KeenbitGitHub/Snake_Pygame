import numpy as np

""" Class for a hidden layer and the output layer """
class HiddenLayer:
    def __init__(self, dimensions, dim_from):
        self.dimensions = dimensions
        self.a = np.zeros((dimensions, 1))
        self.b = np.random.uniform(size = (dimensions, 1))
        self.grad = np.zeros((dimensions, 1))
        self.weights = np.random.uniform(low = -1.0, high = 1.0, size = (dimensions, dim_from))
        
    def feedforward(self, input_weights, input_a):
        for i in range(self.dimensions):
            self.a[i] = 1/(1 + np.exp(-1 * (np.matmul(input_weights[i], input_a) + self.b[i])))