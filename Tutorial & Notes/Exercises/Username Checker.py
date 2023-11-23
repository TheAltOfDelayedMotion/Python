#Username Checker 
#Chapter: Comparison Operators

username = input('Enter your username here: ')

while True:
  if len(username) <= 3:
    print('Username too short!')
    username = input('Enter your username here: ')

  elif (len(username) > 3) and not (len(username) > 10):
    print('Username available!')
    break

  else:
    print('Username too long!')
    username = input('Enter your username here: ')