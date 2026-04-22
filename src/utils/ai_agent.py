import os 
from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_news_content(title):
    prompt = f"""
    Чи бол мэдээний шинжээч. Дараах мэдээний гарчигт анализ хий: "{title}"
    Хариуг зөвхөн JSON форматаар дараах хэлбэрээр өг:
    {{
        "sentiment": "Эерэг" эсвэл "Сөрөг" эсвэл "Саармаг",
        "category": "Улс төр", "Эдийн засаг", "Спорт" эсвэл "Бусад"
    }}
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            response_format={"type": "json_object"}
        )
        return json.loads(chat_completion.choices[0].message.content)
    except Exception as e:
        print(f"AI error: {e}")
        return None
    
    


