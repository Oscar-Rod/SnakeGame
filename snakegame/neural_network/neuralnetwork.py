import numpy as np
import pickle


class NeuralNetwork(object):
    def __init__(self, inputs, hidden, output):
        self.weights_ih = np.matrix(np.random.rand(hidden, inputs))
        self.weights_ho = np.matrix(np.random.rand(output, hidden))
        self.bias_ih = np.random.rand(hidden, 1)
        self.bias_ho = np.random.rand(output, 1)

    def sigmoid(self, x):
        # return 1 / (1 + np.exp(-x))
        return x

    def linear_trans(self, space1, space2):
        m = (space2[0] - space2[1]) / (space1[0] - space1[1])
        b = space2[0] - space1[0] * m
        return [m, b]

    def predict(self, value_in, input_space=[0, 1], output_space=[0, 1]):
        input_v = np.matrix(value_in).transpose()

        # from input to hidden
        mat_ih = self.weights_ih * input_v
        mat_h = mat_ih + self.bias_ih
        mat_h_sigmoid = self.sigmoid(mat_h)

        # from hidden to output
        mat_ho = self.weights_ho * mat_h_sigmoid
        mat_o = (mat_ho + self.bias_ho)
        output_v = self.sigmoid(mat_o)

        # linear transformation
        # [m, b] = self.linear_trans(input_space, output_space)
        # output_linear = m * output_v + b

        return output_v

    def save_to_file(self, filename):
        weights = [self.weights_ih, self.weights_ho, self.bias_ih, self.weights_ho]
        with open(filename + ".pkl", "wb") as output:
            pickle.dump(weights, output, pickle.HIGHEST_PROTOCOL)
