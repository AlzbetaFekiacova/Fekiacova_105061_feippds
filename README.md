# TASK 02 - IMPLEMENT BARBER PROBLEM

## TASK SPECIFICATION:

1. Implement Barber problem with overrunning. Source code must:   
  
   -  be compatible with Python 3.10
    
   - contain module header with module description, author's name and licence
    
   - be comprehensive and well documented
    
   - each function (class and its methods) must have docstring in PEP 257
    
   - PEP 8
2. Test your implementation.
3. Write documentation. Documentation should contain all necessary details about the implementation. Example of your program input must also be part of it.
4. In your final solution, set number of customers to 5 and number of waiting seats to 3.
---
## TASK SOLUTION:

Source code contains implementation of Barber problem with outrun. The implementation can be found in file [barber_shop.py](https://github.com/AlzbetaFekiacova/Fekiacova_105061_feippds/blob/02/barber_shop.py)

To execute the program you need to have  using `fei.ppds` module installed. It can be done via `pip install --user fei.ppds`. Source code contains `if __name__ == "__main__"` idiom, so the program will be executed when you run the file. When you run the file, n number of threads will be created. 1 represents the barber and the remaing n - 1 represent customers (currently 5). Both barber and the customers perform their functions in an infinite loop.

### What is Barber problem?
Barber problem is a synchronisation problem introduced by Edsger Dijkstra in 1965. 
The problem is based on a barber shop with following characteristics:
   -  barber shop has two rooms:
      - waiting room for N clients
      - barber's room
   - if there is no client waiting, barber sleeps
   - if clients enters:
      - and all the seats in the waiting room are taken, the client leaves
      - if barber is cutting hair, but there is a free seat in the waiting room, the client sits and waits to have his hair done
      - if the barber is sleeping, the client wakes him up, take a seat and wait for the barber to wake up and cut his hair

The main task is to handle the coordination between the barber and the customers.

### Implementation

```python
from fei.ppds import Semaphore, Mutex


class Shared(object):
    def __init__(self):
        self.mutex = Mutex()
        self.waiting_room = 0
        self.customer = Semaphore(0)
        self.barber = Semaphore(0)
        self.customer_done = Semaphore(0)
        self.barber_done = Semaphore(0)
```

The class shared represents a barber shop. In the code above, we see the constructor of the class. It has 6 attributes to represent all the necessary information about the barber shop.

- attribute mutex (Binary Semaphore = Mutex):
  
  - protects integrity of counter
    
- attribute waiting_room (int):
  
  - counter
    
  - it represents number of how many people are already in the barber shop
    
  - it can have values from 0 to N (number of seats in the shop)
    
- attribute customer (Semaphore):
  
  - represent customer
    
  - customer sits in the waiting room (if there is a seat) and waits until the barber calls him
    
- attribute barber (Semaphore):
  
  - represents barber
    
  - barber waits for the customer come, or he sleeps
    
- attribute customer_done (Semaphore):
  
  - after the haircut is done, it signalises the barber that he is content with the haircut, finished and waits for the barber to finish (e.g. clean the room)
    
- attribute barber_done (Semaphore):
  
  - after the barber finishes cutting hair, semaphore signals to customer that the barber has finished and waits for the customer to finish (e.g. takes his stuff) and leave

This class provides us everything we need for implementation. All we need is to implement behaviour of the barber and the customers. 
#### Customer

```
customer():
    mutex.lock()

    if waiting_room == N:
        mutex.unlock()
        balk()
    else:
        waitng_room += 1
        mutex.unlock()

        customer.signal()
        barber.wait()
    
        get_haircut()
    
        customer_done.signal()
        barber_done.wait()

        mutex.lock()
        waiting_room -= 1
        mutex.unlock()
    
```
Barber
```
barber():
    customer.wait()
    barber.signal()

    cut_hair()

    customer_done.wait()
    barber_done.signal()
```
The first pseudocode above represents behaviour of a customer, the second one represents behaviour of a barber.

For customer, we need to protect the integrity of the counter, as entering the barber shop or leaving it changes the number of available seats. That is why need to lock the mutex before accessing and modifying the number of waiting the customers.  
If customer wants to sit in the Barber shop, he has to check whether there is any seat left. If there is none, the customer leaves and wait some time before checking again. This behaviour is represented by function balk().  
If there is a seat left, the customer sits and gives a signal that he is there and is waiting for the barber.  
Then comes Rendez-vous or mutual signalisation. On customer side, he signals the barber that customer is here and waiting for the barber to call him. On barber's side. The barber is waiting for the customer and signaling him that he is free to take care of his hair.  
After the Rendez-vous happens, the action of cutting hair and getting hair cut can happen.  
After the hair is cut, another Rendez-vous must happen.  
The customer signals the barber that he is content with his hairstyle and waits for barber to finish. Barber, on the other hand, is waiting for the customer to finish and signaling that he is done with cutting the hair.  
After this Rendez-vous is successful, the customer may leave.  
He again needs to lock the mutex, so the integrity of the counter stays protected. Leave the room, reduce the counter by one and of course, unlock the mutex again.

### Sources:
- [Lecture 2022-02](https://www.youtube.com/watch?v=sR5RWW1uj5g&ab_channel=Paraleln%C3%A9programovanieadistribuovan%C3%A9syst%C3%A9my)
  
- [Seminar 2021-06](https://www.youtube.com/watch?v=IOeO6RDhhac&ab_channel=Paraleln%C3%A9programovanieadistribuovan%C3%A9syst%C3%A9my)
  
- [Seminar 2023-03](https://elearn.elf.stuba.sk/moodle/pluginfile.php/75802/mod_resource/content/1/PPDS_cv3.pdf)
  
- [A simple guide to The Sleeping Barber Problem](https://www.youtube.com/watch?v=cArBsUK1ufQ&ab_channel=EliTadeo)