##################################################################
# Generates a simple "certificate" containing a subject, a public
# key, and the public key algorithm. Will also create a similar 
# certificate file containing the private key.
##################################################################
# Certificate files are formatted as a JSON file containing 
# the cert subject, the public key algorithm, a flag indicating
# if this is a public or private cert, and the key data
##################################################################

import argparse
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

parser = argparse.ArgumentParser()
parser.add_argument("-s", help="Alphanumeric string, subject of the keypair")
parser.add_argument("-pub", help="Path to write public key to")
parser.add_argument("-priv", help="Path to write private key to")
args = parser.parse_args()

if not args.s or not args.pub or not args.priv:
    print("ERROR: Please supply all three arguments.")

key = RSA.generate(2048)

# Write the public-key cert file
pubData = {}
pubData['subject'] = args.s
pubData['algorithm'] = "RSA"
pubData['keydata'] =  str(key.publickey().exportKey("PEM"), "utf-8")
pubData['type'] = "public"
with open(args.pub, "w") as outfile:
    json.dump(pubData, outfile)

# Write the private-key cert file
privData = {}
privData['subject'] = args.s
privData['algorithm'] = "RSA"
privData['keydata'] =  str(key.exportKey("PEM"), "utf-8")
privData['type'] = "private"
with open(args.priv, "w") as outfile:
    json.dump(privData, outfile)

print("Done!")

# Just a litle section that sanity checks the keys
with open("public.json") as f_pubcert:
    pubcert = json.load(f_pubcert)

pubKey = RSA.importKey(pubcert['keydata'])
cipher_rsa = PKCS1_OAEP.new(pubKey)

with open("encrypted.bin", "wb") as outfile:
    ciphertext = cipher_rsa.encrypt(b"TeStInG 123...!")
    outfile.write(ciphertext)

# Read the file, decrypt, then print out
with open("private.json") as f_privcert:
    privcert = json.load(f_privcert)

privKey = RSA.importKey(privcert['keydata'])
cipher_rsa_private = PKCS1_OAEP.new(privKey)
print(cipher_rsa_private.decrypt(ciphertext))