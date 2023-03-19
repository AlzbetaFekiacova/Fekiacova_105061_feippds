# BIG TASK: TASK 04 - IMPLEMENT FEASTING SAVAGES PROBLEM

## TASK SPECIFICATION:
1.  Implement solution for Feasting Savages problem with one or multiple cooks.
2.  Source code must:
   -  be compatible with Python 3.10

   -  contain module header with module description, author's name and licence
    
   -  be comprehensive and well documented
    
   -  each function (class and its methods) must have docstring in PEP 257
    
   -  PEP 8 
3.  Use multiple print functions to demonstrate correct functionality of your solution.
4.  Test your implementation.
  
5.  Write documentation. Documentation should contain all necessary details about the implementation.
  
6.  Explain usage of synchronisation mechanisms on examples from your code.
---
## TASK SOLUTION:
Source code contains implementation of a solution for the Feasting Savages problem with multiple chefs. The implementation can be found in file [feasting_savages.py](https://github.com/AlzbetaFekiacova/Fekiacova_105061_feippds/blob/04/feasting_savages.py)

To execute the program you need to have  `fei.ppds` module installed. It can be done via `pip install --user fei.ppds`. Source code contains `if __name__ == "__main__"` idiom, so the program will be executed when you run the file. When you run the file, 8 threads will be created. 5 threads represent the savages, the remaining three represent chefs. The treads execute their function in an infinite loop.

### What is the Feasting Savages problem?
The Feasting Savages problem is another example of synchronisation problem in which we need to solve problem of mutual exclusion of different types of processes during program execution.

#### Problem definition:
Savages in Equatorial Guinea are very social and advanced type of savages.
Not only do they always eat together every day, but they also have excellent
chefs who prepare delicious vegetarian stew. However, they need a
reliable system in which all their actions will be announced. The multiple rules they follow are:
   -   Savages always eat together. The one, who arrived last, signals them that they are all and that they can start to feast.
   -   Each of the savages takes his/her own portion until the pot is empty.
   -   The one savage, that notice that the pot is empty, notifies the chefs that new meal must be cooked.
   -   The savages wait for the chefs to finish cooking.
   -   Chefs:
     -   In case of multiple chefs, each chef always cook only one portion and puts it into the shared pot.
     -   In case of one chef, the chef cooks full pot.
   -   If the pot is full, the savages may start to feast again.
   -   The process is repeated in an endless cycle.

![](savages_vegetarian.png)

### Implementation
```python
class Shared:
    def __init__(self, servings):
        self.savages_mutex = Mutex()
        self.chefs_mutex = Mutex()
        self.pot_portions = servings

        self.full_pot = Event()
        self.empty_pot = Event()

        self.barrier_1 = SimpleBarrier(SAVAGES_COUNT)
        self.barrier_2 = SimpleBarrier(SAVAGES_COUNT)

        self.barrier_1_cooks = SimpleBarrier(CHEFS_COUNT)
        self.barrier_2_cooks = SimpleBarrier(CHEFS_COUNT)

        self.cooks_count = 0      
```
The class Shared has been created and used to represent multiple information needed to be shared between the savages and the chefs. In the code snippet, we see the constructor of the class. I will explain what each of the attribute is used for in few lines.

We need a variable to represent the shared pot. It is by variable pot_portions. At the program execution it is initialised to 0, as the chefs need to cook the meal first.

As savages and cooks modify the content of the pot, we need to guarantee the integrity of the number of portions. That is the reason why we weed two mutexes, one for the savages eating from the pot (decreasing the number of portions) and the other one for the chefs, who are putting portions to the pot(increasing the number of portions).

In the task definition, it was mentioned that the savages eat only when they are together. For such a behavior we need a barrier.

For the chefs, as I understood from the task assignment, their behaviour was not specified, but to make the implementation easier it was recommended to force such a behavior also for the chefs. That is the reason why there is also another barrier for the chefs.

The last thing we need is something for the signalisation. For the savages to notify the chefs, that the pot is empty and for the chefs to notify the savages that the pot is full, and they can feast.

Last but not least, there is a variable cooks_count, that represents how many cooks have cooked or had a look at the full pot.

#### Savage behaviour
In this section I will explain the function that represents behaviour of the savages. The control prints have reduced to make the code shorter. The commentaries have been added for better explanation.
```python
    while True:
        # the savages are waiting for each other
        shared.barrier_1.wait()
        shared.barrier_2.wait()
        shared.savages_mutex.lock() # integrity of the pot
        if shared.pot_portions == 0: # there is no more portions 
            shared.empty_pot.signal() # signal to the chefs that the pot is empty
            shared.full_pot.clear() # clear the event so it can be used again
            shared.full_pot.wait() # wait for the pot to be full

        shared.pot_portions -= 1 # take a portion 
        shared.savages_mutex.unlock() # integrity have been satisfied
        eat(i) # feast
```



## Sources
- [Seminar 2023-04](https://www.youtube.com/watch?v=54zi8qdBjdk&ab_channel=Mari%C3%A1n%C5%A0ebe%C5%88a)
- [Seminar 2022-05](https://www.youtube.com/watch?v=iotYZJzxKf4&ab_channel=Paraleln%C3%A9programovanieadistribuovan%C3%A9syst%C3%A9my)
- [GitHub of the course PPDS](https://github.com/tj314/ppds-2023-cvicenia)