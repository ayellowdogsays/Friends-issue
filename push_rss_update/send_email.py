import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
import os

def email_sender(
    target_email, 
    sender_email, 
    smtp_server, 
    port, 
    password, 
    subject, 
    body,
    template_path=None,
    template_data=None,
    use_tls=True,
    ):
    """
    发送电子邮件。

    参数：
    target_email (str): 目标邮箱地址。
    sender_email (str): 发信邮箱地址。
    smtp_server (str): SMTP 服务地址。
    port (int): SMTP 服务端口。
    password (str): SMTP 服务密码。
    subject (str): 邮件主题。
    body (str): 邮件内容。
    template_path (str): HTML 模板文件路径。默认为 None。
    template_data (dict): 渲染模板的数据。默认为 None。
    use_tls (bool): 是否使用 TLS 加密。默认为 True。
    """
    # 创建 MIME 对象
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = target_email
    msg['Subject'] = subject

    if template_path and template_data:
        # 使用 Jinja2 渲染 HTML 模板
        env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))
        template = env.get_template(os.path.basename(template_path))
        html_content = template.render(template_data)
        msg.attach(MIMEText(html_content, 'html'))
    else:
        # 添加纯文本邮件内容
        msg.attach(MIMEText(body, 'plain'))

    # 连接到 SMTP 服务器并发送邮件
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            if use_tls:
                server.starttls()  # 启动安全模式
            server.login(sender_email, password)
            server.sendmail(sender_email, target_email, msg.as_string())
            print(f'邮件已发送到 {target_email}')
    except Exception as e:
        print(f'无法发送邮件到 {target_email}. 错误: {e}')

def send_emails(emails, sender_email, smtp_server, port, password, subject, body, template_path=None, template_data=None, use_tls=True):
    """
    循环发送邮件给指定的多个邮箱。

    参数：
    emails (list): 包含目标邮箱地址的列表。
    sender_email (str): 发信邮箱地址。
    smtp_server (str): SMTP 服务地址。
    port (int): SMTP 服务端口。
    password (str): SMTP 服务密码。
    subject (str): 邮件主题。
    body (str): 邮件内容。
    template_path (str): HTML 模板文件路径。默认为 None。
    template_data (dict): 渲染模板的数据。默认为 None。
    use_tls (bool): 是否使用 TLS 加密。默认为 True。
    """
    for email in emails:
        print(f'正在发送邮件到 {email}')
        print(f'---------------------------\n邮件主题: {subject}\n邮件内容: {body}\n发件人: {sender_email}\n---------------------------')
        email_sender(email, sender_email, smtp_server, port, password, subject, body, template_path, template_data, use_tls)