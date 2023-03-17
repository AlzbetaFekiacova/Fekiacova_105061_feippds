from fei.ppds import Thread, Mutex, Semaphore, print

from time import sleep

# savages
D: int = 3

# cooks
K: int = 1

# pot portions
H: int = 2


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
        self.mutex_1 = Mutex()
        self.mutex_2 = Mutex()
        self.servings = m
        self.full_pot = Semaphore(0)
        self.empty_pot = Semaphore(0)

        self.barrier_1 = SimpleBarrier(D)
        self.barrier_2 = SimpleBarrier(D)


def eat(i: int):
    print(f'Savage -{i}- started eating.')
    sleep(1)
    print(f'Savage -{i}- finished eating.')


def savage(i: int, shared: Shared):
    sleep(1)
    while True:
        shared.barrier_1.wait()
        shared.barrier_2.wait(each=f'savage -{i}-: before the dinner',
                              last=f'savage -{i}- we are all')
        shared.mutex_1.lock()
        if shared.servings == 0:
            print(f'Savage -{i}- signals pot is empty.')
            shared.empty_pot.signal()
            shared.full_pot.wait()
        print(f'Savage -{i}- takes a portion.')
        shared.servings -= 1
        shared.mutex_1.unlock()
        eat(i)


def cook(shared: Shared):
    while True:
        shared.empty_pot.wait()
        print(f'Cook cooks')
        sleep(1)
        print(f'cook cooked {H} portions --> pot')
        shared.mutex_2.lock()
        shared.servings += H
        shared.mutex_2.unlock()
        shared.full_pot.signal()


def main():
    """Run main."""
    print(f'NUMBER OF SAVAGES:{D}\nNUMBER OF COOKS:{K}\nPOT CAPACITY:{H}')
    shared: Shared = Shared(0)
    savages: list[Thread] = [
        Thread(savage, i, shared) for i in range(D)
    ]
    savages.append(Thread(cook, shared))

    for s in savages:
        s.join()


if __name__ == "__main__":
    main()
