a = '1'
b = '2'
try:
    print(a / b)
except TypeError:
    print(int(a)/int(b))
