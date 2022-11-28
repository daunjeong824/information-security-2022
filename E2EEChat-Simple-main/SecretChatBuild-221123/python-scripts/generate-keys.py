
from Crypto import Random
from Crypto.PublicKey import RSA
import base64

def encode_base64(p):
    return base64.b64encode(p).decode('ascii')

secret = Random.get_random_bytes(32) 

rsa = RSA.generate(2048) 
pubkey = rsa.public_key().export_key()
prikey = rsa.export_key()

secret_str = encode_base64(secret)
pubkey_str = encode_base64(pubkey)
prikey_str = encode_base64(prikey)

print(secret_str + '\n')
print(pubkey_str + '\n')
print(prikey_str + '\n')