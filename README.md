# TASK 05 - CUDA

## TASK SPECIFICATION:
1. Load image in jpg format, converts it to grayscale with
using GPU and write to a new file.
2. Load image in jpg format, converts it to grayscale with
using the CPU and write to a new file.
3. Convert a large number of images with both methods. Record it
are the average conversion times.
4. Source code must:
   -  be compatible with Python 3.10

   -  contain module header with module description, author's name and licence
    
   -  be comprehensive and well documented
    
   -  each function (class and its methods) must have docstring in PEP 257
    
   -  PEP 8 
5. Write documentation. In the documentation, include information about the assignment, instructions for starting and
CPU and GPU conversion comparison. Add
several examples of converted images. Don't forget to mention what
computation have been used for the conversion.
-------------------
## TASK SOLUTION:
Source code contains implementation of converting colour image to grayscale both on CPU and GPU. The implementation can be found in file [cuda_task.py](https://github.com/AlzbetaFekiacova/Fekiacova_105061_feippds/blob/05/cuda_task.py).
Python version 3.10.x is necessary.
To execute the program you need to have multiple modules installed: 
-  `fei.ppds`  module
-   `numpy`  module
-  `matplotlib`  module
-  `matplotlib`  module
-  `numba`  compiler


Installation can be done via `pip install` in the console or directly through PyCharm IDE through Python Packages. Source code contains `if __name__ == "__main__"` idiom, so the program will be executed when you run the file. 
When you run the code, first gray scaling of 20 test images on CPU is executed, then gray scaling on GPU is executed on the same set of testing images. Converted images are stored into separate files.
## Sources
[Images source](https://pixabay.com/)
