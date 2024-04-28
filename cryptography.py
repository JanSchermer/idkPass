import hashlib

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from base64 import b64decode, b64encode

import json


def get_base64_noise():
    noise = get_random_bytes(64)
    encoded_noise = b64encode(noise).decode('utf8')
    return encoded_noise


def sha256(word, rounds=1):
    encoded = word.encode('utf-8')
    hash = hashlib.sha256(encoded)
    hexdigits = hash.hexdigest()
    if rounds > 1:
        return sha256(hexdigits, rounds=rounds - 1)
    return hexdigits


def sha256_with_salt(word, salt, rounds=1):
    return sha256(word + salt, rounds=rounds)


def encrypt(word, key):
    nonce = get_random_bytes(64)
    to_encrypt = json.dumps({
        'word': word,
        'noise': get_base64_noise()
    })
    cipher = AES.new(bytes(key, 'utf8'), mode=AES.MODE_SIV, nonce=nonce)
    cipher_text, tag = cipher.encrypt_and_digest(to_encrypt.encode('utf8'))
    encrypted_data = {
        'nonce': b64encode(nonce).decode('utf8'),
        'tag': b64encode(tag).decode('utf8'),
        'cipher_text': b64encode(cipher_text).decode('utf8')
    }
    return encrypted_data


def decrypt(data, key):
    nonce = b64decode(data['nonce'])
    tag = b64decode(data['tag'])
    cipher_text = b64decode(data['cipher_text'])
    cipher = AES.new(bytes(key, 'utf8'), mode=AES.MODE_SIV, nonce=nonce)
    decrypted_data = json.loads(cipher.decrypt_and_verify(cipher_text, tag))
    word = decrypted_data['word']
    return word

