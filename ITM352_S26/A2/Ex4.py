# Read in a  file from a URL and save a local CSV file with the first 10 rows.
# 

import time

import pandas as pd
import numpy as np
import pyarrow


pd.set_option('display.max_columns', None)  # Show all columns in the output


def load_csv(filepath):
    print(f"Loading data from {filepath}...")
    start_time = time.time()
    try:
        df = pd.read_csv(filepath, engine='python')
        end_time = time.time()
        load_time = end_time - start_time
        print(f"CSV file loaded succesfully in {load_time:.2f} seconds.")
        print(f"number of rows: {len(df)}")
        print(f"Columns: {df.columns.tolist()}")
        df['order_date'] = pd.to_datetime(df['order_date'], format='%m/%d/%Y', errors='coerce')  # Convert order_date to datetime, coercing errors to NaT
#        df.fillna(0, inplace=True)  # Fill NaN values with 0 for numeric columns
        df['sales'] = df['quantity'] * df['unit_price']  # Create a new 'sales' column as quantity * unit_price

        required_columns = ['quantity', 'unit_price', 'order_date']
        # Check if required columns are present
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"Warning: Missing required columns: {missing_columns}")        
        else: 
            print("All required columns are present.")

        return df
    
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None


def display_initial_rows(dataframe):
    print("Enter rows to display:")
    print(f"- Enter a number 1 to {len(dataframe)}")
    print("- Enter 'all' to display all rows")
    print("- to skip preview, press Enter")
    user_input = input("Your choice: ").strip().lower()

    if user_input == '':
        print("Skipping preview.")
        return
    elif user_input == 'all':
        print("Displaying all rows:")
        print(dataframe)
    elif user_input.isdigit() and 1 <= int(user_input) <= len(dataframe):
        print(f"Displaying first {user_input} rows:")
        print(dataframe.head(int(user_input)))
    else:
        print("Invalid input. Please try again.")


def average_sales_by_region_state_and_type(dataframe):
    print("\nAverage sales by region:")
    by_region = pd.pivot_table(
        dataframe,
        values='sales',
        index='sales_region',
        aggfunc='mean'
    )
    by_region.columns = ['Average Sales']
    print(by_region)

    print("\nAverage sales by state and sale type:")
    by_state_type = pd.pivot_table(
        dataframe,
        values='sales',
        index=['customer_state', 'order_type'],
        aggfunc='mean'
    )
    by_state_type.columns = ['Average Sales']
    print(by_state_type)


def sales_by_customer_and_order_type_by_state(dataframe):
    print("\nSales by customer type and order type by state:")
    result = pd.pivot_table(
        dataframe,
        values='sales',
        index=['customer_state', 'customer_type', 'order_type'],
        aggfunc='sum'
    )
    result.columns = ['Total Sales']
    print(result)


def total_quantity_and_price_by_region_and_product(dataframe):
    print("\nTotal sales quantity and price by region and product:")
    result = pd.pivot_table(
        dataframe,
        values=['quantity', 'sales'],
        index=['sales_region', 'produce_name'],
        aggfunc='sum'
    )
    print(result)


def total_quantity_and_price_by_customer_type(dataframe):
    print("\nTotal sales quantity and price by customer type:")
    result = pd.pivot_table(
        dataframe,
        values=['quantity', 'sales'],
        index='customer_type',
        aggfunc='sum'
    )
    print(result)


def max_min_sales_price_by_category(dataframe):
    print("\nMax and min sales price by category:")
    result = dataframe.groupby('product_category')['unit_price'].agg(['max', 'min'])
    result.columns = ['Max Sales Price', 'Min Sales Price']
    print(result)


def create_custom_pivot_table(dataframe):
    print("\nCreate a custom pivot table")
    print(f"Available columns: {', '.join(dataframe.columns)}")

    values_col = input("Enter values column: ").strip()
    index_input = input("Enter index column(s), comma-separated: ").strip()
    columns_col = input("Enter columns column (or press Enter to skip): ").strip()
    aggfunc = input("Enter aggregation (sum, mean, min, max, count, nunique): ").strip().lower()

    if values_col not in dataframe.columns:
        print("Invalid values column.")
        return

    index_cols = [col.strip() for col in index_input.split(',') if col.strip()]
    if not index_cols:
        print("You must provide at least one index column.")
        return

    invalid_index_cols = [col for col in index_cols if col not in dataframe.columns]
    if invalid_index_cols:
        print(f"Invalid index columns: {invalid_index_cols}")
        return

    if columns_col and columns_col not in dataframe.columns:
        print("Invalid columns column.")
        return

    if aggfunc not in ['sum', 'mean', 'min', 'max', 'count', 'nunique']:
        print("Invalid aggregation function.")
        return

    try:
        custom_pivot = pd.pivot_table(
            dataframe,
            values=values_col,
            index=index_cols,
            columns=columns_col if columns_col else None,
            aggfunc=aggfunc
        )
        print("\nCustom pivot table:")
        print(custom_pivot)
    except Exception as e:
        print(f"Error creating custom pivot table: {e}")

def show_employees_by_region(dataframe):
    pivot_table = pd.pivot_table(dataframe, values='employee_id', index='sales_region', aggfunc=pd.Series.nunique)
    pivot_table.columns = ['Number of Employees']
    print("\nNumber of employees by region:")
    print(pivot_table)
    return

def exit_program(dataframe):
    print("Exiting the program. Goodbye!")
    exit(0)


def display_menu(dataframe):
    menu_options = (
        ("Show the first n rows of sales data", display_initial_rows),
        ("Show the number of employees by region", show_employees_by_region),
        ("Average sales by region with average sales by state and sale type", average_sales_by_region_state_and_type),
        ("Sales by customer type and order type by state", sales_by_customer_and_order_type_by_state),
        ("Total sales quantity and price by region and product", total_quantity_and_price_by_region_and_product),
        ("Total sales quantity and price by customer type", total_quantity_and_price_by_customer_type),
        ("Max and min sales price by category", max_min_sales_price_by_category),
        ("Number of unique employees by region", show_employees_by_region),
        ("Create a custom pivot table", create_custom_pivot_table),
        ("Exit", exit_program)      
    )

    print("\nAvailable options:")
    for i, (description, _) in enumerate(menu_options, start=1):
        print(f"{i}. {description}")

    try:
        menu_len = len(menu_options)
        choice = int(input(f"Enter your choice (1-{menu_len}): "))
        if 1 <= choice <= menu_len:
            action = menu_options[choice - 1][1]
            action(dataframe)
        else:
            print("Invalid choice. Please enter a number corresponding to the options.")

    except ValueError:
        print("Invalid input. Please enter a number corresponding to the options.")


# Call load_csv to load the data and print the first 10 rows
#filename = "https://drive.google.com/uc?id=1ujY0WCcePdotG2xdbLyeECFW9lCJ4t-K"
filename = "sales_data_test.csv"
sales_data = load_csv(filename)


# Run the main processing loop
def main():
    while True:
        print("Sales Data Dashboard")
        display_menu(sales_data)

# Check if this is the main module being run
if __name__ == "__main__":
    main()