# Ask the uesr to enter their weight in pounds.
# Convert the weight to kilogram (1 pound = 0.453592 kilogram
# Name: Andrew Lin
# Date: Jan, 22, 2026

kg_to_pound = 0.453592

weight_in_pounds = input("Please enter your weight in pounds: ")
weight_in_pounds_float = float(weight_in_pounds)
weight_in_kg = weight_in_pounds_float * kg_to_pound
weight_in_kg_rounded = round(weight_in_kg)

print("You entered", weight_in_pounds_float)
print("Your weight in kilograms is: (weight_in_kg_rounded")
