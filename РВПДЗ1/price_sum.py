
with open('products.csv', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Пропускаем заголовок (первую строку)
data = lines[1:]


adult = 0.0
pensioner = 0.0
child = 0.0


for line in data:

    parts = line.strip().split(',')
    
    # Первый элемент - название продукта, остальные - цены

    
    adult += float(parts[1].strip())
    pensioner += float(parts[2].strip())
    child += float(parts[3].strip())


print(f"{adult:.2f} {pensioner:.2f} {child:.2f}")