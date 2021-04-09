import time
from StockCalculation import main as test


def use_time(fun):
    def wrapper(*args):
        start = time.time()
        res = fun(*args)
        print("{name}:time is {time}ms".format(name=wrapper.__name__, time=(time.time()-start)*1000))
        return res
    return wrapper


@use_time
def main():
    test(1001, 0)
    test(1001, 1)


if __name__ == '__main__':
    main()
