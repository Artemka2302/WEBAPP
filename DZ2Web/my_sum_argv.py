import sys

def my_sum_argv():
    """
    Функция берет аргументы из командной строки
    и возвращает их сумму
    """
    args = sys.argv[1:]  # получаем аргументы командной строки
    
    if not args:
        return 0
    
    # Преобразуем строки в числа
    numbers = [float(arg) for arg in args]
    
    return sum(numbers)


if __name__ == "__main__":
    result = my_sum_argv()
    print(result)