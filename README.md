# TASK 01 - IMPLEMENT BAKERY ALGORITHM

## TASK SPECIFICATION:

1. Implement Bakery Algorithm. Source code must:
   - be compatible with Python 3.10
    
   - contain module header with module description, author's name and licence
    
   - be comprehensive and well documented
    
   - each function (class and its methods) must have docstring in PEP 257
    
   - PEP 8
    
2. Test your implementation
3. Write documentation. Documentation should contain all necessary details about the implementation. Explain reason why Bakery algorithm is correct solution for mutual exclusion problem.
---

## TASK SOLUTION:

Source code contains implementation of Bakery algorithm. The implementation can be found in file [bakery_algorithm.py](https://github.com/AlzbetaFekiacova/Fekiacova_105061_feippds/blob/01/bakery_algorithm.py "bakery_algorithm.py")

To execute the program just run the file. It contains `if __name__ == "__main__"` idiom, so the program will be executed when you run the file. When you run the file, n number (currently 5) of threads will be created. Each of this thread will execute function named process, that simulates a process. The function process contains bakery algorithm implementation along side with execution of critical section. The threads are created and executed in a loop. Default number of runs is set to 10.

### What is Bakery Algorithm?
Bakery algorithm is a algorthm that provides software solution for the problem of critical section. It is more suitable for larger number of processes (threads) compared to the Peterson algorithm. In comparison to the Ticket algorithm it does not depend on atomic instruction. 


