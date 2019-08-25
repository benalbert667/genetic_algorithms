import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from general_genetic_alg import GGA
import numpy as np


def float_arr_to_string(a):
    return ''.join(chr(int(i*96 + 32)) for i in a)


def main():
    print('*GENETIC ALGORITHM WITH STRINGS*')

    goal_str = input('String to match: ')
    goal = np.array(list(map(lambda c: (ord(c) - 32)/96.0, list(goal_str))))

    def success_function(x):
        comp = np.floor(x*96.0)/96.0
        return np.sum(comp == goal)

    ga = GGA(mutate_rate=0.01,
             breed_rate=0.75,
             population_size=1000,
             len_output=goal.size,
             success_function=success_function)

    print('With population size = {}\n{}% of population regenerated every generation\n{}% chance for a gene to mutate'
          .format(ga.ps, ga.br * 100, ga.mr * 100))

    while True:
        ga.increment_generation(1)
        curr_best = ga.get_best_individual()
        print('Generation {0:3}: \'{1}\', score: {2}'.format(
            ga.get_num_generations(),
            float_arr_to_string(curr_best[0]),
            curr_best[1]
        ))
        if curr_best[1] == goal.size:
            break


if __name__ == '__main__':
    main()
