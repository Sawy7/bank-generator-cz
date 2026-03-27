"""Bank code list importer."""

import argparse
import csv
from importlib import resources

import requests

import bank_generator_cz

BANK_CODES_PY = str(resources.files(bank_generator_cz) / "bank_codes.py")


def generate(url):
    """Generate bank_codes.py from the latest data."""
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    if not response.ok:
        raise AssertionError("Could not download CSV with bank codes.")

    csv_file = csv.reader(response.text.splitlines(), delimiter=";")
    header = next(csv_file)
    with open(BANK_CODES_PY, "w") as codes_file:
        codes_file.write('"""Current CZ bank codes.\n\n')
        codes_file.write("Data labels:\n")
        codes_file.write(f'{", ".join(header)}\n"""\n\n')
        codes_file.write("BANKS_CZ = (\n")
        for row in csv_file:
            bank_values = [f'"{col}"' for col in row]
            codes_file.write(f"    ({', '.join(bank_values)}),\n")
        codes_file.write(")\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="generate_bank_list", description="Import bank codes from CSV (web url)")
    parser.add_argument(
        "--url",
        type=str,
        help="URL with CSV file to import.",
        default="https://www.cnb.cz/cs/platebni-styk/.galleries/ucty_kody_bank/download/kody_bank_CR.csv",
    )
    args = parser.parse_args()
    generate(args.url)
