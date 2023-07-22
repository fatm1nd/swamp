from flask import Flask, jsonify, request
from web3 import Web3
from hexbytes import HexBytes
from eth_account.messages import encode_defunct
import random
import string
import eth_account.messages as messages
from flask_cors import CORS, cross_origin
from dotenv import dotenv_values
import database
import time
import hashGenerator
from datetime import datetime, timedelta

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

f = open("shrek_script.txt","r")
shrekScript = f.readline().split()
f.close()

config = dotenv_values(".env")
INFURA_TOKEN = config['INFURA_TOKEN']
PRIVATE_KEY = config['PRIVATE_KEY']

w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/{INFURA_TOKEN}'))

TEMP_CODES = {}
ACCESS_TOKEN_CACHE = {}

def sign_message(message, private_key):
    signable_message = messages.encode_defunct(text=message)
    signed_msg = w3.eth.account.sign_message(signable_message, private_key=private_key)
    return signed_msg.signature.hex()

@app.route("/ping")
def pong():
    return "pong"

@app.route('/user/code', methods=['GET'])
@cross_origin()
def getCode():
    ex_date = datetime.now() + timedelta(minutes=3)
    code = hashGenerator.simpleHash()
    TEMP_CODES[code] = ex_date
    return jsonify({"code":code})


def verify_signature(message, signature, user_address):
    try:
        message = encode_defunct(text=message)
        recovered_address = w3.eth.account.recover_message(message,signature=HexBytes(signature))
        return recovered_address.lower() == user_address.lower()
    except Exception as e:
        print(e, flush=True)
        return False

@app.route('/user/auth',methods=['POST'])
@cross_origin()
def verify():
    data = request.get_json(force=True)
    print(data)
    address = data.get('address')
    signature = data.get('signature')
    code = data.get('code')

    if not all([code, signature, address]):
        return jsonify({"status":"Not enough data"}), 400

    try:
        if verify_signature(code, signature, address):
            token = getAccessToken(address)
            return jsonify(({'token' : token})), 200
        else:
            return jsonify({'error': 'Signature verification failed'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def validateToken(access_token):
    ''' 
    Validate token \n
    0 - token is existed, not expired \n
    1 - token is existed, expired \n
    2 - token is not existed \n
    '''
    if access_token in ACCESS_TOKEN_CACHE:
        if ACCESS_TOKEN_CACHE[access_token]['timestamp'] > (datetime.now()):
            del ACCESS_TOKEN_CACHE[access_token]
            return 1
        else:
            return 0
    else:
        (user_id,temp_token, timestemp) = database.checkAccessToken(access_token)

        if temp_token != False:
            ACCESS_TOKEN_CACHE[temp_token] = {"timestamp":timestemp,"user_id":user_id}
        else:
            return 2


def getAccessToken(address):
    access_token = str(hashGenerator.simpleHash())
    database.updateToken(address,access_token)
    (user_id,temp_token,timestemp) = database.checkAccessToken(access_token)
    ACCESS_TOKEN_CACHE[temp_token] = {"timestamp":timestemp,"user_id":user_id}
    return access_token



@app.route("/uploadCut", methods=["GET", "POST"])
@cross_origin()
def upload_file():
    # Ask user is it paid and ask to send author access_token
    print(request.files,flush=True)
    print(request.form, flush=True)

    # data = request.get_json(force=True)
    # print(data, flush=True)
    # # print(data)
    access_token = request.form['access_token'] 
    paid = request.form['paid']
    # # access_token = data.get('access_token')
    # if database.checkAccessToken(access_token):
    #     return jsonify({'status':'invalid_token'})
    # signature = data.get('signature')
    # code = data.get('code')

    if request.method == "POST":
        # Check if the POST request has the file part
        if "file" not in request.files:
            return jsonify({"status":3})
        
        file = request.files["file"]
        
        # If the user does not select a file, the browser may submit an empty part without a filename
        if file.filename == None:
            return jsonify({"status": 2})
        
        if file.filename[-3:] != ".md":
            return jsonify({"status": 4})


        filename = hashGenerator.textToHash(str(datetime.now()) + file.filename) + ".md"

        # Save the file to the specified folder
        database.addCutToDB("dasiudhnbhwbf87gewf78wevf879g",filename,False)
        file.save(str("./cuts/") + filename)

        

        return jsonify({"status":0})
    else:
        return jsonify({"status":1})
    
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5001,debug=True)
