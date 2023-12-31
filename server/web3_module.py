import json
from web3 import Web3
from hexbytes import HexBytes
from eth_account.messages import encode_defunct
import random
import string
import eth_account.messages as messages
from dotenv import dotenv_values

server_address = '0x3A29f07C909E7DC17eBf545F602ba3300a408391'

config = dotenv_values(".env")
INFURA_TOKEN = config['INFURA_TOKEN']
PRIVATE_KEY = config['PRIVATE_KEY']
leaves_contract_address = config['LEAVES_CONTRACT_ADDRESS']
papernft_contract_address = config['PAPERNFT_CONTRACT_ADDRESS']




w3 = Web3(Web3.HTTPProvider(f'https://polygon-mumbai.infura.io/v3/{INFURA_TOKEN}'))
print("Web3: ",w3.is_connected())
leaves_ABI = [
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "mintor",
				"type": "address"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "Approval",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "approve",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "reader",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "burnTokenFromUser",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "addressOfPaperNFT",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "token_id",
				"type": "uint256"
			},
			{
				"internalType": "uint8",
				"name": "level",
				"type": "uint8"
			}
		],
		"name": "buyPaperNFT",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "subtractedValue",
				"type": "uint256"
			}
		],
		"name": "decreaseAllowance",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "addedValue",
				"type": "uint256"
			}
		],
		"name": "increaseAllowance",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "reader",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "mintTokenForUser",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "transfer",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "Transfer",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "transferFrom",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address[]",
				"name": "users",
				"type": "address[]"
			},
			{
				"internalType": "uint256",
				"name": "amountPerUser",
				"type": "uint256"
			}
		],
		"name": "transferToMany",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			}
		],
		"name": "allowance",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "account",
				"type": "address"
			}
		],
		"name": "balanceOf",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "decimals",
		"outputs": [
			{
				"internalType": "uint8",
				"name": "",
				"type": "uint8"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getFeeCoeff",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "name",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "symbol",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "totalSupply",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

leaves_contract = w3.eth.contract(leaves_contract_address, abi=leaves_ABI)                  


papernft_ABI = [
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "mintor",
				"type": "address"
			},
			{
				"internalType": "uint128",
				"name": "unit_cost",
				"type": "uint128"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "approved",
				"type": "address"
			},
			{
				"indexed": True,
				"internalType": "uint256",
				"name": "tokenId",
				"type": "uint256"
			}
		],
		"name": "Approval",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "operator",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "bool",
				"name": "approved",
				"type": "bool"
			}
		],
		"name": "ApprovalForAll",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "tokenId",
				"type": "uint256"
			}
		],
		"name": "approve",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "token_id",
				"type": "uint256"
			},
			{
				"internalType": "int8",
				"name": "level",
				"type": "int8"
			}
		],
		"name": "changeLevel",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "sign_message",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "reader",
				"type": "address"
			},
			{
				"internalType": "address[]",
				"name": "ai_authors",
				"type": "address[]"
			},
			{
				"internalType": "address[]",
				"name": "begginers_authors",
				"type": "address[]"
			},
			{
				"internalType": "address[]",
				"name": "middle_authors",
				"type": "address[]"
			},
			{
				"internalType": "address[]",
				"name": "pros_authors",
				"type": "address[]"
			},
			{
				"internalType": "address",
				"name": "leavesOperator",
				"type": "address"
			}
		],
		"name": "createNewPaper",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "tokenId",
				"type": "uint256"
			}
		],
		"name": "safeTransferFrom",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "tokenId",
				"type": "uint256"
			},
			{
				"internalType": "bytes",
				"name": "data",
				"type": "bytes"
			}
		],
		"name": "safeTransferFrom",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "operator",
				"type": "address"
			},
			{
				"internalType": "bool",
				"name": "approved",
				"type": "bool"
			}
		],
		"name": "setApprovalForAll",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "token_id",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "sign_message",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "reader",
				"type": "address"
			},
			{
				"internalType": "address[]",
				"name": "ai_authors",
				"type": "address[]"
			},
			{
				"internalType": "address[]",
				"name": "begginers_authors",
				"type": "address[]"
			},
			{
				"internalType": "address[]",
				"name": "middle_authors",
				"type": "address[]"
			},
			{
				"internalType": "address[]",
				"name": "pros_authors",
				"type": "address[]"
			},
			{
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			}
		],
		"name": "setRequest",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"indexed": True,
				"internalType": "uint256",
				"name": "tokenId",
				"type": "uint256"
			}
		],
		"name": "Transfer",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "tokenId",
				"type": "uint256"
			}
		],
		"name": "transferFrom",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "owner",
				"type": "address"
			}
		],
		"name": "balanceOf",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "tokenId",
				"type": "uint256"
			}
		],
		"name": "getApproved",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "token_id",
				"type": "uint256"
			}
		],
		"name": "getRequest",
		"outputs": [
			{
				"components": [
					{
						"internalType": "uint256",
						"name": "token_id",
						"type": "uint256"
					},
					{
						"internalType": "address",
						"name": "reader",
						"type": "address"
					},
					{
						"internalType": "string",
						"name": "sign_message",
						"type": "string"
					},
					{
						"internalType": "uint128",
						"name": "ai_level_cost_request",
						"type": "uint128"
					},
					{
						"internalType": "address[]",
						"name": "ai_authors",
						"type": "address[]"
					},
					{
						"internalType": "uint128",
						"name": "begginers_level_cost_request",
						"type": "uint128"
					},
					{
						"internalType": "address[]",
						"name": "begginers_authors",
						"type": "address[]"
					},
					{
						"internalType": "uint128",
						"name": "middle_level_cost_request",
						"type": "uint128"
					},
					{
						"internalType": "address[]",
						"name": "middle_authors",
						"type": "address[]"
					},
					{
						"internalType": "uint128",
						"name": "pros_level_cost_request",
						"type": "uint128"
					},
					{
						"internalType": "address[]",
						"name": "pros_authors",
						"type": "address[]"
					},
					{
						"internalType": "int8",
						"name": "boughtLevel",
						"type": "int8"
					},
					{
						"internalType": "uint256",
						"name": "timestamp",
						"type": "uint256"
					}
				],
				"internalType": "struct PaperNFT.Request",
				"name": "",
				"type": "tuple"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "operator",
				"type": "address"
			}
		],
		"name": "isApprovedForAll",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "token_id",
				"type": "uint256"
			}
		],
		"name": "isPaperBought",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "name",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "tokenId",
				"type": "uint256"
			}
		],
		"name": "ownerOf",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bytes4",
				"name": "interfaceId",
				"type": "bytes4"
			}
		],
		"name": "supportsInterface",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "symbol",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "tokenId",
				"type": "uint256"
			}
		],
		"name": "tokenURI",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

papernft_contract = w3.eth.contract(papernft_contract_address, abi=papernft_ABI)              


def checkThePaper(paper_id, address):
    result_address = papernft_contract.functions.ownerOf(int(paper_id)).call({'from':server_address})
    print(result_address, address, flush=True)
    return address.lower() == result_address.lower()

def getThePaperLevel(paper_id):
    return papernft_contract.functions.getRequest(int(paper_id)).call({'from':server_address})[-2]

def getSignWord(paper_id):
    return papernft_contract.functions.getRequest(int(paper_id)).call({'from':server_address})[2]

def returnMinterAddress():
    return server_address

def mintSomeTokens(recipient_address, amount):
    
	dict_transaction = {
		'chainId': w3.eth.chain_id,
		'from': server_address,
		'gasPrice': w3.eth.gas_price,
		'nonce': w3.eth.get_transaction_count(server_address)
	}
    
	transaction = leaves_contract.functions.mintTokenForUser(str(recipient_address),int(amount)).build_transaction(dict_transaction)

	signed_txn = w3.eth.account.sign_transaction(transaction, PRIVATE_KEY)

	# txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
	# print(txn_hash.hex())

def balanceOf(address):
    
	dict_transaction = {
		'chainId': w3.eth.chain_id,
		'from': server_address,
		'gasPrice': w3.eth.gas_price,
		'nonce': w3.eth.get_transaction_count(server_address)
	}
    
	transaction = leaves_contract.functions.balanceOf(str(address)).build_transaction(dict_transaction)

	signed_txn = w3.eth.account.sign_transaction(transaction, PRIVATE_KEY)

	# txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# print(getSignWord(2))