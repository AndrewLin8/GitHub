# Read the one thousand lines of text data from the taxi_1000.csv file
# Calculate the total of all fares, average fare, and the max trip distance.

import csv
from pathlib import Path

file_path = Path(__file__).parent.parent / "taxi_1000.csv"

total_fare = 0.0
max_distance = 0.0
num_rows = 0
fare_index = None
distance_index = None

with open(file_path) as csvfile:
    csv_reader = csv.reader(csvfile)

    for line in csv_reader:
        if fare_index is None:
            fare_index = line.index("Fare")
            distance_index = line.index("Trip Miles")
            continue

        fare_val = line[fare_index].strip()
        dist_val = line[distance_index].strip()

        if fare_val and dist_val:
            trip_fare = float(fare_val)
            trip_distance = float(dist_val)
            total_fare += trip_fare
            if trip_distance > max_distance:
                max_distance = trip_distance
            num_rows += 1

average_fare = total_fare / num_rows if num_rows > 0 else 0.0

print(f"Rows processed: {num_rows}")
print(f"Total Fare:     ${total_fare:.2f}")
print(f"Average Fare:   ${average_fare:.2f}")
print(f"Max Distance:   {max_distance:.2f} miles")
