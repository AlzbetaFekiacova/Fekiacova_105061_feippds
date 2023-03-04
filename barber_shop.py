""" This module contains an implementation of Barber problem."""

__authors__ = "Marián Šebeňa, Matus Jokay, Alzbeta Fekiacova"
__email__ = "mariansebena@stuba.sk, xvavro@stuba.sk, xfekiacova@stuba.sk"
__license__ = "MIT"

import fei.ppds
from fei.ppds import Mutex, Thread, Semaphore, print
from time import sleep
from random import randint

C: int = 5
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
    # TODO: Simulate time and print info when customer gets haircut
    fei.ppds.print(f'Customer {i} is getting his hair cut.')
    sleep(3)


def cut_hair():
    # TODO: Simulate time and print info when barber cuts customer's hair
    fei.ppds.print(f'Barber is cutting hair')
    sleep(4)


def balk(i: int):
    # TODO: Represents situation when waiting room is full and print info
    fei.ppds.print(f'Customer {i} cannot enter the waiting room, room is full.')
    sleep(5)


def growing_hair(i: int):
    # TODO: Represents situation when customer wait after getting haircut. So hair is growing and customer is sleeping for some time
    fei.ppds.print(f'Customer {i} waits, hair is growing.')
    sleep(1)


def customer(i: int, shared: Shared):
    global N
    # TODO: Function represents customers behaviour. Customer come to waiting if room is full sleep.
    # TODO: Wake up barber and waits for invitation from barber. Then gets new haircut.
    # TODO: After it both wait to complete their work. At the end waits to hair grow again

    while True:
        # TODO: Access to waiting room. Could customer enter or must wait? Be careful about counter integrity :)

        shared.mutex.lock()
        fei.ppds.print(f'Customer {i} entered the waiting room. \n'
                       f'There are {shared.waiting_room} customers.')
        if shared.waiting_room == N:
            shared.mutex.unlock()
            balk(i)

        else:
            shared.waiting_room += 1
            fei.ppds.print(f'Customer {i} sat in the waiting room')
            shared.mutex.unlock()

            shared.customer.signal()
            shared.barber.wait()
            # TODO: Rendezvous 1
            get_haircut(i)
            # TODO: Rendezvous 2
            shared.customer_done.signal()
            shared.barber_done.wait()
            fei.ppds.print(f'Customer {i} finished getting a haircut.')
            # TODO: Leave waiting room. Integrity again

            shared.mutex.lock()
            shared.waiting_room -= 1
            fei.ppds.print(f'Customer {i} left the room.')
            shared.mutex.unlock()
            growing_hair(i)


def barber(shared: Shared):
    # TODO: Function barber repres
    #  ents barber. Barber is sleeping.
    # TODO: When customer come to get new hair wakes up barber.
    # TODO: Barber cuts customer hair and both wait to complete their work.

    while True:
        shared.customer.wait()
        shared.barber.signal()

        # TODO: Rendezvous 1

        cut_hair()
        # TODO: Rendezvous 2
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


# TODO: Global variables C = 5 numOfCustomers N = 3 sizeOfWaitingRoom


if __name__ == "__main__":
    main()
