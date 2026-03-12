import csv
import os

filename = "my_custom_spreadsheet.csv"
salaries = []

if os.path.exists(filename):
    
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Skip the headers row
        salary_index = headers.index("Annual_Salary")

        print(headers)
        for row in reader:
            print(row)
            salaries.append(float(row[salary_index].replace(",", "")))

    print(salaries)
    if salaries:
        average_salary = sum(salaries) / len(salaries)
        print(f"Average Salary: ${average_salary:.2f}")
        max_salary = max(salaries)
        print(f"Max Salary: ${max_salary:.2f}")
        min_salary = min(salaries)
        print(f"Min Salary: ${min_salary:.2f}")
    else:
        print("No salary data found.")
else:
    print(f"File {filename} does not exist.")