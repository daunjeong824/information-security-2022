from Crypto import Random
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import base64, json

def decode_base64(b64):
    return base64.b64decode(b64)

def encode_base64(p):
    return base64.b64encode(p).decode('ascii')

def make_cert_hash(name, pubKeyBase64):
	message = name + pubKeyBase64 # How to make hash? -> H(name + pubKey)
	return SHA256.new(message.encode('utf-8'))

def read_as_json():
	json_str = decode_base64(input()).decode('utf-8')
	json_obj = json.loads(json_str)
	return json_obj

# https://pycryptodome.readthedocs.io/en/latest/src/signature/pkcs1_v1_5.html
def verify(hash, key, signature):
	key = RSA.import_key(decode_base64(key))
    # PKCS #1 v1.5 => Try - True, Except - False
	try:
		pkcs1_15.new(key).verify(hash, decode_base64(signature))
		return True
	except (ValueError, TypeError):
		return False

cert = read_as_json()

hash_compare = make_cert_hash(cert['name'], cert['pubKey']) # make hash to compare
server_pubkey = cert['serverPubKey'] # bytes: server pub key (HINT: In JSON, Provided in form of BASE64)
signature = cert['signature'] # bytes: server sign (HINT: In JSON, Provided in form of BASE64)

cert['isValid'] = verify(hash_compare, server_pubkey, signature) # Verify signature in cert

json_str = json.dumps(cert).encode('utf-8')

print(encode_base64(json_str))