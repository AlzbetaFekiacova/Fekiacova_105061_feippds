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


### Implementation
Bakery algorithm uses two globally shared arrays between all the processes.  
The length of the arrays is determined by the number of running processes. The arrays are:
- global array num
  - values initialized to 0
- global array choosing
  - values initialized to False
  
The principle of Bakery algorithm stands on the usage of shared num array. Each process has its corresponding index in the num array. The value on the corresponding index of the process represents its ticket (order number).

When a process starts to execute the process function, its corresponding value in the num array changes. The incoming process num value will be assigned to the highest existing value in the num array + 1. So the entered process ticket number will be the new highest value in the array. Before the assigning of the process num value, corresponding value in the array choosing n becomes True. After the assignment, the value in the choosing array becomes False again. After the process ticket number has been assigned it has to wait until its time comes to enter the critical section.

The array choosing array also takes care that if any process is currently being assigned a ticket, no process will enter the critical section. 
When any process is being assigned a ticket, corresponding value in the choosing array of the process is True, other processes have to wait for the assigment of the ticket to finish.
This ensures us that each time the correct number of waiting processes and their correct ticket numbers are being compared.

The remaining question is: What process may enter the critical section? 

The answer is rather simple. The process with the lowest ticket number may, and will enter the critical section. 
If more processes have the same ticket number, then the process with lower process id is favored and may enter the critical section. 

After the execution of the critical section, the corresponding ticket value in the num array of the process is changed back to its starting value, 0. So the process can get a new ticket if it wants to enter the critical section again.
