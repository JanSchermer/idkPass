import os
import time
from getpass import getpass

import master_password
import password_generation
import storage

import pyperclip


def startup():
    master_data = storage.get_master_password_data()
    if master_data is None:
        setup_master_password()
    unlock(master_data)
    main_menu()


def unlock(master_password_data, wrong=False):
    print('Master-Password required to unlock IDKpass.' if not wrong else 'Wrong Master-Password. Try again.')
    password = getpass('Password: ')
    if master_password.verify_master_password(password, master_password_data):
        key = master_password.get_key_from_master_password(password, master_password_data)
        storage.set_key(key)
    else:
        unlock(master_password_data, wrong=True)


def setup_master_password():
    print('Enter a Master-Password, that you would like to use. MAKE SURE TO REMEMBER IT!')
    password = getpass('Password: ')
    reentered_password = getpass('Again: ')
    if password != reentered_password:
        print('Passwords do not match! Try again.')
        setup_master_password()
        return
    data = master_password.create_master_password_data(password)
    storage.set_master_password_data(data)
    print('Master-Password has been set! Start again to use IDKpass.')
    exit()


def get_password(index):
    password = storage.get_password(index)
    pyperclip.copy(password)
    print('Password copied!')


def add_password():
    name = input('Name: ')
    password = getpass('Password (leave empty to generate): ')
    if len(password) < 1:
        password = password_generation.generate()
        pyperclip.copy(password)
        print('A password has been generated and copied to you clipboard.')
    else:
        print('The password has been saved!')
    storage.store_password(password, name)


def main_menu():
    os.system('cls')
    print('Enter a number to copy a password, or use on of these characters: (a = add password, e = exit)')
    passwords = storage.get_passwords()
    for index in range(len(passwords)):
        print(str(index) + ' - ' + passwords[index]['name'])

    print('')
    action = input('> ')

    if action == 'a':
        add_password()
    if action == 'e':
        print('Goodbye!')
        exit()
    if action.isdigit():
        num = int(action)
        if 0 <= num < len(passwords):
            get_password(num)

    time.sleep(3)
    main_menu()
