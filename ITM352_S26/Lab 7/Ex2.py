even_numbers = []
num = 2

while len(even_numbers) == 0 or even_numbers[-1] < 50:
    even_numbers.append(num)
    num += 2

print(even_numbers)
