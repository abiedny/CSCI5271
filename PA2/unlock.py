##################################################################
# Unlocks a directory by recursively verifying MACs, decrypting, 
# and replacing ciphertext files in a directory with their 
# decrypted version
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
parser.add_argument("-p", help="Path to the public key of the locking party - used to verify signatures")
parser.add_argument("-r", help="Path to the private key of the unlocking party - used to decrypt")
parser.add_argument("-s", help="The locking party - who this directory is from")
args = parser.parse_args()

if not args.d or not args.p or not args.r or not args.s:
    print("ERROR: Please supply all four arguments.")

# Setup and loading in files
pub_cert = json.load(open(args.p))
priv_cert = json.load(open(args.r))

# Validate that the subject in the public key matches the subject argument
assert (args.s == pub_cert['subject']), "Public key subject does not match provided subject!"

# Verify the integrity of the keyfile using public key and keyfile.sig
with open("keyfile", "rb") as infile:
    hash = SHA256.new(infile.read())
    with open("keyfile.sig", "rb") as insig:
        rsa_key_priv = RSA.importKey(priv_cert['keydata'])
        pkcs1_15.new(rsa_key_priv).verify(hash, insig.read())

# Get the AES key from the (verified) keyfile
with open("keyfile", "rb") as infile:
    cipher_rsa_priv = PKCS1_OAEP.new(rsa_key_priv)
    aes_key = cipher_rsa_priv.decrypt(infile.read())

# Delete keyfile and its signature file
os.remove("keyfile")
os.remove("keyfile.sig")

# Recursively decrypt files in directory
for root, dirs, files in os.walk(args.d):
    for f in files:
        f_path = os.path.join(os.path.realpath(root), f)
        # Read in contents, decrypt, overwrite
        with open(f_path, "rb") as infile:
            nonce, tag, ciphertext = [ infile.read(x) for x in (16, 16, -1) ]
            cipher_aes = AES.new(aes_key, AES.MODE_GCM, nonce)
            data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        with open(f_path, "wb") as outfile:
            outfile.write(data)
            outfile.truncate()