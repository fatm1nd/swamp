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
import web3_module
import markdown


app = Flask(__name__)
# cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resources={r"/*": {"origins": "*"}})

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

@app.route('/', methods=['OPTIONS'])
def index():
    if request.method == 'OPTIONS':
        # This is the preflight request, so you need to respond with the necessary CORS headers.
        response = jsonify({'message': 'Preflight successful'})
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    return None


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
        print(recovered_address, user_address, flush=True)
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
        if verify_signature(code, signature, address) and validateAuthCode(code):
            user_id, token = database.login(address)
            return jsonify(({'user_id':user_id,'access_token' : token})), 200
        else:
            return jsonify({'error': 'Signature verification failed'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/user/verifyToken',methods=['POST'])
@cross_origin()
def checkToken():
    data = request.get_json(force=True)
    token = data.get('access_token')

    user_id, address, access_token = database.checkAccessToken(token)
    if user_id == False:
        return jsonify({'status':1,'comment':"Code is expired or not existed"})
    else:
        return jsonify({'status':0,'comment':"Success"})
    

def validateAuthCode(code):
    
    print(TEMP_CODES, flush=True)
    if code in TEMP_CODES:
        if TEMP_CODES[code] > datetime.now():
            print("Success Code")
            del TEMP_CODES[code]
            return True
        else:
            print("Time error")
            return False
    else:
        print("There is no code")
        return False
    
@app.route('/paper',methods=['POST','OPTIONS'])
@cross_origin()
def getThePaper():

    if request.method == 'OPTIONS':
        # This is the preflight request, so you need to respond with the necessary CORS headers.
        response = jsonify({'message': 'Preflight successful'})
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    

    data = request.get_json(force=True)
    paper_id = data.get('paper_id')
    access_token = data.get('access_token')
    signature = data.get('signature')
    address = data.get('address')

    user_id, token, date = database.checkAccessToken(access_token)

    if user_id == False:
        return jsonify({'status' : 1})

    print(web3_module.getSignWord(paper_id), signature, address, flush=True)

    # Check the signature
    if not verify_signature(web3_module.getSignWord(paper_id), signature, address):
        return jsonify({'status' : 2, "comment" : "Paper of other user"})
    
    # Check the own
    if not web3_module.checkThePaper(paper_id, address):
        return jsonify({'status':3, "comment":"Buy the paper!"})
    
    level = web3_module.getThePaperLevel(paper_id)

    cuts = database.getPaper(paper_id, level)

    return jsonify(cuts)
    


    

@app.route('/leaves/buy',methods=['POST'])
@cross_origin()
def buyToken():
    
    data = request.get_json(force=True)
    address = data.get('address')
    signature = data.get('signature')
    code = data.get('code')
    amount = data.get('amount')
    recipient_address = data.get('recipient')


    if not all([code, signature, address]):
        return jsonify({"status":"Not enough data"}), 400

    if web3_module.server_address == address:
        return jsonify({"status":"You are not minter"})

    try:
        if verify_signature(code, signature, address) and validateAuthCode(code):
            print(web3_module.mintSomeTokens(recipient_address, amount))
            return jsonify(({'status' : 0})), 200
        else:
            return jsonify({'status' : 1}), 401
    except Exception as e:
        return jsonify({'status': str(e)}), 500


    

@app.route('/leaves/balance',methods=['POST'])
@cross_origin()
def balanceOf():
    data = request.get_json(force=True)
    address = data.get('address')
    
    user_id, address, access_token = database.checkAccessToken(access_token)

    if user_id == False:
        return jsonify({'status' : 1})
    return jsonify({'status':0,'balance': web3_module.balanceOf(address)})



@app.route('/user/papers',methods=['POST'])
@cross_origin()
def cutsOfuser():
    data = request.get_json(force=True)
    access_token = data.get('access_token')
    user_id, address, access_token = database.checkAccessToken(access_token)

    return jsonify(database.getUsersPaper(user_id))




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
    user_id, access_token = database.login(address)
    (user_id,temp_token,timestemp) = database.checkAccessToken(access_token)
    ACCESS_TOKEN_CACHE[temp_token] = {"timestamp":timestemp,"user_id":user_id}
    return access_token



@app.route("/uploadCut", methods=["POST"])
@cross_origin()
def upload_file():
    print(request.files,flush=True)

    data = dict(request.form)
    print(data, flush=True)
    access_token = data['access_token']
    paid = False
    if 'paid' in data:
        paid = bool(data['paid'])

    

    if request.method == "POST":
        # Check if the POST request has the file part
        if "file" not in request.files:
            return jsonify({"status":3})
        
        file = request.files["file"]
        print(file, flush=True)
        
        # If the user does not select a file, the browser may submit an empty part without a filename
        if file.filename == None:
            return jsonify({"status": 2})
        
        if file.filename[-3:] != ".md":
            return jsonify({"status": 4})

        filename = hashGenerator.textToHash(str(datetime.now()) + file.filename) + ".md"

        # Save the file to the specified folder
        database.addCutToDB(access_token,filename, paid)
        file.save(str("./cuts/") + filename)
        return jsonify({"status":0})
    else:
        return jsonify({"status":1})
    
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5001,debug=True)
