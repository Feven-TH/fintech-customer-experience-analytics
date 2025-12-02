import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from wordcloud import WordCloud

df = pd.read_csv("data/clean/reviews_clean.csv")

# --- Sentiment Analysis Using VADER ---
analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    score = analyzer.polarity_scores(str(text))["compound"]
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

df["sentiment"] = df["review"].apply(get_sentiment)
df["sentiment_score"] = df["review"].apply(lambda x: analyzer.polarity_scores(str(x))["compound"])


# --- Wordcloud Functions ---
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


# --- Wordclouds by bank & sentiment ---
for bank in df["bank"].unique():
    all_reviews = df[df["bank"]==bank]["review"].tolist()
    plot_wordcloud(all_reviews, f"{bank} - All Reviews")

    for sentiment in ["Positive", "Neutral", "Negative"]:
        text = df[(df["bank"]==bank) & (df["sentiment"]==sentiment)]["review"].tolist()
        if text:
            plot_wordcloud(text, f"{bank} - {sentiment} Reviews")

# --- Theme Clustering ---
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(df["review"].astype(str))

kmeans = KMeans(n_clusters=5, random_state=42)
df["theme_cluster"] = kmeans.fit_predict(X)

print("Theme cluster counts by bank:")
print(df.groupby(["bank", "theme_cluster"]).size())

# --- Save final CSV ---
df.to_csv("data/clean/reviews_with_sentiment_themes.csv", index=False)
print("Saved: data/clean/reviews_with_sentiment_themes.csv")
