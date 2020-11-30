##################################################################
# Locks a directory by recursively replacing all the files with
# their equivilant cipher texts, and generating a MAC tag for 
# each file.
##################################################################

import os
import argparse
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15

parser = argparse.ArgumentParser()
parser.add_argument("-d", help="Directory to lock")
parser.add_argument("-p", help="Path to the public key of the unlocking party - used to encrypt")
parser.add_argument("-r", help="Path to the private key of the locking party - used to sign")
parser.add_argument("-s", help="The unlocking party - who this is encrypted for")
args = parser.parse_args()

if not args.d or not args.p or not args.r or not args.s:
    print("ERROR: Please supply all four arguments.")

# Setup and loading in files
pub_cert = json.load(open(args.p))
priv_cert = json.load(open(args.r))

# Validate that the subject in the public key matches the subject argument
assert (args.s == pub_cert['subject']), "Public key subject does not match provided subject!"

# Generate a random AES key, encrypt with public key, write ciphertext to keyfile
aes_key = get_random_bytes(16)
cipher_aes = AES.new(aes_key, AES.MODE_GCM)
rsa_key_pub = RSA.importKey(pub_cert['keydata'])
cipher_rsa_pub = PKCS1_OAEP.new(rsa_key_pub)
aes_key_ciphertext = cipher_rsa_pub.encrypt(aes_key)

with open("keyfile", "wb") as outfile:
    outfile.write(aes_key_ciphertext)

# Sign the keyfile with the private key, write to keyfile.sig
rsa_key_priv = RSA.importKey(priv_cert['keydata'])
hash = SHA256.new(aes_key)
signature = pkcs1_15.new(rsa_key_priv).sign(hash)

with open("keyfile.sig", "wb") as outfile:
    outfile.write(signature)

# Encrypt all the files in the directory using AES-GCM, replacing plain text file with cipher text files
# TODO: There's gonna be some weird directory stuff, just use full paths prolly
for root, dirs, files in os.walk(args.d):
    for f in files:
        # Read in contents, then replace with ciphertext
        with open(f, "rb") as infile:
            contents = cipher_rsa_pub.encrypt(infile.read())
        with open(f, "wb") as outfile:
            outfile.write(contents)
            outfile.truncate()