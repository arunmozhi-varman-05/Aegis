from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import tldextract

from feature_extraction import extract_features
from explain import explain_prediction

app = Flask(__name__)
CORS(app)

MODEL_PATH = "url_model.pkl"

HIGH_RISK_THRESHOLD = 0.60
SUSPICIOUS_THRESHOLD = 0.30

TRUSTED_DOMAINS = {
    "google.com", "amazon.com", "amazon.in",
    "github.com", "kaggle.com", "microsoft.com"
}

HARD_TRUST_TLDS = {"gov", "gov.in", "edu", "edu.in", "ac.in"}
HARD_TRUST_CAP = 0.25
TRUST_REDUCTION_FACTOR = 0.4

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)


def get_root_domain(url):
    extracted = tldextract.extract(url)
    return f"{extracted.domain}.{extracted.suffix}", extracted.suffix


@app.route("/check_url", methods=["POST"])
def check_url():
    data = request.json
    url = data.get("url")

    features = extract_features(url)
    df = pd.DataFrame([features])
    reasons = explain_prediction(features)

    phishing_prob = model.predict_proba(df)[0][1]

    root_domain, tld = get_root_domain(url)

    if root_domain in TRUSTED_DOMAINS:
        phishing_prob *= TRUST_REDUCTION_FACTOR

    if tld in HARD_TRUST_TLDS:
        phishing_prob = min(phishing_prob, HARD_TRUST_CAP)

    if phishing_prob >= HIGH_RISK_THRESHOLD:
        label = "PHISHING"
    elif phishing_prob >= SUSPICIOUS_THRESHOLD:
        label = "SUSPICIOUS"
    else:
        label = "LEGITIMATE"

    return jsonify({
        "url": url,
        "domain": root_domain,
        "risk_score": round(phishing_prob * 100, 2),
        "label": label,
        "reasons": reasons
    })


if __name__ == "__main__":
    app.run(debug=True)
