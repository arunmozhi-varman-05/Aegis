import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

from feature_extraction import extract_features


# Load dataset
df = pd.read_csv("dataset/phishing_url.csv")

print("Dataset Loaded:", df.shape)

# Extract features
X = df['url'].apply(extract_features)
X = pd.DataFrame(list(X))

# Labels
y = df['label']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Save model
with open("url_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved successfully!")
