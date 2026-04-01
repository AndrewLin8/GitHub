# Read in a CSV file and create a dataframe
# Pivot the dataframe, aggregating sales by region, with columns defined by order_type and totals.
# Adding in sub-columns showing the average sales by state and by sale type (retail or wholesale).

import pandas as pd
import numpy as np
import pyarrow

filename = "https://drive.google.com/uc?id=1ujY0WCcePdotG2xdbLyeECFW9lCJ4t-K"

pd_set_option = pd.set_option('display.max_columns', None) # Show all columns in the script
pd.set_option('display.float_format', "${:,.2f}".format) # Format float values to 2 decimal places

df = pd.read_csv(filename, engine='pyarrow')
df['order_date'] = pd.to_datetime(df['order_date'], format='%m-%d-%y', errors='coerce') # Convert order_date to datetime format, coerce errors to NaT

# Coerce quantity and unit_price to numeric, setting earrors to NaN
df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
df['sales'] = df['quantity'] * df['unit_price'] # Calculate sales as quantity multiplied by unit price

# Support common state column names in class datasets.
state_col_candidates = ['state', 'customer_state', 'ship_state']
state_col = next((c for c in state_col_candidates if c in df.columns), None)

if state_col is None:
    raise KeyError(f"Could not find a state column. Tried: {state_col_candidates}")

# Add sub-columns showing average sales by state and by sale type 
pivot_table = pd.pivot_table(
    df,
    index='sales_region',
    values='sales',
    columns=[state_col, 'order_type'],
    aggfunc='mean',
    margins=True,
    margins_name='Average Sales'
)

print(pivot_table)