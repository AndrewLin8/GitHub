import json
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt


def is_missing(value) -> bool:
	return value is None or str(value).strip() in {"", "NA", "NaN", "null", "None"}


def main() -> None:
	json_path = Path(__file__).parent.parent / "Trips from area 8.json"

	with open(json_path, "r", encoding="utf-8") as json_file:
		trips = json.load(json_file)

	tips_by_payment = defaultdict(float)

	for trip in trips:
		payment_method = trip.get("payment_type")
		tips_value = trip.get("tips")

		if is_missing(payment_method) or is_missing(tips_value):
			continue

		tips_by_payment[str(payment_method)] += float(tips_value)

	payment_methods = list(tips_by_payment.keys())
	tip_totals = [tips_by_payment[method] for method in payment_methods]

	plt.figure(figsize=(8, 5))
	plt.bar(payment_methods, tip_totals, edgecolor="black")
	plt.title("Total Tips by Payment Method")
	plt.xlabel("Payment Method")
	plt.ylabel("Sum of Tips")
	plt.tight_layout()
	plt.savefig("tips_by_payment_method.png")
	plt.close()

	print("Saved tips_by_payment_method.png")


if __name__ == "__main__":
	main()
