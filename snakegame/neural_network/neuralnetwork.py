import pickle
import random

import numpy as np


class NeuralNetwork(object):
    def __init__(self, inputs, hidden, output):
        self.weights_ih = np.random.randn(hidden, inputs) * 0.1
        self.weights_ho = np.random.randn(output, hidden) * 0.1
        self.bias_ih = np.random.randn(hidden, 1) * 0.1
        self.bias_ho = np.random.randn(output, 1) * 0.1

    def sigmoid(self, Z):
        return 1 / (1 + np.exp(-Z))

    def relu(self, Z):
        return np.maximum(0, Z)

    def predict(self, value_in, input_space=[0, 1], output_space=[0, 1]):
        input_v = np.matrix(value_in).transpose()

        # from input to hidden
        mat_h = np.dot(self.weights_ih, input_v) + self.bias_ih
        mat_h_sigmoid = self.relu(mat_h)

        # from hidden to output
        mat_o = np.dot(self.weights_ho, mat_h_sigmoid) + self.bias_ho
        output_v = self.relu(mat_o)

        return output_v

    def save_to_file(self, filename):
        weights = [self.weights_ih, self.weights_ho, self.bias_ih, self.weights_ho]
        with open(filename + ".pkl", "wb") as output:
            pickle.dump(weights, output, pickle.HIGHEST_PROTOCOL)

    def mutate(self, mutation_rate):
        self.weights_ho += np.random.uniform(-mutation_rate, mutation_rate, self.weights_ho.shape)
        self.weights_ih += np.random.uniform(-mutation_rate, mutation_rate, self.weights_ih.shape)
        self.bias_ho += np.random.uniform(-mutation_rate, mutation_rate, self.bias_ho.shape)
        self.bias_ih += np.random.uniform(-mutation_rate, mutation_rate, self.bias_ih.shape)

    def combine(self, second_brain):
        # for i in range(len(self.weights_ho)):
        #     for j in range(len(self.weights_ho[i])):
        #         self.weights_ho[i][j] = random.choice([self.weights_ho[i][j], second_brain.weights_ho[i][j]])
        #
        # for i in range(len(self.weights_ih)):
        #     for j in range(len(self.weights_ih[i])):
        #         self.weights_ih[i][j] = random.choice([self.weights_ih[i][j], second_brain.weights_ih[i][j]])
        #
        # for i in range(len(self.bias_ho)):
        #     for j in range(len(self.bias_ho[i])):
        #         self.bias_ho[i][j] = random.choice([self.bias_ho[i][j], second_brain.bias_ho[i][j]])
        #
        # for i in range(len(self.bias_ih)):
        #     for j in range(len(self.bias_ih[i])):
        #         self.bias_ih[i][j] = random.choice([self.bias_ih[i][j], second_brain.bias_ih[i][j]])
        self.weights_ho = random.choice([self.weights_ho, second_brain.weights_ho])
        self.weights_ih = random.choice([self.weights_ih, second_brain.weights_ih])
        self.bias_ho = random.choice([self.bias_ho, second_brain.bias_ho])
        self.bias_ih = random.choice([self.bias_ih, second_brain.bias_ih])
