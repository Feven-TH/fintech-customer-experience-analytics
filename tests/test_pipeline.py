import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Load a small sample of cleaned CSV
df = pd.read_csv("data/clean/reviews_clean.csv").head(10)

# Initialize VADER
analyzer = SentimentIntensityAnalyzer()

def test_sentiment_scores():
    """Check sentiment scores are within [-1, 1]"""
    df['sentiment_score'] = df['review'].apply(lambda x: analyzer.polarity_scores(str(x))["compound"])
    assert df['sentiment_score'].min() >= -1
    assert df['sentiment_score'].max() <= 1

def test_sentiment_labels():
    """Check sentiment labels are only Positive/Neutral/Negative"""
    def get_sentiment(text):
        score = analyzer.polarity_scores(str(text))["compound"]
        if score >= 0.05:
            return "Positive"
        elif score <= -0.05:
            return "Negative"
        else:
            return "Neutral"
    df['sentiment'] = df['review'].apply(get_sentiment)
    assert set(df['sentiment'].unique()).issubset({"Positive","Neutral","Negative"})

def test_theme_clusters():
    """Check that theme clustering produces expected number of clusters"""
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df["review"].astype(str))
    kmeans = KMeans(n_clusters=5, random_state=42)
    df["theme_cluster"] = kmeans.fit_predict(X)
    assert df["theme_cluster"].nunique() <= 5

def test_csv_integrity():
    """Check CSV has expected columns"""
    expected_cols = ["review", "rating", "date", "bank", "source"]
    for col in expected_cols:
        assert col in df.columns
