import json
from pathlib import Path

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def is_missing(value) -> bool:
	return value is None or str(value).strip() in {"", "NA", "NaN", "null", "None"}


def main() -> None:
	json_path = Path(__file__).resolve().parent.parent / "Trips from area 8.json"

	with open(json_path, "r", encoding="utf-8") as json_file:
		trips = json.load(json_file)

	fares = []
	miles = []
	dropoff_areas = []

	for trip in trips:
		fare = trip.get("fare")
		trip_miles = trip.get("trip_miles")
		dropoff_area = trip.get("dropoff_community_area")

		if is_missing(fare) or is_missing(trip_miles) or is_missing(dropoff_area):
			continue

		fares.append(float(fare))
		miles.append(float(trip_miles))
		dropoff_areas.append(float(dropoff_area))

	fig = plt.figure(figsize=(8, 6))
	axes = fig.add_subplot(111, projection="3d")
	axes.scatter(fares, miles, dropoff_areas, alpha=0.6)
	axes.set_title("3D Plot of Fare, Trip Miles, and Dropoff Area")
	axes.set_xlabel("Fare")
	axes.set_ylabel("Trip Miles")
	axes.set_zlabel("Dropoff Area")
	plt.tight_layout()
	plt.savefig("fare_miles_dropoff_3d.png")
	plt.close()

	print("Saved fare_miles_dropoff_3d.png")


if __name__ == "__main__":
	main()
