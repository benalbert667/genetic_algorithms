from numpy.random import rand as random_array
from random import random, choice


class GGA:
    def __init__(self, mutate_rate, breed_rate, population_size, len_output, success_function):
        self.mr = mutate_rate  # chance for a gene to mutate
        self.br = breed_rate  # percent of population that is cycled per generation
        self.ps = population_size  # size of population
        self.check_fitness = success_function  # fitness function

        self.__population = self.__generate_random_population(len_output)
        self.__generation = 0

    def get_best_individual(self):
        best = max(self.__population, key=self.check_fitness)
        return best, self.check_fitness(best)  # returns both most successful individual and their fitness score

    def increment_generation(self, num_generations):
        for _ in range(num_generations):
            elite = self.__get_elite_of_population()
            p = elite.copy()  # elite continue into next population
            # fill rest of population with elite's children
            p.extend(self.__breed_random_parents(elite) for _ in range(int(self.ps * self.br)))
            self.__population = p
            self.__generation += 1

    def get_current_population(self):
        return self.__population.copy()

    def get_current_generation(self):
        return self.__generation

    # Creates a new child from two random parents
    def __breed_random_parents(self, parent_pool):
        p1 = choice(parent_pool)
        p2 = choice(parent_pool)
        child = []
        for i in range(len(p1)):
            if random() < self.mr:
                child.append(random())  # random mutation
            elif random() < 0.5:  # select a parent to copy gene i from
                child.append(p1[i])
            else:
                child.append(p2[i])
        return child

    # Gets the top br% of population by fitness
    def __get_elite_of_population(self):
        return sorted(self.__population,
                      key=lambda x: self.check_fitness(x),
                      reverse=True)[0: int(self.ps * (1 - self.br))]

    # Generates a random population (2d array (population size by individual size) of random number 0 to 1)
    def __generate_random_population(self, individual_size):
        return random_array(self.ps, individual_size).tolist()
