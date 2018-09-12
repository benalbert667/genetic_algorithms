import numpy as np
from random import random, choice


class GGA:
    def __init__(self, mutate_rate, breed_rate, population_size, len_output, success_function):
        self.mr = mutate_rate  # chance for a gene to mutate
        self.br = breed_rate  # percent of population that is cycled per generation
        self.ps = population_size  # size of population
        self.check_fitness = success_function  # fitness function

        self.__population = self.__generate_random_population(len_output)
        self.__best_individual = self.__population[0]
        self.__generation = 0

    def get_best_individual(self):
        return self.__best_individual.copy(), self.check_fitness(self.__best_individual)

    def increment_generation(self, num_generations):
        for _ in range(num_generations):
            elite = self.__get_elite_of_population()
            self.__best_individual = elite[0]  # set best individual
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
        child = np.random.rand(p1.size)
        genes = np.random.rand(p1.size)
        pct = (1 - self.mr)/2 + self.mr  # parent choice threshold
        child = np.where(genes > pct, p1, child)  # genes from parent 1
        return np.where((genes > self.mr) & (genes <= pct), p2, child)  # genes from parent 2, remainder are random

    # Gets the top br% of population by fitness
    def __get_elite_of_population(self):
        return sorted(self.__population,
                      key=lambda x: self.check_fitness(x),
                      reverse=True)[:int(self.ps * (1 - self.br))]

    # Generates a random population (2d array (population size by individual size) of random number 0 to 1)
    def __generate_random_population(self, individual_size):
        return np.random.rand(self.ps, individual_size)
