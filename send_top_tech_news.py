import requests, yagmail, os

def fetch_news():
    # 以NewsAPI为例，请替换为实际可用API或网页爬虫
    url = f"https://newsapi.org/v2/top-headlines?category=technology&language=en&pageSize=10&apiKey={os.getenv('NEWSAPI_KEY')}"
    resp = requests.get(url).json()
    news_list = []
    for n in resp.get('articles', []):
        title = n['title']
        url = n['url']
        news_list.append(f"{title}\n{url}")
    return "\n\n".join(news_list)

def send_mail(news, email, password):
    yag = yagmail.SMTP(email, password)
    yag.send(to=email, subject="今日全球科技圈十大新闻", contents=news)

if __name__ == "__main__":
    news = fetch_news()
    send_mail(news, os.getenv('EMAIL_ADDRESS'), os.getenv('EMAIL_PASSWORD'))