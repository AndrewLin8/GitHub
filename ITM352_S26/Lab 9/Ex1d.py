# Open the file name.txt and read its contents and print the number of names

with open("names.txt") as file_object:
    contents_list = file_object.readlines()
    print(contents_list)

with open("names.txt", "a") as file_object:
    print("appending new name to the file...")
    file_object.write("Adam, Jay\n")
    contents_list.append("Adam, Jay\n")
    print(f"Number of names: {len(contents_list)}")