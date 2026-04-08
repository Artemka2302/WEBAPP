
s = input().strip()

vowels = 'AEIOU'
kevin_score = 0
stuart_score = 0
length = len(s)


for i in range(length):
    if s[i] in vowels:
        # Кевин (гласные) - все подстроки, начинающиеся с этой позиции
        kevin_score += length - i
    else:
        # Стюарт (согласные) - все подстроки, начинающиеся с этой позиции
        stuart_score += length - i


if kevin_score > stuart_score:
    print(f"Кевин {kevin_score}")
elif stuart_score > kevin_score:
    print(f"Стюарт {stuart_score}")
else:
    print("Ничья")