from src.scrapers.montsame import get_montsame_news
from src.scrapers.ikon import get_ikon_news
import pandas as pd
from src.utils.cleaning import clean_integrated_data
from src.database import save_to_db
from src.utils.ai_agent import analyze_news_content
from src.database import export_news_by_source, save_to_db, get_unprocessed_news, update_news_analysis
def run_pipeline():
    print("---Мэдээ цуглуулж эхэллээ...---")

   # 1. EXTRACT
    montsame_data = get_montsame_news()
    ikon_data = get_ikon_news()
    all_news = montsame_data + ikon_data
    # Дата байгаа эсэхийг энд шалгах
    if not all_news:
        print("Анхаар: Ямар ч эх сурвалжаас дата цуглуулж чадсангүй. Процесс зогслоо.")
        return
    
    # 2. TRANSFORM
    df_raw = pd.DataFrame(all_news)
    df_clean = clean_integrated_data(df_raw)

    if df_clean.empty:
        print("Анхаар: Цэвэрлэгээний дараа дата хоосон боллоо.")
        return
    
    # 3. LOAD
    save_to_db(df_clean)
    
    # 4. ENRICH (AI Анализ хийх шинэ шат)
    print("\n🤖 AI Анализ эхэлж байна...")
    to_process = get_unprocessed_news()

    for index, row in to_process.iterrows():
        result = analyze_news_content(row['title'])
        if result:
            update_news_analysis(row['url'], result['sentiment'], result['category'])
            print(f"Processed: {row['title'][:30]}...")

    export_news_by_source()
    print("\n--- Бүх процесс дууслаа! --- ")

if __name__ =="__main__":
    run_pipeline()


