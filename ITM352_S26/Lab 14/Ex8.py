from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def main() -> None:
	csv_path = Path(__file__).resolve().parent.parent / "taxi trips Fri 7_7_2017.csv"
	df = pd.read_csv(csv_path)

	filtered_df = df[["pickup_community_area", "dropoff_community_area"]].dropna()
	filtered_df["pickup_community_area"] = filtered_df["pickup_community_area"].astype(int)
	filtered_df["dropoff_community_area"] = filtered_df["dropoff_community_area"].astype(int)

	heatmap_data = pd.crosstab(
		filtered_df["pickup_community_area"],
		filtered_df["dropoff_community_area"],
	)

	plt.figure(figsize=(12, 10))
	sns.heatmap(heatmap_data, cmap="YlOrRd")
	plt.title("Pickup and Dropoff Community Area Heatmap")
	plt.xlabel("Dropoff Community Area")
	plt.ylabel("Pickup Community Area")
	plt.tight_layout()
	plt.savefig("pickup_dropoff_heatmap.png")
	plt.close()

	print("Saved pickup_dropoff_heatmap.png")


if __name__ == "__main__":
	main()
