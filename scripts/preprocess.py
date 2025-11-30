import pandas as pd
from dateutil import parser

def clean_date(date_value):
    """Convert dates to YYYY-MM-DD format."""
    try:
        return parser.parse(str(date_value)).date()
    except:
        return None

def main():
    df = pd.read_csv("data/raw/reviews_raw.csv")
    df = df.rename(columns={
        "content": "review",
        "score": "rating",
        "at": "date"
    })

    df = df.dropna(subset=["review"])
    df = df.drop_duplicates(subset=["review"])

    df["date"] = df["date"].apply(clean_date)

    df = df.dropna(subset=["date"])

    df.to_csv("data/clean/reviews_clean.csv", index=False)
    print("Preprocessing complete! Saved to data/clean/reviews_clean.csv")

if __name__ == "__main__":
    main()
