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
