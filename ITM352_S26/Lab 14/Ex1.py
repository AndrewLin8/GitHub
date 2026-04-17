import importlib.util

import matplotlib.pyplot as plt


PACKAGES = ["scipy", "statsmodels", "matplotlib"]


def is_installed(package_name: str) -> bool:
	return importlib.util.find_spec(package_name) is not None


def main() -> None:
	for package_name in PACKAGES:
		if is_installed(package_name):
			print(f"{package_name} is installed")
		else:
			print(f"{package_name} is not installed")

	if is_installed("matplotlib"):
		x_values = [1, 2, 3, 4, 5]
		y_values = [2, 4, 1, 5, 3]
		x_values_2 = [1, 2, 3, 4, 5]
		y_values_2 = [3, 1, 4, 2, 5]

		plt.figure(figsize=(6, 4))
		plt.plot(x_values, y_values, marker="o", label="Series 1")
		plt.scatter(x_values, y_values)
		plt.plot(x_values_2, y_values_2, marker="o", label="Series 2")
		plt.title("Line and Scatter Plot")
		plt.xlabel("X Values")
		plt.ylabel("Y Values")
		plt.legend()
		plt.grid(True)
		plt.tight_layout()
		plt.savefig("first_visualization.png")
		plt.close()
		print("Saved first_visualization.png")


if __name__ == "__main__":
	main()
