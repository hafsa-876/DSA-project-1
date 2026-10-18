
import pandas as pd
import matplotlib.pyplot as plt

# Original dataset read karo
df = pd.read_csv("journal_articles.csv")

print("Original dataset shape:", df.shape)

# Missing values check karo
print("\nMissing values:")
print(df.isnull().sum())

# Duplicate articles check karo
print("\nDuplicate rows:", df.duplicated().sum())

# Blank titles remove karo
df = df.dropna(subset=["Title"])
df = df[df["Title"].astype(str).str.strip() != ""]

# Duplicate DOI remove karo
has_doi = df["DOI"].notna() & (
    df["DOI"].astype(str).str.strip() != ""
)

with_doi = df[has_doi].drop_duplicates(subset=["DOI"])
without_doi = df[~has_doi]

df = pd.concat(
    [with_doi, without_doi]
).reset_index(drop=True)

# Cleaned dataset save karo
df.to_csv("journal_articles_cleaned.csv", index=False)

print("\nCleaning complete!")
print("Cleaned dataset shape:", df.shape)
print("Saved: journal_articles_cleaned.csv")

# Year-wise article count
print("\nArticles published per year:")
year_counts = df["Year"].value_counts().sort_index()
print(year_counts)

# Top 10 most cited articles
print("\nTop 10 most cited articles:")
top10 = df.nlargest(10, "Citations").copy()

print(
    top10[["Title", "Year", "Citations"]].to_string(index=False)
)

# Graph 1: Articles published per year
plt.figure(figsize=(14, 6))
plt.bar(year_counts.index.astype(str), year_counts.values)
plt.title("Number of Journal Articles Published Per Year")
plt.xlabel("Publication Year")
plt.ylabel("Number of Articles")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# Graph 2: Top 10 most cited articles
top10["Short Title"] = top10["Title"].str.slice(0, 35)

plt.figure(figsize=(12, 7))
plt.barh(top10["Short Title"], top10["Citations"])
plt.title("Top 10 Most Cited Articles")
plt.xlabel("Number of Citations")
plt.ylabel("Article Title")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# Save analysis reports
year_counts.to_csv(
    "articles_per_year.csv",
    header=["Article Count"]
)

top10.to_csv("top_10_cited_articles.csv", index=False)

print("\nAnalysis reports saved successfully!")
print("1. articles_per_year.csv")
print("2. top_10_cited_articles.csv")
