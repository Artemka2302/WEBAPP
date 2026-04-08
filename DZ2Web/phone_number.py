def wrapper(f):
    def fun(numbers):
        cleaned = []
        for num in numbers:
            digits = ''.join(filter(str.isdigit, num))

            if len(digits) == 11 and digits[0] in ('7','8'):
                digits = digits[1:]
            elif len(digits) == 10:
                pass
            else:
                raise ValueError(f"Неправильный формат номера: {num}")
            cleaned.append(digits)

        sorted_array = f(cleaned)
        forma = [f'+7 ({n[:3]}) {n[3:6]}-{n[6:8]}-{n[8:]}' for n in sorted_array]
        return forma
    return fun

@wrapper
def sort_phone(l):
    return sorted(l, key=int)

if __name__ == '__main__':
    l = [input().strip() for _ in range(int(input()))]
    print(*sort_phone(l), sep='\n')
