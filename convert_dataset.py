import pandas as pd

# Load legitimate URLs
legit_df = pd.read_csv("dataset/Phishing URL dataset/URL dataset.csv")

# Load phishing URLs
phish_df = pd.read_csv("dataset/Phishing URL dataset/Phishing URLs.csv")

# Keep only URL column (handle column name case)
legit_df = legit_df[['url']]
phish_df = phish_df[['url']]

# Add numeric labels
legit_df['label'] = 0   # Legitimate
phish_df['label'] = 1   # Phishing

# Balance dataset (optional but recommended)
min_size = min(len(legit_df), len(phish_df))
legit_df = legit_df.sample(n=min_size, random_state=42)
phish_df = phish_df.sample(n=min_size, random_state=42)

# Combine datasets
final_df = pd.concat([legit_df, phish_df])

# Clean dataset
final_df.dropna(inplace=True)
final_df.drop_duplicates(inplace=True)

# Shuffle dataset
final_df = final_df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save final dataset
final_df.to_csv("dataset/phishing_url.csv", index=False)

print("✅ Dataset converted successfully!")
print("Total samples:", len(final_df))
print(final_df.head())
