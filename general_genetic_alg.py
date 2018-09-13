import numpy as np
from numpy.random import rand, shuffle
from math import ceil


class GGA:
    def __init__(self, mutate_rate, breed_rate, population_size, len_output, success_function):
        self.mr = mutate_rate  # chance for a gene to mutate
        self.br = breed_rate  # percent of population that is cycled per generation
        self.ps = population_size  # size of population
        self.check_fitness = success_function  # fitness function (higher result = more fit)

        self.__population = rand(self.ps, len_output)  # entire population
        self.__best_individuals = None  # sorted list of top (1-br)% individuals
        self.__generation = 0

    def get_best_individual(self):
        # Returns the individual from the current population with the highest fitness
        if self.__best_individuals is not None:
            return self.__best_individuals[-1].copy(), self.check_fitness(self.__best_individuals[-1])
        return None

    def increment_generation(self, num_generations):
        if self.__generation == 0:
            self.__best_individuals = self.__get_elite_of_population()
        for _ in range(num_generations):
            self.__breed_random_parents()
            self.__generation += 1
            self.__best_individuals = self.__get_elite_of_population()

    def get_current_population(self):
        return self.__population.copy()

    def get_num_generations(self):
        return self.__generation

    def __breed_random_parents(self):
        ga = rand(*self.__population.shape)  # Gene assignments
        # Create parent pool from current elite of population
        parents = np.repeat(self.__best_individuals, int(ceil((1 / (1 - self.br)))), axis=0)
        shuffle(parents)
        # Resize parents to population's size (cutting off a random selection of repeated parents)
        parents = parents[:self.__population.shape[0]]

        # Create mother and father populations
        mothers = parents.copy()
        shuffle(parents)
        fathers = parents.copy()

        # Parent Choice Threshold: Used to determine which parent a child should inherit a gene from
        pct = (1 - self.mr) / 2 + self.mr
        # Wipe current population
        self.__population = rand(*self.__population.shape)
        # Inherit genes randomly from either the father or the mother gene pools (or randomly mutate)
        self.__population = np.where((ga > self.mr) & (ga <= pct), fathers,
                                     np.where(ga > pct, mothers, self.__population))
        # Re-introduce previous generation's elite into population
        self.__population[:self.__best_individuals.shape[0]] = self.__best_individuals

    def __get_elite_of_population(self):
        # Get the top (1-br)% of population by fitness
        return np.array(sorted(self.__population, key=self.check_fitness))[-int(self.ps*(1-self.br)):]
