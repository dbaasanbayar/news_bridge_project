import logging
import os
from datetime import datetime

def setup_logger():
    # 1. Logs хавтас байхгүй бол үүсгэх
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 2. Логгерийг тохируулах
    logger = logging.getLogger("NewsBridge")
    logger.setLevel(logging.INFO)

    # 3. Файл руу бичих тохиргоо (Formatter)
    # Цаг хугацаа - Төрөл (INFO/ERROR) - Мессеж гэсэн бүтэцтэй
    log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Өдөр бүр шинэ лог файл үүсэх (Заавал биш, гэхдээ цэгцтэй)
    log_file = os.path.join(log_dir, f"pipeline_{datetime.now().strftime('%Y-%m-%d')}.log")
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(log_format)

    # 4. Терминал руу бас харуулж байх тохиргоо
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)

    # Логгерт нэмэх
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    return logger

# Ганцхан удаа үүсгээд хаа сайгүй ашиглах
logger = setup_logger()
