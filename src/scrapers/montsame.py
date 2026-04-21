import requests
from bs4 import BeautifulSoup

def get_montsame_news():
    url = "https://montsame.mn/mn/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        news_list = []
        links = soup.find_all('a', href=True)
        
        for link in links:
            url_path = link['href']
            if '/read/' in url_path:
                title = link.text.strip()
                if len(title) < 15: continue
                
                full_url = url_path if url_path.startswith('http') else "https://montsame.mn" + url_path
                
                # СТАНДАРТ ЗАГВАР
                news_list.append({
                    'source': 'Montsame',
                    'title': title,
                    'url': full_url
                })
        return news_list
    except Exception as e:
        print(f"Montsame Error: {e}")
        return []