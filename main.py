import time

def fib(n):
    if n == 0 or n == 1:
        return n
    return fib(n - 1) + fib(n - 2)

def profile_cpu(n = 30):
    start = time.time()
    fib(n)
    return time.time() - start()
