import pandas as pd

# Load the two CSV files (they're in the same folder)
print("Loading True.csv and Fake.csv...")
real = pd.read_csv("True.csv")
fake = pd.read_csv("Fake.csv")

# Add labels: 0 = real, 1 = fake
real["label"] = 0
fake["label"] = 1

# Combine into one dataset
df = pd.concat([real, fake], ignore_index=True)

# Keep only the headline (title) and label, and remove any rows with missing titles
df = df[["title", "label"]].dropna()

# Save as a single clean CSV
df.to_csv("isot_fake_news.csv", index=False)

print(f"✅ Done! Combined {len(df)} headlines.")
print(f" - Real news: {sum(df['label'] == 0)}")
print(f" - Fake news: {sum(df['label'] == 1)}")
print("Saved as 'isot_fake_news.csv'")