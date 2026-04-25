import requests
from email.mime.text import MIMEText
import smtplib
import schedule
import time

def get_news():
    # 以Hacker News为例
    resp = requests.get('https://hn.algolia.com/api/v1/search?tags=story&hitsPerPage=10')
    news_list = resp.json()['hits']
    return [(news['title'], news['url']) for news in news_list]

def send_email(news_list, receiver_email):
    content = '\n\n'.join([f"{idx+1}. {title}\n{url}" for idx, (title, url) in enumerate(news_list)])
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = '每日科技新闻推送'
    msg['From'] = '你的邮箱'
    msg['To'] = receiver_email

    # 以qq邮箱为例，这里需要填写你的SMTP服务器信息和授权码
    smtp = smtplib.SMTP_SSL('smtp.qq.com', 465)
    smtp.login('你的邮箱', '你的授权码')
    smtp.sendmail('你的邮箱', [receiver_email], msg.as_string())
    smtp.quit()

def job():
    news_list = get_news()
    send_email(news_list, '你的收件邮箱')

# 生产环境用定时任务，不建议死循环
schedule.every().day.at("08:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)