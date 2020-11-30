##################################################################
# Locks a directory by recursively replacing all the files with
# their equivilant cipher texts, and generating a MAC tag for 
# each file.
##################################################################

import argparse
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

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
