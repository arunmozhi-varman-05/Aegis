import pickle
import pandas as pd
import tldextract
from feature_extraction import extract_features
from explain import explain_prediction


# ==============================
# Configuration
# ==============================
MODEL_PATH = "url_model.pkl"

HIGH_RISK_THRESHOLD = 0.60
SUSPICIOUS_THRESHOLD = 0.30

# Trusted domains (expandable)
TRUSTED_DOMAINS = {
    "google.com",
    "amazon.com",
    "amazon.in",
    "github.com",
    "kaggle.com",
    "microsoft.com",
    "apple.com",
    "youtube.com",
    "linkedin.com",
    "facebook.com"
}
# Hard-trusted TLDs (Government & Education)
HARD_TRUST_TLDS = {"gov", "gov.in", "edu", "edu.in", "ac.in"}
HARD_TRUST_CAP = 0.25  # max 25% risk


TRUST_REDUCTION_FACTOR = 0.4  # reduce risk by 60%

# ==============================
# Load model
# ==============================
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

print("🔐 AI-Based Phishing Detection System")
print("⚙️ Risk Levels: High / Suspicious / Safe")
print("🛡️ Trusted Domain Protection Enabled\n")

# ==============================
# Helper: extract root domain
# ==============================
def get_root_domain(url):
    extracted = tldextract.extract(url)
    return f"{extracted.domain}.{extracted.suffix}"

# ==============================
# Prediction loop
# ==============================
while True:
    try:
        url = input("Enter URL (or type exit): ").strip()

        if url.lower() == "exit":
            print("👋 Exiting phishing detection system.")
            break

        # prediction code here

    except KeyboardInterrupt:
        print("\n👋 Program stopped.")
        break

    # Feature extraction
    features = extract_features(url)
    df = pd.DataFrame([features])
    reasons = explain_prediction(features)
    extracted = tldextract.extract(url)
    tld = extracted.suffix



    # Base phishing probability
    phishing_prob = model.predict_proba(df)[0][1]

    # Domain trust adjustment
    root_domain = get_root_domain(url)
    trusted = root_domain in TRUSTED_DOMAINS

    if trusted:
        phishing_prob *= TRUST_REDUCTION_FACTOR
    
    # 🔐 HARD TRUST TLD ADJUSTMENT (CORRECT PLACE)
    if tld in HARD_TRUST_TLDS:
        phishing_prob = min(phishing_prob, HARD_TRUST_CAP)
        print("🏛️ Government/Education TLD detected (hard trust applied)")

    # Output
    print("\n🔎 URL:", url)
    print(f"🌐 Domain: {root_domain}")
    print(f"📊 Risk Score: {phishing_prob * 100:.2f}%")

    if trusted:
        print("🛡️ Trusted Domain Detected (risk adjusted)")

    # Decision logic
    if phishing_prob >= HIGH_RISK_THRESHOLD:
        print("🚨 HIGH RISK: PHISHING URL")
    elif phishing_prob >= SUSPICIOUS_THRESHOLD:
        print("⚠️ SUSPICIOUS URL (Proceed with caution)")
    else:
        print("✅ LEGITIMATE URL")

    print("-" * 60)
    print("🧠 Reason(s):")
    for r in reasons:
        print(f" - {r}")
    

