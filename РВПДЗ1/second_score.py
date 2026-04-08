n = int(input(""))
a = []
for i in range(n):
    s = int(input())
    a.append(s) 
a = list(set(a))
a.sort()
print(a[-2])
