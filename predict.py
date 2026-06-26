import pickle
import pandas as pd
import tldextract
import whois
import datetime
import requests
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

SAFE_BROWSING_API_KEY = "YOUR_API_KEY_HERE"

def get_domain_age_days(domain):
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if creation_date:
            age = (datetime.datetime.now() - creation_date).days
            return age
    except Exception:
        pass
    return None

def check_google_safe_browsing(url):
    if SAFE_BROWSING_API_KEY == "YOUR_API_KEY_HERE":
        return False
    
    api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={SAFE_BROWSING_API_KEY}"
    payload = {
        "client": {"clientId": "aegis", "clientVersion": "1.0.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }
    try:
        response = requests.post(api_url, json=payload, timeout=3)
        if response.status_code == 200:
            data = response.json()
            if "matches" in data and len(data["matches"]) > 0:
                return True
    except Exception:
        pass
    return False

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
    
    # Real-time checks
    root_domain = get_root_domain(url)
    extracted = tldextract.extract(url)
    tld = extracted.suffix
    
    domain_age = get_domain_age_days(root_domain)
    is_safe_browsing_flagged = check_google_safe_browsing(url)
    
    reasons = explain_prediction(features, domain_age, is_safe_browsing_flagged)

    # Base phishing probability
    phishing_prob = model.predict_proba(df)[0][1]

    # Domain trust adjustment
    root_domain = get_root_domain(url)
    trusted = root_domain in TRUSTED_DOMAINS

    if trusted:
        phishing_prob *= TRUST_REDUCTION_FACTOR
    
    if tld in HARD_TRUST_TLDS:
        phishing_prob = min(phishing_prob, HARD_TRUST_CAP)
        print("🏛️ Government/Education TLD detected (hard trust applied)")
        
    # WHOIS and Safe Browsing adjustments
    if domain_age is not None and domain_age < 30:
        phishing_prob = max(phishing_prob, 0.85)
        print(f"⚠️ Domain is very new! Age: {domain_age} days (risk adjusted)")
        
    if is_safe_browsing_flagged:
        phishing_prob = 0.99
        print("🚨 FLAG: Google Safe Browsing marked this as a threat!")

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
    

