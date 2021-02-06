import requests
import urllib.parse
import jwt
import pprint

from config import DBS_CLIENT_ID, AUTH_CODE_B64, REDIRECT_URL_PARSED, \
	DBS_AUTH_URL, DBS_TOKEN_URL, DBS_REFRESH_URL, DBS_PARTIES_URL, DBS_PAYNOW_URL


def get_access_code():
	
	headers = {
		"Content-Type": "application/json"
	}

	payload = (
		("client_id", DBS_CLIENT_ID),
		("scope", "Read"),
		("response_type", "code"),
		("redirect_uri", REDIRECT_URL_PARSED)
	)
	
	response = requests.request("POST", DBS_AUTH_URL, data=payload, headers=headers)
	print(response)
	print(response.text)


def get_access_token(access_code):

	access_code_parsed = urllib.parse.quote(access_code, safe="")

	payload = "code=%s&redirect_uri=%s&grant_type=code" % (access_code_parsed, REDIRECT_URL_PARSED)

	headers = {
		"authorization": "Basic %s" %AUTH_CODE_B64,
		"content-type": "application/x-www-form-urlencoded",
		"cache-control": "no-cache"
	}
	
	print(payload)
	print(headers)

	response = requests.request("POST", DBS_TOKEN_URL, data=payload, headers=headers)
	print(response)
	print(response.text)


def get_refresh_code(refresh_token):
	
	refresh_token_parsed = urllib.parse.quote(refresh_token, safe="")
	
	payload = "refresh_token=%s&grant_type=refresh_token" %refresh_token_parsed
	headers = {
		"authorization": "Basic %s" %AUTH_CODE_B64,
		"content-type": "application/x-www-form-urlencoded",
		"cache-control": "no-cache",
		"clientId": DBS_CLIENT_ID
	}

	print(payload)
	print(headers)

	response = requests.request("POST", DBS_REFRESH_URL, data=payload, headers=headers)
	print(response)
	print(response.text)

	access_token_json = response.json()
	for k, v in access_token_json.items():
		print(k, v)

	return access_token_json


def get_deposit_accounts(party_id, access_token):

	get_url = "https://www.dbs.com/sandbox/api/sg/v1/parties/%s/deposits" %party_id
	headers = {
		"clientId": DBS_CLIENT_ID,
		"accessToken": access_token
	}

	response = requests.get(get_url, headers=headers)
	response_json = response.json()
	print(response)
	for currAcc in response_json["currentAccounts"]:
		print(currAcc["accountNumber"], 
			currAcc["balances"]["availableBalance"]["amount"], 
			currAcc["balances"]["availableBalance"]["currency"], 
			currAcc["productDescription"], currAcc["id"], currAcc["status"]
		)
	for saveAcc in response_json["savingsAccounts"]:
		print(saveAcc["accountNumber"], 
			saveAcc["balances"]["availableBalance"]["amount"], 
			saveAcc["balances"]["availableBalance"]["currency"], 
			saveAcc["productDescription"], saveAcc["id"], saveAcc["status"]
		)
	
	return response_json


def paynow_transfer(party_id, access_token, debitAccountId, uuid):

	request = {
		"fundTransferDetl": {
			"partyId": party_id,
			"debitAccountId": debitAccountId,
			"payeeReference": {
				"referenceType": "MOBILE",
				"referenceDesc": "MOBILE",
				"reference": "6533441117"
			},
			"amount": 0,
			"transferCurrency": "SGD",
			"comments": "hi",
			"purpose": "hi",
			"referenceId": "93292733C649266803089"
		}
	}

	headers = {
		"content-type": "application/json",
		"client_id": DBS_CLIENT_ID,
		"accessToken": access_token,
		"uuid": uuid
	}

	response = requests.post(DBS_PAYNOW_URL, json=request, headers=headers)
	print(response)
	print(response.text)


# ad-hoc testing code, edit accordingly
if __name__ == "__main__":
	# get_access_code() // requires visiting of the webpage
	# access_token = get_access_token(access_code=)
	# get_refresh_code(refresh_token=)

	auth_response = {'access_token': 'eyJhbGciOiJIUzI1NiJ9.eyJpc3MiIDogImh0dHBzOi8vY2FwaS5kYnMuY29tIiwiaWF0IiA6IDE2MDQwNzY4MzE3MTcsICJleHAiIDogMTYwNDA4MDQzMTcxNywic3ViIiA6ICJTVmN3TXpZPSIsInB0eXR5cGUiIDogMSwiY2xuaWQiIDogImIyYzhjOGM1LTIyOTEtNGNkYS1hOTM2LWVlMjczZTgxMmM0OCIsImNsbnR5cGUiIDogIjIiLCAiYWNjZXNzIiA6ICIxRkEiLCJzY29wZSIgOiAiMkZBLVNNUyIgLCJhdWQiIDogImh0dHBzOi8vY2FwaS5kYnMuY29tL2FjY2VzcyIgLCJqdGkiIDogIjIzMDE2MzgyMzE3NTQwODM1MjQiICwiY2luIiA6ICJRMGxPTURBd01EQXgifQ.0cT6NyHh7RXJYEAYWMbuDGiveFVUh4LhPc6MytnqBrc', 'party_id': 'SVcwMzY=', 'expire_in': '1604080431717', 'token_type': 'bearer', 'refresh_token': 'P0J/csHOumo4rMn17jssNxsZVeUwVz36Fw+U+BIPlGY='}
	access_token = auth_response["access_token"]

	decoded_jwt_token = jwt.decode(access_token, verify=False)
	party_id = decoded_jwt_token["cin"]
	uuid = decoded_jwt_token["clnid"] #"f5bfc01c-1acf-11eb-adc1-0242ac120002"
	deposit_accounts = get_deposit_accounts(party_id, access_token)
	
	debit_account_id = deposit_accounts["currentAccounts"][0]["id"]
	print(party_id)
	print(access_token)
	print(debit_account_id)
	print(uuid)
	
	paynow_transfer(party_id, access_token, debit_account_id, uuid)


"""
adhoc transfer

response_header = {
	clientId: "84b47543-5594-4ce8-80bb-12aa37919970",
	accessToken: "eyJhbGciOiJIUzI1NiJ9.eyJpc3MiIDogImh0dHBzOi8vY2FwaS5kYnMuY29tIiwiaWF0IiA6IDE2MDQwNjk2MjY3NzEsICJleHAiIDogMTYwNDA3MzIyNjc3MSwic3ViIiA6ICJTVmN3TXpZPSIsInB0eXR5cGUiIDogMSwiY2xuaWQiIDogIjg0YjQ3NTQzLTU1OTQtNGNlOC04MGJiLTEyYWEzNzkxOTk3MCIsImNsbnR5cGUiIDogIjIiLCAiYWNjZXNzIiA6ICIxRkEiLCJzY29wZSIgOiAiMkZBLVNNUyIgLCJhdWQiIDogImh0dHBzOi8vY2FwaS5kYnMuY29tL2FjY2VzcyIgLCJqdGkiIDogIjU0Njg5MjUyNTMzNDc0MzI2MzkiICwiY2luIiA6ICJRMGxPTURBd01EQXgifQ.EqwnKx3S0jHa7hoF012lz7Os3Rly6CYANNNiFfTT0cY",
	uuid: "8e90f51d-7f8e-4fdf-aa8d-e903d99aa1f5"
}

request_body = {
    "fundTransferDetl": {
        "debitAccountId": "16614260647620470151010",
        "creditAccountNumber": "04210926930011", # Jasmine Raj
        "bankCode": null,
        "payeeName": "DBS Bank Customer",
        "paymentChannel": "CAS",
        "alternatePayeeReference": {
            "alternateReferenceType": "MOBILE",
            "alternateReferenceDesc": "MOBILE",
            "alternateReference": "9790888878"
        },
        "amount": 1,
        "sourceCurrency": "SGD",
        "destinationCurrency": "SGD",
        "transferCurrency": "SGD",
        "comments": "adfsf",
        "purpose": " ",
        "transferType": "INSTANT",
        "valueDate": "2020-10-30",
        "partyId": "Q0lOMDAwMDAx",
        "referenceId": "11248da6-ec6b-4f29-b013-fcf2acb15e6"
    }
}
"""