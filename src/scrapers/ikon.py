import requests
from bs4 import BeautifulSoup

def get_ikon_news(is_test=False):
    if is_test:
        # Системээ шалгахын тулд үргэлж 1 "Хуурамч" мэдээ буцаана
        return [{
            'source': 'Ikon',
            'title': 'TEST: Системийн шалгалт амжилттай',
            'url': 'https://ikon.mn/test-check'
        }]
    
    url = "https://ikon.mn/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}

    try: 
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        news_list = []
        # Ikon-ий мэдээний гарчгууд ихэвчлэн 'a' таг дотор, 
        # тодорхой мэдээний замуудтай байдаг (/n/ гэх мэт)
        links = soup.find_all('a', href=True)

        for link in links:
            url_path = link['href']
            if url_path.startswith('/n/'):
                title =link.text.strip()
                if len(title) < 20: continue 

                full_url = "https://ikon.mn" + url_path

                # СТАНДАРТ ЗАГВАР
                news_list.append({
                'source': "Ikon",
                'title': title,
                'url': full_url
                })
        return news_list
    except Exception as e:
        print(f"Ikon Error: {e}")
        return []
    