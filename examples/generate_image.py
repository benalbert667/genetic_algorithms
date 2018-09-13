from general_genetic_alg import GGA
from PIL import Image
import numpy as np


def int_to_rgb(rgb_int):
    return [(rgb_int >> 16) & 255, (rgb_int >> 8) & 255, rgb_int & 255]


def flat_arr_to_image(a, width, height):
    x = []
    for i in range(height):
        row = []
        for j in range(width):
            rgb = int(a[width * i + j] * (2 ** 24))
            row.append(int_to_rgb(rgb))
        x.append(row)
    return Image.fromarray(np.uint8(np.array(x)))


def main():
    print('*GENETIC ALGORITHM WITH IMAGES*')

    filename = input('Filename of image: ')
    orig_img = Image.open(filename)
    # orig_img.show()

    flat_orig = np.array(orig_img).flatten()
    goal = []
    for i in range(int(flat_orig.size / 3)):
        i *= 3
        rgb = flat_orig[i]
        rgb = (rgb << 8) + flat_orig[i + 1]
        rgb = (rgb << 8) + flat_orig[i + 2]
        goal.append(rgb)
    goal = np.array(goal)

    width, height = orig_img.size

    goal_for_func = np.array([int_to_rgb(int(p)) for p in goal])

    def success_function(x):
        x = np.array([int_to_rgb(int(rgb_x)) for rgb_x in np.round(np.array(x) * (2 ** 24))])
        return -np.sum(abs(x - goal_for_func))

    ga = GGA(mutate_rate=0.01,
             breed_rate=0.75,
             population_size=1000,
             len_output=goal.size,
             success_function=success_function)

    print('{}x{} image'.format(width, height))
    print('With population size = {}\n{}% of population regenerated every generation\n{}% chance for a gene to mutate'
          .format(ga.ps, ga.br * 100, ga.mr * 100))

    while True:
        ga.increment_generation(1)
        curr_best = ga.get_best_individual()
        print('Generation {} success: {}'.format(ga.get_num_generations(), curr_best[1]))
        # im = flat_arr_to_image(curr_best[0], width, height)
        # im.show()
        if curr_best[1] >= 0:
            break

    print('{} generations'.format(ga.get_num_generations()))


if __name__ == '__main__':
    main()
