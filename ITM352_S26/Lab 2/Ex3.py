# Ask the user to enter a floating point number. Square the number 
# Print the orginal number and the squared number.
# Name: Andrew Lin
# Date: Jan, 22, 2026

input_value = input("Please enter a floating point number")
float_value = float(input_value)
squared_value = float_value ** 2

print ("you entered", round(float_value, 2))
print ("The squared value is", round(squared_value, 2))