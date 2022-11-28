
from Crypto import Random
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import base64

def decode_base64(b64):
    return base64.b64decode(b64)

def encode_base64(p):
    return base64.b64encode(p).decode('ascii')

def make_message_hash(msg):
    return SHA256.new(msg.encode('utf-8'))

def read_from_base64():
    return [ input(), decode_base64(input()), decode_base64(input()) ]

# https://pycryptodome.readthedocs.io/en/latest/src/signature/pkcs1_v1_5.html
def verify(msg, key, signature):
    
    h = make_message_hash(msg)
    key = RSA.import_key(key)
    try:
        pkcs1_15.new(key).verify(h, signature)
        #ok_str = "ok"
        #ok_str_bytes = ok_str.encode('ascii')
        #ok_base64 = decode_base64(ok_str_bytes)
        #ok_base64.decode('ascii') 
        return "ok"
    except (ValueError, TypeError):
        return "Error"
    
[msg, pubkey, signature] = read_from_base64()

verify_result = verify(msg, pubkey, signature)
print( verify_result )