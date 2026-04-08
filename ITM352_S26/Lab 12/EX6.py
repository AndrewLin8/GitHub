import requests
from bs4 import BeautifulSoup
import re


URL = "https://www.hicentral.com/hawaii-mortgage-rates.php"


def fetch_mortgage_rate_rows(url: str) -> list[dict[str, str]]:
	response = requests.get(url, timeout=30)
	response.raise_for_status()

	# Parse HTML so we can search and extract table data.
	soup = BeautifulSoup(response.text, "html.parser")
	rate_table = soup.find("table")

	if rate_table is None:
		raise ValueError("Could not find a mortgage rate table on the page.")

	# Collect all table rows.
	rows = rate_table.find_all("tr")
	extracted_rows: list[dict[str, str]] = []
	current_lender = ""

	# Skip the first row because it is the column header.
	for row in rows[1:]:
		cells = [cell.get_text(" ", strip=True) for cell in row.find_all(["td", "th"])]

		if not cells:
			continue

		if len(cells) == 5:
			current_lender, term_type, interest_rate, points, apr = cells
		elif len(cells) == 4:
			if not current_lender:
				continue
			term_type, interest_rate, points, apr = cells
		else:
			continue

		# Save one normalized output record per mortgage row.
		extracted_rows.append(
			{
				"lender": current_lender,
				"term_type": term_type,
				"interest_rate": interest_rate,
				"points": points,
				"apr": apr,
			}
		)

	return extracted_rows


if __name__ == "__main__":
	# Retrieve all mortgage rate rows from the source page.
	mortgage_rows = fetch_mortgage_rate_rows(URL)

	print("Bank name and current rates (per row):")
	for row in mortgage_rows:
		# Remove phone/NMLS details so only the bank/lender name is shown.
		bank_name = re.sub(r"\s+\d{3}-\d{3}-\d{4}.*$", "", row["lender"]).strip()
		print(
			f"Bank: {bank_name} | "
			f"Term/Type: {row['term_type']} | "
			f"Interest Rate: {row['interest_rate']} | "
			f"Points: {row['points']} | "
			f"APR: {row['apr']}"
		)

	# Show how many mortgage rows were extracted in total.
	print(f"\nTotal rows extracted: {len(mortgage_rows)}")
