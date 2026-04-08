n = int(input(""))
arr = []
command = []
for i in range(n):
    command = []
    commandlite = []
    commandlite = input().split()
    command.append(commandlite[0])
    if len(commandlite) > 1:
        command.append(int(commandlite[1]))
    if len(commandlite) > 2:
        command.append(int(commandlite[2]))
                   
    if command[0] == 'insert':
        arr.insert(command[1], command[2])
    if command[0] == 'print':
        print(arr)
    if command[0] == 'remove':
        arr.remove(command[1])
    if command[0] == 'append':
        arr.append(command[1])
    if command[0] == 'sort':
        arr.sort()
    if command[0] == 'pop':
        arr.pop()
    if command[0] == 'reverse':
        arr.reverse()