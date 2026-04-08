import subprocess
import pytest
import sys
import os
import tempfile
import shutil
# Для Windows
INTERPRETER = 'python'


def run_script(filename, input_data=None):
    proc = subprocess.run(
        [INTERPRETER, filename],
        input='\n'.join(input_data if input_data else []),
        capture_output=True,
        text=True,
        check=False
    )
    return proc.stdout.strip()

test_data = {
    'fact': [
        (5, 120),
        (3, 6),
    ],
    'fact_err':[
        (10 ** 6, ValueError), 
        (-5, ValueError)
    ],
    'show_employee': [
        ("Иванов Иван Иванович", 30000, "Иванов Иван Иванович: 30000 ₽"),
        ("Петров Петр", None, "Петров Петр: 100000 ₽"),  
        ("Сидоров", 0, "Сидоров: 0 ₽"),
        ("Мария", 50000, "Мария: 50000 ₽"),
        ("Алексей", None, "Алексей: 100000 ₽")
    ],
    'sum_sum':[
        ((3, 4), (7, -1)),
        ((0, 8), (8, -8))
    ]
}

from fact import fact_it

@pytest.mark.parametrize("input_data, expected", test_data['fact'])
def test_fact_it(input_data, expected):
    assert fact_it(input_data) == expected

from fact import fact_rec

@pytest.mark.parametrize("input_data, expected", test_data['fact'])
def test_fact_rec(input_data, expected):
    assert fact_rec(input_data) == expected


@pytest.mark.parametrize("input_data, expected_error", test_data['fact_err'])
def test_fact_it_err(input_data, expected_error):
    """Тест итерационной функции с неправильными значениями"""
    with pytest.raises(expected_error):
        fact_it(input_data)


@pytest.mark.parametrize("input_data, expected_error", test_data['fact_err'])
def test_fact_rec_err(input_data, expected_error):
    """Тест рекурсивной функции с неправильными значениями"""
    with pytest.raises(expected_error):
        fact_rec(input_data)

from show_employee import show_employee


@pytest.mark.parametrize("name, salary, expected", test_data['show_employee'])
def test_show_employee(name, salary, expected):
    if salary is None:
        assert show_employee(name) == expected
    else:
        assert show_employee(name, salary) == expected


from sum_and_sub import sum_and_sub

@pytest.mark.parametrize("test_data, expected", test_data['sum_sum'])
def test_sum_and_sum(test_data, expected):
    a, b = test_data
    assert sum_and_sub(a, b) == expected



from process_list import process_list, process_list_comp, process_list_gen

test_data_process = [
    ([1, 2, 3, 4], [1, 4, 27, 16]),
    ([2, 4, 6], [4, 16, 36]),
    ([1, 3, 5], [1, 27, 125]),
    ([0, 1], [0, 1]),
    ([10], [100])
]

test_data_process_invalid = [
    list(range(1, 10 ** 4))
]

@pytest.mark.parametrize("input_data, expected", test_data_process)
def test_process_list(input_data, expected):
    assert process_list(input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data_process)
def test_process_list_comp(input_data, expected):
    assert process_list_comp(input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data_process)
def test_process_list_gen(input_data, expected):
    assert list(process_list_gen(input_data)) == expected

# Тесты на ошибки (отдельно)
@pytest.mark.parametrize("input_data", test_data_process_invalid)
def test_process_list_invalid(input_data):
    """Тест на вызов ошибки при неправильной длине списка"""
    with pytest.raises(ValueError):
        process_list(input_data)

@pytest.mark.parametrize("input_data", test_data_process_invalid)
def test_process_list_comp_invalid(input_data):
    """Тест на вызов ошибки при неправильной длине списка"""
    with pytest.raises(ValueError):
        process_list_comp(input_data)

@pytest.mark.parametrize("input_data", test_data_process_invalid)
def test_process_list_gen_invalid(input_data):
    """Тест на вызов ошибки при неправильной длине списка"""
    with pytest.raises(ValueError):
        list(process_list_gen(input_data))

from my_sum import my_sum

test_data_my_sum = [
    ([1, 2, 3], 6),
    ([1, 2, 3, 4, 5], 15),
    ([10, 20, 30], 60),
    ([1.5, 2.5], 4.0),
    ([], 0),
    ([-5, 5], 0),
]


@pytest.mark.parametrize("input_data, expected", test_data_my_sum)
def test_my_sum(input_data, expected):
    assert my_sum(*input_data) == expected


test_data_my_sum_argv = [
    (["1", "2", "3", "4", "5"], "15"),
    (["1.5", "2.5", "3.5"], "7.5"),
    (["1", "2.5", "3"], "6.5"),
    (["42"], "42"),
    ([], "0"),
    (["-5", "5", "-2", "2"], "0"),
]
from my_sum_argv import my_sum_argv
@pytest.mark.parametrize("args, expected", test_data_my_sum_argv)
def my_sum_argv(args, expected):
    """Параметризованный тест для my_sum"""
    cmd = [sys.executable, "my_sum_argv.py"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.stdout.strip() == expected


def test_my_sum_command_line_invalid():
    """Тест с некорректными аргументами"""
    result = subprocess.run(
        [sys.executable, "my_sum_argv.py", "1", "2", "abc"],
        capture_output=True,
        text=True
    )
    assert result.returncode != 0



test_data_files_sort = [
    (['a.py', 'b.py', 'c.py', 'a.txt', 'b.txt', 'c.txt'],
     ['a.py', 'b.py', 'c.py', 'a.txt', 'b.txt', 'c.txt']),
    (['1.txt', '2.doc', '3.txt', '4.doc', '5.pdf'],
     ['2.doc', '4.doc', '5.pdf', '1.txt', '3.txt']),
    
    (['a.z', 'b.a', 'c.b', 'd.c'],
     ['b.a', 'c.b', 'd.c', 'a.z']),
    (['test.py', 'test.pyc', 'test.txt', 'README.md'],
     ['README.md', 'test.py', 'test.pyc', 'test.txt']),
]

test_data_files_sort_empty = [
    ([], []),
    (['dir1', 'dir2'], []),
]

test_data_files_sort_invalid = [
    'несуществующая_директория',
    '/путь/которого/нет',
]

from files_sort import get_sorted_files_by_ext

@pytest.mark.parametrize("files, expected", test_data_files_sort)
def test_get_sorted_files_by_ext(files, expected):
    with tempfile.TemporaryDirectory() as temp_dir:
        for f in files:
            if '.' in f:
                open(os.path.join(temp_dir, f), 'w').close()
            else:
                os.mkdir(os.path.join(temp_dir, f))
        
        assert get_sorted_files_by_ext(temp_dir) == expected

@pytest.mark.parametrize("files, expected", test_data_files_sort_empty)
def test_get_sorted_files_by_ext_empty(files, expected):
    with tempfile.TemporaryDirectory() as temp_dir:
        for f in files:
            if '.' in f:
                open(os.path.join(temp_dir, f), 'w').close()
            else:
                os.mkdir(os.path.join(temp_dir, f))
        
        assert get_sorted_files_by_ext(temp_dir) == expected

@pytest.mark.parametrize("invalid_path", test_data_files_sort_invalid)
def test_get_sorted_files_by_ext_invalid(invalid_path):
    with pytest.raises((NotADirectoryError, FileNotFoundError)):
        get_sorted_files_by_ext(invalid_path)




from file_search import find_and_print_file
import os
from io import StringIO
test_data = [
    ('my_sum.py', ['def my_sum(*a):', '    return sum(a)', '', '', 'if __name__ == "__main__":']),
    ('show_employee.py', ['def show_employee(name, salary = 100000):', '    return f"{name}: {salary} ₽"', '', 'if __name__ == "__main__":', '    name = input("")']),
    ('файл_которого_нет.txt', ['Файл файл_которого_нет.txt не найден']),
]

@pytest.mark.parametrize("filename, expected", test_data)
def test_find_and_print_file(filename, expected):
    """Тест поиска файла и вывода первых 5 строк"""
    original_stdout = sys.stdout
    captured = StringIO()
    sys.stdout = captured
    
    try:
        find_and_print_file(filename)
        output = captured.getvalue().strip().split('\n')
        assert output == expected
    finally:
        sys.stdout = original_stdout



from email_validation import fun, filter_mail


test_data_fun = [
    ('lara@mospolytech.ru', True),
    ('brian-23@mospolytech.ru', True),
    ('britts_54@mospolytech.ru', True),
    ('user123@gmail.com', True),
    ('my-name@website.org', True),
    ('test_test@test.ru', True),
    ('a@b.c', True),
    ('invalid@email', False),
    ('brian@23@mospolytech.ru', False),
    ('britts_54@mospolytech.ruru', False),
    ('user@.com', False),
    ('@gmail.com', False),
]

@pytest.mark.parametrize("email, expected", test_data_fun)
def test_fun(email, expected):
    assert fun(email) == expected


test_data_filter = [
    (
        ['lara@mospolytech.ru', 'brian-23@mospolytech.ru', 'britts_54@mospolytech.ru'],
        ['brian-23@mospolytech.ru', 'britts_54@mospolytech.ru', 'lara@mospolytech.ru']
    ),
    (
        ['test@gmail.com', 'test@gmail.c', 'invalid@email', 'wrong@.com'],
        ['test@gmail.c', 'test@gmail.com']
    ),
    (
        ['a@b.c', 'a@b.cc', 'a@b.ccc', 'invalid'],
        ['a@b.c', 'a@b.cc', 'a@b.ccc']
    ),
]

@pytest.mark.parametrize("emails, expected", test_data_filter)
def test_filter_mail(emails, expected):
    result = filter_mail(emails)
    result.sort()
    assert result == expected

from fibonacci import cube, fibonacci


test_data_fibonacci_cubes = [

    (5, [0, 1, 1, 8, 27]),
    (6, [0, 1, 1, 8, 27, 125]),
    (11, [0, 1, 1, 8, 27, 125, 512, 2197, 9261, 39304, 166375]),
]

@pytest.mark.parametrize("n, expected", test_data_fibonacci_cubes)
def test_fibonacci_cubes(n, expected):
    result = fibonacci(n)
    assert result == expected

test_data_invalid = [
    (0, ValueError),
    (-1, ValueError),
    (16, ValueError),
    (20, ValueError),
    (100, ValueError),
]

@pytest.mark.parametrize("n, expected_error", test_data_invalid)
def test_fibonacci_invalid(n, expected_error):
    with pytest.raises(expected_error):
        fibonacci(n)



from average_scores import compute_average_scores 

test_data_average_scores = [
    (
        [
            (89, 90, 78, 93, 80),
            (90, 91, 85, 88, 86),
            (91, 92, 83, 89, 90.5),
        ],
        (90.0, 91.0, 82.0, 90.0, 85.5),
    ),
    (
        [
            (10, 20),
            (30, 40),
        ],
        (20.0, 30.0),
    ),
]

@pytest.mark.parametrize("scores, expected", test_data_average_scores)
def test_average_scores(scores, expected):
    assert compute_average_scores(scores) == expected

@pytest.mark.parametrize("scores", [
    [],                                # пустой список
    [(1, 2), (3,)],                    # разная длина кортежей
    [(101,2)]
])
def test_average_scores_invalid(scores):
    with pytest.raises(ValueError):
        compute_average_scores(scores)

def test_empty_scores():
    with pytest.raises(ValueError):
        compute_average_scores([])

def test_limits():
    scores = [(1,)] *101 
    with pytest.raises(ValueError):
        compute_average_scores(scores)


import math
from plane_angle import plane_angle, Point

def test_point_operations():
    A = Point(1, 2, 3)
    B = Point(4, 5, 6)

    C = B - A
    assert (C.x, C.y, C.z) == (3, 3, 3)

    D = Point(1, 0 ,0)
    E = Point(0, 1, 0)

    assert D.dot(E) == 0
    assert D.dot(D) == 1

    F = D.cross(E)
    assert (F.x, F.y, F.z) == (0, 0, 1)

    G = Point(3, 4 ,0)
    assert G.absolute() == 5.0

def test_plane_angle_simple():
    # Две плоскости, угол 90°
    A = Point(0, 0, 0)
    B = Point(1, 0, 0)
    C = Point(0, 1, 0)
    D = Point(0, 1, 1)  # выбираем D так, чтобы плоскости не вырождались
    
    angle = plane_angle(A, B, C, D)
    assert math.isclose(angle, 90.0, abs_tol=1e-6)

def test_plane_angle_parallel_planes():
    # Плоскости параллельны: угол = 0°
    A = Point(0, 0, 0)
    B = Point(1, 0, 0)
    C = Point(0, 1, 0)
    D = Point(1, 1, 0.0001)  # немного смещаем, чтобы не было нулевого вектора
    
    angle = plane_angle(A, B, C, D)
    assert math.isclose(angle, 0.0, abs_tol=1.0)  # допускаем погрешность

def test_plane_angle_arbitrary():
    A = Point(1, 2, 3)
    B = Point(4, 5, 6)
    C = Point(7, 8, 0)
    D = Point(1, 0, 1)
    
    angle = plane_angle(A, B, C, D)
    assert 0 <= angle <= 180


from phone_number import sort_phone

test_data_phone_number = [
    # пример из условия
    (
        ["+7895462130", "89875641230", "9195969878"],
        [
            "+7 (789) 546-21-30",
            "+7 (919) 596-98-78",
            "+7 (987) 564-12-30"
        ]
    ),
    # номера с разными префиксами
    (
        ["+79123456789", "81234567890", "1234567890", "9123456789"],
        [
            "+7 (123) 456-78-90",
            "+7 (123) 456-78-90",
            "+7 (912) 345-67-89",
            "+7 (912) 345-67-89"
        ]
    ),
    # проверка сортировки
    (
        ["89123456789", "89111222333", "89123456788"],
        [
            "+7 (911) 122-23-33",
            "+7 (912) 345-67-88",
            "+7 (912) 345-67-89"
        ]
    ),
    # короткие номера (только 10 цифр)
    (
        ["1234567890", "0987654321"],
        [
            "+7 (098) 765-43-21",
            "+7 (123) 456-78-90"
        ]
    )
]

@pytest.mark.parametrize("numbers, expected", test_data_phone_number)
def test_sort_phone(numbers, expected):
    assert sort_phone(numbers) == expected




from people_sort import name_format

test_data_people = [
    # Пример из условия
    (
        [
            ["Mike", "Thomson", 20, "M"],
            ["Robert", "Bustle", 32, "M"],
            ["Andria", "Bustle", 30, "F"]
        ],
        [
            "Mr. Mike Thomson",
            "Ms. Andria Bustle",
            "Mr. Robert Bustle"
        ]
    ),
    # Проверка одинакового возраста
    (
        [
            ["Alice", "Smith", 25, "F"],
            ["Bob", "Brown", 25, "M"],
            ["Charlie", "Davis", 22, "M"]
        ],
        [
            "Mr. Charlie Davis",
            "Ms. Alice Smith",
            "Mr. Bob Brown"
        ]
    ),
    # Все женщины
    (
        [
            ["Mary", "Johnson", 30, "F"],
            ["Linda", "Lee", 28, "F"]
        ],
        [
            "Ms. Linda Lee",
            "Ms. Mary Johnson"
        ]
    ),
    # Все мужчины
    (
        [
            ["John", "Doe", 40, "M"],
            ["Mike", "Roe", 35, "M"]
        ],
        [
            "Mr. Mike Roe",
            "Mr. John Doe"
        ]
    )
]

@pytest.mark.parametrize("people, expected", test_data_people)
def test_name_format(people, expected):
    assert name_format(people) == expected


def test_too_few_people():
    # Меньше 1 человека
    people = []
    with pytest.raises(ValueError) as excinfo:
        name_format(people)
    assert "Количество человек должно быть от 1 до 10" in str(excinfo.value)

def test_too_many_people():
    # Больше 10 человек
    people = [["A", "B", 20, "M"]] * 11
    with pytest.raises(ValueError) as excinfo:
        name_format(people)
    assert "Количество человек должно быть от 1 до 10" in str(excinfo.value)


from complex_numbers import Complex

test_data_complex = [
    (2, 1, 5, 6, 
     "7.00+7.00i", "-3.00-5.00i", "4.00+17.00i", "0.26-0.11i", "2.24+0.00i", "7.81+0.00i"),
    (0, 3, 4, -2,
    "4.00+1.00i", "-4.00+5.00i", "6.00+12.00i", "-0.30+0.60i", "3.00+0.00i", "4.47+0.00i"),
    (3, 0, 0, -5,
     "3.00-5.00i", "3.00+5.00i", "0.00-15.00i", "0.00+0.60i", "3.00+0.00i", "5.00+0.00i"),
    (0, 0, 0, 0,
     "0.00+0.00i", "0.00+0.00i", "0.00+0.00i", "nan+nan*i", "0.00+0.00i", "0.00+0.00i"),
]


@pytest.mark.parametrize(
    "r1,i1,r2,i2,expected_add,expected_sub,expected_mul,expected_div,expected_mod_c1,expected_mod_c2",
    test_data_complex
)
def test_complex_operations(r1, i1, r2, i2, expected_add, expected_sub, expected_mul, expected_div, expected_mod_c1, expected_mod_c2):
    c1 = Complex(r1, i1)
    c2 = Complex(r2, i2)

    # Сложение
    assert str(c1 + c2) == expected_add

    # Вычитание
    assert str(c1 - c2) == expected_sub

    # Умножение
    assert str(c1 * c2) == expected_mul

    # Деление — обработка деления на ноль
    try:
        div_result = c1 / c2
        assert str(div_result) == expected_div
    except ZeroDivisionError:
        assert expected_div == "nan+nan*i"

    # Модуль
    assert str(c1.mod()) == expected_mod_c1
    assert str(c2.mod()) == expected_mod_c2

# Проверка __str__ на разные комбинации
@pytest.mark.parametrize(
    "r,i,expected",
    [
        (0, 3, "0.00+3.00i"),
        (0, -3, "0.00-3.00i"),
        (3, 0, "3.00+0.00i"),
        (3, 4, "3.00+4.00i"),
        (3, -4, "3.00-4.00i"),
        (0, 0, "0.00+0.00i")
    ]
)
def test_str_format(r, i, expected):
    c = Complex(r, i)
    assert str(c) == expected


from circle_square_mk import circle_square_mk

@pytest.mark.parametrize("r, n", [
    (1, 10000),
    (2, 50000),
    (5, 100000),
    (10, 100000),
])
def test_circle_square_mk_accuracy(r, n):
    """Проверка, что оценка площади близка к точной"""
    estimated_area = circle_square_mk(r, n)
    exact_area = math.pi * r**2
    error = abs(estimated_area - exact_area)
    relative_error = error / exact_area

    # Допустимая относительная погрешность ~1% при больших n
    assert relative_error < 0.01, f"Погрешность слишком велика: {relative_error:.4f}"

def test_circle_square_zero_radius():
    """Площадь круга с радиусом 0 должна быть 0"""
    assert circle_square_mk(0, 1000) == 0.0

def test_circle_square_small_n():
    """Функция должна возвращать число даже при малом n"""
    area = circle_square_mk(1, 10)
    assert isinstance(area, float)


#log_decorator.py

import time
from log_decorator import function_logger

def test_logger_basic(tmp_path):
    log_file = tmp_path / "log.txt"

    @function_logger(log_file)
    def add(a, b):
        return a + b
    
    result = add(3, 5)
    assert result == 8

    # Проверяем содержимое файла
    content = log_file.read_text(encoding="utf-8")
    assert "add" in content
    assert "(3, 5)" in content
    assert "8" in content
    assert "seconds" in content

def test_logger_with_kwargs(tmp_path):
    log_file = tmp_path / "log.txt"

    @function_logger(log_file)
    def greet(name, greeting="Hello"):
        return f"{greeting}, {name}!"

    result = greet("Alice", greeting="Hi")
    assert result == "Hi, Alice!"

    content = log_file.read_text(encoding="utf-8")
    assert "greet" in content
    assert "{'greeting': 'Hi'}" in content
    assert "Hi, Alice!" in content


def test_logger_exception(tmp_path):
    log_file = tmp_path / "log.txt"

    @function_logger(log_file)
    def fail_func():
        raise ValueError("Oops!")

    with pytest.raises(ValueError, match="Oops!"):
        fail_func()

    content = log_file.read_text(encoding="utf-8")
    # Даже если функция упала, лог должен содержать имя функции и "-"
    assert "fail_func" in content
    assert "-" in content  # Результат при исключении