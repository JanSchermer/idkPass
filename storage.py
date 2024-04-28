import datetime
import json
import os.path
import time

import cryptography

MAIN_DIR = os.path.expanduser('~') + '\\Documents\\idkPass\\'
STORAGE_FILE_LOCATION = MAIN_DIR + 'storage.json'
MASTER_PASSWORD_FILE_LOCATION = MAIN_DIR + 'master.json'

storage = []
key = ''


def get_master_password_data():
    try:
        f = open(MASTER_PASSWORD_FILE_LOCATION, 'r')
        data = json.load(f)
        f.close()
        return data
    except FileNotFoundError:
        return None


def set_master_password_data(data):
    with open(MASTER_PASSWORD_FILE_LOCATION, 'w') as f:
        json.dump(data, f)


def load():
    global storage
    if not os.path.exists(MAIN_DIR):
        os.mkdir(MAIN_DIR)
    try:
        with open(STORAGE_FILE_LOCATION, 'r') as f:
            storage = json.load(f)
    except FileNotFoundError:
        return


def save():
    with open(STORAGE_FILE_LOCATION, 'w') as f:
        json.dump(storage, f)


def sort():
    global storage
    storage = sorted(storage, key=lambda item: item['last_use'], reverse=True)


def set_key(master_key):
    global key
    key = master_key


def store_password(password, name):
    encrypted_password = cryptography.encrypt(password, key)
    data = {
        'name': name,
        'last_use': time.time(),
        'password': encrypted_password
    }
    storage.insert(0, data)
    save()


def get_password(index):
    data = storage[index]
    decrypted_password = cryptography.decrypt(data['password'], key)
    data['last_use'] = time.time()
    sort()
    save()
    return decrypted_password


def get_passwords():
    return storage
