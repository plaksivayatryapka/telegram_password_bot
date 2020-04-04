#! /usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
from datetime import datetime, timedelta
import random
import string

TEXT_HELP = '/random - андомный сложный пароль\n/uptime - время работы бота\n/all - все логины\n/mail - отправка файла на почту'


def get_random_password():

    # usage: send_message(chat_id, get_random_password()

    letters_l = random.sample(string.ascii_lowercase, 7)  # get 7 lowercase letters
    letters_u = random.sample(string.ascii_uppercase, 7)
    numbers = random.sample('0123456789', 4)
    symbols = random.sample('_-!.,', 2)
    password = letters_l + letters_u + numbers + symbols
    random.shuffle(password)  # shuffle letters and symbols
    return ''.join(password)  # return string with random password, length = 20


def get_start_time(title):
    try:
        start_time = subprocess.check_output(['systemctl',
                                              'show',
                                              title,
                                              '--property=ActiveEnterTimestamp'])
        return start_time.decode('utf-8').split('=')[-1].replace('\n', '')
    except:
        return 'что-то пошло не так'


def get_datetime():
    return str(datetime.utcnow()).replace(' ', '_').replace(':', '-')[:19]


def get_moscow_time():
    return datetime.utcnow() + timedelta(hours=3)


def get_help():
    return TEXT_HELP
