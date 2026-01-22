# Ask the user to enter a temperature in farenheit.
# Conver the temperature to celsius using the formula C = (F - 32) * 5/9
# Name: Andrew Lin
# Date: Jan, 22, 2026

farenheit_input = input("Please enter a temperature in farenheit: ")
farenheit_float = float(farenheit_input)
celsius_temp = (farenheit_float - 32) * 5 / 9
celsius_temp_rounded = round(celsius_temp, 1)

print("You entered", farenheit_float)
print("The temperature in celsius is", celsius_temp_rounded)