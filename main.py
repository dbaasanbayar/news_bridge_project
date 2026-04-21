from src.scrapers.montsame import get_montsame_news
from src.scrapers.ikon import get_ikon_news
import pandas as pd
from src.utils.cleaning import clean_integrated_data
from src.database import save_to_db

def run_pipeline():
    print("Мэдээ цуглуулж эхэллээ...")

    # 1. EXTRACT
    # Олон эх сурвалжаас өгөгдөл цуглуулах (Extract)
    montsame_data = get_montsame_news()
    ikon_data = get_ikon_news()
    # Нэгтгэх (Integrate)
    all_news = montsame_data + ikon_data
    print("Extracting...")

    # 2. TRANSFORM

    df_raw = pd.DataFrame(all_news)
    df_clean = clean_integrated_data(df_raw)
    print("Transforming...")

    # 3. LOAD
    # Хүснэгт болгох
    save_to_db(df_clean)
    print("Loading...")

    print(f"\n--- Тайлан ---")
    print(f"Нийт цуглуулсан: raw - {len(df_raw)}")
    print(f"Нийт цуглуулсан: clean - {len(df_clean)}")
    print(df_raw['source'].value_counts()) # Эх сурвалж бүрээр тоолох

    print("\n--- ETL Process Finished Successfully! ---")

if __name__ =="__main__":
    run_pipeline()
