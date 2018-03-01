from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from binascii import hexlify
from app_setting import public_key
import base64

def salt_txt(word):
    hash = SHA256.new()
    hash.update(word.encode('utf-8'))
    return hexlify(hash.digest())


def _create_aes_key(private_key, public_key=public_key):
    return AES.new(private_key, AES.MODE_CBC, public_key)


def _encrypt_aes(txt, key):
    while True:
        if len(txt) % 16 == 0:
            break
        txt += ' '

    try:
        r = key.encrypt(txt)
    except:
        print(txt, 'not encrypted')
        return base64.b64encode('1'*16)
    return base64.b64encode(r)


def _decrypt_aes(ciphertext, key):
    ciphertext = base64.b64decode(ciphertext)
    return key.decrypt(ciphertext).strip()


def create_key(private_key, public_key, cypher='AES'):
    return _create_aes_key(private_key, public_key=public_key)


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

