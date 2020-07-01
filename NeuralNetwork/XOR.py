"""
================================================================================
                        EXAMPLE ON USING THE NEURAL NETWORK
--------------------------------------------------------------------------------

The following is an exmple on how to use the neural network library in
NeuralNetwor.py.
In the following example, the neural network is being trained and tested on the 
XOR-problem
================================================================================
"""

import numpy as np
from NeuralNetwork import NeuralNetwork
import random

# Creating model
model = NeuralNetwork(2) # Creates an input layer with 2 input nodes
model.add_layer(2, activation = "sigmoid") # Creates a hidden layer with 2 input nodes
model.add_layer(1, activation = "sigmoid") # Creates an output layer with 1 output node

# Constants
N_EPOCHS = 100
N_SAMPLES = 1000
LEARNING_RATE = 0.1

# Generating data
X = np.array([[0, 0]]).reshape((1, -1))
y = np.array([[0]]).reshape((1, -1))

for i in range(N_SAMPLES - 1):
    rnd = random.randint(0, 3)
    if (rnd == 0):
        X = np.concatenate((X, [[0, 0]]), axis = 0)
        y = np.concatenate((y, [[0]]), axis = 0)
    elif (rnd == 1):
        X = np.concatenate((X, [[1, 0]]), axis = 0)
        y = np.concatenate((y, [[1]]), axis = 0)
    elif (rnd == 2):
        X = np.concatenate((X, [[0, 1]]), axis = 0)
        y = np.concatenate((y, [[1]]), axis = 0)
    elif (rnd == 3):
        X = np.concatenate((X, [[1, 1]]), axis = 0)
        y = np.concatenate((y, [[0]]), axis = 0)

# Training
model.fit(X, y, N_EPOCHS, learning_rate = LEARNING_RATE)

# Predictions
print(model.predict([0, 0])) # Should be 0
print(model.predict([1, 1])) # Should be 0
print(model.predict([1, 0])) # Should be 1
print(model.predict([0, 1])) # Should be 1
