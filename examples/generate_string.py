import sys
import os
import numpy as np
from time import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from general_genetic_alg import GGA


def float_arr_to_string(a):
    return ''.join(chr(int(i*96 + 32)) for i in a)


def main():
    print('*GENETIC ALGORITHM WITH STRINGS*')

    goal_str = input('String to match: ')
    goal = np.array(list(map(lambda c: (ord(c) - 32)/96.0, list(goal_str))))

    def success_function(x):
        comp = np.floor(x*96.0)/96.0
        return np.sum(comp == goal)

    init_timer = time()

    ga = GGA(mutate_rate=0.01,
             breed_rate=0.75,
             population_size=1000,
             len_output=goal.size,
             success_function=success_function)

    print('With population size = {}\n{}% of population regenerated every generation\n{}% chance for a gene to '
          'mutate\nGGA initialized in {:.3f} seconds'
          .format(ga.ps, ga.br * 100, ga.mr * 100, time() - init_timer))

    process_timer = time()

    while True:
        curr_best = ga.get_best_individual()
        print('Generation {0:3}: \'{1}\', score: {2}'.format(
            ga.get_num_generations(),
            float_arr_to_string(curr_best[0]),
            curr_best[1]
        ))
        if curr_best[1] == goal.size:
            break
        ga.increment_generation(1)

    process_timer = time() - process_timer
    print('Processed in {:.2f} seconds ({:.3f} seconds per generation)'
          .format(process_timer, process_timer / ga.get_num_generations()))


if __name__ == '__main__':
    main()
