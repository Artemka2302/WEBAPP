n = int(input())
m = []
if 1 <= n <= 20:
    while n > 0:
        n -= 1
        m.append(n ** 2)
m.sort()
for i in range(len(m)):
    print(m[i])
          
