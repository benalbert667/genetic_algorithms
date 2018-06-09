from general_genetic_alg import GGA


def float_arr_to_string(a):
    return ''.join(chr(int(i*96 + 32)) for i in a)


def main():
    print('*GENETIC ALGORITHM WITH STRINGS*')

    goal = input('String to match: ')

    def success_function(x):
        score = 0
        x = float_arr_to_string(x)
        for a, b in zip(x, goal):
            score += int(a == b)
        return score

    ga = GGA(mutate_rate=0.01,
             breed_rate=0.75,
             population_size=1000,
             len_output=len(goal),
             success_function=success_function)

    print('With population size = {}\n{}% of population regenerated every generation\n{}% chance for a gene to mutate'
          .format(ga.ps, ga.br * 100, ga.mr * 100))

    while True:
        ga.increment_generation(1)
        curr_best = ga.get_best_individual()
        print('Generation {}: \'{}\', score: {}'.format(
            ga.get_current_generation(),
            float_arr_to_string(curr_best[0]),
            curr_best[1]
        ))
        if float_arr_to_string(curr_best[0]) == goal:
            break


if __name__ == '__main__':
    main()
