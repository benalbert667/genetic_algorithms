import numpy as np
from numpy.random import rand, shuffle
from random import random
from math import ceil


class GGA:
    def __init__(self, mutate_rate, breed_rate, population_size, len_output, success_function):
        self.mr = mutate_rate  # chance for a gene to mutate
        self.br = breed_rate  # percent of population that is cycled per generation
        self.ps = population_size  # size of population
        self.os = len_output  # size of each individual
        self.check_fitness = success_function  # fitness function (higher result = more fit)

        self.__population = GAHeap(self.ps, self.check_fitness)  # entire population
        self.__init_population()
        # self.__best_individuals = None  # sorted list of top (1-br)% individuals
        self.__generation = 0

    def get_best_individual(self):
        # Returns the individual from the current population with the highest fitness
        return self.__population.get_max()

    def increment_generation(self, num_generations):
        # if self.__generation == 0:
        #     self.__best_individuals = self.__get_elite_of_population()
        for _ in range(num_generations):
            self.__breed_random_parents()
            self.__generation += 1
            # self.__best_individuals = self.__get_elite_of_population()

    def get_num_generations(self):
        return self.__generation

    def __breed_random_parents(self):
        num_elites = int(self.ps * (1 - self.br))
        elites = [self.__population.delete_max() for _ in range(num_elites)]

        # proportional ranges based on score from 1 to self.mr
        ess = sum(e[1] for e in elites)  # elite score sum
        ppoi = np.cumsum([(e[1] / ess) * (1 - self.mr) for e in elites])  # proportional probabilities of inheritance

        self.__population.clear_heap()

        for _ in range(self.ps - num_elites):
            ga = rand(self.os)
            indv = rand(self.os)
            for i in range(self.os):
                j = np.searchsorted(ppoi, ga[i])
                if j < num_elites:
                    indv[i] = elites[j][0][i]
            self.__population.insert(indv)

        while elites:
            self.__population.insert(elites.pop()[0])



        # ga = rand(*self.__population.shape)  # Gene assignments
        # # Create parent pool from current elite of population
        # parents = np.repeat(self.__best_individuals, int(ceil((1 / (1 - self.br)))), axis=0)
        # shuffle(parents)
        # # Resize parents to population's size (cutting off a random selection of repeated parents)
        # parents = parents[:self.__population.shape[0]]
        #
        # # Create mother and father populations
        # mothers = parents.copy()
        # shuffle(parents)
        # fathers = parents.copy()
        #
        # # Parent Choice Threshold: Used to determine which parent a child should inherit a gene from
        # pct = (1 - self.mr) / 2 + self.mr
        # # Wipe current population
        # self.__population = rand(*self.__population.shape)
        # # Inherit genes randomly from either the father or the mother gene pools (or randomly mutate)
        # self.__population = np.where((ga > self.mr) & (ga <= pct), fathers,
        #                              np.where(ga > pct, mothers, self.__population))
        # # Re-introduce previous generation's elite into population
        # self.__population[:self.__best_individuals.shape[0]] = self.__best_individuals

    # def __get_elite_of_population(self):
    #     # Get the top (1-br)% of population by fitness
    #     return np.array(sorted(self.__population, key=self.check_fitness))[-int(self.ps*(1-self.br)):]

    def __init_population(self):
        for _ in range(self.ps):
            self.__population.insert(rand(self.os))


"""
Heap data structure used to efficiently get the elite of a population
"""


def parent(i):
    return (i - 1) // 2


def l_child(i):
    return i * 2 + 1


def r_child(i):
    return i * 2 + 2


class GAHeap:
    def __init__(self, size, ranker):
        self.len = size
        self.heap = [None] * self.len
        self.nextRB = 0
        self.rank = ranker

    def insert(self, g):
        self.heap[self.nextRB] = (g, self.rank(g))
        self.perc_up()
        self.nextRB += 1

    def delete_max(self):
        self.nextRB -= 1
        self.heap[0], self.heap[self.nextRB] = self.heap[self.nextRB], self.heap[0]

        to_return = self.heap[self.nextRB]
        self.heap[self.nextRB] = None

        self.perc_down()

        return to_return

    def get_max(self):
        return self.heap[0]

    def clear_heap(self):
        self.heap = [None] * self.len
        self.nextRB = 0

    def perc_up(self):
        i = self.nextRB
        while i > 0 and self.heap[i][1] > self.heap[parent(i)][1]:
            self.heap[i], self.heap[parent(i)] = self.heap[parent(i)], self.heap[i]
            i = parent(i)

    def perc_down(self):
        i = 0
        while not self.is_leaf(i) and self.is_less_than_child(i):
            if self.heap[l_child(i)] is None:
                j = r_child(i)
            elif self.heap[r_child(i)] is None:
                j = l_child(i)
            elif self.heap[l_child(i)][1] > self.heap[r_child(i)][1]:
                j = l_child(i)
            else:
                j = r_child(i)

            self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
            i = j

    def is_leaf(self, i):
        if l_child(i) >= self.len or r_child(i) >= self.len:
            return True
        return self.heap[l_child(i)] is None and self.heap[r_child(i)] is None

    def is_less_than_child(self, i):
        if self.heap[l_child(i)] is None and self.heap[r_child(i)] is not None:
            return self.heap[r_child(i)][1] > self.heap[i][1]
        elif self.heap[l_child(i)] is not None and self.heap[r_child(i)] is None:
            return self.heap[l_child(i)][1] > self.heap[i][1]
        return self.heap[l_child(i)][1] > self.heap[i][1] or self.heap[r_child(i)][1] > self.heap[i][1]
