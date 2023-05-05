import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
from pprint import pprint


def get_first_new():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 OPR/97.0.0.0"
    }
    url = 'https://www.securitylab.ru/news/'
    r = requests.get(url = url, headers = headers)
    soup = BeautifulSoup(r.text, 'lxml')
    articl_cards = soup.find_all('a', class_ = 'article-card')
    print(articl_cards)

    news_dict = {}
    for articl in articl_cards:
        articl_title = articl.find('h2', class_='article-card-title').text.strip()
        articl_desc = articl.find('p').text.strip()
        articl_url = f'https://www.securitylab.ru{articl.get("href")}'
        articl_date_time = articl.find('time').get('datetime')
        date_from_iso = datetime.fromisoformat(articl_date_time)
        date_time = datetime.strftime(date_from_iso, "%H:%M  %d/%m/%Y")
        article_id = articl_url.split('/')[-1]
        article_id = article_id[:-4]

        news_dict[article_id] = {
            'date_time': date_time,
            'articl_title': articl_title,
            'articl_url': articl_url,
            'articl_desc': articl_desc
        }

        with open('news/news_dict.json', 'w') as file:
            json.dump(news_dict, file, indent= 4, ensure_ascii=False)

def check_for_new_news():
    with open('news/news_dict.json') as file:
        news_dict = json.load(file)
#    pprint(news_dict)
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 OPR/97.0.0.0"
    }
    url = 'https://www.securitylab.ru/news/'
    r = requests.get(url=url, headers=headers)
#    soup = BeautifulSoup(r.text, 'lxml')
    soup = BeautifulSoup(r.text, 'lxml')
    articl_cards = soup.find_all('a', class_='article-card')

    fresh_news = {}
#    print(type(fresh_news))
    for articl in articl_cards:
        articl_url = f'https://www.securitylab.ru{articl.get("href")}'
        article_id = articl_url.split('/')[-1]
        article_id = article_id[:-4]
        if article_id in news_dict:
            continue
        else:
            articl_title = articl.find('h2', class_='article-card-title').text.strip()
            articl_desc = articl.find('p').text.strip()
            articl_date_time = articl.find('time').get('datetime')
            date_from_iso = datetime.fromisoformat(articl_date_time)
            date_time = datetime.strftime(date_from_iso, "%H:%M  %d/%m/%Y")

            news_dict[article_id] = {
                'date_time': date_time,
                'articl_title': articl_title,
                'articl_url': articl_url,
                'articl_desc': articl_desc
            }
            with open('news_dict.json', 'w') as file:
                json.dump(news_dict, file, indent=4, ensure_ascii=False)

            fresh_news[article_id] = {
                'date_time': date_time,
                'articl_title': articl_title,
                'articl_url': articl_url,
                'articl_desc': articl_desc

            }
    return fresh_news



def main():
    get_first_new()
    check_for_new_news()


if __name__ == '__main__':
    main()