# This program demonstrates variable scope in python.
# Name: Andrew Lin
# Date: Jan, 27, 2026

def calculate_discounted(price):
    discount = 0.9
    price = price * discount
    print(f"Inside function, discounted price: {price:.2f}")
    return price

discount = 0.6
price = 100
print(f"original price before function call: {price:.2f}")
discounted_price = calculate_discounted(price)

print(f"Original price after function call: {price:.2f}")
print("discount*,discount")