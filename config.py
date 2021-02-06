import urllib.parse
import base64

TELEBOT_TOKEN = "<telegram-bot-token>"
HEROKU_URL = "<heroku-app-url>"

_dbs_client_secret = "<dbs-client-secret>"
DBS_CLIENT_ID = "<dbs-client-id>"
DBS_REDIRECT_URL = "{heroku_url}{telebot_token}/receive_access_token/".format(
    heroku_url=HEROKU_URL, telebot_token=TELEBOT_TOKEN)

_auth_code = "%s:%s" %(DBS_CLIENT_ID, _dbs_client_secret)
AUTH_CODE_B64 = base64.b64encode(_auth_code.encode("ascii")).decode("ascii")
REDIRECT_URL_PARSED = urllib.parse.quote(DBS_REDIRECT_URL, safe="")

DBS_AUTH_URL = "https://www.dbs.com/sandbox/api/sg/v1/oauth/authorize"
DBS_TOKEN_URL = "https://www.dbs.com/sandbox/api/sg/v1/oauth/tokens"
DBS_REFRESH_URL = "https://www.dbs.com/sandbox/api/sg/v1/access/refresh"
# DBS_ADHOC_TRANSFER_URL = "https://www.dbs.com/sandbox/api/sg/v1/transfers/adhocTransfer"
DBS_PARTIES_URL = "https://www.dbs.com/sandbox/api/sg/v2/parties"
DBS_PAYNOW_URL = "https://www.dbs.com/sandbox/api/sg/v1/transfers/payNow"