import sqlite3
import os
import pandas as pd
def save_to_db(df, db_name="data/news_bridge.db"):
    # Хавтас байхгүй бол үүсгэх
    os.makedirs(os.path.dirname(db_name), exist_ok=True)

    with sqlite3.connect(db_name) as conn:
        # Датаг хадгалах
        df.to_sql('integrated_news', conn, if_exists='append', index=False)

        # Индекс үүсгэх (Хурдан хайлт хийхийн тулд)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_title ON integrated_news(title)")

    print(f"Датаг '{db_name}' сан руу амжилттай хадгаллаа.")

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

