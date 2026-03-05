searchMe = [2, 5, 7, 11, 15, 22, 27, 30, 34, 41, 55, 57, 58, 60, 77]

number = int(input("Enter a number to search for: "))

found = False
for num in searchMe:
    if num == number:
        found = True
        break

if found:
    print("Found!")
else:
    print("Not Found!")