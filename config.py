import urllib.parse
import base64

TELEBOT_TOKEN = "1395910915:AAG8iA2bYXrsQvcVPDOdIv-_Avht875vPEc"
HEROKU_URL = "https://please-let-me-test-bot.herokuapp.com/"

_dbs_client_secret = "60838a10-e083-4dd7-bd01-9dd951f25ae6"
DBS_CLIENT_ID = "b2c8c8c5-2291-4cda-a936-ee273e812c48"
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