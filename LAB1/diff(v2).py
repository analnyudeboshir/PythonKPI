import sys
print 'Python', sys.version
print "Hello, World!"
result = 7 / 2
print"7 / 2 =", result
s = 'Hello'
print type(s)
u = u'Hello'
print type(u)
for i in xrange(5):
    print i
name = raw_input("Enter your name: ")
print"Hello,", name
try:
    result = 10 / 0
except ZeroDivisionError, e:
    print "Error:", e 
num = 2 ** 64
print type(num)
d = {'a': 1, 'b': 2, 'c': 3}
print d.keys() 
print d.values() 
print d.items() 
a = [1, 2, 3]
b = [4, 5, 6]
z = zip(a, b)
print z 
print [1, 2] < 'abc' 
it = iter([1, 2, 3])
print it.next()