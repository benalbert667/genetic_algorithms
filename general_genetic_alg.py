import numpy as np
from numpy.random import rand
from math import ceil


class GGA:
    def __init__(self, mutate_rate, breed_rate, population_size, len_output, success_function):
        self.mr = mutate_rate  # chance for a gene to mutate
        self.br = breed_rate  # percent of population that is cycled per generation
        self.ps = population_size  # size of population
        self.os = len_output  # size of each individual
        self.check_fitness = success_function  # fitness function (higher result = more fit)

        self.__population = GAHeap(self.ps, self.check_fitness)  # entire population
        self.__init_population()  # initialize the population randomly
        self.__generation = 0

    def get_best_individual(self):
        # Returns the individual from the current population with the highest fitness
        return self.__population.get_max()

    def increment_generation(self, num_generations):
        for _ in range(num_generations):
            self.__breed_elite()
            self.__generation += 1

    def get_num_generations(self):
        return self.__generation

    def __breed_elite(self):
        # retrieve the elite of the population from the heap
        num_elites = ceil(self.ps * (1 - self.br))
        elites, elite_scores = [], []
        for _ in range(num_elites):
            e, s = self.__population.delete_max()
            elites.append(e)
            elite_scores.append(s)

        # add a random individual to the elite that the next generation will inherit as mutations
        elites = np.array(elites + [rand(self.os)])
        elite_scores = np.array(elite_scores)

        # delete the current population
        self.__population.clear_heap()

        # Proportional probabilities of inheritance:
        # these values will determine the likelihood that an individual in the next generation will inherit
        # a gene from any one elite.  the likelihood is scaled linearly by the elite's fitness
        ppoi = np.cumsum(elite_scores) / elite_scores.sum() * (1 - self.mr)

        # create random gene assignments for each new individual based on the proportional probabilities
        # ga will be a matrix of indices where each index is the index of the elite that gene will be inherited from
        ga = np.searchsorted(ppoi, rand(self.ps - num_elites, self.os))

        # inherit the selected genes
        ga = np.diagonal(elites[ga], axis1=1, axis2=2)

        # make a pop-able list of all the individuals moving on to the next generation
        ga = list(np.concatenate((ga, elites[:-1])))

        # add all individuals back in to the empty heap
        while ga:
            self.__population.insert(ga.pop())

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
