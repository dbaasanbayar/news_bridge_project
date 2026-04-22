from src.scrapers.montsame import get_montsame_news
from src.scrapers.ikon import get_ikon_news
import pandas as pd
from src.utils.cleaning import clean_integrated_data
from src.database import save_to_db
from src.utils.ai_agent import analyze_news_content
from src.database import export_news_by_source, save_to_db, get_unprocessed_news, update_news_analysis
from src.utils.logger import logger

def run_pipeline():
    logger.info("--- Шинэ ETL цикл эхэллээ ---")

   # 1. EXTRACT
    try:
        # 1. Скрапер бүрийг шалгах
        montsame_data = get_montsame_news()
        if not montsame_data:
            # Энэ бол "Warning" - вэбсайт ажиллаж байгаа ч мэдээ алга
            logger.warning("Montsame-аас шинэ мэдээ олдсонгүй. Вэбсайт өөрчлөгдсөн үү?")

        ikon_data = get_ikon_news()
        if not ikon_data:
            logger.warning("Ikon-оос шинэ мэдээ олдсонгүй.")

        all_news = montsame_data + ikon_data
        
        if not all_news:
            logger.error("Critical: Аль ч эх сурвалжаас дата ирсэнгүй. Процесс зогслоо.")
            return

        # ... Transform & Load ...
        logger.info(f"Амжилттай: {len(all_news)} мэдээ боловсрууллаа.")

        # 2. TRANSFORM
        logger.info(f"Цуглуулсан нийт мэдээ: {len(all_news)}. Цэвэрлэж байна...")
        df_clean = clean_integrated_data(pd.DataFrame(all_news))

        # 3. LOAD
        save_to_db(df_clean)
        logger.info("Өгөгдлийн санд амжилттай хадгаллаа.")

        # 4. ENRICH (AI Анализ хийх шинэ шат)
        logger.info("AI анализ эхэлж байна...")
        to_process = get_unprocessed_news()

        # Хэрэв анализ хийх мэдээ байхгүй бол
        if to_process.empty:
            logger.info("Шинээр анализ хийх мэдээ олдсонгүй.")
        else:
            for index, row in to_process.iterrows():
                result = analyze_news_content(row['title'])
                if result:
                    update_news_analysis(row['url'], result['sentiment'], result['category'])
                logger.info(f"Анализ хийгдлээ: {row['title'][:30]}...")
        
        # 5. EXPORT
        export_news_by_source()
        logger.info("--- Бүх процесс амжилттай дууслаа ---")

    except Exception as e:
        # Энэ хэсэг "Reliability"-г хангана. Хаана алдаа гарсныг лог руу маш дэлгэрэнгүй бичнэ.
        logger.critical(f"Системийн ноцтой алдаа: {str(e)}", exc_info=True)
    
if __name__ == "__main__":
    run_pipeline()

