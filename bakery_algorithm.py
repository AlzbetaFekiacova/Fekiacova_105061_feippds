"""This module contains an implementation of Bakery's algorithm."""

__authors__ = "Alžbeta Fekiačová, Tomáš Vavro"
__email__ = "xfekiacova@stuba.sk, xvavro@stuba.sk"
__licence__ = "MIT"

from fei.ppds import Thread

number_of_threads: int = 10
num_list: list[int] = [0 for _ in range(number_of_threads)]
in_list: list[:bool] = [False for _ in range(number_of_threads)]


def process(tid: int):
    in_list[tid] = True
    num_list[tid] = 1 + max(num_list)
    in_list[tid] = False

    for j in range(number_of_threads):
        while in_list[j]:
            continue
        while num_list[j] != 0 and (num_list[j] < num_list[tid] or (
                num_list[j] == num_list[tid] and j < tid)):
            continue


if __name__ == '__main__':
    DEFAULT_NUM_OF_RUNS = 10
    threads = [Thread(process, i) for i in range(number_of_threads)]
    [t.join() for t in threads]
