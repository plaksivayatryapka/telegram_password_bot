#! /usr/bin/env python
# -*- coding: utf-8 -*-


import telepot  # библиотека для телеграм
from telepot.loop import MessageLoop

from functions_mail import mail_send
from functions_other import get_start_time, get_help
from add_get import get_df, add_password, get_password, get_all_logins
from functions_crypto import get_random_password
from confidence import TOKEN, MAIL_RECIPIENT, is_me


SERVICE_NAME = 'pass_bot'
TelegramBot = telepot.Bot(TOKEN)
send_message = TelegramBot.sendMessage


def on_chat_message(msg):

    content_type, chat_type, chat_id = telepot.glance(msg)

    df = get_df(chat_id)

    if content_type != 'text':
        return

    incoming_text = msg['text']

    if incoming_text.lower() in ['commands', '/start']:
        send_message(chat_id, 'mail=send email,\nrandom=get random password,\nuptime=get uptime')
        return

    if chat_id not in list(MAIL_RECIPIENT.keys()):
        for id_ in list(MAIL_RECIPIENT.keys()):
            send_message(id_, f'Stranger is using bot! Text = {incoming_text}, chat_id={chat_id}')

    # PARSE COMMANDS
    print(incoming_text)
    
    if incoming_text.lower() == '/mail':
        mail_send(df, MAIL_RECIPIENT[chat_id])
        send_message(chat_id, 'sent')
        return

    if incoming_text.lower() == '/random':
        send_message(chat_id, get_random_password())
        return

    if incoming_text.lower() == '/help':
        send_message(chat_id, get_help())
        return

    if incoming_text.lower() == '/uptime':
        send_message(chat_id, get_start_time(SERVICE_NAME))
        return

    # PARSE PASSWORDS

    incoming_text = incoming_text.split()
    print(incoming_text)
    if len(incoming_text) == 2:
        if is_me(chat_id, incoming_text) is not True:
            send_message(chat_id, 'ошибка')
            return

        message_id = msg['message_id']
        TelegramBot.deleteMessage((chat_id, message_id))

        login = incoming_text[0]
        master_password = incoming_text[1]

        if incoming_text[0].lower() == '/all':
            all_logins = get_all_logins(df, master_password)
            if all_logins == list():
                send_message(chat_id, 'empty')
                return

            send_message(chat_id, '\n'.join(all_logins))
            return

        passwords = get_password(df, login, master_password)
        if passwords is None:
            send_message(chat_id, 'Потеряна связь с базой данных =(. Попробуйте завтра.')
            return

        print(login, master_password)
        if len(passwords) == 1:
            send_message(chat_id, passwords[0])
            return

        if len(passwords) >= 2:
            send_message(chat_id, '\n'.join(passwords))
            return

        return

    if len(incoming_text) == 3:
        message_id = msg['message_id']
        TelegramBot.deleteMessage((chat_id, message_id))
        login = incoming_text[0]
        password = incoming_text[1]
        master_password = incoming_text[2]

        df = add_password(chat_id, df, login, password, master_password)
        mail_send(df, MAIL_RECIPIENT[chat_id])
        send_message(chat_id, 'ok')
        return


print('started')
MessageLoop(TelegramBot, {'chat': on_chat_message}).run_forever()
