CSV_PATH = 'ITM352_S26/sales_data.csv'


def main():
    try:
        import pandas as pd
        df = pd.read_csv(CSV_PATH)
        print('First 5 rows:')
        print(df.head())
        print('\nData types:')
        print(df.dtypes)
    except Exception:
        # Minimal fallback if pandas is not available
        import csv
        with open(CSV_PATH, newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [next(reader) for _ in range(5)]
        print('First 5 rows (csv fallback):')
        print([header])
        for r in rows:
            print(r)
        print('\nData types: pandas not installed')


if __name__ == '__main__':
    main()
CSV_PATH = 'ITM352_S26/sales_data.csv'


def main():
    try:
        import pandas as pd
        df = pd.read_csv(CSV_PATH)
        print('First 5 rows:')
        print(df.head())
        print('\nData types:')
        print(df.dtypes)
    except Exception:
        # Minimal fallback if pandas is not available
        import csv
        with open(CSV_PATH, newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [next(reader) for _ in range(5)]
        print('First 5 rows (csv fallback):')
        print([header])
        for r in rows:
            print(r)
        print('\nData types: pandas not installed')


if __name__ == '__main__':
    main()
