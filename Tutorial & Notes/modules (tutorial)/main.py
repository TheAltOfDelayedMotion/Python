import module as m #import whole module
from module import function1 #you dont have to type module.______ if you import the specific function 

#call files in the same directory into the code
#you can use functions or classes defined in the modules

n = int(input('Please type 5 here: '))
if m.ncheck(n):
    print('Number 5 Recieved')

else:
    print('You did not type 5')

text = input("What would you like to say? ")
number = int(input("Enter a number: "))
m.function1(text, number)