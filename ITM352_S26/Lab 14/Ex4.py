import json
from pathlib import Path

import matplotlib.pyplot as plt


def is_missing(value) -> bool:
	return value is None or str(value).strip() in {"", "NA", "NaN", "null", "None"}


def main() -> None:
	json_path = Path(__file__).resolve().parent.parent / "Trips_Fri07072017T4 trip_miles gt1.json"

	with open(json_path, "r", encoding="utf-8") as json_file:
		trips = json.load(json_file)

	fares = []
	tips = []

	for trip in trips:
		fare = trip.get("fare")
		tip = trip.get("tips")

		if is_missing(fare) or is_missing(tip):
			continue

		fares.append(float(fare))
		tips.append(float(tip))

	plt.figure(figsize=(8, 5))
	plt.scatter(fares, tips, alpha=0.6, edgecolors="none")
	plt.title("Scatter Plot of Fare vs. Tips")
	plt.xlabel("Fare")
	plt.ylabel("Tips")
	plt.tight_layout()
	plt.savefig("fare_vs_tips_scatter.png")
	plt.close()

	print("Saved fare_vs_tips_scatter.png")


if __name__ == "__main__":
	main()
