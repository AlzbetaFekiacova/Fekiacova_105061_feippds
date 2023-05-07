"""This module shows basic usage of cuda using numba."""

__authors__ = "Marián Šebeňa, Matúš Jókay, Tomáš Vavro, Alžbeta Fekiačová"
__email__ = "mariansebena@stuba.sk, xvavro@stuba.sk, xfekiacova@stuba.sk"
__licence__ = "MIT"

import numpy as np
from matplotlib import pyplot as plt
from timeit import default_timer as timer


def rgb_to_gray(input_image):
    output_image = np.zeros((input_image.shape[0], input_image.shape[1], input_image.shape[2]),
                            dtype=np.float32)
    for x in range(len(input_image)):
        for y in range(len(input_image[x])):
            r = input_image[x, y, 0]
            g = input_image[x, y, 1]
            b = input_image[x, y, 2]
            gray = 0.299 * r + 0.587 * g + 0.114 * b
            output_image[x, y] = gray
    return output_image


def cpu_func(image_path):
    input_pixels = plt.imread(image_path)
    start = timer()
    converted_image = rgb_to_gray(input_pixels)
    output_img = np.clip(converted_image, 0, 255).astype(np.uint8)
    end = timer()
    print(f"-CPU- Conversion to grayscale took : {end - start} seconds.")

    image_path_split = image_path.split(".")
    image_path_split[0] = image_path_split[0] + "_grayscale_CPU"
    image_path_output = ".".join(image_path_split)
    plt.imsave(image_path_output, output_img, format="jpg")


def cpu_main():
    basic_path = "images/flower"
    for i in range(16):
        current_path = basic_path + str(i) + ".jpg"
        cpu_func(current_path)


if __name__ == '__main__':
    cpu_main()
