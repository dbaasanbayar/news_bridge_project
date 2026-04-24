import sqlite3
import pandas as pd
import os

DB_PATH = "data/news_bridge.db"

def run_analysis():
    print("📊 --- Өгөгдлийн сангийн шинжилгээ эхэллээ --- \n")
    with sqlite3.connect(DB_PATH) as conn:
        # 1. Эх сурвалжийн тоо (Pandas ашиглавал харахад илүү цэгцтэй)
        print("1. Эх сурвалж бүрийн мэдээний тоо:")
        df1 = pd.read_sql_query("SELECT source, COUNT(*) as count FROM integrated_news GROUP BY source", conn)
        print(df1, "\n")
        # 2. AI анализ хийгдээгүй мэдээнүүд
        df2 = pd.read_sql_query("SELECT COUNT(*) as remaining FROM integrated_news WHERE sentiment IS NULL", conn)
        print(df2)
        df3 = pd.read_sql_query("SELECT category, sentiment FROM integrated_news WHERE category = 'Эдийн засаг' AND sentiment = 'Эерэг'", conn)
        print(df3)
    
    os.makedirs("data/query", exist_ok=True)
    with sqlite3.connect(DB_PATH) as conne:
        df1 = pd.read_sql_query("SELECT sentiment AS sentiment_name  FROM integrated_news WHERE sentiment = 'Саармаг' ", conne)
        print(f"aa {df1}")
        sentiment = df1
        sentiment.to_csv("data/query/sentiment_saarmag.csv", index=False)
if __name__ == "__main__":
    run_analysis()


