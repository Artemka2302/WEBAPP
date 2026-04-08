
n, m = map(int, input().split())


items = []

for _ in range(m):
    data = input().split()
    name = data[0]
    weight = int(data[1])
    cost = int(data[2])
    
    value_per_weight = cost / weight
    
    items.append((name, weight, cost, value_per_weight))


items.sort(key=lambda x: x[3], reverse=True)

remaining = n
result = []


for name, weight, cost, value_per_weight in items:
    if remaining <= 0:
        break
    
    if weight <= remaining:
        
        result.append((name, weight, cost, 0))
        remaining -= weight
    else:
        part_weight = remaining
        part_cost = value_per_weight * remaining
        result.append((name, part_weight, part_cost, 1))  
        remaining = 0


for name, weight, cost, part_flag in result:

    if weight == int(weight):
        weight_str = str(int(weight))
    else:
        weight_str = f"{weight:.2f}"
    

    if part_flag == 0:

        cost_str = str(int(cost))
    else:

        cost_str = f"{cost:.2f}"
    
    print(f"{name} {weight_str} {cost_str}")