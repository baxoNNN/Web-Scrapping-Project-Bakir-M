import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_hacker_news(pages=5):
    titles = []
    authors = []
    scores = []

    for page in range(1, pages + 1):
        url = f"https://news.ycombinator.com/news?p={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for story in soup.find_all('tr', class_='athing'):
            title = story.find('a', class_='storylink').get_text()
            titles.append(title)

            subtext = story.find_next_sibling('tr')
            author = subtext.find('a', class_='hnuser').get_text()
            authors.append(author)

            score = subtext.find('span', class_='score')
            if score:
                scores.append(int(score.get_text().split()[0]))
            else:
                scores.append(0)

    df = pd.DataFrame({'Title': titles, 'Author': authors, 'Score': scores})
    df.to_csv('hacker_news.csv', index=False)

if __name__ == "__main__":
    scrape_hacker_news()
