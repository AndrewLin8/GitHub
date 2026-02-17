health = 100

while health > 0:
    print(f"Your health: {health}.")
    damage = int(input("Enter the damage taken: "))
    health -= damage

print ("Game over!")
