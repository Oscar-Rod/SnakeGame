from snakegame.neural_network.neuralnetwork import NeuralNetwork


class Brain:

    def __init__(self, perception, number_of_cells):
        self.perception = self.get_perception(perception, number_of_cells)
        self.number_of_cells = number_of_cells
        self.neural_network = NeuralNetwork(self.perception.set_architecture())

    @staticmethod
    def get_perception(perception_name, number_of_cells):
        module = __import__("snakegame.perceptions." + perception_name)
        name_of_the_class = dir(getattr(module.perceptions, perception_name))[0]
        return getattr(getattr(module.perceptions, perception_name), name_of_the_class)(number_of_cells)

    def predict(self, snake):
        X = self.perception.get_perception(snake)
        return self.neural_network.predict(X)

    def mutate(self, mutation_rate):
        self.neural_network.mutate(mutation_rate)

    def combine(self, second_brain):
        self.neural_network.combine(second_brain.neural_network)
