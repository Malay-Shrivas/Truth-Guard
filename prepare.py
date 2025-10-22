import pandas as pd

# Load real and fake news
real = pd.read_csv("True.csv")
fake = pd.read_csv("Fake.csv")

real["label"] = 0  # Real
fake["label"] = 1  # Fake

# Combine
df = pd.concat([real, fake], ignore_index=True)

# Keep only headlines (title) and label
df = df[["title", "label"]].dropna()

# Save
df.to_csv("combined.csv", index=False)
print("✅ Saved combined.csv with", len(df), "headlines.")
