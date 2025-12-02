import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

df = pd.read_csv("data/clean/reviews_with_sentiment_themes.csv")

# --- Wordcloud Function ---
def plot_wordcloud(text, title):
    if not text:
        return
    wc = WordCloud(width=800, height=400, background_color="white").generate(" ".join(text))
    plt.figure(figsize=(10,5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(title)
    plt.tight_layout()
    filename = f"plots/{title.replace(' ', '_')}.png"
    plt.savefig(filename)
    plt.close()
    print(f"Saved wordcloud: {filename}")

# --- Generate Wordclouds by Bank & Sentiment ---
for bank in df["bank"].unique():
    all_reviews = df[df["bank"]==bank]["review"].tolist()
    plot_wordcloud(all_reviews, f"{bank} - All Reviews")

    for sentiment in ["Positive", "Neutral", "Negative"]:
        text = df[(df["bank"]==bank) & (df["sentiment"]==sentiment)]["review"].tolist()
        if text:
            plot_wordcloud(text, f"{bank} - {sentiment} Reviews")

# --- Theme Cluster Summary ---
print("Theme cluster counts by bank:")
theme_counts = df.groupby(["bank", "theme_cluster"]).size()
print(theme_counts)

# --- Basic Sentiment Insights ---
for bank in df["bank"].unique():
    print(f"\n--- {bank} ---")
    bank_data = df[df["bank"]==bank]
    pos = bank_data[bank_data["sentiment"]=="Positive"].shape[0]
    neu = bank_data[bank_data["sentiment"]=="Neutral"].shape[0]
    neg = bank_data[bank_data["sentiment"]=="Negative"].shape[0]
    print(f"Positive reviews: {pos}, Neutral: {neu}, Negative: {neg}")
    print(f"Average sentiment score: {bank_data['sentiment_score'].mean():.3f}")

# --- Top Negative Reviews for Each Bank ---
for bank in df["bank"].unique():
    bank_data = df[df["bank"]==bank]
    top_negative = bank_data.nsmallest(5, "sentiment_score")[["review", "sentiment_score"]]
    print(f"\nTop negative reviews for {bank}:")
    print(top_negative.to_string(index=False))

# --- Optional: Save Aggregated Insights ---
summary = []
for bank in df["bank"].unique():
    bank_data = df[df["bank"]==bank]
    summary.append({
        "bank": bank,
        "positive_count": bank_data[bank_data["sentiment"]=="Positive"].shape[0],
        "neutral_count": bank_data[bank_data["sentiment"]=="Neutral"].shape[0],
        "negative_count": bank_data[bank_data["sentiment"]=="Negative"].shape[0],
        "avg_sentiment_score": bank_data["sentiment_score"].mean()
    })

summary_df = pd.DataFrame(summary)
summary_df.to_csv("data/clean/sentiment_summary.csv", index=False)
print("\nSaved sentiment summary: data/clean/sentiment_summary.csv")
