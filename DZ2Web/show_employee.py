def show_employee(name, salary = 100000):
    return f"{name}: {salary} ₽"

if __name__ == "__main__":
    name = input("") 
    salary = input()
    print(show_employee(name, salary))

