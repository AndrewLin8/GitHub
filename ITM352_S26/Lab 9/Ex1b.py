from pathlib import Path

file_path = Path(__file__).with_name("names.txt")

with open(file_path, "r") as f:
	print(type(f))
