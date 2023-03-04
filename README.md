# TASK 02 - IMPLEMENT BARBER PROBLEM

## TASK SPECIFICATION:

1. Implement Barber problem with overtaking. Source code must:   
  
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

Source code contains implementation of Barber problem. The implementation can be found in file [barber_shop.py](https://github.com/AlzbetaFekiacova/Fekiacova_105061_feippds/blob/02/barber_shop.py)

To execute the program you need to have  using `fei.ppds` module installed. It can be done via `pip install --user fei.ppds`. Source code contains `if __name__ == "__main__"` idiom, so the program will be executed when you run the file. When you run the file, n number of threads will be created. 1 represents the barber and the remaing n - 1 represent customers (currently 5). Both barber and the customers perform their functions in an infinite loop.
