data = {
	'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva'],
	'Age': [25, 30, 35, 40, 22],
	'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
	'Salary': [70000, 80000, 120000, 90000, 60000]
}


def main():
	try:
		import pandas as pd
		df = pd.DataFrame(data)
		print('DataFrame:')
		print(df)
	except Exception:
		print('pandas not installed — printing data as rows:')
		names = data['Name']
		ages = data['Age']
		cities = data['City']
		salaries = data['Salary']
		print(f"{'Name':<10}{'Age':>6}{'City':>15}{'Salary':>12}")
		for n, a, c, s in zip(names, ages, cities, salaries):
			print(f"{n:<10}{a:>6}{c:>15}{s:>12}")


if __name__ == '__main__':
	main()

