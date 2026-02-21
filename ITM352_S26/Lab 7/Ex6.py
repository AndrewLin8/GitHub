my_tuple = ("hello", 10, "goodbye", 3, "goodnight", 5)

# Ask user for input
user_input = input("Enter a value to add to the tuple: ")

# Try to append directly to the tuple (which will cause an error)
try:
    my_tuple.append(user_input)
except AttributeError as e:
    print(f"Attempted to append a value to the tuple.")
    print(f"Error: {e}")
    
    # Convert tuple to list, append the value, and convert back to tuple
    my_list = list(my_tuple)
    my_list.append(user_input)
    my_tuple = tuple(my_list)

# Print the final tuple
print(f"Tuple successfully modified: {my_tuple}")