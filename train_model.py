import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

from feature_extraction import extract_features


# =========================
# Load FINAL dataset
# =========================
df = pd.read_csv("dataset/final_urls.csv")

print("Dataset Loaded:", df.shape)
print(df["label"].value_counts())  # Important check

# =========================
# Feature extraction
# =========================
X = df["url"].apply(extract_features)
X = pd.DataFrame(list(X))

# Labels
y = df["label"]

# =========================
# Train-test split
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.25,
    random_state=42,
    stratify=y  # VERY IMPORTANT
)

# =========================
# Train model (IMPROVED)
# =========================
model = LogisticRegression(
    max_iter=2000,
    class_weight="balanced"  # 🔥 KEY FIX
)

model.fit(X_train, y_train)

# =========================
# Evaluation
# =========================
y_pred = model.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# =========================
# Save model
# =========================
with open("url_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model retrained and saved successfully!")
