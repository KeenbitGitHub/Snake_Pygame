"""
====================================================================
                        Hidden Layer
--------------------------------------------------------------------
The following is a class representing a hidden layer and the output
layer of the neural network, as well as the input weights of the 
layer. The class takes the amount of dimensions of the layer and the
amount of dimensions of the input layer as parameters.
====================================================================
"""

import numpy as np

class HiddenLayer:
    def __init__(self, dimensions, dim_from, activation):
        self.dimensions = dimensions # Amount of dimensions of the layer
        self.a = np.zeros((dimensions, 1)) # Values of the nodes
        self.b = np.random.normal(0, 1, (dimensions, 1)) # Bias of each node
        self.grad = np.zeros((dimensions, 1)) # Used for gradient descent
        self.weights = np.random.normal(0, 1, (dimensions, dim_from)) # Input weights
        self.activation = activation # Activation function of the layer
        
    # Sigmoid activation function
    def sigmoid(self, input_a, i):
        return 1/(1 + np.exp(-1 * (np.matmul(self.weights[i], input_a) + self.b[i])))
    
    # ReLu activation function
    def relu(self, input_a, i):
        res = np.matmul(self.weights[i], input_a) + self.b[i]
        return max(res, 0)
    
    # Feeds forward the layer
    def feedforward(self, input_a):
        if (self.activation == "sigmoid"):
            for i in range(self.dimensions):
                self.a[i] = self.sigmoid(input_a, i)
                
        elif (self.activation == "relu"):
            for i in range(self.dimensions):
                self.a[i] = self.relu(input_a, i)
                
        else:
            raise Exception("Unknown activation function: " + self.activation)