# train_model.py – Garud AI ML Module
# Trains a Naive Bayes spam classifier on the UCI SMS Spam Collection dataset.
# This is classic ML (NOT deep learning) — fast, lightweight, and explainable.
#
# Run this ONCE to generate model.pkl + vectorizer.pkl:
#     python train_model.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle

print("📂 Loading dataset...")
# Dataset: UCI SMS Spam Collection (5,574 labeled messages: ham/spam)
df = pd.read_csv("sms_dataset.tsv", sep="\t", header=None, names=["label", "message"])
print(f"   Loaded {len(df)} messages  →  {(df.label=='spam').sum()} spam / {(df.label=='ham').sum()} ham")

# Convert labels to binary (spam=1, ham=0)
df["target"] = (df["label"] == "spam").astype(int)

# Split into train/test sets
X_train, X_test, y_train, y_test = train_test_split(
    df["message"], df["target"], test_size=0.2, random_state=42, stratify=df["target"]
)

print("\n🔤 Vectorizing text (TF-IDF)...")
# TF-IDF converts text into numeric features based on word importance
vectorizer = TfidfVectorizer(lowercase=True, stop_words="english", max_features=3000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

print("🧠 Training Naive Bayes classifier...")
# Multinomial Naive Bayes — simple, fast, works great for text classification
model = MultinomialNB()
model.fit(X_train_vec, y_train)

# Evaluate
y_pred = model.predict(X_test_vec)
acc = accuracy_score(y_test, y_pred)
print(f"\n✅ Test Accuracy: {acc*100:.2f}%")
print("\n" + classification_report(y_test, y_pred, target_names=["ham", "spam"]))

# Save model + vectorizer to disk
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("\n💾 Saved model.pkl and vectorizer.pkl — ready to use in app.py!")
