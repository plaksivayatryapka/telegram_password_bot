#! /usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import os
import random
import string
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def get_encrypted(password, masterpassword):
    password = bytes(password, encoding='ascii')
    masterpassword = bytes(masterpassword, encoding='ascii')

    salt = os.urandom(16)
    salt_decimal = get_decimal(salt)

    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                     length=32,
                     salt=salt,
                     iterations=100000,
                     backend=default_backend())

    key = base64.urlsafe_b64encode(kdf.derive(masterpassword))
    f = Fernet(key)
    token = f.encrypt(password).decode('utf-8')
    return token, salt_decimal


def get_decrypted(string, master_password, salt_decimal):
    string = bytes(string, encoding='ascii')
    master_password = bytes(master_password, encoding='ascii')
    salt = get_bytes(int(salt_decimal))

    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                     length=32,
                     salt=salt,
                     iterations=100000,
                     backend=default_backend())

    key = base64.urlsafe_b64encode(kdf.derive(master_password))
    f = Fernet(key)
    try:
        return f.decrypt(string).decode('utf-8')
    except:
        return None


def get_decimal(_bytes):
    return int.from_bytes(_bytes, byteorder='big')


def get_bytes(integer):
    return integer.to_bytes(16, byteorder='big') 


def get_random_password():
    letters_l = random.sample(string.ascii_lowercase, 7)
    letters_u = random.sample(string.ascii_uppercase, 7)
    numbers = random.sample('0123456789', 4)
    symbols = random.sample('_-!.,', 2)
    password = letters_l + letters_u + numbers + symbols
    random.shuffle(password)
    return ''.join(password)
