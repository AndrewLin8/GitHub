data = [
	{"company":"Taxi Affiliation Services","payment_type":"Cash","fare":5.65},
	{"company":"Choice Taxi Association","payment_type":"Credit Card","fare":8.45},
	{"company":"Taxi Affiliation Services","payment_type":"Cash","fare":8.25},
	{"company":"Taxi Affiliation Services","payment_type":"Credit Card","fare":11.65},
	{"company":"Taxi Affiliation Services","payment_type":"Credit Card","fare":4.45},
	{"company":"Dispatch Taxi Affiliation","payment_type":"Credit Card","fare":7.45},
	{"company":"Dispatch Taxi Affiliation","payment_type":"Cash","fare":4.25},
	{"company":"Dispatch Taxi Affiliation","payment_type":"Cash","fare":5.05},
	{"company":"Taxi Affiliation Services","payment_type":"Cash","fare":9.05},
	{"company":"Taxi Affiliation Services","payment_type":"Credit Card","fare":11.5},
	{"company":"Choice Taxi Association","payment_type":"Cash","fare":6.65},
	{"company":"Blue Ribbon Taxi Association Inc.","payment_type":"Cash","fare":8.65},
	{"company":"Choice Taxi Association","payment_type":"Cash","fare":6.65},
	{"company":"Blue Ribbon Taxi Association Inc.","payment_type":"Cash","fare":5.05},
	{"company":"Taxi Affiliation Services","payment_type":"Cash","fare":5.05},
	{"company":"Dispatch Taxi Affiliation","payment_type":"Credit Card","fare":5.85}
]


def _percentile(sorted_data, p):
	k = (len(sorted_data) - 1) * (p / 100)
	f = int(k)
	c = min(f + 1, len(sorted_data) - 1)
	if f == c:
		return sorted_data[int(k)]
	d0 = sorted_data[f] * (c - k)
	d1 = sorted_data[c] * (k - f)
	return d0 + d1


def main():
	try:
		import pandas as pd
		_HAS_PANDAS = True
	except Exception:
		_HAS_PANDAS = False

	if _HAS_PANDAS:
		import pandas as pd
		df = pd.DataFrame(data)
		print('DataFrame:')
		print(df)
		print()
		print('Summary (describe):')
		print(df.describe(include='all'))
		print()
		print('Median (numeric columns):')
		print(df.median(numeric_only=True))
	else:
		print('pandas not installed — using fallback summary')
		# Print table
		print(f"{'company':<35}{'payment_type':<15}{'fare':>8}")
		for r in data:
			print(f"{r['company']:<35}{r['payment_type']:<15}{r['fare']:8.2f}")

		# Numeric summary for fare
		fares = [r['fare'] for r in data]
		fares_sorted = sorted(fares)
		import statistics
		print()
		print('Fare summary:')
		print(f"count: {len(fares)}")
		print(f"mean: {statistics.mean(fares):.4f}")
		if len(fares) > 1:
			print(f"std: {statistics.stdev(fares):.4f}")
		else:
			print("std: 0.0")
		print(f"min: {min(fares)}")
		print(f"25%: {_percentile(fares_sorted,25):.4f}")
		print(f"50% (median): {_percentile(fares_sorted,50):.4f}")
		print(f"75%: {_percentile(fares_sorted,75):.4f}")
		print(f"max: {max(fares)}")


if __name__ == '__main__':
	main()

