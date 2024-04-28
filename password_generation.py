import secrets
import string

POSSIBLE_CHARACTERS = string.ascii_letters + string.digits + '#$%&=:+*()!-?@'
DEFAULT_PASSWORD_LENGTH = 32

def generate():
    password = ''
    for i in range(DEFAULT_PASSWORD_LENGTH):
        password += secrets.choice(POSSIBLE_CHARACTERS)
    return password
