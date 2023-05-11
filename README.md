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

### Implementation

#### Conversion functions

For gray scale conversion I have used specific formula, that is the same for execution both on CPU and GPU.
```python
def convert_image(image, x, y):
    r = image[x, y, 0]
    g = image[x, y, 1]
    b = image[x, y, 2]
    return 0.299 * r + 0.587 * g + 0.114 * b      
```
This function server to compute gray scaled value of a pixel on position x, y in the image. 

Then I have defined 2 functions, rgb_to_gray_cpu and rgb_to_gray_cuda. 

The function executed on CPU has one parameter, image. It executes two for loops to travers though all the pixels of the input image and call the convert_image (explained above) on each of the image pixel.

The function executed on GPU has two parameters, the input_image and output_image as the function cannot return anything. By calling cuda.grid(2) we are able to determine the current thread's position based on the grid and block dimensions. 
Then we can execute check whether the computed position is valid position in the image. If it is, convert_image (explained above) can be called with the computed x and y positions and the output is saved to the output_image.



-----------------------
## Sources
[Images source](https://pixabay.com/)
