import random 
import math

def circle_square_mk(r,n):
    i = 0
    count = 0

    while i < n:
        x = random.uniform(-r,r)
        y = random.uniform(-r,r)

        if (pow(x, 2) + pow(y, 2)) < r**2:
            count+=1

        i+=1

    square_area = (2*r)**2
    circle_square = (count / n) * square_area    
    return circle_square

if __name__ == "__main__":
    r = 5
    n = 1000000

    func_area = circle_square_mk(r, n)
    real_area = math.pi * r**2
    error = abs(func_area - real_area)

    print(f"Оценка площади методом Монте-Карло: {func_area:.5f}")
    print(f"Точная площадь: {real_area:.5f}")
    print(f"Погрешность: {error:.5f}")