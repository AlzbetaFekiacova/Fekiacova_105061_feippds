"""This module contains grayscale conversion of image on CPU and GPU with usage of cuda using numba."""

__authors__ = "Marián Šebeňa, Matúš Jókay, Tomáš Vavro, Alžbeta Fekiačová"
__email__ = "mariansebena@stuba.sk, xvavro@stuba.sk, xfekiacova@stuba.sk"
__licence__ = "MIT"

import numpy as np
from matplotlib import pyplot as plt
from timeit import default_timer as timer
from numba import cuda


def convert_image(image, x, y):
    """Function to calculate the grayscale value of a pixel on position x,y of the image."""
    r = image[x, y, 0]
    g = image[x, y, 1]
    b = image[x, y, 2]
    return 0.299 * r + 0.587 * g + 0.114 * b


def rgb_to_gray_cpu(input_image):
    """Function to convert all the pixels of input image to gray scale on CPU."""
    output_image = np.zeros((input_image.shape[0], input_image.shape[1], input_image.shape[2]),
                            dtype=np.float32)
    for x in range(len(input_image)):
        for y in range(len(input_image[x])):
            output_image[x, y] = convert_image(input_image, x, y)
    return output_image


def cpu_func(image_path):
    """Function to convert, save and compute time of image conversion to gray scale on CPU."""
    input_pixels = plt.imread(image_path)
    start = timer()
    converted_image = rgb_to_gray_cpu(input_pixels)
    output_img = np.clip(converted_image, 0, 255).astype(np.uint8)
    end = timer()
    print(f"-CPU- Conversion to grayscale took : {end - start} seconds.")
    # execute on sports
    # image_path = image_path.replace("copied", "sports_transformed_CPU")

    # execute on flowers
    image_path = image_path.replace("original", "transformed_CPU")

    image_path_split = image_path.split(".")
    image_path_split[0] = image_path_split[0] + "_grayscale_CPU"
    image_path_output = ".".join(image_path_split)
    plt.imsave(image_path_output, output_img, format="jpg")
    return end - start


def cpu_main():
    """Function to convert images to gray scale in a for loop on CPU."""
    # path to sports
    # basic_path = "images/copied/image_"

    # path to images
    basic_path = "images/original/flower_s"
    cpu_time = 0

    # to execute on all sports images set loop to 100
    for i in range(20):
        current_path = basic_path + str(i) + ".jpg"
        cpu_time += cpu_func(current_path)
    return cpu_time


@cuda.jit
def rgb_to_gray_cuda(input_image, output_image):
    """Function to convert all the pixels of input image to gray scale on GPU."""
    x, y = cuda.grid(2)
    if x < input_image.shape[0] and y < input_image.shape[1]:
        output_image[x, y] = convert_image(input_image, x, y)


def cuda_func(image_path):
    """Function to convert, save and compute time of image conversion to gray scale on GPU."""
    image = plt.imread(image_path)
    height = image.shape[0]
    weight = image.shape[1]
    channel = image.shape[2]
    output = np.zeros((height, weight, channel), dtype=np.float32)

    d_input_image = cuda.to_device(image)
    d_output_image = cuda.to_device(output)

    threads_per_block = (16, 16)
    blocks_per_grid_x = height // threads_per_block[0]
    blocks_per_grid_y = weight // threads_per_block[1]
    blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)
    start = timer()

    rgb_to_gray_cuda[blocks_per_grid, threads_per_block](d_input_image, d_output_image)
    end = timer()
    print(f'-GPU- Conversion to grayscale took {end - start} seconds')

    output_img = np.clip(d_output_image.copy_to_host(), 0, 255).astype(np.uint8)

    # execute on sports
    # image_path = image_path.replace("copied", "sports_transformed_GPU")

    # execute on flowers
    image_path = image_path.replace("original", "transformed_GPU")

    image_path_split = image_path.split(".")
    image_path_split[0] = image_path_split[0] + "_grayscale_GPU"
    image_path_output = ".".join(image_path_split)
    plt.imsave(image_path_output, output_img, format="jpg")
    return end - start


def gpu_main():
    """Function to convert images to gray scale in a for loop on GPU."""
    # path to sports
    # basic_path = "images/copied/image_"

    # path to flowers
    basic_path = "images/original/flower_s"

    gpu_time = 0
    # to execute on all sports images set loop to 100
    for i in range(20):
        current_path = basic_path + str(i) + ".jpg"
        gpu_time += cuda_func(current_path)
    return gpu_time


if __name__ == '__main__':
    c_time = cpu_main()
    g_time = gpu_main()

    print(f'Average conversion on CPU took -{c_time / 100}- time.')
    print(f'Average conversion on GPU took -{g_time / 100}- time.')
