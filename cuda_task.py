"""This module shows basic usage of cuda using numba."""

__authors__ = "Marián Šebeňa, Matúš Jókay, Tomáš Vavro, Alžbeta Fekiačová"
__email__ = "mariansebena@stuba.sk, xvavro@stuba.sk, xfekiacova@stuba.sk"
__licence__ = "MIT"

import numpy as np
from matplotlib import pyplot as plt
from timeit import default_timer as timer
from numba import cuda


def convert_image(image, x, y):
    r = image[x, y, 0]
    g = image[x, y, 1]
    b = image[x, y, 2]
    return 0.299 * r + 0.587 * g + 0.114 * b


def rgb_to_gray(input_image):
    output_image = np.zeros((input_image.shape[0], input_image.shape[1], input_image.shape[2]),
                            dtype=np.float32)
    for x in range(len(input_image)):
        for y in range(len(input_image[x])):
            output_image[x, y] = convert_image(input_image, x, y)
    return output_image


def cpu_func(image_path, cpu_time):
    input_pixels = plt.imread(image_path)
    start = timer()
    converted_image = rgb_to_gray(input_pixels)
    output_img = np.clip(converted_image, 0, 255).astype(np.uint8)
    end = timer()
    print(f"-CPU- Conversion to grayscale took : {end - start} seconds.")
    cpu_time += (end - start)
    image_path = image_path.replace("copied", "sports_transformed_CPU")
    image_path_split = image_path.split(".")
    image_path_split[0] = image_path_split[0] + "_grayscale_CPU"
    image_path_output = ".".join(image_path_split)
    plt.imsave(image_path_output, output_img, format="jpg")


def cpu_main(cpu_time):
    basic_path = "images/copied/image_"
    for i in range(100):
        current_path = basic_path + str(i) + ".jpg"
        cpu_func(current_path, cpu_time)


@cuda.jit
def rgb_to_gray_cuda(input_image, output_image):
    x, y = cuda.grid(2)
    if x < input_image.shape[0] and y < input_image.shape[1]:
        output_image[x, y] = convert_image(input_image, x, y)


def cuda_func(image_path, gpu_time):
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
    gpu_time += (end - start)

    output_img = np.clip(d_output_image.copy_to_host(), 0, 255).astype(np.uint8)

    image_path = image_path.replace("copied", "sports_transformed_GPU")
    image_path_split = image_path.split(".")
    image_path_split[0] = image_path_split[0] + "_grayscale_GPU"
    image_path_output = ".".join(image_path_split)
    plt.imsave(image_path_output, output_img, format="jpg")


def gpu_main(gpu_time):
    basic_path = "images/copied/image_"
    for i in range(100):
        current_path = basic_path + str(i) + ".jpg"
        cuda_func(current_path, gpu_time)


if __name__ == '__main__':
    cpu_time = 0
    gpu_time = 0
    cpu_main(cpu_time)
    gpu_main(gpu_time)

    print(f'Average conversion time on CPU took -{cpu_time/100}-')
    print(f'Average conversion time on GPU took -{gpu_time/100}-')
