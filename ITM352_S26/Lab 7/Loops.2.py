prices = [100, 50, 20, 160]

total = 0
item_count = 0

for price in prices:
    item_count += 1
    if item_count > 2:
        discounted_price = price * 0.9 # apply 10% discount
        discounted_price += price * 0.1 
    else:
        discounted_price = price 
        total += price


rounded_total = round(total, 2) #round to 2 decimal places
print(f"total price after discount: ${rounded_total:.2f}")