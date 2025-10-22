# test_clean.py
import os
os.environ["HF_HUB_DISABLE_IMPLICIT_TOKEN"] = "1"

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

print("Testing with jy46604793/Fake-News-Bert-Detect...")

model_name = "vikram71198/distilroberta-base-finetuned-fake-news-detection"

try:
    tokenizer = AutoTokenizer.from_pretrained(model_name, token=False)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, token=False)
    print("✅ Model loaded!")

    # Test
    inputs = tokenizer("The government announced new economic reforms.", return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits
    probs = torch.softmax(logits, dim=-1).tolist()[0]
    pred = "Real" if probs[1] > probs[0] else "Fake"
    print(f"Prediction: {pred} (Fake: {probs[0]:.2%}, Real: {probs[1]:.2%})")

except Exception as e:
    print("❌ Error:", e)