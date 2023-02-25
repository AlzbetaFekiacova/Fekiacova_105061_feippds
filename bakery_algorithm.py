"""This module contains an implementation of Bakery's algorithm."""

__authors__ = "Alžbeta Fekiačová, Tomáš Vavro"
__email__ = "xfekiacova@stuba.sk, xvavro@stuba.sk"
__licence__ = "MIT"

from fei.ppds import Thread
from time import sleep

number_of_threads: int = 10
num: list[int] = [0 for _ in range(number_of_threads)]
choosing: list[:bool] = [False for _ in range(number_of_threads)]


def process(tid: int, num_runs: int):
    """ Simulates a process.

    Arguments:
        tid      -- thread id
        num_runs -- number of executions of critical section
    """
    global choosing, num

    for n in range(num_runs):
        choosing[tid] = True
        num[tid] = 1 + max(num)
        choosing[tid] = False

        for j in range(number_of_threads):
            while choosing[j]:
                continue
            while (num[j] != 0 and (num[j] < num[tid] or (
                    num[j] == num[tid] and j < tid))):
                continue
        # execute critical section
        print(f"Process {tid} runs a complicated computation!")
        sleep(1)
        # exit critical section
        num[tid] = False


if __name__ == '__main__':
    DEFAULT_NUM_OF_RUNS = 10
    threads = [Thread(process, i, DEFAULT_NUM_OF_RUNS) for i in range(number_of_threads)]
    [t.join() for t in threads]
