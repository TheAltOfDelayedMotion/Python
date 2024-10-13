import numpy as np

inputs = [[1, 2, 3, 2.5],
          [2.0, 5.0, -1.0, 2.0],
          [-1.5, 2.7, 3.3, -0.8]]

# First Layer
weights =  [[0.2, 0.8, -0.5, 1.0],
           [0.5, -0.91, 0.26, -0.5],
           [-0.26, -0.27, 0.17, 0.87]]

biases = [2, 3, 0.5]

#Second Layer
weights2 = [[0.1, -0.14, 0.5],
            [-0.5, 0.12, -0.33],
            [-0.44, 0.73, -0.13]]

biases2 = [-1, 2, -0.5]

weights = np.array(weights)
weights2 = np.array(weights2)

#First Layer of Calculation
output1 = np.dot(inputs, weights.T) + biases
print(output1)
print("")

#       1      2       3
# 1 [[ 4.8    1.21   2.385]
# 2  [ 8.9   -1.81   0.2  ]
# 3  [ 1.41   1.051  0.026]] 
# Each dimension of the output is the output of the first hidden layer, and each value in the dimension is the output of 1 neuron in the first hidden layer for one specific batch

output2 = np.dot(output1, weights2.T) + biases2
print(output2)




