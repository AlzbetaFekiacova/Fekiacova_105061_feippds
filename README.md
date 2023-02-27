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

To execute the program you need to have  using `fei.ppds` module installed. It can be done via `pip install --user fei.ppds`. Source code contains `if __name__ == "__main__"` idiom, so the program will be executed when you run the file. When you run the file, n number (currently 5) of threads will be created. Each of this thread will execute function named process, that simulates a process. The function process contains bakery algorithm implementation along side with execution of critical section. The threads are created and executed in a loop. Default number of runs is set to 10.

### What is Bakery Algorithm?
Bakery algorithm is a algorthm that provides software solution for the problem of mutual exclusion. It is more suitable for larger number of processes (threads) compared to the Peterson algorithm. In comparison to the Ticket algorithm it does not depend on any instruction to be atomic. 


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

#### Correctness of Bakery Algorithm

The solution for problem of mutual exclusion must satisfy these four rules. I will provide the rule first, then how it applies to the Bakery algorithm.

1. In the critical section, no more than one process may be executed at one time.
   - In Bakery algorithm this rule is satisfied by only letting the process with the lowest ticket number (value in the num array) to enter the critical section.
   - If more than one process have the same ticket number, the process with lower process id enters the critical section. As the process id is unique for each process, this rule is fulfilled.
   - Other process have to wait for their assigned ticket number to become the new lowest.
2. Process that is being executing outside the critical section cannot prevent other processes entry to the critical section.
   - This rule is satisfied because in the Bakery algorithm only the process itself can assign its own ticket number.
   - Other processes cannot change the values assigned in the num array of other processes, so they cannot prevent other processes entry the critical section.
3. The decision about the entry must come within a deadline.
   - As the number of processes is n, that means that there is a final number of processes. 
   - As only one process may enter the critical section, other processes must wait. 
   - They are waiting in two loops.
     - First loop
       - If a process is waiting in the first loop, it means that some other process is getting his ticket number assigned.
       - We can believe that the planner is fair and the process that got replanned while getting the ticket will be planned in some time and will be able to finish getting the ticket.
     - Second loop
         - If a process is waiting in the second loop it can mean two things.
         - It can mean that its ticket number is not the current lowest from the waiting process.
         - It can also mean that the process ticket is the lowest, but the there is some other process with the same ticket number. In that case the process with the lower process id may enter the critical section.
         - As I mention earlier, we can believe that the planner is fair, it plans the processes reasonably, and the process with the lowest ticket number will execute the critical section, change its ticket value to zero, so the process with next new lowest can enter the critical section and this wil also be planed in fair time and this will be repeated until all the waiting process have executed the critical section.
   - Based on those two loops, and their breaking to enter the critical section, we can say that the decision about the entry will come within a deadline.
4. Processes entering the critical section cannot assume anything about the mutual timing (planning).
   - This rules tells us about that the decision for a process must come in a bounded time. It does not tell when, or how long the bounded time should be. It just tells us, that the process will eventually enter the critical section.
   - However, we can't predict when the interruption comes. We cannot say how the planner is going to plan the processes. So in the worst case scenario, the process may not ever get to the critical section, as it may always be replanned. It can always get replanned during getting the ticket and by this, also block other processes from entering the critical section, but this scenario is highly unlikely. 
   - As probability of that happening is very low and rare, we can say, that Bakery algorithm satisfies the fourth rule.
---
## Conclusion
The Bakery algorithm is a correct solution to mutual exclusion problem for multiple number of process. It fulfills all four necessary conditions of a correct implementation. 
