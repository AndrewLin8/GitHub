# Read in a  file from a URL and save a local CSV file with the first 10 rows.

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


def total_sales_by_region_and_order_type(dataframe):
    result = (
        dataframe
        .groupby(['sales_region', 'order_type'], dropna=False)['sales']
        .sum()
        .reset_index()
        .sort_values(['sales_region', 'order_type'])
    )
    print("\nTotal sales by region and order type:")
    print(result)


def average_sales_views(dataframe):
    by_region = (
        dataframe
        .groupby('sales_region', dropna=False)['sales']
        .mean()
        .reset_index(name='avg_sales')
        .sort_values('sales_region')
    )

    by_state_and_type = (
        dataframe
        .groupby(['customer_state', 'order_type'], dropna=False)['sales']
        .mean()
        .reset_index(name='avg_sales')
        .sort_values(['customer_state', 'order_type'])
    )

    print("\nAverage sales by region:")
    print(by_region)
    print("\nAverage sales by state and sale type:")
    print(by_state_and_type)


def sales_by_customer_and_order_type_by_state(dataframe):
    result = (
        dataframe
        .groupby(['customer_state', 'customer_type', 'order_type'], dropna=False)['sales']
        .sum()
        .reset_index()
        .sort_values(['customer_state', 'customer_type', 'order_type'])
    )
    print("\nSales by customer type and order type by state:")
    print(result)


def total_quantity_and_sales_by_region_and_product(dataframe):
    result = (
        dataframe
        .groupby(['sales_region', 'produce_name'], dropna=False)
        .agg(total_quantity=('quantity', 'sum'), total_sales=('sales', 'sum'))
        .reset_index()
        .sort_values(['sales_region', 'produce_name'])
    )
    print("\nTotal sales quantity and price by region and product:")
    print(result)


def total_quantity_and_sales_by_customer_type(dataframe):
    result = (
        dataframe
        .groupby('customer_type', dropna=False)
        .agg(total_quantity=('quantity', 'sum'), total_sales=('sales', 'sum'))
        .reset_index()
        .sort_values('customer_type')
    )
    print("\nTotal sales quantity and price by customer type:")
    print(result)


def max_min_sales_price_by_category(dataframe):
    result = (
        dataframe
        .groupby('product_category', dropna=False)
        .agg(max_sales_price=('unit_price', 'max'), min_sales_price=('unit_price', 'min'))
        .reset_index()
        .sort_values('product_category')
    )
    print("\nMax and min sales price by category:")
    print(result)

def show_employees_by_region(dataframe):
    pivot_table = pd.pivot_table(dataframe, values='employee_id', index='sales_region', aggfunc=pd.Series.nunique)
    pivot_table.columns = ['Number of Employees']
    print("\nNumber of employees by region:")
    print(pivot_table)
    return

# Create a pivot table generator. (AI helped with this)
def create_custom_pivot_table(dataframe):
    print("\n--- Pivot Table Generator ---")

    row_choices = {
        '1': 'employee_name',
        '2': 'sales_region',
        '3': 'product_category'
    }

    column_choices = {
        '1': 'order_type',
        '2': 'customer_type'
    }

    value_choices = {
        '1': 'quantity',
        '2': 'sales'
    }

    agg_choices = {
        '1': 'sum',
        '2': 'mean',
        '3': 'count'
    }

    def parse_multi_selection(user_input, choices, allow_empty=False):
        if allow_empty and user_input.strip() == '':
            return []

        selected_keys = [item.strip() for item in user_input.split(',') if item.strip()]
        if not selected_keys:
            return None

        if any(key not in choices for key in selected_keys):
            return None

        # Remove duplicates while saving the order
        selected_fields = []
        for key in selected_keys:
            field_name = choices[key]
            if field_name not in selected_fields:
                selected_fields.append(field_name)

        return selected_fields

    print("\nSelect rows:")
    print("1. employee_name")
    print("2. sales_region")
    print("3. product_category")
    row_input = input("Enter the number(s) of your choice(s), separated by commas: ")
    index_fields = parse_multi_selection(row_input, row_choices)
    if not index_fields:
        print("Invalid row selection.")
        return

    print("\nSelect columns (optional):")
    print("1. order_type")
    print("2. customer_type")
    column_input = input("Enter the number(s) of your choice(s), separated by commas (enter for no grouping): ")
    column_fields = parse_multi_selection(column_input, column_choices, allow_empty=True)
    if column_fields is None:
        print("Invalid column selection.")
        return

    print("\nSelect values:")
    print("1. quantity")
    print("2. sale_price")
    value_input = input("Enter the number(s) of your choice(s), separated by commas: ")
    value_fields = parse_multi_selection(value_input, value_choices)
    if not value_fields:
        print("Invalid values selection.")
        return

    print("\nSelect aggregation function:")
    print("1. sum")
    print("2. mean")
    print("3. count")
    agg_input = input("Enter the number(s) of your choice(s), separated by commas: ").strip()
    agg_key = agg_input.split(',')[0].strip() if agg_input else ''
    if agg_key not in agg_choices:
        print("Invalid aggregation function selection.")
        return
    aggfunc_name = agg_choices[agg_key]

    try:
        pivot_table = pd.pivot_table(
            dataframe,
            values=value_fields,
            index=index_fields,
            columns=column_fields if column_fields else None,
            aggfunc=aggfunc_name,
            dropna=False
        )
        print("\nCustom pivot table result:")
        print(pivot_table)
    except Exception as e:
        print(f"Error creating custom pivot table: {e}")

def exit_program(dataframe):
    print("Exiting the program. Goodbye!")
    exit(0)


def display_menu(dataframe):
    menu_options = (
        ("Show the first n rows of sales data", display_initial_rows),
        ("Total sales by region and order_type", total_sales_by_region_and_order_type),
        ("Average sales by region with average sales by state and sale type", average_sales_views),
        ("Sales by customer type and order type by state.", sales_by_customer_and_order_type_by_state),
        ("Total sales quantity and price by region and product", total_quantity_and_sales_by_region_and_product),
        ("Total sales quantity and price customer type", total_quantity_and_sales_by_customer_type),
        ("Max and min sales price of ales by category", max_min_sales_price_by_category),
        ("Number of unique employees by region", show_employees_by_region),
        ("Create a custom pivot table", create_custom_pivot_table),
        ("Exit", exit_program)      
    )

    print("\n--- Sales Data Dashboard ---")
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
    if sales_data is None:
        print("Unable to start dashboard because data could not be loaded.")
        return

    while True:
        display_menu(sales_data)

# Check if this is the main module being run
if __name__ == "__main__":
    main()