input = [1, 2, 3, 2.5]
weights = [[0.2, 0.8, -0.5, 1.0],
           [0.5, -0.91, 0.26, -0.5],
           [-0.26, -0.27, 0.17, 0.87]]
bias = [2, 3, 0.5]

final_output = []

for sweights, sbias in zip(weights, bias):
    #sweights as a list, sbias as a value
    neuron_value = 0
    for sinput, wweights in zip(input, sweights):
        #sinput as a value, wweights as a value
        neuron_value += sinput*wweights
        
    neuron_value += sbias
    final_output.append(neuron_value)
    
print(final_output)
