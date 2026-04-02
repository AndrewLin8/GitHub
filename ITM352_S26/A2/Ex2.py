# Read in a file from a URL and use a local CSV file with the first 10 rows.

import time

import pandas as pd
import numpy as np
import pyarrow



def load_csv(filepath):
    print(f"Loading CSV file from: {filepath}")
    start_time = time.time()
    try:
        df = pd.read_csv(filepath, engine='pyarrow')
        end_time = time.time()
        load_time = end_time - start_time
        print(f"CSV file loaded successfully in {load_time:.2f} seconds.")
        print(f"number of rows: {len(df)}")
        print(f"number of columns: {len(df.columns)}")
        df['order_date'] = pd.to_datetime(df['order_date'], format='%Y-%m-%d', errors='coerce') # Convert order_date to datetime format, coerce errors to NaT
        df.fillna(0, inplace=True) # Fill missing values with 0

        required_column = ['quantity', 'unit_price', 'order_date']
        # Check if required columns are present
        missing_columns = [col for col in required_column if col not in df.columns]
        if missing_columns:
            print(f"Warning: Missing required columns: {missing_columns}")
        else:
            print("All required columns are present.")

        return df
    
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None

# Call load csv to load the data and print the first 10 rows.
filename = "https://drive.google.com/file/d/1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA/view?usp=sharing"
#filename = "sales_data_test.csv"
sales_data = load_csv(filename)

if sales_data is not None:
    print(sales_data.head(10))
    

