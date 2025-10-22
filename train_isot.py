# train_isot.py
import pandas as pd
from datasets import Dataset
from transformers import (
    DistilBertTokenizer,
    DistilBertForSequenceClassification,
    Trainer,
    TrainingArguments,
    DataCollatorWithPadding
)
import torch
import numpy as np

print("📂 Loading ISOT dataset...")
df = pd.read_csv("isot_fake_news.csv")
print(f"✅ Loaded {len(df)} headlines.")

# Initialize tokenizer
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")

def tokenize(batch):
    return tokenizer(batch["title"], truncation=True, padding=True, max_length=128)

# Prepare dataset
dataset = Dataset.from_pandas(df)
tokenized = dataset.map(tokenize, batched=True)
tokenized = tokenized.rename_column("label", "labels")
tokenized.set_format("torch", columns=["input_ids", "attention_mask", "labels"])

# Split into train (90%) and eval (10%)
split = tokenized.train_test_split(test_size=0.1)
train_ds = split["train"]
eval_ds = split["test"]

# Load model
print("🧠 Loading DistilBERT model...")
model = DistilBertForSequenceClassification.from_pretrained(
    "distilbert-base-uncased", num_labels=2
)

# Use Apple Silicon GPU (MPS) if available, else CPU
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
model.to(device)
print(f"➡️  Training on {device}")

# Training configuration
training_args = TrainingArguments(
    output_dir="./isot_model",
    num_train_epochs=2,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    warmup_steps=200,
    weight_decay=0.01,
    logging_steps=100,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="eval_accuracy",
    greater_is_better=True,
    report_to="none",
    fp16=torch.backends.mps.is_available(),  # Faster on M1/M2/M3
)

def compute_metrics(eval_pred):
    preds, labels = eval_pred
    preds = np.argmax(preds, axis=1)
    accuracy = (preds == labels).mean()
    return {"accuracy": accuracy}

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_ds,
    eval_dataset=eval_ds,
    tokenizer=tokenizer,
    data_collator=DataCollatorWithPadding(tokenizer),
    compute_metrics=compute_metrics,
)

print("🚀 Starting training (this will take 20–60 minutes)...")
trainer.train()

# Save final model and tokenizer
trainer.save_model("./isot_model")
tokenizer.save_pretrained("./isot_model")
print("✅ Training complete! Model saved to ./isot_model")
