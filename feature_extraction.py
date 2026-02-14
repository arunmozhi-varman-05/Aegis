import re
import math
import tldextract
from urllib.parse import urlparse


# ==============================
# Suspicious keyword lists
# ==============================
PHISHING_KEYWORDS = [
    "login", "verify", "account", "secure", "update",
    "bank", "support", "help", "signin", "password"
]

BRAND_KEYWORDS = [
    "paypal", "amazon", "google", "apple",
    "facebook", "microsoft", "netflix", "bank"
]


# ==============================
# Entropy calculation
# ==============================
def calculate_entropy(text):
    if not text:
        return 0
    probabilities = [text.count(c) / len(text) for c in set(text)]
    entropy = -sum(p * math.log2(p) for p in probabilities)
    return entropy


# ==============================
# Feature Extraction
# ==============================
def extract_features(url):
    features = {}

    parsed_url = urlparse(url)
    extracted = tldextract.extract(url)
    domain = f"{extracted.domain}.{extracted.suffix}"

    # --------------------------
    # 1. URL length
    # --------------------------
    features["url_length"] = len(url)

    # --------------------------
    # 2. HTTPS presence
    # --------------------------
    features["https"] = 1 if parsed_url.scheme == "https" else 0

    # --------------------------
    # 3. IP address usage
    # --------------------------
    ip_pattern = r'(\d{1,3}\.){3}\d{1,3}'
    features["has_ip"] = 1 if re.search(ip_pattern, url) else 0

    # --------------------------
    # 4. '@' symbol
    # --------------------------
    features["has_at"] = 1 if "@" in url else 0

    # --------------------------
    # 5. Special character count
    # --------------------------
    features["special_char_count"] = len(re.findall(r'[-@_.?=#]', url))

    # --------------------------
    # 6. Subdomain count
    # --------------------------
    features["subdomain_count"] = (
        len(extracted.subdomain.split('.'))
        if extracted.subdomain else 0
    )

    # --------------------------
    # 7. Hyphen count
    # --------------------------
    features["hyphen_count"] = url.count("-")

    # --------------------------
    # 8. Digit count
    # --------------------------
    features["digit_count"] = sum(char.isdigit() for char in url)

    # --------------------------
    # 9. Phishing keyword count
    # --------------------------
    url_lower = url.lower()
    features["phishing_keyword_count"] = sum(
        1 for kw in PHISHING_KEYWORDS if kw in url_lower
    )

    # --------------------------
    # 10. Brand keyword presence
    # --------------------------
    features["brand_keyword"] = sum(
        1 for brand in BRAND_KEYWORDS if brand in url_lower
    )

    # --------------------------
    # 11. URL entropy (randomness)
    # --------------------------
    features["url_entropy"] = calculate_entropy(url)

    return features
