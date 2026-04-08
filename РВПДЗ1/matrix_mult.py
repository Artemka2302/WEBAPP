# Читаем размерность матрицы
n = int(input())

# Читаем матрицу A
A = []
for _ in range(n):
    row = list(map(int, input().split()))
    A.append(row)

# Читаем матрицу B
B = []
for _ in range(n):
    row = list(map(int, input().split()))
    B.append(row)

# Создаем результирующую матрицу C = A * B
C = [[0 for _ in range(n)] for _ in range(n)]

# Вычисляем произведение матриц
for i in range(n):  # строки A
    for j in range(n):  # столбцы B
        for k in range(n):  # общий индекс
            C[i][j] += A[i][k] * B[k][j]

# Выводим результат
for i in range(n):
    print(' '.join(map(str, C[i])))