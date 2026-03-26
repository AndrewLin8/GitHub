# Open names.txt, append Andrew Lin, print full contents, and print total names.

from pathlib import Path

file_path = Path(__file__).with_name("names.txt")

with open(file_path, "a") as file_object:
    print("Appending new name to the file...")
    file_object.write("Andrew Lin\n")

with open(file_path, "r") as file_object:
    contents = file_object.read()

print("Entire file contents:")
print(contents)

names = [line.strip() for line in contents.splitlines() if line.strip()]
print(f"Number of names: {len(names)}")