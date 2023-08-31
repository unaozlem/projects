# My poor solution
numbers = range(100)
print(numbers)

for x in numbers:
  if x % 3 == 0 and x % 5 == 0:
    print("FizzBuzz")
  elif x % 3 == 0:
    print("Fizz")
  elif x % 5 == 0:
    print("Buzz")
  else:
    print(x)


#for i in range(101):
#  print(i, 'Fizz'*(i%3==0) + 'Buzz'*(i%5==0))