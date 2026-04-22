# 🚀 News Bridge: AI-Powered Multi-Source News Analytics Pipeline

Монголын мэдээллийн томоохон эх сурвалжуудаас (Montsame, Ikon) автоматаар мэдээ цуглуулж, AI (Llama 3.1) ашиглан анализ хийж, нэгдсэн өгөгдлийн сан үүсгэх зорилготой ETL дамжлага юм.

## 🏗️ Системийн бүтэц (Architecture)
Төсөл нь **Modular Design** зарчмаар бүтээгдсэн бөгөөд дараах шат дамжлагуудаар ажиллана:

1.  **Extract:** Beautiful Soup ашиглан Montsame болон Ikon-оос түүхий өгөгдөл цуглуулна.
2.  **Transform:** Pandas ашиглан давхардлыг арилгаж, өгөгдлийг стандарт формат руу шилжүүлнэ.
3.  **Load:** Цэвэрлэсэн өгөгдлийг SQLite өгөгдлийн санд индексжүүлэн хадгална.
4.  **Enrich:** Groq API (Llama 3.1) ашиглан мэдээний өнгө аяс (Sentiment) болон ангиллыг (Category) тодорхойлно.
5.  **Monitor:** Бүх үйлдлийг `logs/` хавтас дотор нарийн бүртгэж (Logging) хянана.

## 🛠️ Технологийн стек
- **Хэл:** Python 3.x
- **Дата сан:** SQLite3
- **Сангууд:** Pandas, BeautifulSoup4, Requests
- **AI Модел:** Groq SDK (Llama-3.1-8b-instant)
- **Хяналт:** Logging module

## 📂 Хавтасны бүтэц
```text
news_bridge_project/
├── data/               # SQLite DB болон Export хийсэн CSV-үүд
├── logs/               # Системийн ажиллагааны бүртгэл (.log)
├── src/                # Эх код
│   ├── scrapers/       # Вэб хусах модулиуд (Ikon, Montsame)
│   ├── utils/          # Цэвэрлэгээ, AI болон Logger-ийн туслах кодууд
│   └── database.py     # SQL үйлдлүүд
├── main.py             # Pipeline-ийг ажиллуулах үндсэн файл
└── requirements.txt    # Шаардлагатай сангуудын жагсаалт