#Debugging exercise # 4
# Retrieving elements from a list
def get_element(items, index):
    if 0 <= index < len(items):
        return items[index]
    return "Index out of range"


my_list = [1, 2, 3, 4, 5]
print(get_element(my_list, 2))  
print(get_element(my_list, 5))
