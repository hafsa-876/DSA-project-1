
import urllib.request
import urllib.parse
import json
import csv
import time
import os
import getpass

# OpenAlex API key
API_KEY = getpass.getpass(
    "Enter your OpenAlex API key: "
).strip()

BASE_URL = "https://api.openalex.org/works"
CSV_FILE = "journal_articles.csv"
TARGET = 15000

articles = []
cursor = "*"

# Articles scrape karo
while len(articles) < TARGET:

    params = {
        "filter": "type:article",
        "per-page": 100,
        "cursor": cursor,
        "api_key": API_KEY
    }

    url = BASE_URL + "?" + urllib.parse.urlencode(params)

    try:
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "JournalArticlesScraper/1.0"
            }
        )

        with urllib.request.urlopen(
            request, timeout=120
        ) as response:
            raw_data = response.read().decode("utf-8")

        data = json.loads(raw_data)

    except Exception as error:
        print("Error:", error)
        print("Retrying in 5 seconds...")
        time.sleep(5)
        continue

    results = data.get("results", [])

    if not results:
        print("No more articles available.")
        break

    articles.extend(results)
    articles = articles[:TARGET]

    print("Articles collected:", len(articles))

    next_cursor = data.get("meta", {}).get("next_cursor")

    if len(articles) >= TARGET:
        break

    if not next_cursor or next_cursor == cursor:
        print("No next page available.")
        break

    cursor = next_cursor
    time.sleep(0.5)

# CSV file save karo
with open(
    CSV_FILE, "w", newline="", encoding="utf-8-sig"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "Title",
        "Year",
        "DOI",
        "Authors",
        "Journal Name",
        "Citations",
        "OpenAlex ID",
        "Publication Type"
    ])

    for article in articles:

        authors = ", ".join(
            item.get("author", {}).get("display_name", "")
            for item in article.get("authorships", [])
        )

        location = article.get("primary_location") or {}
        source = location.get("source") or {}

        writer.writerow([
            article.get("title"),
            article.get("publication_year"),
            article.get("doi"),
            authors,
            source.get("display_name"),
            article.get("cited_by_count"),
            article.get("id"),
            article.get("type")
        ])

print("\nDataset saved!")
print("Total articles:", len(articles))
print("Total columns: 8")
print("CSV location:", os.path.abspath(CSV_FILE))
