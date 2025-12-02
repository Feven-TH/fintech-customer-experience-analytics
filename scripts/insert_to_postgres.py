import pandas as pd
import psycopg2
from dotenv import dotenv_values 

# --- Load Environment Variables ---
config = dotenv_values(".env")

DB_NAME = config.get("DB_NAME")
DB_USER = config.get("DB_USER")
DB_PASSWORD = config.get("DB_PASSWORD")
DB_HOST = config.get("DB_HOST")

# The port must be explicitly converted to an integer for psycopg2
try:
    DB_PORT = int(config.get("DB_PORT"))
except (TypeError, ValueError):
    print("Error: DB_PORT must be an integer in the .env file.")
    exit()

if not all([DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT]):
    print("Error: Database credentials not found in .env file or are incomplete.")
    exit()

# --- Data Loading ---
df = pd.read_csv("data/clean/reviews_with_sentiment_themes.csv")
print(f"Loaded {len(df)} reviews from CSV.")

# --- Database Connection ---
print("Attempting to connect to the database...")
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()
    print("Successfully connected to PostgreSQL.")

    # --- Data Insertion Logic ---

    # 1. Insert banks (unique)
    banks = df["bank"].unique()
    bank_id_map = {}

    for bank in banks:
        cur.execute("SELECT bank_id FROM banks WHERE bank_name = %s", (bank,))
        result = cur.fetchone()
        
        if result:
            bank_id_map[bank] = result[0]
        else:
            cur.execute("INSERT INTO banks (bank_name, app_name) VALUES (%s, %s) RETURNING bank_id",
                        (bank, f"{bank} Mobile App"))
            bank_id_map[bank] = cur.fetchone()[0]

    conn.commit()
    print(f"Processed {len(banks)} unique banks.")

    # 2. Insert reviews
    review_count = 0
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO reviews (bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, source)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (
            bank_id_map[row["bank"]],
            row["review"],
            row["rating"],
            row["date"],
            row["sentiment"],
            row["sentiment_score"], 
            row["source"]
        ))
        review_count += 1

    conn.commit()
    print(f"Inserted {review_count} reviews into the 'reviews' table.")
    
    # --- Cleanup ---
    cur.close()
    conn.close()
    print("Database connection closed.")

except psycopg2.Error as e:
    print(f"Database connection or operation error: {e}")
    if 'conn' in locals() and conn:
        conn.rollback()

print("Finished data ingestion process.")