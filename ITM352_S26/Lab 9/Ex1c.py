from pathlib import Path

file_path = Path(__file__).with_name("names.txt")

with open(file_path, "r") as f:
	contents = f.read()

names = [line.strip() for line in contents.splitlines() if line.strip()]

print("Names:")
for name in names:
	print(name)

print(f"Total names: {len(names)}")