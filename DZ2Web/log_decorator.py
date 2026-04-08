# log_decorator.py
import time
from datetime import datetime
from functools import wraps

def function_logger(log_file):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            start_perf = time.perf_counter()

            # Выполнение функции
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                result = '-'
                raise e
            finally:
                end_time = datetime.now()
                end_perf = time.perf_counter()
                elapsed = end_perf - start_perf

                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(f"{func.__name__}\n")
                    f.write(f"{start_time.strftime('%Y-%m-%d %H:%M:%S.%f')}\n")
                    if args:
                        f.write(f"{args}\n")
                    if kwargs:
                        f.write(f"{kwargs}\n")
                    f.write(f"{result}\n")
                    f.write(f"{end_time.strftime('%Y-%m-%d %H:%M:%S.%f')}\n")
                    f.write(f"{elapsed:.6f} seconds\n\n")
            return result
        return wrapper
    return decorator

if __name__ == "__main__":
    @function_logger("test.log")
    def greeting(name):
        return f"Hello, {name}!"

    @function_logger("test.log")
    def divide(a, b):
        return a / b

    print(greeting("John"))   # Вызов функции
    print(divide(10, 2))      # Вызов функции
    try:
        divide(5, 0)          # Попытка деления на ноль
    except ZeroDivisionError:
        print("Caught division by zero")