import random

def f(x):
    return x**2 - 1

def f1(x):
    return 2*x



def newtons_method(x0, f, f1, e):
    #f1 - производная
    x0 = float(x0)
    while True:
        x1 = x0 - (f(x0) / f1(x0))
        if abs(x1 - x0) < e:
            return x1
        x0 = x1

print(newtons_method(random.random()*20-10, f, f1, 1e-3))