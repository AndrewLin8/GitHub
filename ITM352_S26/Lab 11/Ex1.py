# Read in a CSV file and create a dataframe

import pandas as pd
import numpy as np
import pyarrow
filename = "https://drive.google.com/uc?id=1ujY0WCcePdotG2xdbLyeECFW9lCJ4t-K"

pd_set_option = pd.set_option('display.max_columns', None) # Show all columns in the script

df = pd.read_csv(filename, engine='pyarrow')
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce') # Convert order_date to datetime format, coerce errors to NaT

print(df.info())
print(df.describe())
print(df.head())