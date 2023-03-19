"""This module contains an implementation of Feasting Savages problem."""

__authors__ = "Marián Šebeňa, Matúš Jókay, Tomáš Vavro, Alžbeta Fekiačová"
__email__ = "mariansebena@stuba.sk, xvavro@stuba.sk, xfekiacova@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread, Mutex, Semaphore, Event, print

from time import sleep

# savages
SAVAGES_COUNT: int = 3

# cooks
CHEFS_COUNT: int = 5

# pot portions
PORTIONS_COUNT: int = 2


class SimpleBarrier:
    def __init__(self, n):
        self.n = n
        self.counter = 0
        self.mutex = Mutex()
        self.turnstile1 = Semaphore(0)
        self.turnstile2 = Semaphore(0)

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
    def __init__(self, m):
        self.savages_mutex = Mutex()
        self.chefs_mutex = Mutex()
        self.servings = m

        self.full_pot = Event()
        self.empty_pot = Event()

        self.barrier_1 = SimpleBarrier(SAVAGES_COUNT)
        self.barrier_2 = SimpleBarrier(SAVAGES_COUNT)

        self.barrier_1_cooks = SimpleBarrier(CHEFS_COUNT)
        self.barrier_2_cooks = SimpleBarrier(CHEFS_COUNT)

        self.cooks_count = 0


def eat(i: int):
    print(f'SAVAGE-{i}- is feasting.')
    sleep(1)


def savage(i: int, shared: Shared):
    while True:
        shared.barrier_1.wait()
        shared.barrier_2.wait(each=f'SAVAGE-{i}-: Came for dinner.',
                              last=f'SAVAGE-{i}-: We are all, let\'s eat.')
        shared.savages_mutex.lock()
        print(f'SAVAGE-{i}-: Arrived, there is {shared.servings} portions left.')
        if shared.servings == 0:
            print(f'\nSAVAGE-{i}-: Signals pot is empty.\n')
            shared.empty_pot.signal()
            shared.full_pot.clear()
            shared.full_pot.wait()

        print(f'\nSAVAGE-{i}-: Takes a portion.')
        shared.servings -= 1
        print(f'\nPOT   :{shared.servings} portions left.')
        shared.savages_mutex.unlock()
        eat(i)


def cook(i: int, shared: Shared):
    while True:
        shared.barrier_1_cooks.wait()
        shared.barrier_2_cooks.wait(each=f'COOK-{i}-: I am waiting for other chefs.',
                                    last=f'COOK-{i}-: Let\'s cook.')

        shared.empty_pot.wait()
        shared.chefs_mutex.lock()
        shared.cooks_count += 1

        if shared.servings < PORTIONS_COUNT:
            shared.servings += 1
            print(f'COOK-{i}-: I cooked a portion\nPOT: {shared.servings} servings')
        else:
            print(f'COOK-{i}-: POT:-{shared.servings}- is full, I do not cook.')

        if shared.servings == PORTIONS_COUNT and shared.cooks_count == CHEFS_COUNT:
            print(f'COOK-{i}-: Signals pot is full.\n')
            print(f'POT: {shared.servings} portions.\n')
            shared.cooks_count = 0
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
