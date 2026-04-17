import json
from pathlib import Path

import matplotlib.pyplot as plt


def is_missing(value) -> bool:
	return value is None or str(value).strip() in {"", "NA", "NaN", "null", "None"}


def main() -> None:
	json_path = Path(__file__).resolve().parent.parent / "Trips from area 8.json"

	with open(json_path, "r", encoding="utf-8") as json_file:
		trips = json.load(json_file)

	fares = []
	miles = []

	for trip in trips:
		fare = trip.get("fare")
		trip_miles = trip.get("trip_miles")

		if is_missing(fare) or is_missing(trip_miles):
			continue

		trip_miles = float(trip_miles)
		if trip_miles == 0 or trip_miles < 2:
			continue

		fares.append(float(fare))
		miles.append(trip_miles)

	plt.figure(figsize=(8, 5))
	plt.scatter(fares, miles, alpha=0.6)
	plt.title("Fares vs. Trip Miles")
	plt.xlabel("Fare")
	plt.ylabel("Trip Miles")
	plt.tight_layout()
	plt.savefig("FaresXmiles.png")
	plt.close()

	print("Saved FaresXmiles.png")
	print("Anomalies: a few trips have much higher fares than expected for their miles, especially around 3-4 miles and 17-18 miles, so there are some clear outliers above the main trend.")


if __name__ == "__main__":
	main()
