from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from binascii import hexlify
from app_setting import PUBLIC_KEY, CHECK_CYPHER
import base64


def salt_txt(word):
    salt = SHA256.new()
    salt.update(word.encode('utf-8'))
    return hexlify(salt.digest())


def _create_aes_key(private_key, public_key=PUBLIC_KEY):
    return AES.new(private_key, AES.MODE_CBC, public_key)


def _encrypt_aes(txt, key):
    while True:
        if len(txt) % 16 == 0:
            break
        txt += ' '

    try:
        r = key.encrypt(txt)
    except:
        raise ValueError
    return base64.b64encode(r)


def _decrypt_aes(ciphertext, key):
    try:
        ciphertext = base64.b64decode(ciphertext)
    except:
        raise ValueError
    return key.decrypt(ciphertext).strip()


def create_key(private_key, public_key=PUBLIC_KEY, cypher='AES'):
    if cypher == 'AES':
        return _create_aes_key(private_key, public_key=public_key)
    else:
        raise NotImplemented


def encrypt(txt, private_key, public_key, cypher='AES'):
    if cypher == 'AES':
        key = _create_aes_key(private_key, public_key)
        return _encrypt_aes(txt, key)
    else:
        raise NotImplemented


def decrypt(txt, private_key, public_key, cypher='AES'):
    if cypher == 'AES':
        key = _create_aes_key(private_key, public_key)
        return _decrypt_aes(txt, key)
    else:
        raise NotImplemented


def validate_private_key(private_key, public_key=PUBLIC_KEY, cypher='AES'):
    if cypher == 'AES':
        try:
            return encrypt('test text', private_key, public_key, cypher) == CHECK_CYPHER
        except:
            return False
    return False
