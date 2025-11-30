# 🇪🇹 FinTech CX Analysis: Ethiopian Banking Apps

## Project Overview

Analysis of customer experience for **Commercial Bank of Ethiopia (CBE)**, **Bank of Abyssinia (BOA)**, and **Dashen Bank** mobile apps using Google Play Store reviews. The goal is to provide actionable recommendations to enhance customer retention and satisfaction.

---

### ⚙️ Setup and Execution

1.  **Clone Repo & Install:**
    ```bash
    git clone [https://github.com/Feven-TH/fintech-customer-experience-analytics.git]
    cd fintech-cx-analytics
    pip install -r requirements.txt
    ```
2.  **Run Pipeline (Sequential):**
    ```bash
    python scripts/scrape_reviews.py
    python scripts/preprocess_data.py
    # ... then proceed to Task 2 analysis
    ```

---

## ✅ Task 1: Data Collection & Preprocessing (Complete)

**Goal:** Collect $\mathbf{1,200+}$ clean reviews (400+ per bank).

### Status

* **Scraping Status:** **Functionally Complete.** Fixed `KeyError` and implemented country code (`et`). Successfully collected **600+ reviews for CBE**. Requires rerun to collect data for BOA and Dashen using corrected IDs.
* **App IDs:** Updated to point to current, active apps.
    * **BOA:** `com.boa.boaMobileBanking`
    * **Dashen:** `com.dashen.dashensuperapp`
* **Deliverable:** `data/raw/reviews_raw.csv` and `data/clean/reviews_clean.csv`.

---

## 🔬 Task 2: Sentiment and Thematic Analysis

**Goal:** Apply NLP to quantify user emotion and identify recurring pain points and feature requests.

### Key Activities

* **Sentiment Analysis:** Compute scores (positive/negative/neutral) using a transformer model or VADER/TextBlob.
* **Thematic Analysis:** Extract keywords (TF-IDF/spaCy) and cluster them into 3-5 high-level themes (e.g., 'Account Access', 'Transaction Performance').

---

## 💾 Task 3: Store Cleaned Data in PostgreSQL

**Goal:** Design and implement a relational database to store the processed review data persistently.

### Database Schema

* **Database:** `bank_reviews`
* **Tables:** `Banks` (Bank ID, Name) and `Reviews` (Review ID, **Foreign Key to Bank ID**, Text, Rating, Date, Sentiment Label, Theme).
* **Tooling:** Use `psycopg2` or `SQLAlchemy` for insertion via Python.

---
