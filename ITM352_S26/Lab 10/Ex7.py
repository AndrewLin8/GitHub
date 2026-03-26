URL = 'https://drive.google.com/uc?id=1ujY0WCcePdotG2xdbLyeECFW9lCJ4t-K'


def main():
    try:
        import pandas as pd
        print('Reading CSV from URL with pandas (pyarrow dtype backend), skipping bad lines...')
        df = pd.read_csv(URL, on_bad_lines='skip', dtype_backend='pyarrow')
        print('\nLoaded — shape:', df.shape)

        # Robustly parse order_date into datetime: try default parsing, then dayfirst for remaining
        if 'order_date' in df.columns:
            parsed = pd.to_datetime(df['order_date'], errors='coerce', infer_datetime_format=True)
            missing = parsed.isna()
            if missing.any():
                parsed_alt = pd.to_datetime(df.loc[missing, 'order_date'], errors='coerce', dayfirst=True, infer_datetime_format=True)
                parsed.loc[missing] = parsed_alt
            df['order_date'] = parsed

        print('\nData types (pyarrow-backed):')
        print(df.dtypes)
        print('\nFirst 10 rows:')
        print(df.head(10))

        # Coerce quantity and unit_price to numeric and compute sales
        import numpy as np
        if 'quantity' in df.columns and 'unit_price' in df.columns:
            df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
            df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
            df['sales'] = df['quantity'] * df['unit_price']

            # Ensure pandas displays all columns
            pd.set_option('display.max_columns', None)
            pd.set_option('display.float_format', "${:,.2f}".format)

            # Create pivot table aggregated by sales_region and split by order_type
            pivot = df.pivot_table(index='sales_region', columns='order_type', values='sales', aggfunc=[np.sum, np.mean], margins=True, margins_name='margins')
            print('\nPivot table (sales by region x order_type) with margins:')
            print(pivot)
    except Exception as e:
        print('Error reading CSV with pandas:', e)
        print('\nRetrying with requests and a pandas fallback (no pyarrow dtype conversion)...')
        try:
            import requests, io, pandas as pd
            resp = requests.get(URL, timeout=30)
            resp.raise_for_status()
            df = pd.read_csv(io.BytesIO(resp.content), on_bad_lines='skip')

            if 'order_date' in df.columns:
                parsed = pd.to_datetime(df['order_date'], errors='coerce', infer_datetime_format=True)
                missing = parsed.isna()
                if missing.any():
                    parsed_alt = pd.to_datetime(df.loc[missing, 'order_date'], errors='coerce', dayfirst=True, infer_datetime_format=True)
                    parsed.loc[missing] = parsed_alt
                df['order_date'] = parsed

            print('\nLoaded via requests — shape:', df.shape)
            print('\nData types:')
            print(df.dtypes)
            print('\nFirst 10 rows:')
            print(df.head(10))
            
            # Coerce quantity and unit_price to numeric and compute sales (fallback path)
            if 'quantity' in df.columns and 'unit_price' in df.columns:
                import numpy as np
                df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
                df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
                df['sales'] = df['quantity'] * df['unit_price']

                pd.set_option('display.max_columns', None)
                pd.set_option('display.float_format', "${:,.2f}".format)
                pivot = df.pivot_table(index='sales_region', columns='order_type', values='sales', aggfunc=[np.sum, np.mean], margins=True, margins_name='margins')
                print('\nPivot table (sales by region x order_type) with margins (fallback):')
                print(pivot)
        except Exception as e2:
            print('Retry failed:', e2)


if __name__ == '__main__':
    main()
