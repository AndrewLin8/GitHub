# List of individuals ages
ages = [25, 30, 22, 35, 28, 40, 50, 18, 60, 45]


# Lists of individuals names and genders
names = ["Joe", "Jaden", "Max", "Sidney", "Evgeni", "Taylor", "Pia", "Luis", "Blanca", "Cyndi"]
gender = ["M", "M", "M", "F", "M", "F", "F", "M", "F", "F"]


# Create a list of (age, gender) tuples using zip()
age_gender = list(zip(ages, gender))


if __name__ == "__main__":
	print("ages:", ages)
	print("names:", names)
	print("gender:", gender)
	print()
	print("age_gender:", age_gender)

	# Try to use pandas to build a DataFrame
	try:
		import pandas as pd
		_HAS_PANDAS = True
	except Exception:
		_HAS_PANDAS = False

	if _HAS_PANDAS:
		df = pd.DataFrame({'Age': ages, 'Gender': gender}, index=names)
		print()
		print('DataFrame:')
		print(df)
		print()
		print('DataFrame summary (describe):')
		
		# include='all' to show summary for non-numeric column as well
		print(df.describe(include='all'))
		print()
		print('Average age by gender:')
		print(df.groupby('Gender')['Age'].mean())
	else:
		print()
		print('pandas not installed — printing table and a basic summary instead')
		print(f"{'Name':<10}{'Age':>6}{'Gender':>8}")
		for n, a, g in zip(names, ages, gender):
			print(f"{n:<10}{a:>6}{g:>8}")
			
		# basic numeric summary for ages
		import statistics
		def _percentile(data, p):
			data_sorted = sorted(data)
			k = (len(data_sorted)-1) * (p/100)
			f = int(k)
			c = min(f+1, len(data_sorted)-1)
			if f == c:
				return data_sorted[int(k)]
			d0 = data_sorted[f] * (c - k)
			d1 = data_sorted[c] * (k - f)
			return d0 + d1
		ages_list = ages
		print()
		print('Summary for Age:')
		print(f"count: {len(ages_list)}")
		print(f"mean: {statistics.mean(ages_list):.2f}")
		print(f"std: {statistics.stdev(ages_list):.2f}")
		print(f"min: {min(ages_list)}")
		print(f"25%: {_percentile(ages_list,25)}")
		print(f"50%: {_percentile(ages_list,50)}")
		print(f"75%: {_percentile(ages_list,75)}")
		print(f"max: {max(ages_list)}")
		print()
		
		# average age by gender (fallback)
		for g in sorted(set(gender)):
			vals = [a for a, gg in zip(ages, gender) if gg == g]
			print(f"Average age for {g}: {statistics.mean(vals):.2f}")

