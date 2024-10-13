import numpy as np

input = [[1, 2, 3, 2.5]]
weights = [[0.2, 0.8, -0.5, 1.0],
           [0.5, -0.91, 0.26, -0.5],
           [-0.26, -0.27, 0.17, 0.87]]
bias = [2, 3, 0.5]

final_product = []

for sweights, sbias in zip(weights, bias):
    final_product.append(np.dot(sweights, input) + sbias)
    
print(final_product)

#or you could also do it like that
print(np.dot(weights, input) + bias) 
#[4.8   1.21  2.385] now this saves it as an numpy array, not a python list


