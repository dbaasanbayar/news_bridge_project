import pandas as pd
import html
import re


def clean_integrated_data(df):
    print("\n--- Нэгдсэн датаг цэвэрлэж байна ---")

    # 1. Гарчиг цэвэрлэх (Standardize text)
    df['title'] = df['title'].apply(html.unescape)
    df['title'] = df['title'].str.replace(r'\s+', ' ', regex=True).str.strip()
    
    # 2. URL цэвэрлэх
    df['url'] = df['url'].apply(lambda x: x.split('?')[0])

    # 3. Эхний шатны давхардал арилгах (URL-аар)
    df = df.drop_duplicates(subset=['url'], keep='first')

    # 4. Хоёр дахь шатны давхардал арилгах (Гарчгаар)
    # Заримдаа өөр сайтууд яг ижил гарчиг ашигладаг

    df = df.drop_duplicates(subset=['title'], keep='first')

    return df