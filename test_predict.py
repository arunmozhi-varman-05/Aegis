import pickle
import pandas as pd
import tldextract
from feature_extraction import extract_features

MODEL_PATH = "url_model.pkl"

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

urls_to_test = [
    "google.com",
    "paypal-secure-login-123.com",
    "github.com",
    "login.update-apple-security.com"
]

for url in urls_to_test:
    features = extract_features(url)
    df = pd.DataFrame([features])
    phishing_prob = model.predict_proba(df)[0][1]
    print(f"URL: {url} -> Phishing Prob: {phishing_prob:.4f}")
