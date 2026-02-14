🛡️ Aegis — AI-Based Phishing Detection System
📌 Overview

Aegis is a hybrid AI-powered phishing detection system designed to protect users from malicious and deceptive URLs. It combines machine learning with security heuristics and explainable AI to classify URLs as Legitimate, Suspicious, or Phishing.

The system prioritizes real-world security behavior, reducing false positives while maintaining strong phishing detection.

🔍 Key Features

Machine Learning–based phishing detection (Logistic Regression)

URL feature extraction and entropy analysis

Phishing keyword and impersonation detection

Trusted domain risk reduction

Hard-trusted TLD handling (.gov.in, .ac.in, .edu)

Risk-based classification (High / Suspicious / Safe)

Explainable AI output (WHY a URL was flagged)

Security-focused evaluation metrics

⚙️ How It Works
User URL
   ↓
Feature Extraction
   ↓
ML Model Prediction
   ↓
Trusted Domain Adjustment
   ↓
Hard-Trusted TLD Logic
   ↓
Explainable AI Output
   ↓
Final Risk Decision

🚦 Risk Levels

🚨 High Risk – Strong phishing indicators detected

⚠️ Suspicious – Unusual structure, proceed with caution

✅ Legitimate – No significant phishing patterns

🧪 Example Output
🔎 URL: https://gov.in
🌐 Domain: gov.in
📊 Risk Score: 25.00%
🏛️ Government/Education TLD detected (hard trust applied)
✅ LEGITIMATE URL

🧠 Reason(s):
 - No strong phishing indicators detected

🧠 Explainable AI

Aegis does not act as a black box.
For every prediction, it provides human-readable explanations such as:

Presence of phishing-related keywords

Brand impersonation attempts

URL structure anomalies

Absence of strong phishing indicators

🧪 Model Evaluation

The model is evaluated using:

Confusion Matrix

Precision

Recall (Phishing-focused)

F1-score

Security emphasis is placed on minimizing false negatives.

🛠️ Tech Stack

Python

Scikit-learn

Pandas

NumPy

tldextract

▶️ How to Run
pip install -r requirements.txt
python train_model.py
python predict.py

🔐 Security Design Choices

Datasets and trained models are excluded using .gitignore

Government and educational TLDs are hard-trusted to prevent false positives

The system errs on the side of caution for unknown domains

🚀 Future Scope

Browser extension integration

User feedback–based adaptive learning (controlled retraining)

DNS and SSL certificate analysis

Real-time web interface

🎓 Academic Note

This project is developed for educational and research purposes only and does not perform any real phishing activity.

⭐ One-Line Summary

Aegis is a hybrid AI-based phishing detection system that acts as a digital shield against malicious URLs using explainable and security-aware intelligence.