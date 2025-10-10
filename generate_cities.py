import pandas as pd
import json
import random
import os

# Paths
csv_path = os.path.join("data", "worldcities.csv")
os.makedirs("data", exist_ok=True)
json_path = os.path.join("data", "global_cities.json")

# Load dataset
df = pd.read_csv(csv_path)

# Optional: filter out tiny towns (population < 10k)
df = df[df["population"].notna()]  # remove rows with missing population
df = df[df["population"] >= 1000]  # optional lower limit

# Create weighted list: weight = city population
weights = df["population"].tolist()
coords = df[["lat", "lng"]].to_dict(orient="records")

# Sample 10,000 coordinates with weighting by population
sample_size = min(10000, len(coords))
sample = random.choices(coords, weights=weights, k=sample_size)

# Save to JSON
with open(json_path, "w") as f:
    json.dump(sample, f, indent=2)

print(f"✅ Saved {len(sample)} coordinates to {json_path}")
