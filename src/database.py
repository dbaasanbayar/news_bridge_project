import sqlite3
import os

def save_to_db(df, db_name="data/news_bridge.db"):
    # Хавтас байхгүй бол үүсгэх
    os.makedirs(os.path.dirname(db_name), exist_ok=True)

    with sqlite3.connect(db_name) as conn:
        # Датаг хадгалах
        df.to_sql('integrated_news', conn, if_exists='append', index=False)

        # Индекс үүсгэх (Хурдан хайлт хийхийн тулд)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_title ON integrated_news(title)")

    print(f"Датаг '{db_name}' сан руу амжилттай хадгаллаа.")
    