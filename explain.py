def explain_prediction(features):
    reasons = []

    # Keyword-based reasons
    if features.get("phishing_keyword_count", 0) >= 2:
        reasons.append("Contains phishing-related keywords")

    if features.get("brand_keyword", 0) >= 1:
        reasons.append("Possible brand impersonation detected")

    # Structural reasons
    if features.get("has_ip", 0) == 1:
        reasons.append("Uses IP address instead of domain name")

    if features.get("has_at", 0) == 1:
        reasons.append("Contains '@' symbol (URL redirection trick)")

    if features.get("https", 1) == 0:
        reasons.append("Does not use HTTPS")

    if features.get("hyphen_count", 0) >= 3:
        reasons.append("Excessive use of hyphens in URL")

    if features.get("url_entropy", 0) > 4.0:
        reasons.append("URL appears random or obfuscated")

    # Fallback
    if not reasons:
        reasons.append("No strong phishing indicators detected")

    return reasons
