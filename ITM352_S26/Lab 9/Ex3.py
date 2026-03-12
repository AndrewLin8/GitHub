# Read the one thousand lines of text data from the taxi_1000.csv file
# Calculate the total of all fares, average fare, and the max.
# Trip distance

import csv
filename = "taxi_1000.csv"
with open(filename) as csvfile:
    csv_reader = csv.reader(csvfile)

    total_fare = 0.0
    max_distance = 0.0
    average_fare = 0.0
    num_rows = 0
    max_rows = 0

    for line in csv_reader:
        if (num_rows == 0):
            fare_index = line.index("fare")
            distance_index = line.index("Trip Mile")
            num_rows += 1
            continue
        
        trip_fare = float(line[16])
        trip_distance = float(line[4])
        total_fare += trip_fare
        if trip_distance > max_distance:
            max_distance = trip_distance
        max_rows += 1

if max_rows > 0:
    average_fare = total_fare / max_rows

print(f"Total Fare: ${total_fare:.2f}")
print(f"Average Fare: ${average_fare:.2f}")
print(f"Max Distance: {max_distance:.2f} miles")
