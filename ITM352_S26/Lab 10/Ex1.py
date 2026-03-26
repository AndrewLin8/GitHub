
percentile_incomes = [
	(10, 14629),
	(20, 25600),
	(30, 37002),
	(40, 50000),
	(50, 63179),
	(60, 79542),
	(70, 100162),
	(80, 130000),
	(90, 184292),
]

try:
	import numpy as np
	_HAS_NUMPY = True
except ImportError:
	_HAS_NUMPY = False


def main():
	if _HAS_NUMPY:
		arr = np.array(percentile_incomes)
		shape = arr.shape
		size = arr.size
	else:
		arr = percentile_incomes
		shape = (len(arr), 2)
		size = len(arr) * 2

	print("Array shape:", shape)
	print("Number of elements:", size)
	print()
	print(f"{'Percentile':<12}{'Income'}")
	for pct, income in arr:
		print(f"{int(pct):<12}{int(income)}")


if __name__ == "__main__":
	main()

