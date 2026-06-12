import feedparser
import requests
from bs4 import BeautifulSoup
import json
import time

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_article_content(url):
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    title_tag = soup.find("h1")
    title = title_tag.get_text(" ", strip=True) if title_tag else ""

    paragraphs = []
    article = soup.find("article")
    if article:
        for p in article.find_all("p"):
            text = p.get_text(" ", strip=True)
            if text:
                paragraphs.append(text)

    content = "\n".join(paragraphs)

    return title, content

rss_url = "https://ir.thomsonreuters.com/rss/news-releases.xml?items=15"
feed = feedparser.parse(rss_url)

news_items = []

for entry in feed.entries[:5]:
    link = entry.get("link", "")
    raw_title = entry.get("title", "")
    summary = entry.get("summary", "")
    published = entry.get("published", "")

    try:
        article_title, content = get_article_content(link)
    except Exception as e:
        article_title = ""
        content = ""
        print("抓文章失敗:", link, e)

    news_items.append({
        "source": "Reuters",
        "raw_title": raw_title,
        "title": article_title if article_title else raw_title,
        "link": link,
        "summary": summary,
        "published": published,
        "content": content
    })

    time.sleep(1)

with open("reuters_news.json", "w", encoding="utf-8") as f:
    json.dump(news_items, f, ensure_ascii=False, indent=2)
