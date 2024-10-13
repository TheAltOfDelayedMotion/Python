input = [1, 2, 3]
weights = [[0.5, 0.6, 0.7],
           [0.7, -0.4, 3],
           [6, -0.2, -1]]
bias = [2, -2 ,5]

for sinput, sweight in zip(input, weights):
    print(sinput)
    print(sweight)

#basically zip justs like takes the two items and breaks them down (idk how to say)