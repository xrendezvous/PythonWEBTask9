import requests
from bs4 import BeautifulSoup
import json

BASE_URL = 'https://quotes.toscrape.com/'


def get_author_details(author_url):
    response = requests.get(BASE_URL + author_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    born_date = soup.find('span', class_='author-born-date').text
    born_location = soup.find('span', class_='author-born-location').text
    description = soup.find('div', class_='author-description').text.strip()

    return {
        "born_date": born_date,
        "born_location": born_location,
        "description": description
    }


def scrape_quotes():
    authors_details = {}
    quotes_data = []
    page_url = '/page/1/'

    while page_url:
        response = requests.get(BASE_URL + page_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        quotes = soup.find_all('div', class_='quote')
        for quote in quotes:
            text = quote.find('span', class_='text').text
            author_name = quote.find('small', class_='author').text
            author_url = quote.find('a')['href']
            tags = [tag.text for tag in quote.find_all('a', class_='tag')]

            if author_name not in authors_details:
                authors_details[author_name] = get_author_details(author_url)

            quotes_data.append({
                "tags": tags,
                "author": author_name,
                "quote": text
            })

        next_btn = soup.find('li', class_='next')
        page_url = next_btn.find('a')['href'] if next_btn else None

    return quotes_data, authors_details


def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(list(data.values()) if isinstance(data, dict) else data, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    quotes, authors = scrape_quotes()
    save_to_json(quotes, 'quotes.json')

    authors_json = []
    for name, details in authors.items():
        authors_json.append({
            "fullname": name,
            **details
        })
    save_to_json(authors_json, 'authors.json')

