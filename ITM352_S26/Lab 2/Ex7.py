# Ask the user to enter a temperature in farenheit.
# Convert the temperature to celsius using the formula C = (F - 32) * 5/9
# Name: Andrew Lin
# Date: Jan, 22, 2026

# Function to convert fahrenheit to celsius
def fahrenheit_to_celsius(fahrenheit):
    """Convert fahrenheit temperature to celsius and round to 1 decimal place"""
    celsius_temp = (fahrenheit - 32) * 5 / 9
    celsius_temp_rounded = round(celsius_temp, 1)
    return celsius_temp_rounded

# Get user input
fahrenheit_input = input("Please enter a temperature in farenheit: ")
fahrenheit_float = float(fahrenheit_input)

# Call the function and display results
celsius_result = fahrenheit_to_celsius(fahrenheit_float)
print("You entered", fahrenheit_float)
print("The temperature in celsius is", celsius_result)
