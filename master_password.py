import cryptography


def verify_master_password(password, password_data):
    return password_data['hash'] == cryptography.sha256_with_salt(password, password_data['salt'], rounds=5)


def get_hash_from_master_password(password, password_data):
    return cryptography.sha256_with_salt(password, password_data['salt'], rounds=5)


def get_key_from_master_password(password, password_data):
    return cryptography.sha256_with_salt(password, password_data['salt'])


def create_master_password_data(password):
    salt = cryptography.get_base64_noise()
    data = {
        'salt': salt,
        'hash': get_hash_from_master_password(password, {'salt': salt})
    }
    return data
