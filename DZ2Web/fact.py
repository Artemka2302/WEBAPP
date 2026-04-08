import time


def fact_rec(n):
    if n < 1 or n > 10**5:
        raise ValueError("n должно быть от 1 до 100000")
    
    if n == 1:
        return 1
    return n * fact_rec(n - 1)


def fact_it(n):
    if n < 1 or n > 10**5:
        raise ValueError("n должно быть от 1 до 100000")
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


if __name__ == '__main__':
    # Сравнение скорости
    print("Сравнение скорости (n=500):")
    
    start = time.time()
    n = int(input(""))
    fact_it(n)
    print(f"Итерационно: {time.time() - start:.6f} сек", fact_it(n))
    
    start = time.time()
    n = int(input(""))
    print(f"Рекурсивно: {time.time() - start:.6f} сек", fact_rec(n))
