#Number to text
lists = {
    "0" : "zero", 
    "1" : "one", 
    "2" : "two", 
    "3" : "three", 
    "4" : "four", 
    "5" : "five", 
    "6" : "six",              
    "7" : "seven", 
    "8" : "eight", 
    "9" : "nine"
    }

numbers = str(input("Phone Number: "))
x = ""

for number in numbers:
  if number == " ":
    numbers.replace(" ", "")
  else:
    x += lists[number] + " "

print(x)