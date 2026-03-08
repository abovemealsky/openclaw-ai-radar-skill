import feedparser

url = "https://export.arxiv.org/rss/cs.AI"
feed = feedparser.parse(url)

for entry in feed.entries[:5]:
    print(entry.title)
