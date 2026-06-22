# 🦅 Garud AI — Threat Intelligence Dashboard

A hybrid **rule-based + machine learning** dashboard that detects scams, fake news, hate speech, financial fraud, and misinformation in any text message — with full explainability and zero external API dependency.

Built for [Hackathon Name] · 2026

---

## ✨ Features

- **5 Detection Modules** — Scam, Fake News, Hate Speech, Financial Fraud, Misinformation
- **Hybrid AI** — Transparent rule-based scoring + an independent Naive Bayes ML classifier (97.49% accuracy)
- **Fully Explainable** — Every flagged signal is shown with the exact category and reasoning
- **100% Local** — No internet connection or API key required once installed
- **Accessible & Responsive** — Keyboard navigable, screen-reader friendly, mobile-responsive layout

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/garud-ai.git
cd garud-ai

# 2. Install dependencies
python -m pip install -r requirements.txt

# 3. Train the ML model (one-time — generates model.pkl + vectorizer.pkl)
python train_model.py

# 4. Run the app
python -m streamlit run app.py
```

The app opens automatically at `http://localhost:8501`.

---

## 🧱 Project Structure

```
garud-ai/
├── app.py              # Streamlit dashboard (UI + layout)
├── engine.py            # Rule-based detection engine (5 modules)
├── ml_engine.py          # ML inference wrapper (loads trained model)
├── train_model.py        # One-time training script (Naive Bayes + TF-IDF)
├── sms_dataset.tsv       # UCI SMS Spam Collection (training data)
├── requirements.txt      # Python dependencies
└── README.md
```

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Frontend | Streamlit + custom CSS |
| Backend Logic | Python (regex-based rule engine) |
| Machine Learning | scikit-learn (Multinomial Naive Bayes + TF-IDF) |
| Dataset | UCI SMS Spam Collection (5,574 labeled messages) |

---

## 📊 How Scoring Works

Each module (Scam, Fraud, etc.) scores 0–100 based on weighted keyword categories, with escalation for repeated signals. The **overall threat score** is driven by the single strongest module, plus a small bonus when multiple modules fire — ensuring one severe signal is never diluted by quieter ones.

The ML module runs independently, giving a second, statistically-trained opinion alongside the explainable rule engine.

---

## 📄 License

This project was built for hackathon purposes. Feel free to fork and build on it.
