import requests
from email.mime.text import MIMEText
from email.header import Header
import smtplib

# === 基本配置 ===
QQ_EMAIL = "你的QQ邮箱@qq.com"
QQ_SMTP_PASS = "你的授权码"
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465
RECEIVER = "你的QQ邮箱@qq.com"

# --- 新闻抓取 ---
def get_hackernews():
    """获取Hacker News 热门新闻（英文）"""
    url = 'https://hn.algolia.com/api/v1/search?tags=story&hitsPerPage=15'
    resp = requests.get(url)
    news_list = resp.json()['hits']
    results = []
    for item in news_list:
        if item['title'] and item['url']:
            results.append({'title': item['title'], 'url': item['url']})
        if len(results) >= 10:
            break
    return results

# --- 自动翻译（用DeepL/百度/有道/可选OpenAI，示例用百度翻译API，可换成自己喜欢的） ---
def translate_to_cn(text):
    # 百度通用文本翻译API文档: https://fanyi-api.baidu.com/doc/21
    appid = '你的百度翻译appid'
    key = '你的百度翻译密钥'
    salt = '12345678'
    sign = requests.utils.quote(appid + text + salt + key)
    url = f"https://fanyi-api.baidu.com/api/trans/vip/translate?q={requests.utils.quote(text)}&from=en&to=zh&appid={appid}&salt={salt}&sign={sign}"
    res = requests.get(url).json()
    if 'trans_result' in res:
        return res['trans_result'][0]['dst']
    return "[翻译失败]"

# --- 编排列表 ---
def build_news_list(news_items):
    lines = []
    for i, news in enumerate(news_items, 1):
        title_en = news['title']
        title_cn = translate_to_cn(title_en)
        lines.append(f"{i}. {title_en}\n   {title_cn}\n   {news['url']}\n")
    return '\n'.join(lines)

# --- 邮件发送 ---
def send_mail(subject, content):
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = QQ_EMAIL
    msg['To'] = RECEIVER
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(QQ_EMAIL, QQ_SMTP_PASS)
        server.sendmail(QQ_EMAIL, [RECEIVER], msg.as_string())

if __name__ == '__main__':
    news = get_hackernews()
    news_list_str = build_news_list(news)
    subject = "每日科技新闻 - 中英文对照"
    send_mail(subject, news_list_str)