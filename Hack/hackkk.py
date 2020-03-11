import requests
from bs4 import BeautifulSoup


def extract_news(text):
    data = []
    total = text.find_all("tr", {"class": "athing"})
    inf = text.find_all("td", {"class": "subtext"})
    for a, b in enumerate(total):
        points = ""
        author = ""
        comments = ""
        title = ""
        url = ""
        author = b.find("span", {"class": "sitestr"})
        if author:
            author = author.text
        comments = inf[a].find_all("a")[-1].text.split()[0]
        points = inf[a].find("span", {"class" : "score"}).text.split()[0]
        title = b.find("a", {"class": "storylink"}).text
        url = b.find("a", {"class": "storylink"})["href"]
        data.append({"author": author,
                    "comments": comments,
                    "points": points,
                    "title": title,
                    "url": url})
    return data


def get_news(url, n_pages):
    data = []
    while n_pages:
        response = requests.get(url)
        text = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(text)
        next = text.find('a', {"class": "morelink"})["href"]
        url = "https://news.ycombinator.com/" + next
        data.extend(news_list)
        n_pages -= 1
        print("Collecting data from page:", url)
    return data
