n = int(input(""))
students = []
names = []
if 2 <= n <= 5: 
    for i in range(n):
        name = input("")
        score = float(input(""))
        students.append([name, score])
    sort_students = sorted(students, key=lambda x: x[1], reverse=False)
    names.append(sort_students[1][0])
    for i in range(2, len(sort_students)):
        if sort_students[1][1] == sort_students[i][1]:
            names.append(sort_students[i][0])

    names.sort()
    for i in range(len(names)):
        print(names[i])