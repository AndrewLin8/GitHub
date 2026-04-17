import json
from pathlib import Path

import matplotlib.pyplot as plt


def is_missing(value) -> bool:
	return value is None or str(value).strip() in {"", "NA", "NaN", "null", "None"}


def load_fare_and_miles(json_path: Path) -> tuple[list[float], list[float]]:
	with open(json_path, "r", encoding="utf-8") as json_file:
		trips = json.load(json_file)

	fares = []
	miles = []

	for trip in trips:
		fare = trip.get("fare")
		trip_miles = trip.get("trip_miles")

		if is_missing(fare) or is_missing(trip_miles):
			continue

		fares.append(float(fare))
		miles.append(float(trip_miles))

	return fares, miles


def main() -> None:
	json_path = Path(__file__).resolve().parent.parent / "Trips from area 8.json"
	fares, miles = load_fare_and_miles(json_path)

	plt.figure(figsize=(8, 5))
	plt.plot(fares, miles, linestyle="none", marker="v", color="cyan", alpha=0.2)
	plt.title("Fare vs. Trip Miles")
	plt.xlabel("Fare")
	plt.ylabel("Trip Miles")
	plt.tight_layout()
	plt.savefig("fare_vs_miles_fancy.png")
	plt.close()

	print("Saved fare_vs_miles_fancy.png")
	print("Conclusion: fares and trip miles have a strong positive relationship, so longer trips usually cost more, although the points still show some spread.")


if __name__ == "__main__":
	main()
