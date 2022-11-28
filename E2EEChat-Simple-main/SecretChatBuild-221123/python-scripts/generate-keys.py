#-*- coding:utf-8 -*-
from Crypto import Random
from Crypto.PublicKey import RSA
import base64

def encode_base64(p):
    return base64.b64encode(p).decode('ascii')

secret = Random.get_random_bytes(32) # 32바이트 (256비트) 랜덤 비밀키 생성

rsa = RSA.generate(2048) # RSA 2048 키 생성 시작
pubkey = rsa.public_key().export_key()# 공개키 export
prikey = rsa.export_key()# 개인키 export

secret_str = encode_base64(secret)
pubkey_str = encode_base64(pubkey)
prikey_str = encode_base64(prikey)

print(secret_str + '\n')
print(pubkey_str + '\n')
print(prikey_str + '\n')