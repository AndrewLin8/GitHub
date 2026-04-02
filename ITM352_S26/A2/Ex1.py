# Read in a file from a URL and use a local CSV file with the first 10 rows.

import pandas as pd
import numpy as np
import pyarrow

filename = "https://drive.google.com/file/d/1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA/view?usp=sharing"

pd_set_option = pd.set_option('display.max_columns', None) # Show all columns in the script

df = pd.read_csv(filename, engine='pyarrow')

out_file = "sales_data_test.csv"
df.head(10).to_csv("first 10 rows", index=False)

