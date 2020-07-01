"""
================================================================================================================
                                NEURAL NETWORK IMPLEMENTATION FROM SCRATCH
----------------------------------------------------------------------------------------------------------------
The Following is an implementation of a fully connected neural network only using Python.
The network supports multiple layers, each with different dimensions. However, the only activationfunction
supported is the sigmoid function, and the only loss function suported is the mean squared error.
The class has been tested on the XOR-problem.
All the training data needs to be of 2D shape (both X and Y) - for prediction, the data should be of 1D shape.
================================================================================================================
"""

import numpy as np
from .HiddenLayer import HiddenLayer
from .InputLayer import InputLayer

class NeuralNetwork:
    def __init__(self, input_dimensions):
        self.n_layers = 1
        self.layers = np.array([InputLayer(input_dimensions)])
        
    # Method for adding a layer. The last added layer will be used as the output layer of the network.
    # Takes as argument the amount of dimensions of the layer.
    def add_layer(self, dimensions, activation = "sigmoid"):
        self.layers = np.append(self.layers, HiddenLayer(dimensions, self.layers[self.n_layers - 1].dimensions, activation))
        self.n_layers += 1
        
    # Derived sigmoid activation function
    def sigmoid_derived(self, x):
        return np.multiply(x, 1.0 - x)
    
    # Derived relu activation function
    def relu_derived(self, x):
        return 0 if x <= 0 else 1
    
    # Mean squared error
    @staticmethod
    def find_error(prediction, true_value):
        return np.mean(np.power(np.subtract(prediction, true_value), 2))
        
    # Fits the network.
    # Parameters:
    #   X: The input data
    #   Y: The targeted data
    #   n_epoch: The amount of epochs the network should fit for
    #   learning_rate: The learning rate.
    def fit(self, X, Y, n_epoch, learning_rate = 1.0):
        def update_weights(l, j, k):
            if (self.layers[l].activation == "sigmoid"):
                self.layers[l].weights[j, k] -= learning_rate * self.layers[l - 1].a[k] * self.sigmoid_derived(self.layers[l].a[j]) * self.layers[l].grad[j]
            elif (self.layers[l].activation == "relu"):
                self.layers[l].weights[j, k] -= learning_rate * self.layers[l - 1].a[k] * self.relu_derived(self.layers[l].a[j]) * self.layers[l].grad[j]
            
        def update_bias(l, j):
            if (self.layers[l].activation == "sigmoid"):
                self.layers[l].b[j] -= learning_rate * self.sigmoid_derived(self.layers[l].a[j]) * self.layers[l].grad[j]
            elif (self.layers[l].activation == "relu"):
                self.layers[l].b[j] -= learning_rate * self.relu_derived(self.layers[l].a[j]) * self.layers[l].grad[j]
        
        for epoch in range(n_epoch):
            for (index, x), y in zip(enumerate(X), Y):
                
                # Forwardpropagation
                self._forwardprop(x)
                
                # Backpropagation
                for l in reversed(range(1, self.n_layers)): # Iterates through each layer (except input layer)
                    for j in range(self.layers[l].dimensions): # Iterates through each node of layer l
                        if (l == self.n_layers - 1): # If layer l is the output layer
                            self.layers[l].grad[j] += 2 * (self.layers[l].a[j] - y[j])
                        else:
                            for _j in range(self.layers[l + 1].dimensions):
                                if (self.layers[l].activation == "sigmoid"):
                                    self.layers[l].grad[j] += self.layers[l + 1].weights[_j, j] * self.sigmoid_derived(self.layers[l + 1].a[_j]) * self.layers[l + 1].grad[_j]
                                elif (self.layers[l].activation == "relu"):
                                    self.layers[l].grad[j] += self.layers[l + 1].weights[_j, j] * self.relu_derived(self.layers[l + 1].a[_j]) * self.layers[l + 1].grad[_j]
                
                # Adjusting weights
                for l in reversed(range(1, self.n_layers)):
                    for j in range(self.layers[l].dimensions):
                        for k in range(self.layers[l - 1].dimensions):
                            update_weights(l, j, k)
                        update_bias(l, j)
                        self.layers[l].grad[j] = 0
           
            if (epoch % 10 == 0):
                print("Epoch {} done. Error: {}".format(epoch, NeuralNetwork.find_error(self.predict(x), y)))
                
    # Loads weights into the network
    # Parameter:
    #   weights: the weights which should be loaded into the network. Should be of 3d shape.
    def load_weights(self, weights):
        for l in range(1, self.n_layers):
            if (self.layers[l].weights.shape != weights[l - 1].shape):
                raise Exception("Wrong dimensions given. Expected: {}, Given:{}".format(self.layers[l].weights.shape, weights[l - 1].shape))
            self.layers[l].weights = weights[l - 1].copy()
    
    # Forward propogation. Used for fitting                        
    def _forwardprop(self, x):
        self.layers[0].feedforward(x)
        for l in range(1, self.n_layers):
            self.layers[l].feedforward(self.layers[l - 1].a)
    
    # Method for predicting.    
    def predict(self, x):
        self._forwardprop(x)
            
        return self.layers[self.n_layers - 1].a