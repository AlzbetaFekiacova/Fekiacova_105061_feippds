"""This module contains an implementation of Feasting Savages problem with multiple cooks."""

__authors__ = "Marián Šebeňa, Matúš Jókay, Tomáš Vavro, Alžbeta Fekiačová"
__email__ = "mariansebena@stuba.sk, xvavro@stuba.sk, xfekiacova@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread, Mutex, Semaphore, Event, print
from time import sleep

# savages
SAVAGES_COUNT: int = 5

# cooks
CHEFS_COUNT: int = 3

# pot portions
PORTIONS_COUNT: int = 8


class SimpleBarrier:
    """ Reusable barrier from seminar 3. """

    def __init__(self, n):
        self.n = n
        self.counter = 0
        self.mutex = Mutex()
        self.turnstile1 = Semaphore(0)
        self.turnstile2 = Semaphore(0)

    """
        Modified wait function of the barrier introduced on seminar 5 last year.
        The modification contains print functions for each thread and a special one for the last thread.
        
        :param each: message to be printed by each thread
        :param last: message to be printed by last thread       
    """

    def wait(self, each=None, last=None):
        self.mutex.lock()
        self.counter += 1
        if each:
            print(each)
        if self.counter == self.n:
            self.turnstile1.signal(self.n)
            if last:
                print(last)
        self.mutex.unlock()
        self.turnstile1.wait()

        sleep(1 / 5)
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            self.turnstile2.signal(self.n)
        self.mutex.unlock()
        self.turnstile2.wait()


class Shared:
    """Represent shared data for all threads."""

    def __init__(self, servings):
        self.savages_mutex = Mutex()
        self.chefs_mutex = Mutex()
        self.pot_portions = servings

        self.full_pot = Event()
        self.empty_pot = Event()

        self.barrier_1_savages = SimpleBarrier(SAVAGES_COUNT)
        self.barrier_2_savages = SimpleBarrier(SAVAGES_COUNT)

        self.barrier_1_cooks = SimpleBarrier(CHEFS_COUNT)
        self.barrier_2_cooks = SimpleBarrier(CHEFS_COUNT)


def eat(i: int):
    """
        Simulate eating.

        :param i: savage's id
    """
    print(f'SAVAGE-{i}- is feasting.')
    sleep(1.5)


def cook_portion(i: int):
    """
        Simulate cooking.

        :param i: cook's id
    """
    print(f'COOK-{i}- is cooking.')
    sleep(1)


def savage(i: int, shared: Shared):
    """
        Run savage's code.

        :param i: savage's id
        :param shared: shared data
    """
    while True:
        shared.barrier_1_savages.wait()
        shared.barrier_2_savages.wait(each=f'SAVAGE-{i}-: Came for dinner.',
                                      last=f'SAVAGE-{i}-: We are all, let\'s '
                                           f'have a look at the pot'
                                           f'.\n----------------------------------------------------------------------')
        shared.savages_mutex.lock()
        print(f'SAVAGE-{i}-: Arrived, there is {shared.pot_portions} portions left.')

        if shared.pot_portions == 0:
            print(f'\nSAVAGE-{i}-: Signals pot is empty.\n')
            shared.empty_pot.signal()
            shared.full_pot.clear()
            shared.full_pot.wait()

        shared.pot_portions -= 1
        print(f'Savage-{i}- Takes a portion, there are {shared.pot_portions} portions left.')
        shared.savages_mutex.unlock()
        eat(i)


def cook(i: int, shared: Shared):
    """
        Run cook's code.

        :param i: cook's id
        :param shared: shared data
    """
    while True:
        shared.barrier_1_cooks.wait()
        shared.barrier_2_cooks.wait(each=f'COOK-{i}-: Waiting for other chefs.',
                                    last=f'COOK-{i}-: Let\'s wait for the pot to be empty and cook.')

        shared.chefs_mutex.lock()
        shared.empty_pot.wait()
        if shared.pot_portions < PORTIONS_COUNT:
            cook_portion(i)
            shared.pot_portions += 1
            print(f'COOK-{i}-: Cooked a portion, now there are {shared.pot_portions} servings.')

        if shared.pot_portions == PORTIONS_COUNT:
            print(f'COOK-{i}-: Signals pot is full, there are {shared.pot_portions} servings in the pot. Capacity of '
                  f'pot is {PORTIONS_COUNT}.'
                  f'\n----------------------------------------------------------------------')
            shared.full_pot.signal()
            shared.empty_pot.clear()
        shared.chefs_mutex.unlock()


def main():
    """Run main."""
    print(f'NUMBER OF SAVAGES:{SAVAGES_COUNT}\nNUMBER OF COOKS:{CHEFS_COUNT}\nPOT CAPACITY:{PORTIONS_COUNT}\n')
    shared: Shared = Shared(0)
    savages: list[Thread] = [
        Thread(savage, i, shared) for i in range(SAVAGES_COUNT)
    ]
    cooks: list[Thread] = [
        Thread(cook, i, shared) for i in range(CHEFS_COUNT)
    ]

    savages_and_cooks = savages + cooks

    for p in savages_and_cooks:
        p.join()


if __name__ == "__main__":
    main()
