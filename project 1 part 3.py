
import pandas as pd

# Cleaned dataset load karo
df = pd.read_csv("journal_articles_cleaned.csv")

# Top 10 most cited articles
print("\nTop 10 most cited articles:")
print(
    df[["Title", "Year", "Citations", "OpenAlex ID"]]
    .sort_values("Citations", ascending=False)
    .head(10)
    .to_string(index=False)
)

# Unique IDs aur total rows
print("\nUnique article IDs:", df["OpenAlex ID"].nunique())
print("Total rows:", len(df))
