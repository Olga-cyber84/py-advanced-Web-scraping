import requests
import bs4
from fake_headers import Headers

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

base_url = "https://habr.com"
url = base_url + '/ru/all/'


def get_result(KEYWORDS, article, info, title, link, time_container="tm-article-snippet__datetime-published"):
    for word in KEYWORDS:
        if word in info.lower():
            published_date = article.find(class_=time_container).text
            print(f'{published_date} - {title} - {link}')
            break


def generating_headers():
    header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
        headers=True  # generate misc headers
    )
    return header.generate()


if __name__ == "__main__":
    response = requests.get(url, headers=generating_headers())
    text = response.text

    soup = bs4.BeautifulSoup(text, features="html.parser")
    articles = soup.find_all("article")
    articles_links = []
    res_checking_preview = []
    res_checking_post = []

    print("Проверка совпадений по preview-информации: ")

    for article in articles:
        title = article.find("h2").find("span").text
        article_body = article.find(class_="article-formatted-body").text
        hubs = article.find_all(class_="tm-article-snippet__hubs-item")
        hubs = [hub.text.strip() for hub in hubs]
        hubs = ' '.join(hubs)
        href = article.find(
            class_="tm-article-snippet__title-link").attrs.get("href")
        link = base_url + href
        articles_links.append(link)
        preview = (title + hubs + article_body).lower()

        checking_preview = get_result(KEYWORDS, article, preview, title, link,
                                      time_container="tm-article-snippet__datetime-published")
        if checking_preview:
            res_checking_preview.append(checking_preview)

    if not res_checking_preview:
        print("совпадений нет")

    print("Проверка совпадений в тексте статьи: ")

    for link in articles_links:
        response = requests.get(link, headers=generating_headers())
        text = response.text
        soup = bs4.BeautifulSoup(text, features="html.parser")

        article = soup.find(class_="tm-article-presenter__content")
        post = article.find(id="post-content-body").text
        title = article.find("h1").text

        checking_post = get_result(KEYWORDS, article, post, title, link,
                                   time_container="tm-article-snippet__datetime-published")
        if checking_post:
            res_checking_post.append(checking_post)

    if not res_checking_post:
        print("совпадений нет")
