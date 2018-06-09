from PIL import Image
import numpy

a = numpy.array([[1, 2], [3, 4]]).flatten()
b = numpy.array([[4, 5], [6, 7]]).flatten()


def int_to_rgb(rgb_int):
    return [(rgb_int >> 16) & 255, (rgb_int >> 8) & 255, rgb_int & 255]


ggg = int_to_rgb()

print(ggg)
