CSV_PATH = 'ITM352_S26/homes_data.csv'


def main():
	try:
		import pandas as pd
		df = pd.read_csv(CSV_PATH)
		print('Loaded with pandas')
		print('Dimensions (rows, cols):', df.shape)

		print('\nDtypes before coercion:')
		print(df.dtypes)

		# Coerce columns to appropriate dtypes
		int_cols = ['id', 'borough', 'block', 'lot', 'year_built']
		for c in int_cols:
			if c in df.columns:
				df[c] = pd.to_numeric(df[c], errors='coerce').astype('Int64')

		# Numeric columns that may contain non-numeric placeholders
		num_cols = ['units', 'land_sqft', 'gross_sqft']
		for c in num_cols:
			if c in df.columns:
				df[c] = pd.to_numeric(df[c].astype(str).str.replace(r'[^0-9.-]', '', regex=True), errors='coerce')

		# sale_price may contain '-' placeholders; clean and coerce
		if 'sale_price' in df.columns:
			df['sale_price'] = pd.to_numeric(df['sale_price'].astype(str).str.replace(r'[^0-9.-]', '', regex=True), errors='coerce')

		print('\nDtypes after coercion:')
		print(df.dtypes)

		print('\nFirst 10 rows of cleaned data:')
		print(df.head(10))

		# Now proceed with filtering as before using cleaned units
		df['units'] = pd.to_numeric(df['units'], errors='coerce')

		# Drop rows with any nulls (cleaned DataFrame)
		df_clean = df.dropna()
		print('\nAfter dropping rows with nulls — dimensions:', df_clean.shape)
		print('\nFirst 10 rows after dropping nulls:')
		print(df_clean.head(10))

		# Drop duplicate rows
		df_clean_nodup = df_clean.drop_duplicates()
		print('\nAfter dropping duplicates — dimensions:', df_clean_nodup.shape)
		print('\nFirst 10 rows after dropping duplicates:')
		print(df_clean_nodup.head(10))

		# Filter properties with >=500 units on the cleaned no-null/no-dup DataFrame
		df_filtered = df_clean_nodup[df_clean_nodup['units'] >= 500].copy()
		cols_to_drop = ['block', 'lot', 'easement', 'land_sqft', 'gross_sqft', 'year_built', 'sale_price']
		df_filtered = df_filtered.drop(columns=[c for c in cols_to_drop if c in df_filtered.columns])

		print('\nFiltered properties with >=500 units — dimensions:', df_filtered.shape)
		print('\nFirst 10 rows of filtered data:')
		print(df_filtered.head(10))

		# Filter out zero sale_price values from the cleaned no-null/no-dup DataFrame
		if 'sale_price' in df_clean_nodup.columns:
			df_no_zero_sales = df_clean_nodup[df_clean_nodup['sale_price'] > 0].copy()
			print('\nAfter filtering out zero sale_price — dimensions:', df_no_zero_sales.shape)
			print('\nFirst 10 rows after removing zero sale_price:')
			print(df_no_zero_sales.head(10))
			avg_sale_price = df_no_zero_sales['sale_price'].mean()
			print(f"\nAverage sale_price (excluding zeros): {avg_sale_price:,.2f}")
		else:
			print('\nNo sale_price column found to filter.')
	except Exception:
		# Fallback using csv module
		import csv
		rows = []
		with open(CSV_PATH, newline='') as f:
			reader = csv.reader(f)
			header = next(reader)
			for i, r in enumerate(reader):
				rows.append(r)
		print('pandas not installed — used csv fallback')
		print('Dimensions (rows, cols):', (len(rows), len(header)))
		print()
		print('First 10 rows:')
		print([header])
		for row in rows[:10]:
			print(row)


if __name__ == '__main__':
	main()

