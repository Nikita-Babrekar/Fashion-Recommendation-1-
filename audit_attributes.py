import pandas as pd

# Load just the attributes and description to see the format
df = pd.read_csv("data/fashion_data.csv", usecols=['p_attributes', 'description'], nrows=20)

print("--- RAW ATTRIBUTES SNEAK PEEK ---")
for i, row in df.iterrows():
    print(f"Product {i+1}:")
    print(f"Attributes: {row['p_attributes']}")
    print(f"Description: {row['description'][:100]}...") # Just the first 100 chars
    print("-" * 20)