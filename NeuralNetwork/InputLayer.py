"""
==================================================================
                        Input layer
-----------------------------------------------------------------
The following is a class representing the input layer of the
neural network. It takes the amount of dimensions of the layer
as parameter.
==================================================================
"""


import numpy as np

class InputLayer:
    def __init__(self, dimensions):
        self.dimensions = dimensions # Amount of dimensions of the layer
        self.a = np.zeros((dimensions, 1)) # Values of the nodes
        
    def feedforward(self, x):
        self.a = x