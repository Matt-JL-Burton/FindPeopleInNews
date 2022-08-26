from requests_html import HTMLSession

def main():
    session = HTMLSession()
    url = "https://news.google.com/search?q=%22norwich%20station%22%20%22greater%20anglia%22%20%22manager%22&hl=en-GB&gl=GB&ceid=GB%3Aen"
    r = session.get(url)
    r.html.render(sleep=1)
    articles = r.html.find('article')
    print(articles)


if __name__ == '__main__':
    main()