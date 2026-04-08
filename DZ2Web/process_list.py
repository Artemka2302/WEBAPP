import time

def process_list(arr):
    """Обычная функция с циклом"""
    if 1 <= len(arr) <= 103:
 
        result = []
        for i in arr:
            if i % 2 == 0:
                result.append(i**2)
            else:
                result.append(i**3)
        return result
    else:
        raise ValueError


def process_list_comp(arr):
    """Функция с list comprehension"""
    if 1 <= len(arr) <= 103:
        return [i**2 if i % 2 == 0 else i**3 for i in arr]
    else:
        raise ValueError


def process_list_gen(arr):
    """Функция-генератор"""
    if 1 <= len(arr) <= 103:
        for i in arr:
            if i % 2 == 0:
                yield i**2
            else:
                yield i**3
    else:
        raise ValueError


if __name__ == '__main__':
    test_arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    start = time.time()
    process_list(test_arr)
    print(f"Обычная: {time.time() - start:.8f} сек")
    start = time.time()
    process_list_comp(test_arr)
    print(f"List comprehension: {time.time() - start:.8f} сек")
    start = time.time()
    list(process_list_gen(test_arr))
    print(f"Генератор: {time.time() - start:.8f} сек")
    
    """
    List comprehension обычно быстрее обычного цикла,
    генератор медленнее при преобразовании в список
    """