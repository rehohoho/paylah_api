import requests
import urllib.parse

from config import DBS_CLIENT_ID, AUTH_CODE_B64, REDIRECT_URL_PARSED, \
	DBS_AUTH_URL, DBS_TOKEN_URL, DBS_REFRESH_URL


def get_access_code():
	
	headers = {
		'Content-Type': 'application/json'
	}

	payload = (
		('client_id', DBS_CLIENT_ID),
		('scope', 'Read'),
		('response_type', 'code'),
		('redirect_uri', REDIRECT_URL_PARSED)
	)
	
	response = requests.request("POST", DBS_AUTH_URL, data=payload, headers=headers)
	print(response)
	print(response.text)


def get_access_token():

	access_code = "epKTwuhWIgw+OLxxc+MWAjBNQ60="
	access_code_parsed = urllib.parse.quote(access_code, safe="")

	payload = "code=%s&redirect_uri=%s&grant_type=code" % (access_code_parsed, REDIRECT_URL_PARSED)

	headers = {
		'authorization': "Basic %s" %AUTH_CODE_B64,
		'content-type': "application/x-www-form-urlencoded",
		'cache-control': "no-cache"
	}
	
	print(payload)
	print(headers)

	response = requests.request("POST", DBS_TOKEN_URL, data=payload, headers=headers)
	print(response)
	print(response.text)


def get_refresh_code():
	
	refresh_token = "Z57JN80wXuo8B0NhFYDjm3FVGAaGxebscFhggh103z0="
	refresh_token_parsed = urllib.parse.quote(refresh_token, safe="")
	
	payload = "refresh_token=%s&grant_type=refresh_token" %refresh_token_parsed
	headers = {
		'authorization': "Basic %s" %AUTH_CODE_B64,
		'content-type': "application/x-www-form-urlencoded",
		'cache-control': "no-cache",
		'clientId': DBS_CLIENT_ID
	}

	print(payload)
	print(headers)

	response = requests.request("POST", DBS_REFRESH_URL, data=payload, headers=headers)
	print(response)
	print(response.text)


if __name__ == '__main__':
	# get_access_code() // requires visiting of the webpage
	get_access_token()	
	# get_refresh_code()
