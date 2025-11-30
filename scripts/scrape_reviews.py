from google_play_scraper import Sort, reviews
import pandas as pd

APPS = {
    "CBE": "com.combanketh.mobilebanking",
    "BOA": "com.boa.boaMobileBanking",     
    "Dashen": "com.dashen.dashensuperapp"
}

def scrape_app(app_name, app_id, count=500):
    all_reviews = []

    batch_size = 200
    next_token = None

    while len(all_reviews) < count:
        r, next_token = reviews(
            app_id,
            lang="en",
            country="et",
            sort=Sort.NEWEST,
            count=batch_size,
            continuation_token=next_token
        )

        all_reviews.extend(r)

        if not next_token:
            break

    df = pd.DataFrame(all_reviews)
    df["bank"] = app_name
    df["source"] = "Google Play"
    return df[["content", "score", "at", "bank", "source"]]

def main():
    final_df = pd.DataFrame()

    for bank, app_id in APPS.items():
        print(f"Scraping {bank}...")
        df = scrape_app(bank, app_id)
        final_df = pd.concat([final_df, df], ignore_index=True)

    final_df.to_csv("data/raw/reviews_raw.csv", index=False)
    print("Scraping complete! Saved to data/raw/reviews_raw.csv")

if __name__ == "__main__":
    main()
