""" This module contains an implementation of Barber problem."""

__authors__ = "Marián Šebeňa, Matúš Jókay, Alžbeta Fekiačová"
__email__ = "mariansebena@stuba.sk, xvavro@stuba.sk, xfekiacova@stuba.sk"
__license__ = "MIT"

import fei.ppds
from fei.ppds import Mutex, Thread, Semaphore, print
from time import sleep
from random import randint

# global variable representing total number of customers
C: int = 5
# global variable representing number of seats in the Barber shop
N: int = 3


class Shared(object):

    def __init__(self):
        # TODO : Initialize patterns we need and variables
        self.mutex: Mutex = Mutex()
        self.waiting_room: int = 0

        # self.customer = Rendezvous is implemented as ?
        # self.barber = Rendezvous is implemented as ?
        # self.customer_done = Rendezvous is implemented as ?
        # self.barber_done = Rendezvous is implemented as ?
        self.customer: Semaphore = Semaphore(0)
        self.barber: Semaphore = Semaphore(0)
        self.customer_done: Semaphore = Semaphore(0)
        self.barber_done: Semaphore = Semaphore(0)


def get_haircut(i: int):
    """Simulate time and print info when customer gets haircut."""
    fei.ppds.print(f'Customer {i} is getting his hair cut.')
    sleep(3)


def cut_hair():
    """Simulate time and print info when barber cuts customer's hair."""
    fei.ppds.print(f'Barber is cutting hair')
    sleep(4)


def balk(i: int):
    """Simulate time and print info when the waiting room is full."""
    fei.ppds.print(f'Customer {i} cannot enter the waiting room, room is full.')
    sleep(5)


def growing_hair(i: int):
    """Simulates time and print info when the customer had is hair done and his hair is growing again."""
    fei.ppds.print(f'Customer {i} waits, hair is growing.')
    sleep(1)


def customer(i: int, shared: Shared):
    """Simulates behaviour of a customer in an infinite loop.

    Arguments:
        i      -- customer id
        shared -- Shared object which represents the barber shop
    """
    global N

    while True:
        shared.mutex.lock()
        fei.ppds.print(f'Customer {i} entered the waiting room. \n'
                       f'There are {shared.waiting_room} customers.')
        if shared.waiting_room == N:
            # waiting room is full
            shared.mutex.unlock()
            balk(i)
        else:
            # customer sits
            shared.waiting_room += 1
            fei.ppds.print(f'Customer {i} sat in the waiting room')
            shared.mutex.unlock()

            # Rendez-vous 1
            shared.customer.signal()
            shared.barber.wait()

            get_haircut(i)

            # Rendez-vous 2
            shared.customer_done.signal()
            shared.barber_done.wait()

            fei.ppds.print(f'Customer {i} finished getting a haircut.')

            # leaving the barber shop
            shared.mutex.lock()
            shared.waiting_room -= 1
            fei.ppds.print(f'Customer {i} left the room.')
            shared.mutex.unlock()
            growing_hair(i)


def barber(shared: Shared):
    """Simulates behaviour of the barber in an infinite loop.

    Argument:
        shared -- Shared object which represents the barber shop
    """
    while True:
        # Rendez-vous 1
        shared.customer.wait()
        shared.barber.signal()

        cut_hair()

        # Rendez-vous 2
        shared.customer_done.wait()
        shared.barber_done.signal()

        fei.ppds.print(f'Barber is done cutting hair')


def main():
    shared = Shared()
    customers = []

    for i in range(C):
        customers.append(Thread(customer, i, shared))
    hair_stylist = Thread(barber, shared)

    for t in customers + [hair_stylist]:
        t.join()


if __name__ == "__main__":
    main()
