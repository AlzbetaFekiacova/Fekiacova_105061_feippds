"""This module implements dinning philosophers problem.
 No solution is implemented.
 """

__author__ = "Tomáš Vavro, Alžbeta Fekiačová"
__email__ = "xvavro@stuba.sk, xfekiacova@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread, Mutex, Semaphore, print
from time import sleep

NUM_PHILOSOPHERS: int = 5
NUM_RUNS: int = 35  # number of repetitions of think-eat cycle of philosophers


class Shared:
    """Represent shared data for all threads."""

    def __init__(self):
        """Initialize an instance of Shared."""
        self.forks = [Mutex() for _ in range(NUM_PHILOSOPHERS)]


def think(i: int):
    """Simulate thinking.
    Args:
        i -- philosopher's id
    """
    print(f"Philosopher {i} is thinking!")
    sleep(0.1)


def eat(i: int):
    """Simulate eating.
    Args:
        i -- philosopher's id
    """
    print(f"Philosopher {i} is eating!")
    sleep(0.1)


def philosopher(i: int, shared: Shared):
    """Run philosopher's code.
    Args:
        i -- philosopher's id
        shared -- shared data
    """
    for _ in range(NUM_RUNS):
        think(i)
        # get forks
        if i == 0:
            shared.forks[(i + 1) % NUM_PHILOSOPHERS].lock()
            sleep(0.5)
            shared.forks[i].lock()
            print(f'{i} got forks - left handed')
        else:
            shared.forks[i].lock()
            sleep(0.5)
            shared.forks[(i + 1) % NUM_PHILOSOPHERS].lock()
            print(f'{i} got forks')
        eat(i)
        if i == 0:
            shared.forks[(i + 1) % NUM_PHILOSOPHERS].unlock()
            shared.forks[i].unlock()
            print(f'{i} returned forks - left handed')
        else:
            shared.forks[i].unlock()
            shared.forks[(i + 1) % NUM_PHILOSOPHERS].unlock()
            print(f'{i} returned forks')


def main():
    """Run main."""
    shared: Shared = Shared()
    philosophers: list[Thread] = [
        Thread(philosopher, i, shared) for i in range(NUM_PHILOSOPHERS)
    ]
    for p in philosophers:
        p.join()


if __name__ == "__main__":
    main()
