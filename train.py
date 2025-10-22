import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib

# Load data
df = pd.read_csv("combined.csv")
X = df["title"]
y = df["label"]

# Train model
model = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words="english", max_features=5000, ngram_range=(1,2))),
    ("clf", LogisticRegression(random_state=42, max_iter=1000))
])

print("Training model...")
model.fit(X, y)
joblib.dump(model, "model.pkl")
print("✅ Model saved as model.pkl")