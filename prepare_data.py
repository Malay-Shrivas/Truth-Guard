import pandas as pd

data = {
    'title': [
        "Scientists discover new planet in habitable zone",
        "Aliens landed in New York, government hides truth",
        "Stock market hits all-time high amid economic recovery",
        "Celebrity dies in bizarre accident involving UFO",
        "Vaccines proven safe in largest global study",
        "Secret moon base revealed by whistleblower",
        "Local school wins national science fair",
        "Miracle cure for cancer found in backyard garden"
    ],
    'label': ['REAL', 'FAKE', 'REAL', 'FAKE', 'REAL', 'FAKE', 'REAL', 'FAKE']
}

df = pd.DataFrame(data)
df['label'] = df['label'].map({'REAL': 0, 'FAKE': 1})
df.to_csv('fake_news_headlines.csv', index=False)
print("✅ Sample dataset created: fake_news_headlines.csv")
