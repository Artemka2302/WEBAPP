import os
import sys

def get_sorted_files_by_ext(directory):
    if not os.path.isdir(directory):
        raise NotADirectoryError(f"{directory} не является директорией")
    
    files = [f for f in os.listdir(directory) 
             if os.path.isfile(os.path.join(directory, f))]
    
    files_by_ext = {}
    for f in files:
        ext = os.path.splitext(f)[1]
        files_by_ext.setdefault(ext, []).append(f)
    
    result = []
    for ext in sorted(files_by_ext.keys()):
        result.extend(sorted(files_by_ext[ext]))
    
    return result

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python files_sort.py <директория>")
        sys.exit(1)
    
    try:
        for f in get_sorted_files_by_ext(sys.argv[1]):
            print(f)
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)