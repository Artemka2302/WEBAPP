import os
import sys

def find_and_print_file(filename, start_dir=None):
    """Рекурсивный поиск файла и вывод первых 5 строк"""
    if start_dir is None:
        start_dir = os.path.dirname(os.path.abspath(__file__))
    
    for root, dirs, files in os.walk(start_dir):
        if filename in files:
            filepath = os.path.join(root, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                for i in range(5):
                    line = f.readline()
                    if line:
                        print(line.rstrip('\n'))
                    else:
                        break
            return
    
    print(f"Файл {filename} не найден")

def main():
    if len(sys.argv) < 2:
        return
    
    filename = sys.argv[1]
    find_and_print_file(filename)

if __name__ == "__main__":
    main()