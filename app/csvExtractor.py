import csv
import pandas as pd

# Read input CSV
df = pd.read_csv("parties.csv")

# Extract party names
party_names = df["מטרות"].tolist()

# Create a new CSV file and write party names to it
with open("party_names.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Party Name"])
    for party_name in party_names:
        writer.writerow([party_name])

