cube = lambda x: x ** 3

def fibonacci(n):
    if n < 1 or n > 15:
        raise ValueError("n должно быть от 1 до 15")
    
    fib_list = []
    a, b = 0, 1
    for _ in range(n):
        fib_list.append(a)
        a, b = b, a + b
    return list(map(cube, fib_list))

if __name__ == '__main__':
    n = int(input())
    if n < 1 or n > 15:
        print("Ошибка: n должно быть от 1 до 15")
    else:
        print(list(map(cube, fibonacci(n))))