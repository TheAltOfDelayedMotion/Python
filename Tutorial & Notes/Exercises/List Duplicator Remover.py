
#Duplicator Remover (List)

strings = ['hello', 'hello', 'goodbye', 'wonderful', 'google', 'google', 'bye', 'jayden', 'davion', 'davion']

strings.sort()

count = -1
value = strings[count]

for string in strings:
  if string == value:
    print(f'Duplicated word removed: {string}')
    strings.remove(string)
  
  count += 1
  value = strings[count]

print(f'\nStorted list \n{strings}')

#Duplicator Remover THE WAY HE DID IT

numbers = [2, 2, 4, 6, 3, 4, 6, 1]
uniques = []

for number in numbers:
  if number not in uniques:
    uniques.append(number)

print(uniques)