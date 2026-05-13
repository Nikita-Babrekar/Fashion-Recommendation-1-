import pandas as pd

# Load ONLY the 'colour' column to save your laptop's RAM
print("Reading colors from the 3GB file... please wait...")

# We load the whole column, but nothing else, so it stays fast
df_colors = pd.read_csv("data/fashion_data.csv", usecols=['colour'])

# Get every unique color name and remove any 'NaN' (empty) values
unique_colors = df_colors['colour'].dropna().unique()

# Sort them alphabetically so they are easy to read
unique_colors.sort()

print(f"\nSUCCESS! Found {len(unique_colors)} unique colors.")
print("-" * 30)
print(unique_colors)
print("-" * 30)

# Optional: Save this list to a text file so you don't have to run this again
with open("color_list.txt", "w") as f:
    f.write("\n".join(unique_colors))
    print("Saved color names to 'color_list.txt'")