import numpy as np

np.random.seed(0)

X = [[1, 2, 3, 2.5],
     [2.0, 5.0, -1.0, 2.0],
     [-1.5, 2.7, 3.3, -0.8]]

class Layer_Dense:
    def __init__(self, ninput, nhneurons):
        self.weights = 0.10*np.random.randn(ninput, nhneurons) #multiply by 0.10 to make sure that we return weights in between -1 and +1 
        self.biases = np.zeros((1, nhneurons))
        
    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases 
        #return self.output you dont actually need return, you can just call the variable output
    
layer_1 = Layer_Dense(4, 5)
layer_2 = Layer_Dense(5, 2)

layer_1.forward(X)
layer_2.forward(layer_1.output)
print(layer_2.output)