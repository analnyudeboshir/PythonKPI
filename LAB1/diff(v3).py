import sys
print ('Python', sys.version)
print("Hello, World!")
result = 7 / 2
print("7 / 2 =", result) 
s = 'Hello'
print(type(s))
b = b'Hello'
print(type(b))
for i in range(5):
    print(i) 
name = input("Enter your name: ")
print("Hello,", name)
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print("Error:", e)
d = {'a': 1, 'b': 2, 'c': 3}
print(d.keys())
print(d.values()) 
print(d.items())   
a = [1, 2, 3]
b = [4, 5, 6]
z = zip(a, b)
print(z)
try:
    print([1, 2] < 'abc')
except TypeError as f:
        print("Error:", f);
it = iter([1, 2, 3])
print(next(it))