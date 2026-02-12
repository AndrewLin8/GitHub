# Create a list with a variety of different values
my_list = [42, "hello", 3.14, True, None, 100, "world", 2.71, False, 7, "test", 99, -5]

# Check the length and print different messages
list_length = len(my_list)

if list_length < 5:
    print(f"Your list is small with only {list_length} elements.")
elif list_length >= 5 and list_length <= 10:
    print(f"Your list has a moderate size with {list_length} elements.")
else:
    print(f"Your list is large with {list_length} elements.")

# Test cases covering all conditions
test_cases = [
    [1, 2],                         # length = 2  -> small (<5)
    [1, 2, 3, 4, 5],                # length = 5  -> moderate (boundary)
    list(range(10)),                # length = 10 -> moderate (boundary)
    list(range(15))                 # length = 15 -> large (>10)
]

# Test the original logic with each test case
for idx, test_list in enumerate(test_cases, start=1):
    list_length = len(test_list)
    print(f"\nTest Case {idx}: length = {list_length}")
    
    if list_length < 5:
        print(f"Your list is small with only {list_length} elements.")
    elif list_length >= 5 and list_length <= 10:
        print(f"Your list has a moderate size with {list_length} elements.")
    else:
        print(f"Your list is large with {list_length} elements.")
