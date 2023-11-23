

#Weight Converter Program
#Chapter Revision

import time 

print('Welcome to the Weight Converter Program')
lbskg = input('Please choose input choice: lbs / kg ').lower()

while True:
  if lbskg == 'lbs':
    lbs = True 
    kg = False
    print(f'You choose your input unit to be {lbskg}. ')
    break

  elif lbskg == 'kg':
    kg = True
    lbs = False
    print(f'You choose your input unit to be {lbskg}. ')
    break
 
  else:
    print("Invalid Choice! Please type a valid option: 'lbs' or 'kg' ")
    time.sleep(1)
    lbskg = input('Please choose input choice: lbs / kg ').lower()

while True: 
  try:
    weight = float(input('Please enter your weight: '))
    break

  except ValueError: 
    print('Please enter a number.')

if lbs: 
  weight = round(weight * 0.4535, 2)
  print(f'You are {weight}kg')

if kg:
  weight = round(weight / 0.4535, 2)
  print(f'You are {weight}lbs')
