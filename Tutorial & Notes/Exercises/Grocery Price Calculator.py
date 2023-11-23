
#Grocery Price Calculator
#Chapter: For Loops (loops)
import time

print('''
    Welcome to the Grocery Price Calculator
    ''')
items = []
prices = []
booll = True

time.sleep(2)

while booll:
  choice = input('Would you like to add a product? [y/n]: ')

  if choice == 'y': 
    items.append(input('Enter a product name: '))
    prices.append(input('Enter the cost of the product: $'))
    print('\n')

  elif choice == 'n':
    print('Input of products have ended. \n')
    break

  else:
    print('Please input a valid choice!')



'''
items = ['Slices of Cheese', 'Slices of Ham', 'Apple', 'Orange']
prices = [5, 10, 3.20, 3.50]
'''

count = 0
total_price = 0

try:
  for item in items:
    print(f'Item No: {count + 1}')
    print(f'{item} costs ${prices[count]} \n')
    count += 1 

except TypeError:
  print('an unexpected error occured')

for price in prices:
  total_price += float(price)

total_price = str(total_price)
charc = len(str(total_price))

for letter in str(total_price):

  if letter == '.':
      
    for numbers in range(1  ,10):
        if total_price[charc - 1] == str(numbers):
          total_price = f'{str(total_price)}0'

    else:
      break

print(f'Total Cost: ${total_price}')

#Largest Number

numbers = [53, 6, 5, 2, 4, 7, 8, 10, 503]

max = numbers[0]
for number in numbers:
  if number > max:
    max = number

print(max)
