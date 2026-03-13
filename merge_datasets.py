import pandas as pd

df1 = pd.read_csv("dataset/phishing_url.csv")
df2 = pd.read_csv("dataset/Phishing URL dataset/Phishing URLs.csv")
df3 = pd.read_csv("dataset/Phishing URL dataset/URL dataset.csv")

# Rename columns
df2 = df2.rename(columns={"Type": "label"})
df3 = df3.rename(columns={"type": "label"})

# Merge
merged = pd.concat([df1, df2, df3], ignore_index=True)

# Remove duplicates
merged = merged.drop_duplicates(subset="url")

# Save final dataset
merged.to_csv("dataset/phishing_dataset_final.csv", index=False)

print("Final dataset size:", merged.shape)