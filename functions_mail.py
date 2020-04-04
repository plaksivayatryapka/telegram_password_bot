#! /usr/bin/env python
# -*- coding: utf-8 -*-


import smtplib  # для почты
from email.mime.text import MIMEText  # для почты
from email.mime.multipart import MIMEMultipart  # для почты
from confidence import MAIL_FROM_LOGIN, MAIL_FROM_PASSWORD

def df_to_string(df):
    return '\n\n'.join([f'{i} {j} {k} {l}' for i, j, k, l in zip(df['login'],
                                                                 df['password'],
                                                                 df['salt_login'],
                                                                 df['salt_password'])])
    

def mail_send(df, recipient):
    msg = MIMEMultipart()
    msg.attach(MIMEText(df_to_string(df), 'plain', 'utf-8'))
    msg['From'] = MAIL_FROM_LOGIN  # отправитель
    mail_server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    mail_server.login(MAIL_FROM_LOGIN, MAIL_FROM_PASSWORD)
    msg['To'] = recipient  # получатель
    mail_server.sendmail('telegram_test_bot@mail.ru', recipient, msg.as_string())
    mail_server.close()
    return 
