import json
from pathlib import Path

import matplotlib.pyplot as plt


def main() -> None:
	json_path = Path(__file__).parent.parent / "Trips from area 8.json"

	with open(json_path, "r", encoding="utf-8") as json_file:
		trips = json.load(json_file)

	trip_miles = [float(trip["trip_miles"]) for trip in trips if "trip_miles" in trip]

	plt.figure(figsize=(8, 5))
	plt.hist(trip_miles, bins=20, edgecolor="black")
	plt.title("Histogram of Trip Miles")
	plt.xlabel("Trip Miles")
	plt.ylabel("Frequency")
	plt.tight_layout()
	plt.savefig("trip_miles_histogram.png")
	plt.close()

	print("Saved trip_miles_histogram.png")


if __name__ == "__main__":
	main()
