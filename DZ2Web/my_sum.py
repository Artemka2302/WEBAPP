def my_sum(*a):
    return sum(a)


if __name__ == "__main__":
    n = int(input(''))
    a = list(map(int, range(n)))
    print(my_sum(*a))