import sqlite3
import os
import pandas as pd
def save_to_db(df, db_name="data/news_bridge.db"):
    # Хавтас байхгүй бол үүсгэх
    os.makedirs(os.path.dirname(db_name), exist_ok=True)

    # AI-д зориулсан багануудыг анхнаас нь бэлдэх
    if 'sentiment' not in df.columns:
            df['sentiment'] = None
    if 'category' not in df.columns:
            df['category'] = None

    with sqlite3.connect(db_name) as conn:
        df.to_sql('integrated_news', conn, if_exists='replace', index=False)

        # Индекс үүсгэх (Хурдан хайлт хийхийн тулд)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_title ON integrated_news(title)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_news_url ON integrated_news(url)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_news_sentiment ON integrated_news(sentiment)")

    print(f"Датаг индексжүүлж хадгаллаа.")
    
def get_unprocessed_news(db_name="data/news_bridge.db"):
    with sqlite3.connect(db_name) as conn:
        # Анализ хийгдээгүй (Null) мэдээнүүдийг унших
        query = "SELECT title, url FROM integrated_news WHERE sentiment IS NULL LIMIT 10"
        return pd.read_sql_query(query, conn)
    
def update_news_analysis(url, sentiment, category, db_name="data/news_bridge.db"):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE integrated_news
            SET sentiment = ?, category = ?
            WHERE url = ?
        """, (sentiment, category, url))
        conn.commit()

def export_news_by_source(db_name="data/news_bridge.db"):
    print("Датаг эх сурвалжаар нь салгаж CSV болгон гаргаж байна...")

    with sqlite3.connect(db_name) as conn:
        df = pd.read_sql_query("SELECT * FROM integrated_news", conn)

    # 'data/exports/' хавтас үүсгэх (Цэгцтэй байлгах үүднээс)
    export_path = "data/exports"
    os.makedirs(export_path, exist_ok=True)
    
    # Эх сурвалж бүрээр салгаж хадгалах
    for source_name in df['source'].unique():
        subset = df[df['source'] == source_name]
        file_name = f"{export_path}/{source_name.lower()}_news.csv"
        subset.to_csv(file_name, index=False)
        print(f"{source_name}-ийн {len(subset)} мэдээг '{file_name}' руу хадгаллаа.")


    
