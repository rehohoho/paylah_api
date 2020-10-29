from datetime import datetime
import requests
from requests.exceptions import HTTPError

CLIENT_ID = "b2c8c8c5-2291-4cda-a936-ee273e812c48"
CLIENT_SECRET = "60838a10-e083-4dd7-bd01-9dd951f25ae6"
AUTHORISE_URL = "https://www.dbs.com/sandbox/api/sg/v1/oauth/authorize"
# REDIRECT_URI = "https%3A%2F%2Fwww.dbs.com%2Fdevelopers%2F%23%2Fall-products%2Fplay-ground"

REDIRECT_URI = "https%3A%2F%2Fwww.youtube.com%2F"
# https://www.dbs.com/sandbox/api/sg/v1/oauth/authorize?client_id=b2c8c8c5-2291-4cda-a936-ee273e812c48&redirect_uri=https%3A%2F%2Fwww.dbs.com%2Fdevelopers%2F%23%2Fall-products%2Fplay-ground&scope=Read&response_type=code&state=0399




def main():

	s = requests.Session()

	headers = {
		'Content-Type': 'application/json'
	}

	params = (
		('client_id', CLIENT_ID),
		('scope', 'Read'),
		('response_type', 'code'),
		('redirect_uri', REDIRECT_URI)
	)
	
	try:
		response = s.post(AUTHORISE_URL, headers=headers, params=params)
	except HTTPError as http_err:
		print('%s: HTTP error occured: %s' %(datetime.now().time(), http_err))
	except Exception as err:
		print('%s: Other error occured: %s' %(datetime.now().time(), err))
	else:
		print('%s: Request success' %(datetime.now().time()))
	
	print(response)

if __name__ == '__main__':
	main()


"""
list of urls
auth: https://www.dbs.com/sandbox/api/sg/v1/oauth/authorize?7056811051110888993&client_id=84b47543-5594-4ce8-80bb-12aa37919970&response_type=code&scope=Read&redirect_uri=https%3A%2F%2Fwww.dbs.com%2Fdevelopers%2Frefapps%2Fgref%2FoauthRedirect&state=5938_ft

"""

"""
import requests
import requests.auth

CLIENT_ID = "8cbc160c-89e7-42c6-ba15-aea74ffdf9ff"
CLIENT_SECRET = "b75293ee-626e-4604-b95a-53b0249910f6"
AUTHORISE_URL = "https://www.dbs.com/sandbox/api/sg/v1/oauth/authorize"
SCOPE = "Read"
RESPONSE_TYPE = "code"
REDIRECT_URI = 

authorise_url_with_params = "%s?client_id=%s&scope=%s&response_type=%s&redirect_uri=%s" %(
    AUTHORISE_URL, CLIENT_ID, SCOPE, RESPONSE_TYPE, REDIRECT_URI)
print(authorise_url_with_params)

response = requests.post(AUTHORISE_URL, data=post_data)

client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)

post_data = {"grant_type": "password", "username": "reddit_bot", "password": "snoo"}
headers = {"User-Agent": "ChangeMeClient/0.1 by YourUsername"}
response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
response.json()

headers = {"Authorization": "bearer fhTdafZI-0ClEzzYORfBSCR7x3M", "User-Agent": "ChangeMeClient/0.1 by YourUsername"}
response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
response.json()

customer client id: 8cbc160c-89e7-42c6-ba15-aea74ffdf9ff
customer client secret: b75293ee-626e-4604-b95a-53b0249910f6
"""