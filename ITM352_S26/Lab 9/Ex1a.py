from pathlib import Path

file_path = Path(__file__).with_name("names.txt")

f = open(file_path, "r")
print(type(f))
f.close()
