import numpy as np

inputs = [[1, 2, 3, 2.5],
          [2.0, 5.0, -1.0, 2.0],
          [-1.5, 2.7, 3.3, -0.8]]

# Now you must think of each dimension in the input array as one batch - feeding into the entire neuron input layer
# So if you have 4 input neurons, n1 = 1, n2 =2, n3 = 3, n4 =2.5
# Then, in the second dimension, n1 = 2.0, n2 = 5.0, n3 = -1.0, n4 = 2.0

weights =  [[0.2, 0.8, -0.5, 1.0],
           [0.5, -0.91, 0.26, -0.5],
           [-0.26, -0.27, 0.17, 0.87]]

# Now for weights, you must think of each dimension to be a single hidden layer's neuron connection with the entire input layer
# So 0.2 is the weight for input 1 to neuron 1, 0.8 is the weight for input 2 to neuron 1, -0.5 is the weight for input 3 to neuron 1, and 1.0 is the weight for input 4 to neuron 1

bias = [2, 3, 0.5]

# each dimension in the bias refers to one entire layer of biases of the hidden layer neurons (for neurons in the same hidden layer, they will have the values of the biases found in the same dimension)

final_output = []

#To solving this problem, you can do it like this
for dimension in inputs:
    #inputs is now a 1D array
    final_output.append(np.dot(weights, dimension) + bias)
    
print(np.array(final_output))

# or like this
print(np.dot(inputs, np.array(weights).T) + bias)

#if you visualise what you are doing in the first approach to the problem, you are simply taking each input dimension and multiplying it with each weight dimension x 3 (for each for loop)
# however, you can easily do it with matrix multiplication if you just transpose/flip the weights matrix. to do that, you need to make the matrix into a numpy array/matrix and use transpose (or .T)
# when you transpose, the columns of the matrix becomes the weights of a singular neuron
# https://www.youtube.com/watch?v=TEWy9vZcxW4& 14:43 he does a good explanation