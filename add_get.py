#! /usr/bin/env python
# -*- coding: utf-8 -*-


import pandas as pd
import os
import functions_crypto
import functions_mail
# from functions_other import get_datetime

get_encrypted = functions_crypto.get_encrypted
get_decrypted = functions_crypto.get_decrypted


def add_password(chat_id, df, login, password, master_password):
    encrypted_login, salt_login = get_encrypted(login, master_password)
    encrypted_password, salt_password = get_encrypted(password, master_password)

    df = df.append(pd.DataFrame([[encrypted_login, encrypted_password, salt_login, salt_password]],
                                columns=['login', 'password', 'salt_login', 'salt_password']),
                   sort=True)
    # df.to_csv(f'data_{chat_id}_{get_datetime()}.csv', index=False)
    df.to_csv(f'data_{chat_id}.csv', index=False)
    return df


def get_password(df, target_login, master_password):
    passwords = list()  # if >1 passwords for same login
    for login, password, salt_password in zip(df['login'], df['password'], df['salt_password']):
        print(f'target_login={target_login}, login={login}, pwd={password}, salt={salt_password}')
        if get_login(df, target_login, master_password) == target_login:
            passwords.append(get_decrypted(password, master_password, salt_password))

    if passwords == list():
        return None

    print(passwords)
    if set(passwords) == set([None]):
        return None
    
    return passwords


def get_login(df, target_login, master_password):
    for login, salt in zip(df['login'], df['salt_login']):
        login = get_decrypted(login, master_password, salt)
        if login == target_login:
            return login
    return None


def get_all_logins(df, master_password):
    login_list = list()
    for login, salt in zip(df['login'], df['salt_login']):
        login = get_decrypted(login, master_password, salt)
        if login is not None:
            login_list.append(login)
    return login_list


def get_df(chat_id):
    if f'data_{chat_id}.csv' not in os.listdir():
        df = pd.DataFrame(columns=['login', 'password', 'salt_login', 'salt_password'])

    else:
        df = pd.read_csv(f'data_{chat_id}.csv')
        df = df.fillna('')

    return df
