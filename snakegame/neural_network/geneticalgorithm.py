import copy
import random


class Breeder:
    def __init__(self, mutation_rate):
        self.mutation_rate = mutation_rate

    def mutate_snakes(self, new_snakes, dead_snakes):
        self.order_dead_snakes_by_performance(dead_snakes)
        number_of_snakes = len(dead_snakes)
        number_of_snakes_unchanged = max(int(number_of_snakes * 0.001), 1)
        number_of_snakes_breded = max(int(number_of_snakes * 0.015), 2)
        for i in range(int(number_of_snakes * 0.90)):
            if i is 0:
                scores, lengths = self.generate_string_with_best_snakes(dead_snakes, number_of_snakes_breded)
                print(scores)
                print(lengths)
                print()
            if i <= number_of_snakes_unchanged:
                new_snakes[i].brain = dead_snakes[i].brain
            else:
                brain1 = random.choice(dead_snakes[0:number_of_snakes_breded]).brain
                brain2 = random.choice(dead_snakes[0:number_of_snakes_breded]).brain
                new_brain = copy.deepcopy(brain1)
                new_brain.combine(brain2)
                if bool(random.getrandbits(1)):
                    new_brain.mutate(self.mutation_rate)
                new_snakes[i].brain = new_brain
        return new_snakes

    @staticmethod
    def order_dead_snakes_by_performance(dead_snakes):
        dead_snakes.sort(key=lambda x: x.score, reverse=True)

    @staticmethod
    def generate_string_with_best_snakes(snakes, number):
        list_of_scores = [x.score for x in snakes]
        list_of_length = [x.length for x in snakes]
        return ", ".join(map(str, list_of_scores)), ", ".join(map(str, list_of_length))
