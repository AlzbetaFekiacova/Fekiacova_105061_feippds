# TASK 03 - IMPLEMENT DINING PHILOSOPHERS PROBLEM

## TASK SPECIFICATION:

1. Implement solution of Dining Philosophers problem by:
    - A) usage of right-handed and left-handed philosophers
    - B) usage of token being passed after finish of eating to a neighbour
2. Source code must:   
  
   -  be compatible with Python 3.10

   - contain module header with module description, author's name and licence
    
   - be comprehensive and well documented
    
   - each function (class and its methods) must have docstring in PEP 257
    
   - PEP 8
2. Test your implementation.
3. Write documentation. Documentation should contain all necessary details about the implementation. 
4. Explain difference between your implementation and solution with a waiter.
---
## TASK SOLUTION:

Source code contains implementation of a solution for the Dining Philosophers problem with usage of left-handed philosopher. The implementation can be found in file [philosophers.py](https://github.com/AlzbetaFekiacova/Fekiacova_105061_feippds/blob/03/philosphers.py)

To execute the program you need to have  `fei.ppds` module installed. It can be done via `pip install --user fei.ppds`. Source code contains `if __name__ == "__main__"` idiom, so the program will be executed when you run the file. When you run the file, 5 threads will be created. One thread represents left-handed philosopher and others the right-handed ones. The treads execute their function in a loop. Default number of runs is set to 10.
### What is the Dining Philosophers problem?

Dining Philosophers problem was introduced by Dijkstra in 1965 to illustrate the challenges of avoiding deadlock.  
Hoare modified the problem to form that we know today and that is object of out task. The problem is based on following:

- 5 philosophers are sitting around a round table
- each philosopher has his own place
- each philosopher has his own plate
- between each plate is a fork
- meal must be eaten with two forks
- each philosopher may only alternate between eating or thinking

![img.png](problem_img.png)

On the picture above, we see that there is not enough of the forks for each of them to eat.

The object of the problem is how to design a concurrent algorithm such that no philosopher would starve and each of the philosophers may alternate between eating and thinking forever.