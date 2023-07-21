from flask import Flask, jsonify, request
from web3 import Web3
from hexbytes import HexBytes
from eth_account.messages import encode_defunct
import os
import random
import string
from bip32utils import BIP32Key
import eth_account.messages as messages
import sys
import json
from flask import after_this_request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


# Replace 'YOUR_INFURA_PROJECT_ID' with your Infura project ID or set your own Ethereum node URL
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/{INFURA_TOKEN}'))

# Account on the server side (replace with your private key)




def sign_message(message, private_key):
    signable_message = messages.encode_defunct(text=message)
    signed_msg = w3.eth.account.sign_message(signable_message, private_key=private_key)

    

    return signed_msg.signature.hex()

@app.route('/sign', methods=['POST'])
@cross_origin()
def sign():
    data = request.get_json()
    print(data,flush=True)
    message = data.get('message')



    if not message:
        return jsonify({'error': 'Invalid data'}), 400

    try:
        signature = sign_message(message, PRIVATE_KEY)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'signature': signature}), 200


def verify_signature(message, signature, user_address):
    try:
        message_hash = Web3.keccak(text=message).hex()
        print("Hash: ", message_hash)

        message = encode_defunct(text=message)
        recovered_address = w3.eth.account.recover_message(message,signature=HexBytes(signature))


        # recovered_address = Account.recoverHash(message_hash, signature=signature)

        print(recovered_address)

        return recovered_address.lower() == user_address.lower()
    except Exception as e:
        print(e)
        return False

@app.route('/verify',methods=['POST'])
@cross_origin()
def verify():
    data = request.get_json(force=True)
    print(data)
    message = data.get('message')
    signature = data.get('signature')
    user_address = data.get('user_address')

    if not all([message, signature, user_address]):
        return jsonify({'userAddress': '', "status":"Not enough data"}), 400

    try:
        # Check if the signature is correct
        if verify_signature(message, signature, user_address):
            print("Corect signature")
            # Return a random hash in case of successful verification
            random_hash = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
            print(jsonify(({'token' : random_hash})))
            return jsonify(({'token' : random_hash})), 200
        else:
            return jsonify({'error': 'Signature verification failed'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5001,debug=True)
