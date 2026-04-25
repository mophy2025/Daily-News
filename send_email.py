import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, content, to_addr, smtp_server, smtp_port, user, password):
    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg.attach(MIMEText(content, 'html', 'utf-8'))
    
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(user, password)
    server.sendmail(user, [to_addr], msg.as_string())
    server.quit()