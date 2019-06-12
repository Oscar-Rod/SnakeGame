import random

import numpy as np


class NeuralNetwork(object):

    def __init__(self, nn_architecture):
        self.nn_architecture = nn_architecture
        self.params_values = self.init_layers(nn_architecture)

    def init_layers(self, nn_architecture, seed=99):
        np.random.seed(seed)
        number_of_layers = len(nn_architecture)
        params_values = {}

        for idx, layer in enumerate(nn_architecture):
            layer_idx = idx + 1
            layer_input_size = layer["input_dim"]
            layer_output_size = layer["output_dim"]

            params_values['W' + str(layer_idx)] = np.random.randn(
                layer_output_size, layer_input_size) * 0.1
            params_values['b' + str(layer_idx)] = np.random.randn(
                layer_output_size, 1) * 0.1

        return params_values

    def sigmoid(self, Z):
        return 1 / (1 + np.exp(-Z))

    def relu(self, Z):
        return np.maximum(0, Z)

    def single_layer_forward_propagation(self, A_prev, W_curr, b_curr, activation="relu"):
        Z_curr = np.dot(W_curr, A_prev)

        Z_curr = Z_curr + b_curr.ravel()

        if activation is "relu":
            activation_func = self.relu
        elif activation is "sigmoid":
            activation_func = self.sigmoid
        else:
            raise Exception('Non-supported activation function')

        return activation_func(Z_curr)

    def predict(self, X):
        A_curr = np.asarray(X)

        for idx, layer in enumerate(self.nn_architecture):
            layer_idx = idx + 1
            A_prev = A_curr

            activ_function_curr = layer["activation"]
            W_curr = self.params_values["W" + str(layer_idx)]
            b_curr = self.params_values["b" + str(layer_idx)]
            A_curr = self.single_layer_forward_propagation(A_prev, W_curr, b_curr, activ_function_curr)

        return A_curr

    def mutate(self, mutation_rate):
        for idx, layer in enumerate(self.nn_architecture):
            layer_idx = idx + 1
            layer_input_size = layer["input_dim"]
            layer_output_size = layer["output_dim"]

            self.params_values["W" + str(layer_idx)] += np.random.randn(layer_output_size,
                                                                        layer_input_size) * mutation_rate

            self.params_values["b" + str(layer_idx)] += np.random.randn(layer_output_size, 1) * mutation_rate

    def combine(self, second_brain):
        for idx, layer in enumerate(self.nn_architecture):
            layer_idx = idx + 1

            w2 = second_brain.params_values["W" + str(layer_idx)]
            b2 = second_brain.params_values["b" + str(layer_idx)]

            if bool(random.getrandbits(1)):
                self.params_values["W" + str(layer_idx)] = w2

            if bool(random.getrandbits(1)):
                self.params_values["b" + str(layer_idx)] = b2
